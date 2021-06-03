import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import datetime
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

user_id = ""
test_id = ""


class Report(object):
    def __init__(self, test, fio, group, result, time):
        self.test = test
        self.fio = fio
        self.group = group
        self.result = result
        self.time = time


def index(request, username="", test=""):
    if username == "" or test == "":
        return redirect('/sign_in/')
    return render(request, 'index.html')


def create_test(request):
    return render(request, 'create_test.html')


def test(request):
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    return render(request, 'test.html')


def receive_results(request):

    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    results = json.loads(request.GET.get("results"))

    # print(user_id)
    student_id = Student.objects.filter(id=user_id)[0]
    # print(student_id)
    full_score = sum(results)
    test_object = Test.objects.filter(id=test_id)[0]
    print(test_object.id)
    general_report = GeneralReport.objects.create(student_id=student_id, test_id=test_object, full_score=full_score)

    general_report.save()

    # Attempt.objects.create(student_id=student_id, test_id=Test.objects.get(test_id), status="Done",
                           # general_id=general_report.id)

    return HttpResponse("Received")


def get_first_question(request):
    test_id = request.GET.get('test_id')
    # print(1000000000002)
    # print(test_id)
    test = Test.objects.get(id=test_id)
    # print(1000000000002)
    id = Question.objects.filter(test_id=test)[0].id
    return HttpResponse(str(id))


def get_next_question(request):
    test_id = request.GET.get('test_id')
    question_id = request.GET.get('question_id')
    questions = Question.objects.filter(test_id=test_id)
    if len(questions) == 0:
        raise IndexError
    prev = questions[0]
    # print("To compare", str(question_id))
    for i in range(1, len(questions)):
        question = questions[i]
        if str(prev.id) == str(question_id):
            return HttpResponse(str(question.id))
        prev = question

    return HttpResponse("Finish")


def get_json_question(request):
    test_id = request.GET.get('test_id')
    # print(test_id)
    data = dict()
    current_question = request.GET.get('current_question')
    test_obj = Test.objects.get(id=test_id)
    # print(test_obj)
    if current_question != "Finish":
        question_text = Question.objects.filter(test_id=test_obj, id=current_question)[0]
        question_answers = QuestionAnswer.objects.filter(question_id=current_question)
        data["text"] = question_text.text
        data["answers"] = []
        for i in range(len(question_answers)):
            answer = Answer.objects.filter(id=question_answers[i].answer_id.id)[0]
            data["answers"].append({
                "text": answer.text,
                "points": answer.score
            })

    # print(data)

    return HttpResponse(json.dumps(data))


def handler404(request):
    template_name = '404.html'
    response = render(request, template_name)
    response.status_code = 404
    return response


def submit_agreement(request, user="", _test=""):
    #user_id = request.GET.get('user_id')
    #test_id = request.GET.get('test_id')
    user_id = user
    test_id = _test
    print(user_id)
    print(test_id)
    if user_id == "null" or test_id == "null":
        return handler404(request)
    status = "Agree"
    date = datetime.datetime.now()
    # if len(Attempt.objects.filter(student_id=user_id, test_id=test_id)) > 0:
    #    return handler404(request)
    # student = Student.objects.get(id=user_id)
    # print(test_id)
    # test = Test.objects.get(id=test_id)
    # print(test)
    # attempt = Attempt.objects.create(student_id=student, test_id=test, status=status, date=date)
    # print(attempt)
    # attempt.save()
    return HttpResponseRedirect("/test.html?user_id=" + user_id + "&test_id=" + test_id)


def submit_disagreement(request):
    user_id = request.GET.get('user_id')
    test_id = request.GET.get('test_id')
    if user_id == "null" or test_id == "null":
        return handler404(request)
    status = "Disagree"
    date = datetime.datetime.now()
    if len(Attempt.objects.filter(student_id=user_id, test_id=test_id)) > 0:
        return handler404(request)
    try:
        student = Student.objects.get(id=user_id)
        test = Test.objects.get(id=test_id)
    except Exception as e:
        print(e)
        return handler404(request)
    attempt = Attempt.objects.create(student_id=student, test_id=test, status=status, date=date)
    attempt.save()
    return render(request, "disagreed.html")


def add_test(request):
    if request.method == "GET":
        all_questions = json.loads(request.GET.get("test"))
        print(all_questions)
        test = Test.objects.create(name=all_questions["name"])
        test.save()
        for i in range(len(all_questions["questions"])):
            questions = Question.objects.create(test_id=Test.objects.all().last(),
                                                text=all_questions["questions"][i]["text"])
            questions.save()
            for j in range(len(all_questions["questions"][i]["answers"])):
                answers = Answer.objects.create(score=all_questions["questions"][i]["answers"][j]["points"],
                                                text=all_questions["questions"][i]["answers"][j]["text"])
                answers.save()
                questions_answers = QuestionAnswer.objects.create(question_id=Question.objects.all().last(),

                                                                  answer_id=Answer.objects.all().last())
                questions_answers.save()

    return HttpResponseRedirect("/create_test.html")


def finish(request):
    return render(request, "finish.html")


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
import ssl


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


def sign_in(request):
    if not request.user.is_authenticated:
        return render(request, 'sign_in.html')
    else:
        return redirect('/admin_page/')


def sign_in_user(request):
    username = request.GET.get('login', '')
    password = request.GET.get('password', '')
    print(username)
    print(password)
    if username == '' or password == '':
        return handler404(request)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/admin_page/')
        else:
            pass
            # Return a 'disabled account' error message
    else:
        pass
        # Return an 'invalid login' error message


def log_out_user(request):
    logout(request)
    return HttpResponseRedirect('/sign_in/')


def admin_page(request):
    if request.user.is_authenticated:
        return render(request, 'admin_page.html')
    else:
        return redirect('/sign_in/')


def admin_results(request):

    if request.user.is_authenticated:
        general_reports = GeneralReport.objects.filter()
        reports = [len(general_reports)]
        for i in range (len(general_reports)):
            student = Student.objects.filter(id=general_reports[i].student_id.id)[0]
            reports[i] = Report(general_reports[i].test_id.id, student.full_name, student.group,
                                general_reports[i].full_score, datetime.datetime.now())

        return render(request, 'admin_results.html', {"reports": reports})
    else:
        return redirect('/sign_in/')

