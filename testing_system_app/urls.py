from django.conf.urls import url

from . import views

app_name = 'testing_system_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('create_test', views.create_test, name='create_test'),
    url('test', views.test, name='test')
]