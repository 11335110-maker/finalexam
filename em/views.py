from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Club, Apply
from django.contrib.auth.mixins import LoginRequiredMixin # 類別視圖專用的強迫登入警衛
from django.urls import reverse_lazy                     # 自動找網址別名的雷達
from django.http import HttpResponse                     # 用來噴出警告文字的工具
from django.contrib.auth.decorators import permission_required

class ClubList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_club'#登入才有使用權限
    model = Club
    template_name = 'em/club_list.html'

#  學生頁面
class StudentApplyList(LoginRequiredMixin, ListView):
    model = Apply
    template_name = 'em/student_list.html'  

    #學生只能看到自己送出的申請單
    def get_queryset(self):
        return Apply.objects.filter(applicant=self.request.user)

# 老師頁面
class TeacherApplyList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_apply'       
    model = Apply
    
    # 🌟 請一字不差地複製這行！注意：是 template_name，完全不能拼錯！
    template_name = 'em/teacher_list.html'
    def get_queryset(self):
        # 老師進來可以看到全校所有學生的申請單，方便審核
        return Apply.objects.all()

class ApplyCreate(LoginRequiredMixin, CreateView):
    model = Apply
    fields = ['student_id', 'from_club', 'out_reason'] 
    template_name = 'em/apply_form.html'
    success_url = reverse_lazy('student_list')
    
    def form_valid(self, form):
        user_email = self.request.user.email 
        
        if not user_email.endswith('@dcsh.tp.edu.tw'):
            return HttpResponse("請使用大直高中的 Google 帳號登入系統！", status=403)
        # 防重複申請
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

# 5. 老師審核申請單 
class ApplyUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'em.change_apply'
    model = Apply
    fields = ['status'] # 老師只需要改狀態（同意/不同意）
    template_name = 'em/apply_form.html'

def out_suecces(request, pk):
    apply = get_object_or_404(Apply, pk=pk)
    if apply.status < 5:
        return HttpResponse("妳還沒獲得原社團的轉出許可，不能選擇新社團喔！")
    
    # 只有狀態是 5 的人，才能看到這個選社團的 template
    if request.method == 'POST':
        apply.target_club = request.POST.get('target_club')
        apply.in_reason = request.POST.get('in_reason')
        apply.status = 6 # 填完直接跳到「等待新社長審核」
        apply.save()
        return redirect('student_list')
        
    return render(request, 'em/select_new_club.html', {'apply': apply})
# ... 妳原本上面的各種 class ApplyList, class ApplyCreate ...

def review_apply(request, pk, temp_status):
    # 1. 抓出是哪一筆申請表
    apply = get_object_or_404(Apply, pk=pk)
    # 2. 把它的狀態改成按鈕指定的數字
    apply.status = temp_status
    # 3. 存檔寫進資料庫
    apply.save()
    # 4. 重新導向回清單頁面
    return redirect('teacher_list')
# 首頁
def home_page(request):
    return render(request, 'em/home.html')