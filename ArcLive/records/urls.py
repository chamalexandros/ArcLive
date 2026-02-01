from django.urls import path
from . import views


app_name = 'records'
urlpatterns = [
        path("record/home", views.home, name='home'), #1つ目のURLを通ったらviews.homeを動かすようにする。このURLの名前はhomeという意味
        path("record/create/", views.recordcreate, name='recordcreate'),
        path("record/list/", views.recordlist, name='recordlist'),
        
    ]
    