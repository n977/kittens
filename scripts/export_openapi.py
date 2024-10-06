import sys
import logging
import argparse
import json
from contextlib import nullcontext
from uvicorn.importer import import_from_string

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("app", help="app import string")
parser.add_argument("-o", "--out", help="output file", default=None)


def export():
    args = parser.parse_args()

    if not args.out or args.out == "-":
        out = nullcontext(sys.stdout)
    else:
        out = open(args.out, "w")

    app = import_from_string(args.app)
    openapi = app.openapi()

    with out as f:
        json.dump(openapi, f)

    logger.info("OK")


if __name__ == "__main__":
    export()
