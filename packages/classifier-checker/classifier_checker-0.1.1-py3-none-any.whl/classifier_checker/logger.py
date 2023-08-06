"""
Module containing logger configuration
"""
import logging
from argparse import Namespace
from typing import Set


def configure_logger(logging_level: int) -> None:
    """
    Configures logger

    :param logging_level: The level of logging to use
    """

    class Formatter(logging.Formatter):
        """
        Formatter to improve logging
        """

        def format(self, record: logging.LogRecord) -> str:
            """
            Specific formatting for logging records

            :param record: Record to log
            :return: Formatted string
            """
            if record.levelno == logging.DEBUG or record.levelno == logging.INFO:
                self._style._fmt = "%(message)s"
            else:
                prefix = " " if record.levelno == logging.CRITICAL else "\t"
                self._style._fmt = f"%(levelname)s{prefix}%(message)s"
            return super().format(record)

    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    logging.basicConfig(
        format="%(levelname)s\t%(message)s", level=logging_level, handlers=[handler]
    )


def pretty_print_set(
    set_to_print: Set[str], indent: int = 4, prefix: str = "- ", separator: str = "\n"
) -> str:
    """
    Parses set to pretty print as list of items

    :param set_to_print: The set to print
    :param indent: Indentation to use
    :param prefix: Prefix to use in front of every item
    :param separator: Separator to use
    :return: Pretty print of set
    """
    return f"{separator}".join(f"{indent*' '}{prefix}{_}" for _ in set_to_print)


def configuration_string(args: Namespace) -> str:
    """
    Returns a human-readable configuration

    :param args: Parsed cmdline args
    :return: Human-readable configuration
    """
    strict_mode = "On" if args.strict else "Off"
    ignore_private = "On" if args.ignore_private else "Off"
    trove_check = "On" if args.trove else "Off"
    return f"Configuration -- Strict mode: {strict_mode}, ignore private: {ignore_private}, trove checking: {trove_check}"
