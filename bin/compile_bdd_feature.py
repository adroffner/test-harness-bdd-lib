#! /usr/bin/env python
""" Compile BDD Test Case from Gherkin Feature File.

BDD-Morelia lists the un-implemented test steps from a Feature.
This script creates a full python test module for them.
"""

import argparse
import os.path
import re
import sys
import unittest

from morelia import run

# Fold *.feature file name to valid python3 identifier.
PY_NAME_OK_RE = re.compile(r'\W+', flags=re.ASCII)


def get_py_name(raw_str):
    """ Get Python3 Name.

    Convert `raw_str` to a valid python3 identifier.
    Any non-word characters become '_'.

    :param raw_str: raw input string
    :returns: a python3 identifier
    """

    return PY_NAME_OK_RE.sub('_', raw_str)


def get_bdd_module_name(testing_prefix, feature_filename):
    """ Get BDD Python Module Name.

    Extract the feature file's root name and declare a python module.

    :param str testing_prefix: testing prefix mode, e.g "QA" or "Unit Test"
    :param str feature_filename: feature file's name
    :returns: a valid python module filename
    """

    feature_filename = os.path.split(feature_filename)[-1]
    bdd_filename = '{}_{}.py'.format(testing_prefix, get_py_name(feature_filename))
    return bdd_filename

# ========================================================================

TEST_CASE_FILE_FMT = """
import unittest

from morelia import run


class FeatureTestCase(unittest.TestCase):

    FEATURE_FILE = '{feature_file}'

    def {testing_prefix}_scenario(self):
        "BDD Scenario(s): {feature_file}"
        run(self.FEATURE_FILE, self, verbose=True)
{steps_lines}"""


class BDDTestCaseWriter(unittest.TestCase):
    """ BDD Test Case Writer

    This class creates a BDD Feature Test Class.
    It must have a Gherkin *.feature file as input.
    """

    FEATURE_FILE = ''
    TESTING_PREFIX = 'test'

    def bdd_morelia_write_code(self):
        """ Write BDD feature code """
        try:
            run(self.FEATURE_FILE, self, verbose=True)
        except AssertionError as e:
            steps_code = str(e)

            if steps_code.startswith('Cannot match steps:'):
                steps_lines = '\n'.join(steps_code.split('\n')[1:])

                bdd_filename = get_bdd_module_name(self.TESTING_PREFIX, self.FEATURE_FILE)
                with open(bdd_filename, 'w') as f:
                    print('# Feature File: {}'.format(self.FEATURE_FILE), file=f)
                    print(TEST_CASE_FILE_FMT.format_map({
                        'feature_file': self.FEATURE_FILE,
                        'steps_lines': steps_lines.rstrip(),
                        'testing_prefix': self.TESTING_PREFIX
                    }), file=f)

                # Show the new module's filename.
                print('New BDD Test Case module: "{}"\n'.format(bdd_filename),
                      file=sys.stderr)
            else:
                raise


# ========================================================================


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

    BDDTestCaseWriter.FEATURE_FILE = args.feature_file
    BDDTestCaseWriter.TESTING_PREFIX = args.testing_prefix

    print('Compiling Feature: ', BDDTestCaseWriter.FEATURE_FILE, '...\n\n',
          file=sys.stderr)

    testSuite = unittest.TestSuite()
    testSuite.addTest(BDDTestCaseWriter('bdd_morelia_write_code'))
    result = unittest.TextTestRunner(verbosity=0).run(testSuite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
