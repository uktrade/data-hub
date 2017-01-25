import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_chrome_webdriver():
    """Return the Chrome webdriver."""
    selenium_url = 'http://selenium:{port}/wd/hub'.format(port=os.environ['SELENIUM_PORT'])
    return webdriver.Remote(
        command_executor=selenium_url,
        desired_capabilities=DesiredCapabilities.CHROME
    )


def get_base_rhod_url():
    """Rhod base url."""
    return 'http://rhod:{port}/'.format(port=os.environ['RHOD_PORT'])


def build_rhod_endpoint(endpoint_name):
    """Return full Rhos url."""
    if endpoint_name.startswith('/'):
        endpoint_name = endpoint_name[1:]
    return get_base_rhod_url() + endpoint_name
