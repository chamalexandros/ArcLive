"""
URL configuration for ArcLive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


#プロジェクト全体のルーティング
#path以降は含めたいアプリケーションのルーティングを記載
#例：records/に対してrecords.urlsを紐づけているので、records/を加えるとそのページにアクセス可能になる
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),  # 127.0.0.1:8000/admin/
    path('', include('django.contrib.auth.urls')),
    path('records/', include('records.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
