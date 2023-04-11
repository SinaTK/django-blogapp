from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder':'First name (optional)', }))     #'class':"search-bar s-active input",
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder':'Last name (optional)'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter a valid email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
    password_2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder':'Repeat password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already used fr registration.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already choises. Please choose another one.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password =  cleaned_data.get('password')
        password_2 =  cleaned_data.get('password_2')

        if password != password_2:
            print("Passwords aren't match.")
            raise ValidationError("Passwords aren't match.")
        
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))