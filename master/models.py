from django.db import models

class ServiceItem(models.Model):
    service_code = models.CharField(max_length=50, unique=True, verbose_name='服務代碼')
    service_name = models.CharField(max_length=100, verbose_name='服務名稱')
    reference_price = models.IntegerField(default=0, verbose_name='參考價格')
    DEPARTMENT_CHOICES = [
        ('bookkeeping', '記帳'),
        ('audit', '查帳'),
        ('registration', '登記'),
        ('advance_payment', '代墊'),
    ]
    department = models.CharField(
        max_length=20, 
        choices=DEPARTMENT_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name='部門'
    )
    is_aml_required = models.BooleanField(default=False, verbose_name="需洗錢防制")
    remarks = models.TextField(blank=True, null=True, verbose_name='備註')

    def __str__(self):
        return f"{self.service_code} - {self.service_name}"

    class Meta:
        verbose_name = '收費明細'
        verbose_name_plural = '收費明細'
        ordering = ['service_code']

class KnowledgeNote(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')
    tags = models.CharField(max_length=200, verbose_name='適用情境', help_text='例如：有限公司 跨縣市 變更登記')
    checklist = models.TextField(verbose_name='必備文件', blank=True, null=True)
    steps = models.TextField(verbose_name='操作流程', blank=True, null=True)
    warnings = models.TextField(verbose_name='專家注意事項', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '知識筆記'
        verbose_name_plural = '知識筆記'
        ordering = ['-created_at']

class CaseType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='案件類別名稱')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '案件類別'
        verbose_name_plural = '案件類別'
        ordering = ['name']

class SystemParameter(models.Model):
    gemini_api_key = models.CharField(max_length=255, blank=True, verbose_name='Gemini API Key')
    line_access_token = models.CharField(max_length=255, blank=True, verbose_name='Line Access Token')
    line_web_url = models.URLField(blank=True, verbose_name='Line Web Hook')
    ecpay_merchant_id = models.CharField(max_length=50, blank=True, verbose_name='綠界 Merchant ID')
    ecpay_hash_key = models.CharField(max_length=50, blank=True, verbose_name='綠界 Hash Key')
    ecpay_hash_iv = models.CharField(max_length=50, blank=True, verbose_name='綠界 Hash IV')

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SystemParameter, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "系統參數設定"

    class Meta:
        verbose_name = '系統參數'
        verbose_name_plural = '系統參數'
