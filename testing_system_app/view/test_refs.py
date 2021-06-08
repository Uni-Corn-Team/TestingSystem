from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from testing_system_app.models import Student, Test, UsersTests


def select_test(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_id = 1
            for _user in User.objects.filter():
                if str(_user.username) == str(request.user):
                    user_id = _user.id
                    break
            tests = []
            for test in Test.objects.filter():
                if test.admin_id_id == user_id:
                    tests.append(test)
            return render(request, "tests_to_send.html", {"tests": tests})
    else:
        return redirect('/sign_in/')


def mail_test(request):
    students = Student.objects.filter()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            studs = []
            for stud in students:
                if len(UsersTests.objects.filter(user_id_id=stud.id, test_id_id=request.GET.get('test_id')))==0:
                    studs.append({"student": stud, "checked": False})
                else:
                    studs.append({"student": stud, "checked": True})
            return render(request, "send_test.html",
                  {"students": studs, "test": request.GET.get('test_id'), "test_name": request.GET.get('test_name')})