from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")   #기존 속성에 이메일 속성 추가함

    class Meta:
        model = User
        fields = ("username", "email")