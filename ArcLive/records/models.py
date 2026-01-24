from django.db import models

class Record(models.Model):
    user_id =
    venue_id =
    event_name = models.CharField(max_length=100, blank=True, null=True)
    live_date = models.DateField() #公演日(必須)
    live_image = models.TextField(blank=True, null=True) #参戦記録一覧画面に表示する画像
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Artist_Record(models.Model):
    record_id =
    artist_id =
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Artist(models.Model):
    name = models.CharField(max_length=100) #アーティスト名
    reading_name = models.CharField(max_length=100) #よみがな
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Venue(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) #会場名
    location = models.CharField(max_length=100, blank=True, null=True) #会場所在地
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Design_Setting(models.Model):
    preset_image_id = 
    user_image_id = 
    record_id =
    font_type = models.CharField(max_length=100)
    font_color = models.CharField(max_length=100)
    start_date = models.DateField() #表示する参戦記録の開始日
    end_date = models.DateField() #表示する参戦記録の終了日
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

