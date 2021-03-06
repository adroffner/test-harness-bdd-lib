""" BDD Test Harness: Compiler

Compile a BDD Test Case from its Gherkin Feature file.

BDD-Morelia lists the un-implemented test steps from a Feature.
This module compiles a full python test module to aid in programming.
"""

import os.path
import re
import sys
import unittest

from morelia import run

# Fold *.feature file name to valid python3 identifier.
PY_NAME_OK_RE = re.compile(r'\W+', flags=re.ASCII)


def get_scenario_id(feature_filename):
    """ Get Scenario ID.

    Get scenario ID from the *.feature filename.
    Drop the suffix .feature and sanitize the string.

    Convert `raw_str` to a valid python3 identifier.
    Any non-word characters become '_'.

    :param raw_str: raw input string
    :returns: a python3 identifier
    """

    raw_str = '.'.join(feature_filename.split('.')[:-1])
    scenario_id = PY_NAME_OK_RE.sub('_', raw_str)
    # Cannot start with a digit.
    if re.match(r'^\d', scenario_id):
        scenario_id = 'a' + scenario_id

    return scenario_id


def get_bdd_module_name(testing_prefix, feature_filename):
    """ Get BDD Python Module Name.

    Extract the feature file's root name and scenario ID
    to declare a python module.

    Returns a scenario ID and a valid python module filename.

    :param str testing_prefix: testing prefix mode, e.g "QA" or "Unit Test"
    :param str feature_filename: feature file's name
    :returns: a tuple (scenario_id, feature_filename)
    """

    feature_filename = os.path.split(feature_filename)[-1]
    scenario_id = get_scenario_id(feature_filename)
    bdd_filename = '{}_{}_feature.py'.format(testing_prefix, scenario_id)
    return (scenario_id, bdd_filename)

# ========================================================================

TEST_CASE_FILE_FMT = """
import unittest

from morelia import run


class FeatureTestCase(unittest.TestCase):

    FEATURE_FILE = '{feature_file}'

    def {testing_prefix}_scenario_{scenario_id}(self):
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
    PACKAGE_DIRECTORY = ''

    def bdd_morelia_write_code(self):
        """ Write BDD feature code """
        try:
            run(self.FEATURE_FILE, self, verbose=True)
        except AssertionError as e:
            steps_code = str(e)

            if steps_code.startswith('Cannot match steps:'):
                steps_lines = '\n'.join(steps_code.split('\n')[1:])

                (scenario_id, bdd_filename) = get_bdd_module_name(self.TESTING_PREFIX, self.FEATURE_FILE)
                with open(os.path.join(self.PACKAGE_DIRECTORY, bdd_filename), 'w') as f:
                    print('# Feature File: {}'.format(self.FEATURE_FILE), file=f)
                    print(TEST_CASE_FILE_FMT.format_map({
                        'feature_file': self.FEATURE_FILE,
                        'scenario_id': scenario_id,
                        'steps_lines': steps_lines.rstrip(),
                        'testing_prefix': self.TESTING_PREFIX
                    }), file=f)

                # Show the new module's filename.
                print('New BDD Test Case module: "{}"\n'.format(bdd_filename),
                      file=sys.stderr)
            else:
                raise


# ========================================================================


def compile(feature_file, testing_prefix='test', package_directory='.'):
    """ BDD Test Case Module Compiler.

    This is the main entry point to the compiler.
    It writes a new local file in the current directory.

    :param feature_file: A BDD Gherkin Feature file
    :param testing_prefix: Set Testing Stage Prefix, e.g. "qa" Quality Assurance
    :param package_directory: package directory where test modules will be created
    :returns: True when compilation was successful
    """

    # Cannot re-compile FEATURE_FILE; BDD morelia will just run the existing file.
    (scenario_id, new_testcase_filename) = get_bdd_module_name(testing_prefix, feature_file)
    if os.path.isfile(new_testcase_filename):
        print('Cannot compile new feature file, "{}" already exists.\n'.format(
            new_testcase_filename), file=sys.stderr)
        return False

    BDDTestCaseWriter.FEATURE_FILE = feature_file
    BDDTestCaseWriter.TESTING_PREFIX = testing_prefix
    BDDTestCaseWriter.PACKAGE_DIRECTORY = package_directory

    print('Compiling Feature: {}...\n\n'.format(BDDTestCaseWriter.FEATURE_FILE),
          file=sys.stderr)

    testSuite = unittest.TestSuite()
    testSuite.addTest(BDDTestCaseWriter('bdd_morelia_write_code'))
    result = unittest.TextTestRunner(verbosity=0).run(testSuite)

    return result.wasSuccessful()
