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
    path('password_reset_form/', views.password_reset, name='password_reset_form'), 
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'), 
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'), 
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'), 
]