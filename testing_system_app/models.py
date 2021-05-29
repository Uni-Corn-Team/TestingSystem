from django.db import models


# Create your models here.
class Student(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)


class Test(models.Model):
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)


class Attempt(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    test_id = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=255)


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
    ans_id = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE
    )


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
    full_score = models.IntegerField()


class FullReport(models.Model):
    question_id = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    score = models.IntegerField()


class FullGeneralReport(models.Model):
    full_report_id = models.ForeignKey(
        FullReport,
        on_delete=models.CASCADE
    )
    general_report_id = models.ForeignKey(
        GeneralReport,
        on_delete=models.CASCADE
    )









