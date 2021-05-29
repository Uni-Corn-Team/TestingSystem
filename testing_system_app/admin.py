from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(Answer)
admin.site.register(Attempt)
admin.site.register(Test)
admin.site.register(Description)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(FullReport)
admin.site.register(FullGeneralReport)
admin.site.register(GeneralReport)
# Register your models here.
