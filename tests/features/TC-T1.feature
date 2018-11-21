Feature: 
    @TestCaseKey=TC-T1
    Scenario Outline: Show OSSCWL Servers that are available
        
        When User GETs endpoint <relative_url>
        Then the response code is <status_code>
        And the response content-type is <content_type>
        And the response JSON has fields <field_list>
        
        Examples:
                | relative_url    | status_code | content_type     | field_list  |
                | /swagger.json   | 200         | application/json | swagger,basePath,paths,info,produces,consumes,tags,definitions,responses,host |
        	    | /osscwl/servers | 200         | application/json | WFA_SERVERS,message |
                | /osscwl         | 404         | application/json | message |