Feature: user login

  Scenario: successful login
    Given a user exists and they are allowed to login
    When the user tries to login with correct credentials
    Then the user is logged in successfully
