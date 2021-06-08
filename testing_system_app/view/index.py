import datetime

from django.conf.urls import handler404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from testing_system_app.models import GeneralReport, Student


def index(request, username="", test=""):
    if username == "" or test == "":
        return redirect('/sign_in/')
    general_reports = GeneralReport.objects.filter()
    for report in general_reports:
        if int(report.student_id_id) == int(username) and int(report.test_id_id) == int(test):
            return render(request, 'already_done.html')
    return render(request, 'index.html')


def submit_agreement(request, user="", _test=""):
    user_id = user
    test_id = _test
    if user_id == "null" or test_id == "null":
        return handler404(request)
    return HttpResponseRedirect("/test.html?user_id=" + user_id + "&test_id=" + test_id)
