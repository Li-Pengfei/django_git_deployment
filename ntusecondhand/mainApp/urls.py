from django.conf.urls import url
from mainApp import views

# Template URL
app_name = 'mainApp'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]

