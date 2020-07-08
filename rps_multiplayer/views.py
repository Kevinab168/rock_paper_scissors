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
