""" TM4J Test Run: Test Results

Compose a TM4J test run document from the unittest output.
unittest can create XUnit XML, but not the TM4J "testrun" JSON format.
"""

from junitparser import JUnitXml, TestSuite, Error, Failure, Skipped

import logging
import warnings

log = logging.getLogger(__name__)


class MultipleTestCaseKeysWarning(UserWarning):
    pass


class SuiteStatusCounter(object):
    """ Suite Status Counter.

    Count all test case status codes in this suite.
    The status codes are TM4J strings, e.g. "Passed".

    Finally, determine the whole suite status code.
    """

    def __init__(self):
        self.counters = {
            'Blocked': 0,
            'Fail': 0,
            'Not Executed': 0,
            'Pass': 0
        }

    def tally(self, status):
        """ Tally another test case status.

        :param status: TM4J status string
        """
        if status in self.counters:
            self.counters[status] += 1

    @property
    def status_all(self):
        """ Status All test cases in the suite.

        :returns: the overall test suite status
        """

        if self.counters['Blocked'] > 0:
            return 'Blocked'  # Errors running some test cases
        elif self.counters['Fail'] > 0:
            return 'Fail'
        elif self.counters['Pass'] > 0:
            return 'Pass'
        else:
            # Every other status is zero
            # All test cases were skipped.
            return 'Not Executed'


class TM4JTestRunReporter(object):
    """ TM4J Test Run Reporter.

    Python unittest generates XUnit XML report files.
    This reporter converts the XML into TM4J "/testrun" JSON
    to be posted via the REST API.

        "items"         := XUnit testsuites (expect only one suite)
        "scriptResults" := XUnit testcases
    """

    def __init__(self, xunit_filename, analyst_id, comment='', environment=''):
        """ Init TM4JTestRunReporter.

        :param str xunit_filename: an XUnit XML report file
        :param str analyst_id: Test Analyst user ID in JIRA
        :param str comment: optional comment for test suite(s)
        :param str environment: JIRA Test Environment name (must match exactly)
        """

        self.xunit_filename = xunit_filename
        self.user_key = analyst_id
        self.comment = comment
        self.environment = environment
        self._test_runs_list = []

        xml = JUnitXml.fromfile(self.xunit_filename)
        if isinstance(xml, TestSuite):
            xml = [xml]

        for suite in xml:
            # handle suites as test runs.
            log.debug('[%s] Suite: %s', self.xunit_filename, suite)
            self._test_runs_list.append(self.get_testrun(suite))

    @property
    def all_testrun_reports(self):
        """ All Test Run Reports.

        This is the list of all "testrun" reports as JSON.

        :returns: list of testrun JDON dicts
        """

        return self._test_runs_list

    def testcase_status(self, result):
        """ Test Case Status.

        Convert an XUnit test result to a TM4J status string.

        :param object result: a junitparser result object, e.g. Failure
        :raises ValueError: when the result is not valid
        :returns: a TM4J status
        """

        if isinstance(result, Error):
            return "Blocked"
        elif isinstance(result, Failure):
            return "Fail"
        elif isinstance(result, Skipped):
            return "Not Executed"
        elif result is None:
            return "Pass"
        else:
            raise ValueError('TestCase.status "{}" is invalid'.format(result))

    def get_testrun(self, suite):
        """ Get Test Run.

        Create a Test Run JSON dict from one "testsuite".

        :param suite: an XUnit testsuite DOM
        :returns: a Test Run JSON dict
        """

        (testcase_key, script_results, status_all) = self.get_script_results(suite)

        testrun_json = {
          "projectKey": testcase_key.split('-')[0],
          # "testPlanKey": "TC-P1",  # Are Test Plans required?
          "name": suite.name,
          "status": "Done",
          "items": [
            {
              "testCaseKey": testcase_key,
              "status": status_all,
              "environment": self.environment,
              "comment": self.comment,
              "userKey": self.user_key,
              "executionTime": suite.time,
              "executionDate": suite.timestamp,
              "scriptResults": script_results
            }
          ]
        }

        return testrun_json

    def get_script_results(self, suite):
        """ Get Script Results.

        Get testrun scriptResults from "testcase(s)" in the "testsuite".
        Compose a JSON list of all "testcase(s)" and the overall status code.
        This returns a tuple to report the individual and overall health.

            Return tuple: (script_results, status_all)
            script_results := a list of testrun scriptResults dicts
            status_all     := the worst case status among the scriptResults

            "scriptResults": [
                {
                  "index": 0,
                  "status": "Pass",
                  "comment": "Scenario 1 Passed."
                },
                ...
            ]

        :param suite: an XUnit testsuite DOM
        :returns: a tuple (testcase_key, script_results, status_all)
        """

        script_result_list = []
        testcase_key = ''
        counter = SuiteStatusCounter()

        for index, case in enumerate(suite):
            # handle cases
            log.debug('[%s] Test Case: %s', self.xunit_filename, case)

            # Set TestCaseKey: All keys must match the same ticket.
            if testcase_key:
                if not case.name.endswith(testcase_key.replace('-', '_')):
                    warnings.warn('Only one test-case key is supported.',
                                  MultipleTestCaseKeysWarning)
                    continue  # for loop: suite
            else:
                # Assume JIRA Test Case Key is last 2 tokens in name="..."
                testcase_key = '-'.join(case.name.split('_')[-2:])

            status_code = self.testcase_status(case.result)
            counter.tally(status_code)

            script_result = {
              "index": index,
              "status": status_code,
              "comment": case.name,
            }
            script_result_list.append(script_result)

        return (testcase_key, script_result_list, counter.status_all)


if __name__ == '__main__':  # pragma: no cover
    from pprint import pprint

    xml_test_file = 'tests/testharness/bdd/tm4j/xunit_samples/prove_script_results.xml'
    reporter = TM4JTestRunReporter(xml_test_file, 'someUserKey',
                                   comment='This translates xunit XML to JIRA TM4J JSON testruns.')

    results = reporter.all_testrun_reports
    pprint(results, indent=4)
