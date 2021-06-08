from django.conf.urls import handler404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def sign_in(request):
    if not request.user.is_authenticated:
        return render(request, 'sign_in.html')
    else:
        if request.user.is_superuser:
            return redirect('/admin_page/')
        else:
            return redirect('/user_page')


def sign_in_user(request):
    username = request.GET.get('login', '')
    password = request.GET.get('password', '')
    if username == '' or password == '':
        return handler404(request)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print(user.is_superuser)
            if user.is_superuser:
                return HttpResponseRedirect('/admin_page/')
            else:
                return HttpResponseRedirect('/user_page')
        else:
            return handler404(request)
    else:
        return handler404(request)


def log_out_user(request):
    logout(request)
    return HttpResponseRedirect('/sign_in/')
