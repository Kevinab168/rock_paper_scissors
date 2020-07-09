from play_game.models import User, Game
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def homepage(request):
    return render(request, 'index.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user=user)
            return redirect('homepage')
    return render(request, 'log_in.html')


def games(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user1 = request.user
        user2_name = request.POST['users']
        user2 = User.objects.all().get(username=user2_name)
        new_game = Game.objects.create()
        new_game.users.add(user1, user2)
        return redirect(f'/games/{new_game.pk}')


def game(request, game_id):
    if request.user.is_authenticated:
        current_user = request.user
    game = Game.objects.all().get(pk=game_id)
    user1 = game.users.all()[0]
    user2 = game.users.all()[1]
    if current_user == user1:
        opponent = user2
    else:
        opponent = user1
    context = {
        'current_user': current_user,
        'opponent': opponent,
        'game': game
    }
    return render(request, 'game.html', context)
