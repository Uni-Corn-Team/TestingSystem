from django.conf.urls import url

from . import views

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('create_test', views.create_test, name='create_test'),
    url('add_test/', views.add_test, name='add_test'),
    url('test', views.test, name='test'),
    url('submit_disagreement/', views.submit_agreement, name="disagree"),
    url('submit_agreement/', views.submit_agreement, name="agree"),
    url('error/', views.handler404, name='error'),
    url("receive_results/", views.receive_results, name='receive_results')

]