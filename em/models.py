from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    CATEGORY_CHOICES = [
        ('才藝', '才藝性社團'),
        ('體育', '體育性社團'),
        ('育樂', '育樂性社團'),
        ('學術類自然', '學術類自然社團'),
        ('學術類社會', '學術類社會社團'),
    ]
    category = models.CharField(
        '社團屬性', 
        max_length=10, 
        choices=CATEGORY_CHOICES, 
        default='才藝'            
    )
    clubname = models.CharField('社團名稱', max_length=10)
    leadername = models.CharField('社長名稱', max_length=5)
    teachername = models.CharField('社師名稱', max_length=5)
    memberaccount = models.CharField('社團名額', max_length=3, default='40')
    @property
    def current_vacancy(self):
        try:
            total = int(self.memberaccount)
        except ValueError:
            total = 0
            
        accepted_count = self.apply_set.filter(status=1).count()
        
        vacancy = total - accepted_count
        return vacancy if vacancy > 0 else 0
    def __str__(self):
        return self.clubname


class Apply(models.Model):
    STATUS_CHOICES = [
        (0, '第一關：等待原社社長審核'),
        (1, '第一關失敗：原社社長拒絕'), 
        (2, '第二關：等待原社社師審核'),
        (3, '第二關失敗：原社社師拒絕'), 
        (4, '申請成功：允許轉出'),
        (5, '第三關：選取欲轉入社團並填寫資料'),
        (6, '第四關：等待新社社長審核'),
        (7, '第四關失敗：新社社長拒絕'),
        (8, '第五關：等待新社社師審核'),
        (9, '第五關失敗：新社社師拒絕'), 
        (10, '第六關：等待組長審核'),
        (11, '第六關失敗：組長拒絕'), 
        (12, '第六關成功：申請成功'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='申請者')
    student_id = models.CharField('學號', max_length=20)
    from_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='out_applies', verbose_name='原社團',null=True, blank=True)
    target_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='in_applies', verbose_name='想轉入的社團', null=True, blank=True)
    out_reason = models.TextField('轉出原因', null=True, blank=True)
    in_reason = models.TextField('轉入原因', null=True, blank=True)
    status = models.IntegerField('申請狀態', choices=STATUS_CHOICES, default=0)
def __str__(self):
        if self.applicant:
            return f"[{self.student_id}] {self.applicant.last_name}{self.applicant.first_name} 的轉社申請"
        return f"[{self.student_id}] 訪客 的轉社申請"
