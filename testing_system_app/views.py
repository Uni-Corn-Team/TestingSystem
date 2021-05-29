from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def create_test(request):
    return render(request, 'create_test.html')


def test(request):
    return render(request, 'test.html')

