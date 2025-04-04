from django import forms
from .models import MenuItem  # Ensure you import your model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class MenuItemForm(forms.ModelForm):  # Use forms.ModelForm
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'image']  

# accounts/forms.py




class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username'}),
        help_text=''  # Removes the default help text
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}),
        help_text='',  # Removes the default password help text
        error_messages={'required': 'Password is required'}
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        help_text='',  # Removes the default password confirmation help text
        error_messages={'required': 'Please confirm your password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
