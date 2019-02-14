from django import forms

from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta():
        model = User
        fields = ('username', 'password', 'email')



