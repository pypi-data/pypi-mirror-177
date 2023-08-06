"""
Module to parse cmdline arguments
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .version import __version__

parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    prog="classifier-checker",
    description=f"Classifier-checker v{__version__}.\nClassifier-checker validates configured classifiers for you!",
    epilog="Licensed under MIT, 2022 Thomas Rooijakkers",
)

parser.add_argument("package", type=str, help="Installed package to validate")
parser.add_argument(
    "--strict",
    action="store_true",
    default=False,
    help="Enables strict mode, classifiers should be exactly equal to accepted classifiers",
)
parser.add_argument(
    "--ignore-private",
    action="store_true",
    default=False,
    help='Ignore all classifiers that start with "Private ::"',
)
parser.add_argument(
    "--trove",
    action="store_true",
    default=False,
    help="Ensure that classifiers are in line with trove-classifiers, the canonical source for classifiers on PyPI",
)
parser.add_argument(
    "-a",
    "--accept",
    type=lambda arg: arg.split(","),
    default=[],
    help="Accepted classifier(s) (comma-separated)",
)
parser.add_argument(
    "-d",
    "--deny",
    type=lambda arg: arg.split(","),
    default=[],
    help="Denied classifier(s) (comma-separated)",
)
parser.add_argument(
    "-af",
    "--accept-file",
    type=str,
    default="",
    help="Path to file containing accepted classifier(s) (new line-separated)",
)
parser.add_argument(
    "-df",
    "--deny-file",
    type=str,
    default="",
    help="Path to file containing denied classifier(s) (new line-separated)",
)
parser.add_argument(
    "--verbose", action="store_true", default=False, help="Enable verbose logging"
)
