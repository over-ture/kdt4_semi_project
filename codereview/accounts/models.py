from django.db import models
from django.contrib.auth.models import User

class CodeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.TextField()
    review = models.TextField()
    review_result = models.TextField(blank=True, null=True)
    uploaded_file = models.FileField(upload_to='code_uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s code at {self.timestamp}"