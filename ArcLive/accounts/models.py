from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        #Creates and saves a User with the given email, password
        """
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email,password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    username = None
    first_name =None
    last_name = None
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}|{self.email}|{self.last_login_at}"
    
    USERNAME_FIELD = "email"
    objects = UserManager()



class Preset_Image(models.Model):
    preset_image_url = models.TextField(verbose_name='アプリ内画像')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f"{self.preset_image_url}"
    


class User_Image(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE,verbose_name='ユーザーID')
    user_image_url = models.TextField(blank=True, null=True,verbose_name='ユーザーの本体の画像URL')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)