from play_game.models import Game


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert 'Rock, Paper, Scissors' in driver.page_source
    assert driver.find_element_by_css_selector('[data-test="users"]')
    assert driver.find_element_by_css_selector('[data-test="create-game"]')


def test_create_game_with_made_up_person(driver, live_server, create_game, log_in, user):
    new_user = user('User', 'a;lsdfkjasdf')
    log_in(my_username=new_user.username, my_password='a;lsdfkjasdf')
    users_field = driver.find_element_by_css_selector('[data-test="users"]')
    users_field.send_keys('fake_user_account')
    create_game = driver.find_element_by_css_selector('[data-test="create-game"]')
    create_game.click()
    error_message = driver.find_element_by_css_selector('[data-test="error-message"').text.lower()
    assert 'does not exist' in error_message


def test_create_game_non_user(driver, live_server, create_game, user):
    test_user = user('User', 'asd;alfkajsdf')
    driver.get(live_server.url)
    create_game(test_user)
    error_message = driver.find_element_by_css_selector('[data-test="error-message"]').text.lower()
    assert 'sorry, you must be signed in to do that' in error_message
    log_in_link = driver.find_element_by_css_selector('[data-test="log_in"]')
    log_in_link.click()
    assert driver.current_url == (live_server.url + '/login/')


def test_login(driver, live_server, log_in, user):
    new_user = user('User', 'a;lsdfkjasdf')
    log_in(my_username=new_user.username, my_password='a;lsdfkjasdf')
    assert 'User' in driver.page_source
    assert driver.current_url


def test_logout(driver, live_server, log_in, log_out, user):
    new_user = user('User', 'asd;alfkajsdf')
    log_in(my_username=new_user.username, my_password='asd;alfkajsdf')
    log_out()
    assert new_user.username not in driver.page_source


def test_create_game(driver, log_in, create_game, user):
    user_1 = user('User1', 'a;lsdkfkjasdf')
    user_2 = user('User2', 'adsl;dkfja;sdf')
    log_in(my_username=user_1.username, my_password='a;lsdkfkjasdf')
    create_game(user_2)
    opponents = driver.find_element_by_css_selector('[data-test="opponents"]')
    assert 'User2' in opponents.text
    assert driver.find_element_by_css_selector('[data-test="choice"]')
    assert driver.find_element_by_css_selector('[data-test="send-move"]')


def test_user_sends_move(driver, user, log_in, create_game, select_send_option):
    user_1 = user('User1', 'a;lsdkfkjasdf')
    user_2 = user('User2', 'adsl;dkfja;sdf')
    log_in(my_username=user_1.username, my_password='a;lsdkfkjasdf')
    create_game(user_2)
    select_send_option('paper')
    progress_message = driver.find_element_by_css_selector('[data-test="progress-message"]')
    assert 'waiting for User2' in progress_message.text
    game = Game.objects.all().last()
    assert 'paper' == game.user_1_move


def test_user_sends_move_non_user(driver, live_server, user, log_in, create_game, select_send_option, log_out):
    user_1 = user('User1', 'a;lsdkfkjasdf')
    user_2 = user('User2', 'adsl;dkfja;sdf')
    log_in(my_username=user_1.username, my_password='a;lsdkfkjasdf')
    create_game(user_2)
    log_out()
    game = Game.objects.all().last()
    driver.get(live_server.url + f'/games/{game.pk}')
    error_message = driver.find_element_by_css_selector('[data-test="error-message"]').text.lower()
    assert 'sorry, you must be signed in to do that' in error_message


def test_complete_game(driver, live_server, user, log_in, log_out, create_game, select_send_option):
    user_1 = user('User1', 'a;lsdkfkjasdf')
    user_2 = user('User2', 'adsl;dkfja;sdf')
    log_in(my_username=user_1.username, my_password='a;lsdkfkjasdf')
    create_game(user_2)
    select_send_option('paper')
    log_out()
    log_in(my_username=user_2.username, my_password='adsl;dkfja;sdf')
    game = Game.objects.all().last()
    driver.get(live_server.url + f'/games/{game.pk}')
    select_send_option('scissors')
    game = Game.objects.all().last()
    assert game.in_progress is False
    assert game.winning_user == user_2.username
    progress_message = driver.find_element_by_css_selector('[data-test="progress-message"')
    assert 'Complete' in progress_message.text
    winner = driver.find_element_by_css_selector('[data-test="winner"]')
    assert user_2.username in winner.text
