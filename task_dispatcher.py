#!/usr/bin/env python3

import asyncio
from datetime import timedelta
import pathlib
import sys

from yapapi import (
    Executor,
    Task,
    __version__ as yapapi_version,
    WorkContext,
    windows_event_loop_fix,
)
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.package import vm
from yapapi.rest.activity import BatchTimeoutError

# For importing `utils.py`:
script_dir = pathlib.Path(__file__).resolve().parent
parent_directory = script_dir.parent
sys.stderr.write(f"Adding {parent_directory} to sys.path.\n")
sys.path.append(str(parent_directory))
import utils  # noqa


async def main(subnet_tag: str,
               min_sources: int,
               stream_size: int):
    package = await vm.repo(
        image_hash="8504e7851d3257f145f41fff8b68866a801795875cd17febbcb50d6d",
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )    
    async def worker(ctx: WorkContext, tasks):  
        async for task in tasks:
          mi = task.data["index"]
          length = task.data["stream_size"]          
          commands = (
            f"/opt/generators/csprng {length} > /golem/output/secret.bin;"  
            f"/opt/generators/chaos_prng {length} > /golem/output/chaos.bin"
          )
          ctx.run("/bin/sh",
              "-c",
              commands
          )
          ctx.download_file(f"/golem/output/chaos.bin", f"out/chaos{mi}.bin")
          ctx.download_file(f"/golem/output/secret.bin", f"out/secret{mi}.bin")
          try:
              # Set timeout for executing the script on the provider. Two minutes is plenty
              # of time for computing a single frame, for other tasks it may be not enough.
              # If the timeout is exceeded, this worker instance will be shut down and all
              # remaining tasks, including the current one, will be computed by other providers.
              yield ctx.commit(timeout=timedelta(seconds=75))
              # TODO: Check if job results are valid
              # and reject by: task.reject_task(reason = 'invalid file')             
              task.accept_result(result="Random streams[secret, chaos]")
          except BatchTimeoutError:
              print(
                  f"{utils.TEXT_COLOR_RED}"
                  f"Task timed out: {task}, time: {task.running_time}"
                  f"{utils.TEXT_COLOR_DEFAULT}"
              )
              raise   
    # Iterator over the frame indices that we want to render
    # Worst-case overhead, in minutes, for initialization (negotiation, file transfer etc.)
    # TODO: make this dynamic, e.g. depending on the size of files to transfer
    init_overhead = 3
    # Providers will not accept work if the timeout is outside of the [5 min, 30min] range.
    # We increase the lower bound to 6 min to account for the time needed for our demand to
    # reach the providers.
    min_timeout, max_timeout = 6, 30
    timeout = timedelta(minutes=max(min(init_overhead, max_timeout), min_timeout))
    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Executor(
        package=package,
        max_workers=min_sources,
        budget=10,
        timeout=timeout,
        subnet_tag=subnet_tag,
        event_consumer=log_summary(log_event_repr),
    ) as executor:
        random_list = []
        async for task in executor.submit(worker, [Task(data={"index": mi, "stream_size": stream_size}) for mi in range(min_sources)]):
            print(
                f"{utils.TEXT_COLOR_CYAN}"
                f"Task computed: {task}, result: {task.result}, time: {task.running_time}"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )            

if __name__ == "__main__":
    parser = utils.build_parser("Tap on Golem's entropy ocean")
    parser.set_defaults(log_file="requestor.log")
    args = parser.parse_args()

    # This is only required when running on Windows with Python prior to 3.8:
    windows_event_loop_fix()

    enable_default_logger(log_file=args.log_file)

    loop = asyncio.get_event_loop()

    subnet = args.subnet_tag
    sys.stderr.write(
        f"yapapi version: {utils.TEXT_COLOR_YELLOW}{yapapi_version}{utils.TEXT_COLOR_DEFAULT}\n"
    )
    sys.stderr.write(f"Using subnet: {utils.TEXT_COLOR_YELLOW}{subnet}{utils.TEXT_COLOR_DEFAULT}\n")
    task = loop.create_task(main(subnet_tag=args.subnet_tag,
                                 min_sources=int(args.min_sources),
                                 stream_size=int(args.stream_size)))
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print(
            f"{utils.TEXT_COLOR_YELLOW}"
            "Shutting down gracefully, please wait a short while "
            "or press Ctrl+C to exit immediately..."
            f"{utils.TEXT_COLOR_DEFAULT}"
        )
        task.cancel()
        try:
            loop.run_until_complete(task)
            print(
                f"{utils.TEXT_COLOR_YELLOW}"
                "Shutdown completed, thank you for waiting!"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass
