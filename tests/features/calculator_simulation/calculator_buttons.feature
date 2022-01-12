Feature: Pressing Calculator Buttons
  I want to be able to press Calculator buttons

  Background:
    Given the Calculator is powered off

  Scenario: Calculator has no memory when turned off
    Then the memory value is zero

  Scenario: Calculator loses its memory after I turn it off
    Given the Calculator is powered on
    When I save "5" to the memory
    And I press the calculator button
    Then the memory value is zero