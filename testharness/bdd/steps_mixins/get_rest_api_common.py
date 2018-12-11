""" BDD Test Harness Mixin

This python mixin class holds BDD morelia "def step_*()" functions.
These functions match the "BDD Feature File" provided.

To reuse the code below, place it after the unittest.TestCase.

    class ReusableBDDTestCaseWithMixin(unittest.TestCase, BDDStepsMixin):
        # ...
"""

# BDD Feature File
"""
Feature:
    Scenario Outline: HTTP GET from a REST API.

        When User GETs endpoint <relative_url>
        Then the response code is <status_code>
        And the response content-type is <content_type>
        And the response JSON has fields <field_list>

        Examples:
                | relative_url    | status_code | content_type     | field_list  |
                | /swagger.json   | 200         | application/json | swagger,basePath,paths,info,produces,consumes,tags,definitions,responses,host |
"""


class HttpGetRestApiBDDStepsMixin:
    """ HTTP GET REST API with BDD Steps Mixin.

    Use this mixin to have the common HTTP GET REST API steps.

    The "test client" must be named self.client and have the HTTP GET method.
    """

    def step_User_GETs_endpoint_relative_url(self, relative_url):
        r'User GETs endpoint (.+)'
        self.response = self.client.get(relative_url)

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
