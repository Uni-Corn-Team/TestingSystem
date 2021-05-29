from django.shortcuts import render
import datetime
from .models import *
from django.http import HttpResponse, HttpResponseRedirect


user_id = ""
test_id = ""


def index(request):
    global user_id
    global test_id
    try:
        user_id = Student.objects.filter(id=request.GET.get("user_id", ""))[0]
        test_id = Test.objects.filter(id=request.GET.get("test_id", ""))[0]
    except Exception as e:
        print(e)

    return render(request, 'index.html')


def create_test(request):
    return render(request, 'create_test.html')


def test(request):
    return render(request, 'test.html')


def agree(request):
    global user_id
    global test_id
    print("agree")
    if user_id == "" or test_id == "":  # заменить на адекватную обработку, в теории такой ситуации не должно быть
        return HttpResponseRedirect("/index.html")
    status = "Agree"
    date = datetime.datetime.now()
    if request.method == "POST":
        attempt = Attempt.objects.create(student_id=user_id, test_id=test_id, status=status, date=date)
        attempt.save()
    return HttpResponseRedirect("/test.html")


def disagree(request):
    global user_id
    global test_id
    if user_id == "" or test_id == "":  # заменить на адекватную обработку, в теории такой ситуации не должно быть
        return HttpResponseRedirect("/index.html")
    print("disagree")
    status = "Disagree"
    date = datetime.datetime.now()
    if request.method == "POST":
        attempt = Attempt.objects.create(student_id=user_id, test_id=test_id, status=status, date=date)
        attempt.save()
    return HttpResponseRedirect("/test.html")
