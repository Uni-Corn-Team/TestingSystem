from django.conf.urls import url
from django.urls import path

from . import views
from .view import admin_result, admin_page, authorization, user_test, index, create_test, test_refs, user_page

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', index.index, name='index'),
    path('usr/<str:username>/test/<str:test>', index.index, name='index'),
    url('mail_test', test_refs.mail_test, name='dsgf'),
    url('select_test', test_refs.select_test, name='fdsf'),
    url('create_test', create_test.create_test, name='create_test'),
    url('add_test', create_test.add_test, name='add_test'),
    url('test', user_test.test, name='test'),
    path('submit_agreement/<str:user>/<str:_test>', index.submit_agreement, name="agree"),
    url('error', views.handler404, name='error'),
    url("receive_results", user_test.receive_results, name='receive_results'),
    url("get_first_question", user_test.get_first_question, name='get_first_question'),
    url("get_next_question", user_test.get_next_question, name='get_next_question'),
    url("get_json_question", user_test.get_json_question, name='get_json_question'),
    url("finish", user_test.finish),
    url('sign_in_user', authorization.sign_in_user, name='sign_in_user'),
    url('sign_in', authorization.sign_in, name='sign_in'),
    url('admin_page', admin_page.admin_page, name='admin_page'),
    url('user_page', user_page.user_page, name='user_page'),
    url('admin_result_values', admin_result.admin_result_values, name='admin_result_values'),
    url('admin_results', admin_result.admin_results, name='admin_results'),
    url('log_out_user', authorization.log_out_user, name='logout'),
]
