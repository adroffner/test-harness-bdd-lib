import unittest
from unittest import TestCase, mock

from testharness.bdd.tm4j import utils

TESTCASE_JSON = {
    "owner": "testUser",
    "updatedBy": "testUser",
    "updatedOn": "2018-10-31T12:00:00.000Z",
    "majorVersion": 1,
    "priority": "Normal",
    "createdOn": "2018-10-25T19:30:00.000Z",
    "objective": "Test",
    "projectKey": "TST",
    "folder": "/BDD Examples",
    "latestVersion": True,
    "createdBy": "testUser",
    "testScript": {
      "text": '\n'.join([
          "When User GETs endpoint <relative_url>",
          "Then the response code is <status_code>",
          "And the response content-type is <content_type>",
          "And the response JSON has fields <field_list>"
          "",
          "Examples:",
          "    | relative_url    | status_code | content_type     | field_list  |",
          ("    | /swagger.json   | 200         | application/json | "
           "swagger,basePath,paths,info,produces,consumes,tags,definitions,responses,host |"),
          "    | /sample/servers | 200         | application/json | WFA_SERVERS,message |",
          "    | /sample         | 404         | application/json | message |"
      ]),
      "id": 2,
      "type": "BDD"
    },
    "issueLinks": [
      "TST-13"
    ],
    "lastTestResultStatus": "Not Executed",
    "name": "Test Case Example",
    "parameters": {
      "variables": [],
      "entries": []
    },
    "key": "TST-T1",
    "status": "Approved"
}

SCENARIO_TEXT = """        When User GETs endpoint <relative_url>
        Then the response code is <status_code>
        And the response content-type is <content_type>
        And the response JSON has fields <field_list>
        Examples:
            | relative_url    | status_code | content_type     | field_list  |
            | /swagger.json   | 200         | application/json | swagger,basePath,paths,info,produces,consumes,tags,definitions,responses,host |
            | /sample/servers | 200         | application/json | WFA_SERVERS,message |
            | /sample         | 404         | application/json | message |"""  # noqa: E501


@unittest.skip('Removing JIRA TM4J')
class TM4JUtilsTests(TestCase):

    maxDiff = None

    def test_create_bdd_feature_file(self):
        with mock.patch('testharness.bdd.tm4j.utils.open',
                        mock.mock_open()) as mocked_bdd_file:
            utils.create_bdd_feature_file(TESTCASE_JSON)

            feature_header = utils._get_feature_scenario_header(
                TESTCASE_JSON, has_outline=True)
            self.assertEqual(
                mocked_bdd_file().write.mock_calls, [
                    mock.call(feature_header),
                    mock.call(SCENARIO_TEXT),
                ])
