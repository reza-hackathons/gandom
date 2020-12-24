#!/usr/bin/env python3

import io
import sys
import os
import json
import random
import base64

def main():
  random_list = []
  for filename in os.listdir("./out"):
    if filename.startswith("chaos") and filename.endswith(".bin"):
      with open(f"./out/{filename}", "rb") as f:
        stream = f.read()
        if len(stream):
          random_list.append(stream)
  if not len(random_list):
    print("Not enough entropy.")
    sys.exit(-1)
  chaos_obj = {}
  # pick two, remove them from the list, xor them and put the result back
  if len(random_list) > 2:
    random.seed()
    p = random.sample(range(len(random_list)), k=2)
    e1 = random_list[p[0]]
    e2 = random_list[p[1]]
    for i in p:
      del random_list[i]
    chaos_obj["xored"] = base64.b64encode(bytes(a ^ b for (a, b) in zip(e1, e2))).decode("utf-8")
  chaos_obj["streams"] = [base64.b64encode(e).decode("ASCII") for e in random_list]
  json_obj = {"chaos": chaos_obj}
  with open("random.json", "w") as f:
    json.dump(json_obj, f)  

if __name__ == '__main__':
  main()
