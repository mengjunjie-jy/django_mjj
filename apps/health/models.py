from django.db import models

from django.db import models
from django.utils import timezone


class Health(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=20)
    age = models.IntegerField(verbose_name='年龄')
    body = models.DecimalField(verbose_name='体温', max_digits=3, decimal_places=1)
    location = models.CharField(verbose_name="地理位置", max_length=100)
    time = models.DateField(verbose_name='上传时间')

    class Meta:
        db_table = 'tb_health'
        verbose_name = '健康报备'
        verbose_name_plural = verbose_name

