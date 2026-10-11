from django.urls import path
from . import views


app_name = 'records'
urlpatterns = [
        path("record/home", views.home, name='home'), #1つ目のURLを通ったらviews.homeを動かすようにする。このURLの名前はhomeという意味     
        path("record/create/", views.record_create, name='record_create'),
        path("record/list/", views.record_list, name='record_list'),
        path("record/<uuid:pk>/", views.record_detail, name="record_detail"),
        path("record/<uuid:pk>/update/", views.record_update, name="record_update"),
        path("record/<uuid:pk>/delete/", views.record_delete, name="record_delete"),
        path('generate/', views.generate_view, name='generate'),
        path('result/', views.display_result_view, name='display_result'),
        
    ]
    