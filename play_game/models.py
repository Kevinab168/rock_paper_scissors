from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Game(models.Model):
    users = models.ManyToManyField(User)
    user_1_move = models.CharField(max_length=200)
    user_2_move = models.CharField(max_length=200)
    in_progress = models.BooleanField(default=True)
    winning_user = models.CharField(max_length=200)

    @property
    def game_progress(self):
        user_1 = self.users.all().first()
        user_2 = self.users.all().last()
        if self.user_1_move == '' and self.user_2_move == '':
            return 'waiting for players to make moves'
        elif self.user_1_move == '':
            return f'waiting for {user_1.username} to make a move'
        elif self.user_2_move == '':
            return f'waiting for {user_2.username} to make a move'
        else:
            return 'Complete'

    def set_winner(self):
        self.in_progress = False
        user_1 = self.users.all().first()
        user_2 = self.users.all().last()
        if self.user_1_move == 'paper' and self.user_2_move == 'rock':
            self.winning_user = user_1.username
        elif self.user_1_move == 'scissor' and self.user_2_move == 'rock':
            self.winning_user = user_2.username
        elif self.user_1_move == 'rock' and self.user_2_move == 'rock':
            self.winning_user = 'draw'
        elif self.user_1_move == 'paper' and self.user_2_move == 'scissors':
            self.winning_user = user_2.username
        elif self.user_1_move == 'scissors' and self.user_2_move == 'scissors':
            self.winning_user = 'draw'
        elif self.user_1_move == 'rock' and self.user_2_move == 'scissors':
            self.winning_user = user_1.username
        elif self.user_1_move == 'paper' and self.user_2_move == 'paper':
            self.winning_user = 'draw'
        elif self.user_1_move == 'scissors' and self.user_2_move == 'paper':
            self.winning_user = user_1.username
        elif self.user_1_move == 'rock' and self.user_2_move == 'paper':
            self.winning_user = user_2.user_name
