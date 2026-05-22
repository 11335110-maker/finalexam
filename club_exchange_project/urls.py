from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('em.urls')), # 👈 讓所有的網址一律只聽妳的 em.urls 的話！
    
    # 🪓 原本的 path('accounts/', ...) 已經被我們當場擊殺，直接刪除！
]