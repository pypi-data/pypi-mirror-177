"""
Module containing all checks for validating classifiers
"""
import logging
from typing import Set

from trove_classifiers import all_classifiers as trove_all_classifiers
from trove_classifiers import deprecated_classifiers as trove_deprecated_classifiers

from .logger import pretty_print_set


def disjoint_checker(set_A: Set[str], set_B: Set[str]) -> None:
    """
    Validates that two sets are disjoint

    :param set_A: First set
    :param set_B: Second set
    """
    if not set_A.isdisjoint(set_B):
        pretty_intersection = pretty_print_set(set_A.intersection(set_B))
        logging.critical("Accepted list and denied list are not disjoint.")
        logging.info(
            f"Found the following classifiers in the intersection:\n{pretty_intersection}"
        )
        raise SystemExit(1)


def check_accepted(
    accepted_classifiers: Set[str], classifiers: Set[str], strict_mode: bool = False
) -> None:
    """
    Verifies the overlap between the classifiers and accepted_classifiers.
    In case of strict_mode, the overlap should be exact.

    :param accepted_classifiers: Classifiers that are accepted
    :param classifiers: Classifiers to check
    :param strict_mode: Sets strict_mode
    """
    classifiers_not_in_accepted = classifiers.difference(accepted_classifiers)
    if classifiers_not_in_accepted:
        pretty_not_in_accepted = pretty_print_set(classifiers_not_in_accepted)
        logging.error("Found classifiers that are not explicitely accepted.")
        logging.info(
            f"The following classifiers are missing in the accepted list:\n{pretty_not_in_accepted}"
        )
        raise SystemExit(1)
    if strict_mode:
        classifiers_not_in_package = accepted_classifiers.difference(classifiers)
        if classifiers_not_in_package:
            pretty_not_in_package = pretty_print_set(classifiers_not_in_package)
            logging.error(
                "Actual classifiers and accepted classifiers are not exactly the same."
            )
            logging.info(
                f"The following classifiers are missing in the package classifiers:\n{pretty_not_in_package}"
            )
            raise SystemExit(1)


def check_denied(denied_classifiers: Set[str], classifiers: Set[str]) -> None:
    """
    Checks whether the difference between the classifiers and denied_classifiers is empty.
    In case of strict_mode, the overlap should be exact.

    :param denied_classifiers: Classifiers that are denied
    :param classifiers: Classifiers to check
    """
    classifiers_in_denied = classifiers.intersection(denied_classifiers)
    if classifiers_in_denied:
        pretty_in_denied = pretty_print_set(classifiers_in_denied)
        logging.error("Found classifiers that are denied.")
        logging.info(
            f"The following denied classifiers are found in package classifiers:\n{pretty_in_denied}"
        )
        raise SystemExit(1)


def check_trove(classifiers: Set[str], strict_mode: bool = False) -> None:
    """
    Checks whether the classifiers are in line with trove-classifiers, the canonical source for classifiers on PyPI.
    In case of strict_mode, deprecated classifiers error.

    :param classifiers: Classifiers to check
    """
    classifiers_not_in_trove = classifiers.difference(trove_all_classifiers)
    if classifiers_not_in_trove:
        pretty_not_in_trove = pretty_print_set(classifiers_not_in_trove)
        logging.error("Found classifiers that are not in the trove list.")
        logging.info(
            f"The following classifiers are missing in the trove list:\n{pretty_not_in_trove}"
        )
        raise SystemExit(1)
    classifiers_in_deprecated = classifiers.intersection(
        set(trove_deprecated_classifiers.keys())
    )
    if classifiers_in_deprecated:
        pretty_in_deprecated = pretty_print_set(classifiers_in_deprecated)
        error_text = "Found deprecated classifiers."
        if not strict_mode:
            logging.warning(error_text)
        else:
            logging.error(error_text)
        logging.info(
            f"The following classifiers are deprecated:\n{pretty_in_deprecated}"
        )
        logging.debug("Consider replacing deprecated classifiers.")
        for deprecated_classifier in classifiers_in_deprecated:
            replace_suggestions = set(
                trove_deprecated_classifiers[deprecated_classifier]
            )
            if replace_suggestions:
                logging.debug(
                    f"  '{deprecated_classifier}' can be replaced with one of the following:\n{pretty_print_set(replace_suggestions)}"
                )
            else:
                logging.debug(
                    f"  '{deprecated_classifier}' should be removed, no alternatives suggested."
                )
        if strict_mode:
            raise SystemExit(1)
