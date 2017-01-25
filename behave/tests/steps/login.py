import os

from selenium.webdriver.common.keys import Keys
from behave import *

from utils import build_rhod_endpoint


@given('a user exists and they are allowed to login')
def step_impl(context):
    pass


@when('the user tries to login with correct credentials')
def step_impl(context):
    driver = context.browser
    url = build_rhod_endpoint('login')
    driver.get(url)
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')
    username.send_keys(os.environ['CDMS_USERNAME'].lower())
    password.send_keys(os.environ['CDMS_PASSWORD'])
    driver.find_element_by_css_selector(".button[type='submit']").click()
    assert True is False


@then('the user is logged in successfully')
def step_impl(context):
    assert context.failed is False
