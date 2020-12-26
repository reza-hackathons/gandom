#!/usr/bin/env python3

import io
import sys
import os
import json
import random
import base64

def load_random_files(prefix, path="./out"):
  random_list = []
  for filename in os.listdir(path):
    if filename.startswith(prefix) and filename.endswith(".bin"):
      with open(f"{path}/{filename}", "rb") as f:
        stream = f.read()
        if len(stream):
          random_list.append(stream)
  random_obj = {}
  # pick two, remove them from the list, xor them and put the result back
  if len(random_list) > 2:
    random.seed()
    p = random.sample(range(len(random_list)), k=2)
    e1 = random_list[p[0]]
    e2 = random_list[p[1]]
    for i in p:
      del random_list[i]
    random_obj["xored"] = base64.b64encode(bytes(a ^ b for (a, b) in zip(e1, e2))).decode("utf-8")
  random_obj["streams"] = [base64.b64encode(e).decode("ASCII") for e in random_list]
  return random_obj


def main():
  json_obj = {
    "csprng": load_random_files("secret"),
    "chaos": load_random_files("chaos")
  }
  if not (len(json_obj["csprng"]) + len(json_obj["chaos"])):
    print("Not enough entropy.")
    sys.exit(-1)
  with open("random.json", "w") as f:
    json.dump(json_obj, f)  

if __name__ == '__main__':
  main()
