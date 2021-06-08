import json
from django.shortcuts import render
from django.http import HttpResponse
from testing_system_app.models import Student, GeneralReport, Test, Question, QuestionAnswer, Answer


user_id = ""
test_id = ""


def test(request):
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    return render(request, 'test.html')


def get_first_question(request):
    test_id = request.GET.get('test_id')
    _test = Test.objects.get(id=test_id)
    id = Question.objects.filter(test_id=_test)[0].id
    return HttpResponse(str(id))


def get_next_question(request):
    test_id = request.GET.get('test_id')
    question_id = request.GET.get('question_id')
    questions = Question.objects.filter(test_id=test_id)
    if len(questions) == 0:
        raise IndexError
    prev = questions[0]
    for i in range(1, len(questions)):
        question = questions[i]
        if str(prev.id) == str(question_id):
            return HttpResponse(str(question.id))
        prev = question
    return HttpResponse("Finish")


def get_json_question(request):
    test_id = request.GET.get('test_id')
    data = dict()
    current_question = request.GET.get('current_question')
    test_obj = Test.objects.get(id=test_id)
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
    return HttpResponse(json.dumps(data))


def receive_results(request):
    user_id = request.GET.get("user_id")
    test_id = request.GET.get('test_id')
    results = json.loads(request.GET.get("results"))
    student_id = Student.objects.filter(id=user_id)[0]
    full_score = sum(results)
    test_object = Test.objects.filter(id=test_id)[0]

    general_reports = GeneralReport.objects.filter()
    isnot_exist = True
    for report in general_reports:
        if int(report.student_id_id) == int(user_id) and int(report.test_id_id) == int(test_id):
            isnot_exist = False
            break
    if isnot_exist:
        general_report = GeneralReport.objects.create(student_id=student_id, test_id=test_object, full_score=full_score)
        general_report.save()
    return HttpResponse("Received")


def finish(request):
    return render(request, "finish.html")
