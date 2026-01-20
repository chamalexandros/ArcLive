from django.urls import path
from . import views


app_name = 'records'
urlpatterns = [
        path("", views.index, name='index'), #1つ目のURLを通ったらviews.indexを動かすようにする。このURLの名前はindexという意味
        
    ]
    