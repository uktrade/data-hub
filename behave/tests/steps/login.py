from behave import *


@given('a user exists and they are allowed to login')
def step_impl(context):
    pass


@when('the user tries to login with correct credentials')
def step_impl(context):
    assert True is False


@then('the user is logged in successfully')
def step_impl(context):
    assert context.failed is False
