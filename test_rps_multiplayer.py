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
