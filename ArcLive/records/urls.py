from django.urls import path
from . import views


app_name = 'records'
urlpatterns = [
        path("", views.home, name='home'), #1つ目のURLを通ったらviews.homeを動かすようにする。このURLの名前はhomeという意味
        
    ]
    