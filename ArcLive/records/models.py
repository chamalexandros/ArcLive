from django.db import models

class Record(models.Model):
    user_id = models.ForeignKey('accounts.User',on_delete=models.CASCADE,verbose_name='ユーザーID')
    venue_id = models.OneToOneField('Venue',on_delete=models.CASCADE,verbose_name='会場ID')
    event_name = models.CharField(max_length=100, blank=True, null=True,verbose_name='イベント名')
    live_date = models.DateField(verbose_name='公演日')
    live_image = models.TextField(blank=True, null=True,verbose_name='参戦記録一覧画面に表示する画像')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.live_date}|{self.event_name}"



class Artist_Record(models.Model):
    record_id = models.ForeignKey('Record', on_delete=models.CASCADE,verbose_name='参戦記録ID')
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE,verbose_name='アーティストID')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

class Artist(models.Model):
    name = models.CharField(max_length=100,verbose_name='アーティスト名')
    reading_name = models.CharField(max_length=100,verbose_name='読み方')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"



class Venue(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True,verbose_name='会場名')
    location = models.CharField(max_length=100, blank=True, null=True,verbose_name='会場所在地')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}|{self.location}"
    
    

class Design_Setting(models.Model):
    preset_image_id = models.ForeignKey('accounts.Preset_Image',on_delete=models.CASCADE,verbose_name='アプリ内画像')
    user_image_id = models.ForeignKey('accounts.User_Image',on_delete=models.CASCADE,verbose_name='ユーザー本体の画像') 
    record_id = models.ForeignKey('Record', on_delete=models.CASCADE,verbose_name='参戦記録ID')
    font_type = models.CharField(max_length=100,verbose_name='フォントタイプ')
    font_color = models.CharField(max_length=100,verbose_name='フォントの色')
    start_date = models.DateField(verbose_name='表示する参戦記録の開始日')
    end_date = models.DateField(verbose_name='表示する参戦記録の終了日')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.font_type}|{self.font_color}|{self.start_date}|{self.end_date}"