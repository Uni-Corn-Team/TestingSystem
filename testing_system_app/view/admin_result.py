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
        return render(request, 'admin_results.html')
    else:
        return redirect('/sign_in/')


def admin_result_values(request):
    general_reports = GeneralReport.objects.filter()
    reports = []
    response = ""
    for i in range(len(general_reports)):
        student = Student.objects.filter(id=general_reports[i].student_id.id)[0]
        reports.append(Report(general_reports[i].test_id.id, student.full_name, student.group,
                              general_reports[i].full_score, datetime.datetime.now().date()))
        response += "<tr>"
        response += "<th scope = \"row\">"+str(i+1)+"</th>"
        response += "<td>" + str(reports[i].test) + "</td>"
        response += "<td>" + str(reports[i].fio) + "</td>"
        response += "<td>" + str(reports[i].group) + "</td>"
        response += "<td>" + str(reports[i].result) + "</td>"
        response += "<td>" + str(reports[i].time) + "</td>"
        response += "</tr>"
    return HttpResponse(response)