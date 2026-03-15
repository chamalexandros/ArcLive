from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomPasswordResetForm
from django.views import generic
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView




class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name ='accounts/signup.html'
    success_url = reverse_lazy('login')


class MypageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/mypage.html')
    
    
class ChangeEmailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/change_email.html', {"user": request.user})
    
    def post(self,request):
        new_email = request.POST.get('email')
        request.user.email = new_email
        request.user.save()
        
        #メールアドレス変更後にメッセージを表示
        messages.success(request, 'メールアドレスを変更しました')
        return redirect ('accounts:mypage')
    

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:mypage")
    
    #パスワード変更後にメッセージを表示
    def form_valid(self, form):
        messages.success(self.request, 'パスワードを変更しました')
        return super().form_valid(form)

        

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    form_class = CustomPasswordResetForm
    subject_template_name = 'registration/mail_subject.txt'
    email_template_name = 'registration/mail_message.txt'
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'
   
    

mypage = MypageView.as_view()
change_email = ChangeEmailView.as_view()
change_password = PasswordChangeView.as_view()
signup = SignupView.as_view()
password_reset = PasswordReset.as_view()
password_reset_done = PasswordResetDone.as_view()
password_reset_confirm = PasswordResetConfirm.as_view()
password_reset_complete = PasswordResetComplete.as_view()