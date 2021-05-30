import json

from django.shortcuts import render
import datetime
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404


user_id = ""
test_id = ""


def index(request):
    return render(request, 'index.html')


def create_test(request):
    return render(request, 'create_test.html')


def test(request):
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    return render(request, 'test.html')


def receive_results(request):
    # print("send_answer")
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    results = json.loads(request.GET.get("results"))
    print("safafdgsdgsdgsgsd", user_id)
    student_id = Student.objects.filter(id=user_id)[0]
    # print(student_id)
    full_score = sum(results)
    general_report = GeneralReport.objects.create(student_id=student_id, full_score=full_score)
    for i in range(Question.objects.filter(test_id=test_id).count()):
        question = Question.objects.filter(test_id=test_id)[i]
        question_answers = QuestionAnswer.objects.filter(question_id=question.id)
        answer = Answer.objects.filter(id=question_answers[i].answer_id)
        full_report = FullReport.objects.create(question_id=question[i].id, answer_id=answer.id)
        full_report.save()
        full_general = FullGeneralReport.objects.create(full_report_id=full_report.id,
                                                        general_report_id=general_report.id)
        full_general.save()

    # проверить на существование уже этой записи



    return handler404(request)


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






def handler404(request ):
    template_name = '404.html'
    response = render(request, template_name)
    response.status_code = 404
    return response


def submit_agreement(request):
    user_id = request.GET.get('user_id')
    test_id = request.GET.get('test_id')
    if user_id == "null" or test_id == "null":
        return handler404(request)
    status = "Agree"
    date = datetime.datetime.now()
    if len(Attempt.objects.filter(student_id=user_id, test_id=test_id)) > 0:
        return handler404(request)
    student = Student.objects.get(id=user_id)
    # print(test_id)
    test = Test.objects.get(id=test_id)
    # print(test)
    attempt = Attempt.objects.create(student_id=student, test_id=test, status=status, date=date)
    # print(attempt)
    attempt.save()
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
            questions = Question.objects.create(test_id=Test.objects.all().last(), text=all_questions["questions"][i]["text"])
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

class Report:
    def __init__(self, fio, group, result, datetime_attempt, status):
        """Constructor"""
        self.fio = fio
        self.group = group
        self.result = result
        self.datetime_attempt = datetime_attempt
        self.status = status

def admin_results(request):
    reports = []
    attempts = Attempt.objects.all()
    for attempt in attempts:
        fio = Student.objects.get(id=attempt.student_id.id).full_name
        group = Student.objects.get(id=attempt.student_id.id).full_name
        print(attempt.test_id.id)
        print(Test.objects.get(id=attempt.test_id.id).id)
        test_id = Test.objects.get(id=attempt.test_id.id).id
        question_id = Question.objects.filter(test_id=attempt.test_id.id)[0].id
        print("fdsfds", question_id)
        #print(FullReport.objects.get(question_id=question_id))

        fullreport_id = FullReport.objects.get(question_id=question_id).id
        gfreport_id = FullGeneralReport.objects.get(full_report_id=fullreport_id)
        score = GeneralReport.objects.get(id=gfreport_id).fullscore
        status = attempt.status
        datetime_attempt = attempt.date
        reports.append(Report(fio, group, score,datetime_attempt, status ))
    print(reports)
    return render(request,"admin_results.html",reports)