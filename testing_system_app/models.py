import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    full_name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )


class Test(models.Model):
    name = models.CharField(max_length=255)
    admin_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )


class Attempt(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.datetime.now())
    current_number = models.IntegerField(default=0)
    general_id = models.IntegerField()


class Description(models.Model):
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )
    left_border = models.IntegerField()
    right_border = models.IntegerField()
    text = models.CharField(max_length=255)


class Answer(models.Model):
    score = models.IntegerField()
    text = models.CharField(max_length=255)


class Question(models.Model):
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)


class QuestionAnswer(models.Model):
    question_id = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer_id = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE
    )


class GeneralReport(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        default=0
    )
    full_score = models.IntegerField()
    date = models.DateTimeField(
        default=datetime.datetime.now()
    )


class FullReport(models.Model):
    question_id = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer_id = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        default=0
    )


class FullGeneralReport(models.Model):
    full_report_id = models.ForeignKey(
        FullReport,
        on_delete=models.CASCADE
    )
    general_report_id = models.ForeignKey(
        GeneralReport,
        on_delete=models.CASCADE
    )

