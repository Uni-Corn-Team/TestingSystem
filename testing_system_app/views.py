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
    current_number = Attempt.objects.filter(
        test_id=test_id, student_id=user_id)[0].current_number + 1
    total_number = Question.objects.filter(
        test_id=test_id).count()
    question_text = Question.objects.filter(test_id=test_id)[current_number - 1].text

    return render(request, 'test.html', {"current_number": current_number, "total_number": total_number,
                                         "question_text": question_text})


def receive_results(request):
    print("send_answer")
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    results = json.loads(request.GET.get("results"))
    print(user_id)
    student_id = Student.objects.filter(id=user_id)[0]
    print(student_id)
    full_score = sum(results)
    general_report = GeneralReport.objects.create(student_id=student_id, full_score=full_score)
    for i in range(Question.objects.filter(test_id=test_id).count()):
        question = Question.objects.filter(test_id=test_id)[i]
        full_report = FullReport.objects.create(question_id=question[i].id, score=results[i])
        full_report.save()
        full_general = FullGeneralReport.objects.create(full_report_id=full_report.id,
                                                        general_report_id=general_report.id)
        full_general.save()

    # проверить на существование уже этой записи



    return handler404(request)


def get_first_question(request):
    test_id = request.GET.get('test_id')
    return Question.objects.filter(test_id=test_id)[0]


def get_next_question(request):
    test_id = request.GET.get('test_id')
    question_id = request.GET.get('question_id')
    questions = Question.objects.filter(test_id=test_id)
    if len(questions) == 0:
        raise IndexError
    prev = questions[0]
    for question in questions:
        if prev.id == question_id:
            return question.id
        prev = question

    return "Finish"


def get_json_question(request):
    test_id = request.GET.get('test_id')
    data = dict()
    current_question = request.GET.get('current_question')
    question_text = Question.objects.filter(test_id=test_id, id=current_question)[0]
    question_answers = QuestionAnswer.objects.filter(question_id=current_question)
    data["text"] = question_text
    data["answers"] = []
    for i in range(len(question_answers)):
        answer = Answer.objects.filter(id=question_answers[i].answer_id)[0]
        data["answers"][i]["text"] = answer.text
        data["answers"][i]["points"] = answer.score

    return json.dumps(data)






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
    print(test_id)
    test = Test.objects.get(id=test_id)
    print(test)
    attempt = Attempt.objects.create(student_id=student, test_id=test, status=status, date=date)
    print(attempt)
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


