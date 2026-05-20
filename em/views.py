from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Club, Apply
from django.contrib.auth.mixins import LoginRequiredMixin # 類別視圖專用的強迫登入警衛
from django.urls import reverse_lazy                     # 自動找網址別名的雷達
from django.http import HttpResponse                     # 用來噴出警告文字的工具
from django.contrib.auth.decorators import permission_required

# =================================================================
# 👑 訓育組長登記的「特定審核帳號模擬庫」
# =================================================================
FAKE_TEACHER_DB = {
    '原社長': 'club_leader_out@dcsh.tp.edu.tw',
    '原老師': 'club_teacher_out@dcsh.tp.edu.tw',
    '新社長': 'club_leader_in@dcsh.tp.edu.tw',
    '新老師': 'club_teacher_in@dcsh.tp.edu.tw',
    '訓育組長': 'leader@dcsh.tp.edu.tw'
}

class ClubList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_club' # 登入才有使用權限
    model = Club
    template_name = 'em/club_list.html'

# 👥 學生頁面：學生只能看到自己送出的申請單
class StudentApplyList(LoginRequiredMixin, ListView):
    model = Apply
    template_name = 'em/student_list.html'  

    def get_queryset(self):
        return Apply.objects.filter(applicant=self.request.user)

# 👨‍🏫 老師頁面：【已加入精準權限過濾邏輯】
class TeacherApplyList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_apply'       
    model = Apply
    template_name = 'em/teacher_list.html'
    
    def get_queryset(self):
        # 1. 優先抓取網址有沒有「模擬帳號」，如果沒有，就用真正登入的老師信箱
        user_email = self.request.GET.get('mock_user', self.request.user.email)
        
        # 2. 如果是「訓育組長」進來，放行看「全校全部」
        if user_email == 'leader@dcsh.tp.edu.tw' or self.request.user.is_superuser:
            return Apply.objects.all()
            
        # 3. 大直專屬：根據模擬或登入帳號，對照其負責的社團
        managed_club = None
        if user_email in ['club_leader_out@dcsh.tp.edu.tw', 'club_teacher_out@dcsh.tp.edu.tw']:
            managed_club = "熱舞社"  # 這裡可以改成妳測試用的原社團名稱
        elif user_email in ['club_leader_in@dcsh.tp.edu.tw', 'club_teacher_in@dcsh.tp.edu.tw']:
            managed_club = "吉他社"  # 這裡可以改成妳測試用的新社團名稱
            
        # 4. 開始精準過濾單子
        if managed_club:
            # 該社老師/社長只能看到：原本是我們社團要轉出的，或是想轉入我們社團的學生
            return Apply.objects.filter(from_club=managed_club) | Apply.objects.filter(target_club=managed_club)
            
        # 5. 安全防漏：若不屬於任何設定的社團帳號，則什麼都不顯示
        return Apply.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 傳遞目前正在模擬或登入的帳號信箱，以便在 HTML 畫面上標示身分
        context['current_mock_user'] = self.request.GET.get('mock_user', self.request.user.email)
        return context

# 📝 學生填寫轉社申請表
class ApplyCreate(LoginRequiredMixin, CreateView):
    model = Apply
    fields = ['student_id', 'from_club', 'out_reason'] 
    template_name = 'em/apply_form.html'
    success_url = reverse_lazy('student_list')
    
    def form_valid(self, form):
        user_email = self.request.user.email 
        
        if not user_email.endswith('@dcsh.tp.edu.tw'):
            return HttpResponse("請使用大直高中的 Google 帳號登入系統！", status=403)
            
        # 防重複申請（排除 11 成功、12 失敗結案。代表失敗了可以重新申請填表！）
        active_apply = Apply.objects.filter(
            applicant=self.request.user
        ).exclude(status__in=[11, 12]).exists()

        if active_apply:
            return HttpResponse(
                "<h2>❌ 您目前已有一筆轉社申請正在審核中！</h2><p>在該申請結案前，無法建立新申請。</p><a href='/apply/student/'>查看目前進度</a>", 
                status=400
            )
        form.instance.applicant = self.request.user
        form.instance.status = 0
        return super().form_valid(form)

# 🛠️ 傳統老師修改申請單
class ApplyUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'em.change_apply'
    model = Apply
    fields = ['status'] 
    template_name = 'em/apply_form.html'

# 🚀 學生獲得許可，選填新社團
def out_suecces(request, pk):
    apply = get_object_or_404(Apply, pk=pk)
    if apply.status < 5:
        return HttpResponse("妳還沒獲得原社團的轉出許可，不能選擇新社團喔！")
    
    if request.method == 'POST':
        apply.target_club = request.POST.get('target_club')
        apply.in_reason = request.POST.get('in_reason')
        apply.status = 6 # 填完直接跳到「等待新社長審核」
        apply.save()
        return redirect('student_list')
        
    return render(request, 'em/select_new_club.html', {'apply': apply})

# 🎛️ 審核按鈕一鍵變更狀態總機（已去重、修正完成）
def review_apply(request, pk, temp_status):
    apply = get_object_or_404(Apply, pk=pk)
    apply.status = temp_status
    apply.save()
    
    # 🌟 聰明跳轉：如果是組長在終審頁面按的，就跳回組長頁面；如果是老師按的，就跳回老師頁面
    if 'leader' in request.META.get('HTTP_REFERER', ''):
        return redirect('leader')
        
    return redirect('teacher_list')

# 👑 功能二：訓育組長終極大後台大腦
def leader(request):
    all_applies = Apply.objects.all()
    return render(request, 'em/leader.html', {
        'object_list': all_applies,
        'fake_db': FAKE_TEACHER_DB
    })

# 🏠 系統首頁
def home_page(request):
    return render(request, 'em/home.html')