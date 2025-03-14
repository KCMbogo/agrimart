from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userauths.models import User
from django import forms


class UserCreationForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email  = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        
        
class UserAuthenticationForm(AuthenticationForm):
    
    email  = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ['email', 'password']