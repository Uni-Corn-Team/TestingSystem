from django.shortcuts import render, redirect
from ..models import *
from django.http import HttpResponse, HttpResponseRedirect


class Report(object):
    def __init__(self, test, fio, group, result, time):
        self.test = test
        self.fio = fio
        self.group = group
        self.result = result
        self.time = time


def admin_results(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'admin_results.html')
    else:
        return redirect('/sign_in/')


def admin_result_values(request):
    general_reports = GeneralReport.objects.filter()
    reports = []
    response = ""
    user_id = 1
    for _user in User.objects.filter():
        if str(_user.username) == str(request.user):
            user_id = _user.id
            break
    tests = []
    for test in Test.objects.filter():
        if test.admin_id_id == user_id:
            tests.append(test.id)

    for i in range(len(general_reports)):
        if general_reports[i].test_id_id in tests:
            student = Student.objects.filter(id=general_reports[i].student_id.id)[0]
            reports.append(Report(general_reports[i].test_id.id, student.full_name, student.group,
                                  general_reports[i].full_score, datetime.datetime.now().date()))
            response += "<tr>"
            response += "<th scope = \"row\">" + str(len(reports)-1  + 1) + "</th>"
            response += "<td>" + str(reports[len(reports)-1 ].test) + "</td>"
            response += "<td>" + str(reports[len(reports)-1  ].fio) + "</td>"
            response += "<td>" + str(reports[len(reports)-1  ].group) + "</td>"
            response += "<td>" + str(reports[len(reports)-1  ].result) + "</td>"
            response += "<td>" + str(reports[len(reports)-1  ].time) + "</td>"
            response += "</tr>"
    return HttpResponse(response)
