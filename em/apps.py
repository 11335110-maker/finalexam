from django.apps import AppConfig

class EmConfig(AppConfig): # 類別名稱順便改漂亮一點，不改也可以，但下面一定要改
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'em'  # <--- 務必改成跟你的資料夾名稱一模一