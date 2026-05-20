from django.urls import path
from . import views  # 注意這裡是用 . 引入同資料夾的 views

urlpatterns = [
    # 首頁
    path('', views.home_page, name='home'),
    # 社團列表頁
    path('club/', views.ClubList.as_view(), name='club_list'), 
    path('apply/create/', views.ApplyCreate.as_view(), name='apply_create'),
    path('apply/student/', views.StudentApplyList.as_view(), name='student_list'),
    # 🌟 把它改成這樣（注意看 views. 後面的名字！）：
    path('apply/teacher/', views.TeacherApplyList.as_view(), name='teacher_list'),
   # 老師手動修改狀態表單
    path('apply/<int:pk>/edit/', views.ApplyUpdate.as_view(), name='apply_edit'),
    #學生取得原社轉出許可後，選填新社團的通道
    path('apply/<int:pk>/out_success/', views.out_suecces, name='out_success'),
    #老師快捷一鍵改狀態的通道
    path('apply/<int:pk>/review/<int:temp_status>/', views.review_apply, name='review_apply'),
    path('apply/leader/', views.leader, name='leader'),
]
