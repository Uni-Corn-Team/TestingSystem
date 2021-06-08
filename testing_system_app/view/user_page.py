from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from testing_system_app.models import Student, UsersTests, Test, GeneralReport


def user_page(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            student = Student.objects.filter(user_id_id=request.user.id)[0]
            test_id = []
            for test in UsersTests.objects.filter():
                if test.user_id_id == student.id:
                    test_id.append(test.test_id_id)
            tests = []
            for test in Test.objects.filter():
                if test.id in test_id:
                    res = GeneralReport.objects.filter(student_id_id=student.id, test_id_id=test.id)
                    if len(res)==0:
                        res = '*'
                    else:
                        res = res[0].full_score
                    tests.append({"test":test, "result": res})
            return render(request, 'user_page.html', {"tests": tests, "student": student})
    else:
        return redirect('/sign_in/')


