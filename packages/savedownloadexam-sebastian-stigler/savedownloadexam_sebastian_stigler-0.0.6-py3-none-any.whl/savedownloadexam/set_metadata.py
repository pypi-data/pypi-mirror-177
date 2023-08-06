# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = canvas_api.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import json
import logging
import os.path
import sys
from pprint import pprint

from savedownloadexam import __version__

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def set_metadata(filename: str, base_name: str, list: bool):
    if not os.path.isfile(filename):
        _logger.error(f"{filename} doesn't exist.")
        sys.exit(1)
    if not filename.endswith(".ipynb"):
        _logger.error(f"{filename} is not a jupyter notebook (wrong extension).")
        sys.exit(1)
    try:
        with open(filename) as fil:
            data = json.load(fil)
    except json.JSONDecodeError:
        _logger.error(f"{filename} is not a jupyter notebook (no json data).")
        sys.exit(1)
    for key in ["cells", "metadata", "nbformat", "nbformat_minor"]:
        if key not in data:
            _logger.error(f"Key {key} is not in the jupyter notebook.")
            sys.exit(1)
    if list:
        pprint(data["metadata"])
        return

    data["metadata"]["savedownload"] = {"base_name": base_name}

    with open(filename, "w") as fil:
        json.dump(data, fil)
    print(f"base_name set to '{base_name}'.")


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Set metadata for the use of savedownloadexam."
    )
    parser.add_argument("filename", help="Name of the jupyter notebook file")
    parser.add_argument(
        "-b",
        "--base_name",
        help="The base_name for the submission (default: %(default)s)",
        default="Exam",
    )
    parser.add_argument(
        "-l",
        "--list",
        help="Print the metadata from the jupyter notebook",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="set_metadata {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "%(levelname)s: %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    set_metadata(args.filename, args.base_name, args.list)
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
