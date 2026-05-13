from django.urls import path
from . import views  # 注意這裡是用 . 引入同資料夾的 views

urlpatterns = [
    path('club/', views.ClubList.as_view(), name='club_list'), 
    path('club/<int:mid>/', views.ClubDetail.as_view(), name='club_detail'),
    path('apply/', views.ApplyList.as_view(), name='apply_list'),
    path('apply/add/', views.ApplyCreate.as_view(), name='apply_add'),
    path('apply/<int:pk>/edit/', views.ApplyUpdate.as_view(), name='apply_edit'),
]