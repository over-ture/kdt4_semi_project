from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CodeReview

class CodeReviewForm(forms.ModelForm):
    code = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
    class Meta:
        model = CodeReview
        fields = ['code', 'uploaded_file']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        uploaded_file = cleaned_data.get('uploaded_file')
        if not code and not uploaded_file:
            raise forms.ValidationError('코드나 파일 중 하나는 반드시 입력해야 합니다.')
        return cleaned_data

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='아이디', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}))