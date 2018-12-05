#!/usr/bin/python
import json
import os
import sys


def main():
    directory = sys.argv[1]
    a = [x for x in os.listdir(directory) if x.endswith(".conf")]
    data = [{"{#POOL}": pool.replace('.conf','')} for pool in a]
    print(json.dumps({"data": data}, indent=4))

if __name__ == '__main__':
    main()

