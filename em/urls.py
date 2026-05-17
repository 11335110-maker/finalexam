from django.urls import path
from . import views  # 注意這裡是用 . 引入同資料夾的 views

urlpatterns = [
    # 1. 遊戲主選單首頁
    path('', views.home_page, name='home'),
    
    # 2. 社團列表頁
    path('club/', views.ClubList.as_view(), name='club_list'), 
    
    # 3. 申請表紀錄清單頁 (老師審核與切換角色都在這)
    path('apply/', views.ApplyList.as_view(), name='apply_list'),
    
    # 4. 學生填寫新申請表頁 (我們統一用 apply/create/ 這個網址，對應 name='apply_create')
    path('apply/create/', views.ApplyCreate.as_view(), name='apply_create'),
    
    # 5. 修改申請表頁
    path('apply/<int:pk>/edit/', views.ApplyUpdate.as_view(), name='apply_edit'),
    
    # 6. 後台審核改數字的秘密通道 (把帶有 <int:pk> 的排在純文字後面)
    path('apply/<int:pk>/review/<int:temp_status>/', views.review_apply, name='review_apply'),
]