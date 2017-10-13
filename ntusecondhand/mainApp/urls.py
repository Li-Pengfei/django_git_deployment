from django.conf.urls import url
from mainApp import views

# Template URL
app_name = 'mainApp'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^user_login/$', views.UserLoginView.as_view(), name='user_login'),
]

