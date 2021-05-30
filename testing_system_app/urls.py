from django.conf.urls import url

from . import views

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('create_test', views.create_test, name='create_test'),
    url('add_test', views.add_test, name='add_test'),
    url('test', views.test, name='test'),
    url('submit_disagreement', views.submit_agreement, name="disagree"),
    url('submit_agreement', views.submit_agreement, name="agree"),
    url('error', views.handler404, name='error'),
    url("receive_results", views.receive_results, name='receive_results'),
    url("get_first_question", views.get_first_question, name='get_first_question'),
    url("get_next_question", views.get_next_question, name='get_next_question'),
    url("get_json_question", views.get_json_question, name='get_json_question'),
    url("admin_results", views.admin_results, name='admin_results'),
    url("finish", views.finish)
]