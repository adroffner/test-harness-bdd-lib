""" Create BDD Test Case from Gherkin Feature File.

BDD-Morelia lists the un-implemented test steps from a Feature.
This script create a full test file for them.
"""

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

# ========================================================================

TEST_CASE_FILE_FMT = """
import unittest

from morelia import run


class FeatureTestCase(unittest.TestCase):

    FEATURE_FILE = '{feature_file}'

    def test_feature(self):
        " BDD feature "
        run(self.FEATURE_FILE, self, verbose=True)
{steps_lines}
"""


class BDDTestCaseWriter(unittest.TestCase):
    """ BDD Test Case Writer

    This class creates a BDD Feature Test Class.
    It must have a Gherkin *.feature file as input.
    """

    FEATURE_FILE = ''

    def bdd_morelia_write_code(self):
        """ Write BDD feature code """
        try:
            run(self.FEATURE_FILE, self, verbose=True)
        except AssertionError as e:
            steps_code = str(e)

            if steps_code.startswith('Cannot match steps:'):
                steps_lines = '\n'.join(steps_code.split('\n')[1:])

                bdd_filename = 'test_{}.py'.format(get_py_name(self.FEATURE_FILE))
                with open(bdd_filename, 'w') as f:
                    print('# Feature File: {}'.format(self.FEATURE_FILE), file=f)
                    print(TEST_CASE_FILE_FMT.format_map({
                        'feature_file': self.FEATURE_FILE,
                        'steps_lines': steps_lines
                    }), file=f)
            else:
                raise


# ========================================================================


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: {} <BDD *.feature file>'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)

    BDDTestCaseWriter.FEATURE_FILE = sys.argv.pop()
    print('Compiling Feature: ', BDDTestCaseWriter.FEATURE_FILE, '...\n\n',
          file=sys.stderr)

    # unittest.main(verbosity=2)

    testSuite = unittest.TestSuite()
    testSuite.addTest(BDDTestCaseWriter('bdd_morelia_write_code'))
    result = unittest.TextTestRunner(verbosity=2).run(testSuite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
