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


def send_student_answer(request):
    print("send_answer")
    user_id = 1 #request.GET.get("user_id")
    test_id = 3 #request.GET.get('test_id')
    current_number = 1 # request.GET.get("current_number")
    question = Question.objects.filter(test_id=Test.objects.filter(id=test_id)[0])[current_number - 1]
    print(user_id)
    student_id = Student.objects.filter(id=user_id)[0]
    print(student_id)
    general_report = GeneralReport.objects.create(student_id=student_id, full_score=0)
    student_answer = 0 # request.GET.get("student_answer")
    possible_answers = QuestionAnswer.objects.filter(question_id=question)
    question_answer = QuestionAnswer.objects.filter(question_id=question,
                                                    answer_id=possible_answers[student_answer].answer_id)[0].answer_id
    print(question_answer)
    score = Answer.objects.filter(id=question_answer.id)[0].score
    print(score)
    full_report = FullReport.objects.create(question_id=question, score=score)
    return handler404(request)


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
    print("add_test")
    if request.method == "GET":
        print("post")
        # all_questions = request.POST["questions"]
        all_questions = {
            "name": "Название психологического теста",
            "questions":
                [
                    {
                        "text": "Как часто вы думаете о смерти?",
                        "answers_count": 2,
                        "answers":
                            [
                                {"text": "Часто", "points": 10},
                                {"text": "Редко", "points": 0}
                            ]
                    },
                    {
                        "text": "Как часто вы какаете?",
                        "answers_count": 3,
                        "answers":
                            [
                                {"text": "Очень часто", "points": 10},
                                {"text": "Иногда", "points": 5},
                                {"text": "Очень редко", "points": 0}
                            ]
                    }

                ]
        }
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


