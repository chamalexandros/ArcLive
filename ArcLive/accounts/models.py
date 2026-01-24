from django.db import models

class Preset_Image(models.Model):
    preset_image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class User_Image(models.Model):
    user_id = 
    user_image_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    last_login_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
