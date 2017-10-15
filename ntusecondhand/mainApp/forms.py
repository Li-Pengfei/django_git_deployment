from django import forms
from django.contrib.auth.models import User
from mainApp.models import UserProfileInfo, ItemModel


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfileInfo
        fields = ('wechat', 'postal_code', 'profile_pic')


class AddItemModelForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['category', 'title', 'description', 'condition','estimate_price', 'exchange_address', 'item_pic']

