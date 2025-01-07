from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Workday
from django import forms
from django.forms.widgets import PasswordInput, TextInput

# register / create user form

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
# login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))    
    

# - Create a record

class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = Workday
        fields = ['firstname', 'lastname', 'date', 'month', 'workday_type', 'time_in', 'time_out']


# - Update a record

class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = Workday
        fields = ['firstname', 'lastname', 'date', 'month', 'workday_type', 'time_in', 'time_out']