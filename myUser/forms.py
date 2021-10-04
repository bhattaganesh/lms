from django import forms
from django.forms.widgets import EmailInput, PasswordInput, TextInput
from .models import User
from django.utils import timezone

class LoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. user@gmail.com'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control',}))


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. user@gmail.com'}))
    fullName = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Akon duke'}), label='Full Name')
    contactNo = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': '98xxxxxxxx', 'max': 10, 'min': 10}),label="Contact No.")
    address = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Attariya, kailali',}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control',}))
    cpassword = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control',}), label='Password Confirmation')
    class Meta:
        model = User
        fields = ['email', 'fullName', 'contactNo', 'address','password']

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        cpassword = cleaned_data.get('cpassword')
        password = cleaned_data.get('password')
        if password != cpassword:
            self.add_error('cpassword', 'Confirmation password does not match')

    def save(self, commit=False):
        user = super(UserRegistrationForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
