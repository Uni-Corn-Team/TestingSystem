import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from testing_system_app.models import Question, Answer, Test, QuestionAnswer


def create_test(request):
    if request.user.is_superuser:
        return render(request, 'create_test.html')


def add_test(request):
    if request.method == "GET":
        all_questions = json.loads(request.GET.get("test"))

        user_id = 1
        for _user in User.objects.filter():
            if str(_user.username) == str(request.user):
                user_id = _user.id
                break

        test = Test.objects.create(name=all_questions["name"], admin_id_id=user_id)
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
