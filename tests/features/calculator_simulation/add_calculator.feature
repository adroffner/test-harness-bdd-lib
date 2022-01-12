Feature: Adding numbers with a Calculator
  I want to be able to add numbers using a Calculator

  Background:
    Given the Calculator is powered on

  Scenario: Add two positive numbers
    When I add "1" and "1"
    Then the sum should be "2"

  Scenario: Add a positive and negative number
    When I add "1" and "-1"
    Then the sum should be "0"

  Scenario: Add two negative numbers
    When I add "-1" and "-1"
    Then the sum should be "-2"