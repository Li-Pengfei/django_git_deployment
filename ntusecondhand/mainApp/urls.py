from django.conf.urls import url
from mainApp import views

# Template URL
app_name = 'mainApp'

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^user_login/$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^manage_my_items/$', views.ManageMyItemView.as_view(), name='manage_my_items'),
    url(r'^addItem/$', views.AddItemView.as_view(), name='addItem'),
    url(r'^(?P<item_id>[0-9]+)/', views.ItemDetailView, name='item_detail'),
]
