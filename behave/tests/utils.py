from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_chrome_webdriver():
    """Return the Chrome webdriver."""
    return webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )
