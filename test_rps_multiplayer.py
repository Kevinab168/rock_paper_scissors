def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert 'Rock, Paper, Scissors' in driver.page_source
    assert driver.find_element_by_css_selector('[data-test="users"]')
    assert driver.find_element_by_css_selector('[data-test="create-game"]')


def test_login(driver, live_server, log_in, user):
    new_user = user('User', 'a;lsdfkjasdf')
    log_in(my_username=new_user.username, my_password='a;lsdfkjasdf')
    assert 'User' in driver.page_source
    assert driver.current_url


def test_create_game(driver, log_in, user):
    user_1 = user('User1', 'a;lsdkfkjasdf')
    user('User2', 'adsl;dkfja;sdf')
    log_in(my_username=user_1.username, my_password='a;lsdkfkjasdf')
    users_field = driver.find_element_by_css_selector('[data-test="users"]')
    users_field.send_keys('User2')
    create_game = driver.find_element_by_css_selector('[data-test="create-game"]')
    create_game.click()
    opponents = driver.find_element_by_css_selector('[data-test="opponents"]')
    assert 'User2' in opponents.text
    assert driver.find_element_by_css_selector('[data-test="choice"]')
    assert driver.find_element_by_css_selector('[data-test="send-move"]')
