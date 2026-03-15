from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)
        


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['email'].widget.attrs.update({
        'class': 'form-control',
        })

    #def send_email(self, username, email):
    #    subject = "【ArcLiveパスワード再設定のご案内" + self.cleaned_data["subject"]
    #    message = self.cleaned_data["message"] + f"\n\nBy {username}."
    #   recipient_list = ["onishi.ry3s3k4@gmail.com"]   ### 送信先
    #    try:
    #       send_mail(subject, message, email, recipient_list)
    #        except BadHeaderError:
    #        return HttpResponse("無効なヘッダが検出されました。")
