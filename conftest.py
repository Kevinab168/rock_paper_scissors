import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from play_game.models import User


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


@pytest.fixture
def user():
    def action(username, password):
        new_user = User.objects.create_user(username=username, password=password)
        return new_user
    return action


@pytest.fixture
def log_in(driver, live_server):
    def action(my_username, my_password):
        driver.get(live_server.url + '/login')
        username = driver.find_element_by_css_selector('[data-test="username"]')
        password = driver.find_element_by_css_selector('[data-test="password"]')
        username.send_keys(my_username)
        password.send_keys(my_password)
        log_in = driver.find_element_by_css_selector('[data-test="log-in"]')
        log_in.click()
    return action
