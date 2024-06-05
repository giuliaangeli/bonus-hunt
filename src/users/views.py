from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def user_signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user:
            return HttpResponse('Ja existe um usuario com esse mesmo nome')
        else:
            User.objects.create(username=username, email=email, password=password)
            return redirect('/preferences')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/preferences')
    if request.method=="GET":
        return render(request, 'login.html')
    else:
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/preferences')
        else:
            return HttpResponse('Email ou senha errados')

def user_logout(request):
    logout(request)
    return redirect('/auth/login')