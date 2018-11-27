""" TM4J: Utility Functions

These functions help build BDD processes that interact with TM4J.
"""

import re

SCENARIO_EXAMPLES_RE = re.compile(r'^\s*Examples:\s*$', flags=(re.I | re.M))


def _get_feature_scenario_header(testcase_json, has_outline=False):
    """ Get Feature Scenario header.

    Build the "Feature:" and "Scenario (Outline):" headers.
    TM4J does not store these along with the script.

    When has_outline = True, this has an "Examples:" data table.
    The header must be "Scenario Outline:".

    :param dict testcase_json: a single /testcase/search record
    :param bool has_outline: does this use "Examples:" parameters
    """

    testcase_key = testcase_json['key']
    feature_name = testcase_json.get('name', '')

    header = """Feature:
    @TestCaseKey={testcase_key}
    Scenario{_outline}: {feature_name}
    """.format_map({
        'testcase_key': testcase_key,
        'feature_name': feature_name,
        '_outline': ' Outline' if has_outline else ''
    })

    return header


def create_bdd_feature_file(testcase_json):
    """ Create a BDD Feature File.

    Complete the "Feature:" file for a "BDD" type "test script".
    TM4J does not store the whole thing, just the Gherkin steps.

    This reads a single /testcase/search record, a "test case key".
    Then, it completes and writes the *.feature file to disk.

    The alternate method, REST API /automation/testcases, is wasteful.
    It downloads the whole "bdd-testcases.zip" which sends
    every *.feature file for the whole JIRA project.

    :param dict testcase_json: a single /testcase/search record
    :returns: the *.feature filename that is now on disk
    """

    test_script = testcase_json.get('testScript')
    if test_script is not None and test_script.get('type') == 'BDD':
        # Get script and indent lines 8 spaces under Scenario:.
        scenario_text = test_script.get('text', '')
        scenario_text = (' ' * 8) + scenario_text.replace('\n', '\n' + ' ' * 8)

        if SCENARIO_EXAMPLES_RE.search(scenario_text):
            has_scenario_outline = True
        else:
            has_scenario_outline = False

        feature_header = _get_feature_scenario_header(testcase_json, has_scenario_outline)

        testcase_key = testcase_json['key']
        feature_filename = '{}.feature'.format(testcase_key)

        with open(feature_filename, 'w') as f:
            print(feature_header, file=f)
            print(scenario_text, file=f)

        return feature_filename
