from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Club, Apply

# 1. 顯示所有社團列表 (原本的 ModelList)
class ClubList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_club'
    model = Club
    template_name = 'em/club_list.html' # 記得對應你的 template 檔名

# 2. 顯示單一社團的詳細資料 (原本的 ModelView)
class ClubDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'em.view_club'
    model = Club
    pk_url_kwarg = 'mid'
    template_name = 'em/club_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 這裡幫你寫好：自動抓出「想轉入這個社團」的所有申請單
        ctx['apply_list'] = Apply.objects.filter(targetclub=self.object)
        return ctx

# 3. 顯示所有申請單列表 (原本的 EquipList)
class ApplyList(PermissionRequiredMixin, ListView):
    permission_required = 'em.view_apply'
    model = Apply
    template_name = 'em/apply_list.html'

# 4. 學生填寫申請單 (新增功能)
class ApplyCreate(CreateView):
    model = Apply
    fields = ['applicant', 'student_id', 'targetclub', 'reason']
    template_name = 'em/apply_form.html'
    success_url = '/em/apply/' # 填完後跳轉的頁面

# 5. 老師審核申請單 (原本的 EquipUpdate)
class ApplyUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'em.change_apply'
    model = Apply
    fields = ['status'] # 老師只需要改狀態（同意/不同意）
    template_name = 'em/apply_form.html'