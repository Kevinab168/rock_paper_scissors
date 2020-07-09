import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
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


@pytest.fixture
def create_game(driver, live_server):
    def action(user):
        users_field = driver.find_element_by_css_selector('[data-test="users"]')
        users_field.send_keys(user.username)
        create_game = driver.find_element_by_css_selector('[data-test="create-game"]')
        create_game.click()
    return action


@pytest.fixture
def select_send_option(driver, live_server):
    def action(value):
        select_item = Select(driver.find_element_by_css_selector('[data-test="choice"]'))
        select_item.select_by_value(value)
        send_move = driver.find_element_by_css_selector('[data-test="send-move"]')
        send_move.click()
    return action


@pytest.fixture
def log_out(driver, live_server):
    def action():
        log_out = driver.find_element_by_css_selector('[data-test="log-out"]')
        log_out.click()
    return action
