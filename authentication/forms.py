from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(UserCreationForm):
    nama = forms.CharField(
        label='nama',
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={'id': 'login-nama', 'placeholder': 'Nama'})
    )
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'id': 'login-pass1', 'placeholder': 'Email'}))
