from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.accounts_home, name='accounts_home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # login은 이미 django에서 사용 중이므로 login_view로 명명
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_code, name='upload_code'),
    path('review/<int:code_review_id>/', views.review_result, name='review_result'),
    path('delete/', views.delete_account, name='delete_account'),
    path('delete_review/<int:code_review_id>/', views.delete_review, name='delete_review'),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('find_username/', views.find_username, name='find_username'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

