from django.contrib import admin
from .models import Record, Artist_Record, Artist, Design_Setting, Venue

admin.site.register(Record)
admin.site.register(Artist_Record)
admin.site.register(Artist)
admin.site.register(Design_Setting)
admin.site.register(Venue)
