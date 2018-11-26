""" TM4J Test Run: Test Results

Compose a TM4J test run document from the unittest output.
unittest can create XUnit XML, but not the TM4J "testrun" JSON format.
"""

from junitparser import JUnitXml, TestSuite, Error, Failure, Skipped

import logging

log = logging.getLogger(__name__)


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

        Create a Test Run JSON dict from the test "suite".

        :param suite: an XUnit testsuite DOM
        :returns: a Test Run JSON dict
        """

        (script_results, status_all) = self.get_script_results(suite)

        testrun_json = {
          "projectKey": "TC",
          # "testPlanKey": "TC-P1",  # Are Test Plans required?
          "name": suite.name,
          "status": "Done",
          "items": [
            {
              "testCaseKey": "TC-T1",
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

        Get testrun scriptResults from test suite as JSON list.
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
        :returns: a tuple (script_results, status_all)
        """

        script_result_list = []
        counter = SuiteStatusCounter()

        for index, case in enumerate(suite):
            # handle cases
            log.debug('[%s] Test Case: %s', self.xunit_filename, case)

            status_code = self.testcase_status(case.result)
            counter.tally(status_code)

            script_result = {
              "index": index,
              "status": status_code,
              "comment": case.name,
            }
            script_result_list.append(script_result)

        return (script_result_list, counter.status_all)


if __name__ == '__main__':  # pragma: no cover
    from pprint import pprint

    xml_test_file = 'tests/testharness/bdd/tm4j/xunit_samples/prove_script_results.xml'
    reporter = TM4JTestRunReporter(xml_test_file, 'ad718x')

    results = reporter.all_testrun_reports
    pprint(results, indent=4)
