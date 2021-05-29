from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, World!")


def hello(request):
    return render(request, 'hello.html')
# Create your views here.
