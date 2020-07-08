import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.yield_fixture(scope="session")
def driver():
    if os.environ.get('CI'):
        driver_options = Options()
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
        driver_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=driver_options)
    else:
        driver = webdriver.Remote('http://127.0.0.1:9515')
    with driver:
        yield driver
