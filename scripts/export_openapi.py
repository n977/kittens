from contextlib import nullcontext
import os
import sys

# Include the current directory in PYTHONPATH to make the main package visible.
sys.path.insert(0, os.getcwd())

import logging

# Provide the basic configuration to the logger.
logging.basicConfig()

import argparse
import json

from uvicorn.importer import import_from_string


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("app", help="App import string")
parser.add_argument("--out", help="Output file", default=None)

def export():
    args = parser.parse_args()

    if not args.out or args.out == "-":
        out = nullcontext(sys.stdout)
    else:
        out = open(args.out)

    app = import_from_string(args.app)
    openapi = app.openapi()

    with out as f:
        json.dump(openapi, f)

    logger.info("OK")


if __name__ == "__main__":
    export()
