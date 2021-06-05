from django.shortcuts import render, redirect

from testing_system_app.models import Student, Test


def select_test(request):
    if request.user.is_authenticated:
        tests = Test.objects.filter()
        return render(request, "tests_to_send.html", {"tests": tests})
    else:
        return redirect('/sign_in/')


def mail_test(request):
    students = Student.objects.filter()
    return render(request, "send_test.html",
                  {"students": students, "test": request.GET.get('test_id'), "test_name": request.GET.get('test_name')})