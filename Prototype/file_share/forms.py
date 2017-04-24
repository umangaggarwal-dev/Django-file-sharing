from django import forms
from .models import *

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'id':'username'}))
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)


"""class UploadForm(forms.Form):
    file = forms.FileField()"""

class ShareForm(forms.Form):
    user = forms.CharField(max_length=100)
    file = forms.FileField()

class Friendship(forms.Form):
    user = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Search Users'}))