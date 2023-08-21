from django import forms
from .models import CodeReview

class CodeReviewForm(forms.ModelForm):
    class Meta:
        model = CodeReview
        fields = ['code', 'uploaded_file']