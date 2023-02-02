from django import forms
from django.forms import ModelForm
from app.models import BlogUser, Comments, Subscribe
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'name', 'email', 'website']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment ...'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['website'].widget.attrs['placeholder'] = 'Website (optional)'
        self.fields['website'].required = False

class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

class SignInForm(ModelForm):
    class Meta:
        model = BlogUser
        fields = ['first_name', 'last_name','user_name', 'email', 'password', 'password_2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['last_name'].required = False
        self.fields['user_name'].widget.attrs['placeholder'] = 'User name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Create password'
        self.fields['password_2'].widget.attrs['placeholder'] = 'Confirm password'


class LogInForm(forms.Form):
    user_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)
    # class Meta:
    #     model = BlogUser
    #     fields = ['user_name', 'password']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['placeholder'] = 'User name'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
     
