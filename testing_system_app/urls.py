from django.conf.urls import url

from . import views

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('create_test', views.create_test, name='create_test'),
    # url('test', views.test, name='test'),
    url('submit_disagreement/', views.send_student_answer, name="disagree"),
    url('submit_agreement/', views.submit_agreement, name="agree"),
    url('error/', views.handler404, name='error'),
]