from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('em.urls')), # 這裡會去找 em 資料夾下的 urls.py
]