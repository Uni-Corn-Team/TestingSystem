
from django.shortcuts import render, redirect
from .models import *


def handler404(request):
    template_name = '404.html'
    response = render(request, template_name)
    response.status_code = 404
    return response


def select_test(request):
    if request.user.is_authenticated:
        tests = Test.objects.filter()
        return render(request, "tests_to_send.html", {"tests": tests})
    else:
        return redirect('/sign_in/')


def mail_test(request):
    students = Student.objects.filter()
    return render(request, "send_test.html", {"students": students})


import smtplib


def send_email(recipient, student_name, user_id, test_id):
    user = "miet.xakaton.2021@gmail.com"
    FROM = "miet.xakaton.2021@gmail.com"
    pwd = "morgenshtern"
    TO = recipient if isinstance(recipient, list) else [recipient]

    SUBJECT = "gfds"
    TEXT = "localhost:8000/?user_id=%s&test_id=%s" % (user_id, test_id)

    # Prepare actual message
    print(FROM)
    print(TO)
    print(SUBJECT)
    print(TEXT)
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print("failed to send mail" + str(e))


def send_mail(request):
    email = request.GET.get('email')
    name = request.GET.get('name')
    user_id = request.GET.get('user_id')
    test_id = request.GET.get('test_id')
    send_email(email, name, user_id, test_id)
