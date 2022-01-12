Feature: Pressing Calculator Buttons
  I want to be able to press Calculator buttons

  Scenario: Calculator has no memory when turned off
    Given the Calculator is powered off
    Then the memory value is zero

  Scenario: Calculator loses its memory after I turn it off
    Given the Calculator is powered on
    When I save "5" to the memory
    And I press the calculator power button
    Then the memory value is zero

  Scenario: Calculator loses its memory after I hit clear memory button
    Given the Calculator is powered on
    When I save "31" to the memory
    And I press the calculator clear memory button
    Then the memory value is zero