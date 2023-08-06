"""
Classifier-checker validates configured classifiers for you!
"""

import logging

from .argparser import parser
from .classifier_checks import (
    check_accepted,
    check_denied,
    check_trove,
    disjoint_checker,
)
from .logger import configuration_string, configure_logger, pretty_print_set
from .utils import combine_classifiers, get_package_classifiers
from .version import __version__ as __version__


def main() -> None:
    """
    Main entrypoint of package
    """
    args = parser.parse_args()
    configure_logger(logging.DEBUG if args.verbose else logging.INFO)
    logging.info(configuration_string(args))

    package = args.package
    accepted_classifiers = combine_classifiers(args.accept, args.accept_file)
    denied_classifiers = combine_classifiers(args.deny, args.deny_file)
    disjoint_checker(accepted_classifiers, denied_classifiers)

    logging.info(f"Validating classifiers for package '{package}'")
    package_classifiers = get_package_classifiers(package_name=package)
    logging.debug(
        f"Found the following classifiers:\n{pretty_print_set(package_classifiers)}"
    )
    if args.ignore_private:
        logging.info("Ignoring classifiers starting with 'Private ::'.")
        package_classifiers = {
            package_classifier
            for package_classifier in package_classifiers
            if not package_classifier.startswith("Private ::")
        }
        logging.debug(
            f"Trimmed classifiers to:\n{pretty_print_set(package_classifiers)}"
        )

    if args.trove:
        logging.info("Validating trove classifiers...")
        check_trove(package_classifiers, strict_mode=args.strict)

    if denied_classifiers:
        logging.info("Validating denied classifiers...")
        logging.debug(f"Denied classifiers:\n{pretty_print_set(denied_classifiers)}")
        check_denied(denied_classifiers, package_classifiers)
    else:
        logging.info("Skipping denied classifiers check, deny list is empty.")

    if accepted_classifiers:
        logging.info("Validating accepted classifiers...")
        logging.debug(
            f"Accepted classifiers:\n{pretty_print_set(accepted_classifiers)}"
        )
        check_accepted(
            accepted_classifiers, package_classifiers, strict_mode=args.strict
        )
    else:
        logging.info("Skipping accepted classifiers check, accept list is empty.")

    logging.info("Success! No issues discovered.")
