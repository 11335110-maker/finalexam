from django.contrib import admin
from .models import Club, Apply, ClubProfile 
admin.site.register(Club)
admin.site.register(Apply)

@admin.register(ClubProfile)
class ClubProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'club', 'role']           # 後台清單要顯示 帳號、社團、職位
    list_filter = ['role', 'club']                    # 右側過濾小幫手
    search_fields = ['user__username', 'user__email'] # 支援用帳號和信箱搜尋