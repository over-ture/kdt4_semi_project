from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CodeReview
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError

class CodeReviewForm(forms.ModelForm):
    code = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 10, 'cols': 60}))
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

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # 비밀번호 길이가 8자 이상인지 확인
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 8자 이상이어야 합니다.")

        common_password_validator = CommonPasswordValidator()

        # 너무 흔한 비밀번호인지 검사하고 오류 메시지 리스트에 추가
        password_validation_errors = []
        try:
            common_password_validator.validate(password1)
        except ValidationError as error:
            password_validation_errors.extend(error.messages)

        if password_validation_errors:
            raise forms.ValidationError("이 비밀번호는 너무 흔한 비밀번호입니다. 다른 비밀번호를 선택하세요.")

        return password1