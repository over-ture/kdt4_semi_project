from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # login은 이미 django에서 사용 중이므로 login_view로 명명
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_code, name='upload_code'),
    path('review/<int:code_review_id>/', views.review_result, name='review_result'),
]
