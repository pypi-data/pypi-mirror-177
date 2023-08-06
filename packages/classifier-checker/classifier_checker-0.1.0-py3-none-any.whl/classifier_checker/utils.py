"""
Module containing utilities
"""
import logging
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path
from typing import List, Set


def get_package_classifiers(package_name: str) -> Set[str]:
    """
    Infers the classifiers of a package

    :param package_name: Name of the package
    :return: Set of classifiers
    """
    classifiers = set()
    try:
        classifiers = set(metadata(package_name).get_all("Classifier"))
    except PackageNotFoundError:
        logging.critical(
            f"Package '{package_name}' not found, please ensure '{package_name}' is installed."
        )
        raise SystemExit(1)
    return classifiers


def combine_classifiers(listed_classifiers: List[str], path_to_file: str) -> Set[str]:
    """
    Combines classifiers (from list and file) into a single set of classifiers

    :param listed_classifiers: List of classifiers
    :param path_to_file: Path to file containing classifiers (new line-separated)
    :return: Union set of all classifiers
    """
    classifiers = set(_.strip() for _ in listed_classifiers)
    if path_to_file:
        try:
            path = Path(path_to_file)
            with open(path, "r") as file:
                classifiers.update(set(_.strip() for _ in file.read().splitlines()))
        except FileNotFoundError:
            logging.critical(
                f"File '{path_to_file}' was not found. Tried to access file at {path.absolute()}."
            )
            raise SystemExit(1)
    # Discard the new line
    classifiers.discard("")
    return classifiers
