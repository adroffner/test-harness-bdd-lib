""" BDD Test Harness Mixin

This python mixin class holds BDD morelia "def step_*()" functions.
These functions match the "BDD Feature File" provided.

To reuse the code below, place it after the unittest.TestCase.

    class ReusableBDDTestCaseWithMixin(unittest.TestCase, BDDStepsMixin):
        # ...
"""

from testharness.bdd.loader_mixins.common import JSONDataLoaderMixin

# BDD Feature File
"""
Feature:
    Scenario Outline: HTTP POST from a REST API.

        When User POSTs endpoint <relative_url> with <post_payload>
        Then the response code is <status_code>
        And the response content-type is <content_type>
        And the response JSON has fields <field_list>
        And the response JSON message contains <message_text>

        Examples:
                | relative_url    | status_code | content_type     | field_list | message_text | post_payload |
                | /sample/view    | 401         | application/json | TRK,ROWS,message    | SEC102E INCORRECT OR INVALID SIGNON | sample_view_login_failure_input.json |
"""


class HttpPostRestApiBDDStepsMixin(JSONDataLoaderMixin):
    """ HTTP POST REST API with BDD Steps Mixin.

    Use this mixin to have the common HTTP POST REST API steps.

    The "test client" must be named self.client and have the HTTP POST method.
    """

    def step_User_POSTs_endpoint_relative_url_with_post_payload(self, relative_url, post_payload):
        r'User POSTs endpoint (.+) with (.+)'
        post_payload = self.load_json(post_payload)
        self.response = self.client.post(relative_url, post_payload)

    def step_the_response_JSON_message_contains_message_text(self, message_text):
        r'the response JSON message contains (.+)'
        json_dict = self.response.json()
        self.assertIn(message_text, json_dict.get('message'))

    def step_the_response_code_is_status_code(self, status_code):
        r'the response code is (.+)'
        self.assertEqual(self.response.status_code, int(status_code))

    def step_the_response_content_type_is_content_type(self, content_type):
        r'the response content-type is (.+)'
        self.assertEqual(self.response.headers.get("Content-Type"), content_type)

    def step_the_response_JSON_has_fields_field_list(self, field_list):
        r'the response JSON has fields (.+)'
        field_list = field_list.split(',')
        json_dict = self.response.json()
        self.assertEqual(list(json_dict.keys()), field_list)
