from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

app_name='register'

urlpatterns=[
    path('register/',views.register,name='registration'),
    path('login/',views.login_user,name='login_user'),
    path('password_reset/',PasswordResetView,name='forgot_pass'),
    path('password_reset_done/',PasswordResetDoneView,name='password_reset_done'),
    path('password_reset_confirm/',PasswordResetConfirmView,name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView,name='password_reset_complete')
]