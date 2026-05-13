from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Club(models.Model):
    clubname = models.CharField('社團名稱', max_length=10)
    leadername = models.CharField('社長名稱', max_length=5)
    teachername = models.CharField('社師名稱', max_length=5)
    
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

