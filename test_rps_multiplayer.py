from play_game.models import Game


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
