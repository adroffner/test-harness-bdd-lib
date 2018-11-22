#! /usr/bin/env python
""" Compile BDD Test Case from Gherkin Feature File.

BDD-Morelia lists the un-implemented test steps from a Feature.
This script creates a full python test module for them.
"""

import argparse
import sys

from testharness.bdd.compiler import testcase_writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compile BDD Test Case module from Gherkin Feature File.")

    parser.add_argument("-p", "--testing_prefix",
                        metavar='"test_stage"',
                        choices=['test', 'qa'],
                        default="test",
                        help='Set Testing Stage Prefix, e.g. "qa" Quality Assurance')
    parser.add_argument("feature_file",
                        metavar="<BDD *.feature>",
                        help="A BDD Gherkin Feature file")

    args = parser.parse_args()

    result_ok = testcase_writer.compile(args.feature_file, args.testing_prefix)

    if result_ok:
        sys.exit(0)
    else:
        sys.exit(1)
