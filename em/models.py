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
    STATUS_CHOICE = [(0, '待審核'), (1, '同意'), (2, '拒絕')]
    
    applicant = models.CharField('申請者', max_length=5)
    student_id = models.CharField('學號', max_length=20)
    targetclub = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='想轉入的社團')
    reason = models.TextField('轉社原因', blank=True)
    status = models.IntegerField('申請狀態', choices=STATUS_CHOICE, default=0)

    def __str__(self):
       return f"{self.applicant} 的申請單"

