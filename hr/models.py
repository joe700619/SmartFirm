from django.db import models
from django.urls import reverse

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, verbose_name='員工編號')
    name = models.CharField(max_length=100, verbose_name='姓名')
    id_number = models.CharField(max_length=20, unique=True, verbose_name='身份證字號')
    mobile = models.CharField(max_length=20, verbose_name='手機')
    address = models.CharField(max_length=255, verbose_name='通訊地址')
    line_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='LineID')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    # Status Choices
    STATUS_CHOICES = [
        ('active', '在職'),
        ('resigned', '離職'),
        ('leave', '留職停薪'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active', 
        verbose_name='狀態'
    )

    # Group Choices
    GROUP_CHOICES = [
        ('A', 'A組'),
        ('B', 'B組'),
    ]
    group = models.CharField(
        max_length=10, 
        choices=GROUP_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name='組別'
    )

    # Job Title Choices
    JOB_TITLE_CHOICES = [
        ('member', '組員'),
        ('leader', '組長'),
        ('accountant', '會計師'),
    ]
    job_title = models.CharField(
        max_length=20, 
        choices=JOB_TITLE_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name='職稱'
    )

    extension = models.CharField(max_length=10, blank=True, null=True, verbose_name='分機號碼')
    is_deleted = models.BooleanField(default=False, verbose_name='是否刪除')

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

    class Meta:
        verbose_name = '員工資料'
        verbose_name_plural = '員工資料'
        ordering = ['employee_id']
