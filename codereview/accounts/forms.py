from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CodeReview

class CodeReviewForm(forms.ModelForm):
    class Meta:
        model = CodeReview
        fields = ['code', 'uploaded_file']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}))