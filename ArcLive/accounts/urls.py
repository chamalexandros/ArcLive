from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name= 'login'),
    path('logout/', LogoutView.as_view(), name= 'logout'),
    path('mypage/', views.mypage, name="mypage"),
    path('change_email/', views.change_email, name="change_email"),
    path('change_password/', views.change_password, name="change_password"),
    path('signup/', views.signup, name="signup"),
    # パスワード再発行フォーム
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), 
    # パスワード再発行メール送信完了
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # パスワード再設定
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # パスワード再設定完了
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]