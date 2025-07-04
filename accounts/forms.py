# accounts/forms.py
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput({
            'class':        'form-control',
            'placeholder':  'Choose a username (4–30 chars)',
            'required':     'required',
            'minlength':    '4',
            'maxlength':    '30',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput({
            'class':        'form-control',
            'placeholder':  'you@example.com',
            'required':     'required',
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput({
            'class':        'form-control',
            'placeholder':  '10-digit phone number',
            'required':     'required',
            'pattern':      r'\d{10}',
            'title':        'Enter exactly 10 digits.',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput({
            'class':        'form-control',
            'placeholder':  'At least 8 chars, incl. uppercase, number & symbol',
            'required':     'required',
            'minlength':    '8',
            # this regex requires at least one uppercase, one digit, one non-word (symbol)
            'pattern':      r'(?=.*[A-Z])(?=.*\d)(?=.*\W).+',
            'title':        'Must include at least one uppercase letter, one number, and one symbol.',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput({
            'class':        'form-control',
            'placeholder':  'Repeat your password',
            'required':     'required',
            'minlength':    '8',
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'\d{10}', phone):
            raise forms.ValidationError("Phone must be exactly 10 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput({
        'class':       'form-control',
        'id':          'id_username',
        'placeholder': 'Username',
        'required':    'required'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class':       'form-control',
        'id':          'id_password',
        'placeholder': 'Password',
        'required':    'required'
    }))