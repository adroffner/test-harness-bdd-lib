Feature: 
    @TestCaseKey=TC-T2
    Scenario Outline: Show SAMPLE Login Failure
        
        When User POSTs endpoint <relative_url> with <post_payload>
        Then the response code is <status_code>
        And the response content-type is <content_type>
        And the response JSON has fields <field_list>
        And the response JSON message contains <message_text>
        
        Examples:
                | relative_url    | status_code | content_type     | field_list | message_text | post_payload |
                | /sample/view    | 401         | application/json | TRK,ROWS,message    | SEC102E INCORRECT OR INVALID SIGNON | sample_view_login_failure_input.json |