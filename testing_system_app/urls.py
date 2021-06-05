from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('usr/<str:username>/test/<str:test>', views.index, name='index'),
    url('send_mail', views.send_mail, name='fdsfd'),
    url('mail_test', views.mail_test, name='dsgf'),
    url('select_test', views.select_test, name='fdsf'),
    url('create_test', views.create_test, name='create_test'),
    url('add_test', views.add_test, name='add_test'),
    url('test', views.test, name='test'),
    url('submit_disagreement', views.submit_agreement, name="disagree"),
    path('submit_agreement/<str:user>/<str:_test>', views.submit_agreement, name="agree"),
    url('error', views.handler404, name='error'),
    url("receive_results", views.receive_results, name='receive_results'),
    url("get_first_question", views.get_first_question, name='get_first_question'),
    url("get_next_question", views.get_next_question, name='get_next_question'),
    url("get_json_question", views.get_json_question, name='get_json_question'),
    url("finish", views.finish),
    url('sign_in_user', views.sign_in_user, name='sign_in_user'),
    url('sign_in', views.sign_in, name='sign_in'),
    url('admin_page', views.admin_page, name='admin_page'),
    url('admin_result_values', views.admin_result_values, name='admin_result_values'),
    url('admin_results', views.admin_results, name='admin_results'),
    url('log_out_user', views.log_out_user, name='logout'),
]
