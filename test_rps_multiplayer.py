def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert 'Rock, Paper, Scissors' in driver.page_source
    assert driver.find_element_by_css_selector('[data-test="users"]')
    assert driver.find_element_by_css_selector('[data-test="create-game"]')
