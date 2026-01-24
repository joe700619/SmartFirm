from django.db import models
from admin_module.models import BasicInformation

from django.conf import settings

class SmartFirmBaseModel(models.Model):
    """基礎模型：包含建立/修改資訊與軟刪除功能"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='建立者'
    )
    is_deleted = models.BooleanField(default=False, verbose_name='是否刪除')

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """軟刪除：標記為已刪除"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """還原刪除"""
        self.is_deleted = False
        self.save()

class Shareholder(SmartFirmBaseModel):
    """股東基本資料模型（集中管理）"""
    identifier = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='身分證字號/統一編號',
        help_text='個人股東填身分證字號，法人股東填統一編號'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='股東姓名'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='地址'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='聯絡電話'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='電子郵件'
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='生日'
    )

    class Meta:
        db_table = 'shareholder'
        verbose_name = '股東'
        verbose_name_plural = '股東'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.identifier})"


class CompanyShareholding(SmartFirmBaseModel):
    """公司持股關係模型"""
    shareholder = models.ForeignKey(
        Shareholder,
        on_delete=models.CASCADE,
        related_name='company_holdings',
        verbose_name='股東'
    )
    company = models.ForeignKey(
        BasicInformation,
        on_delete=models.CASCADE,
        related_name='shareholdings',
        verbose_name='公司'
    )

    class Meta:
        db_table = 'company_shareholding'
        verbose_name = '持股關係'
        verbose_name_plural = '持股關係'
        unique_together = [['shareholder', 'company']]
        ordering = ['company', 'shareholder']

    def __str__(self):
        return f"{self.shareholder.name} - {self.company.companyName}"


class StockTransaction(SmartFirmBaseModel):
    """股權交易記錄模型"""
    TRANSACTION_TYPE_CHOICES = [
        ('founding', '設立'),
        ('capital_reduction', '減資'),
        ('trade', '買賣'),
        ('gift', '贈與'),
        ('transfer_in', '轉入'),
        ('transfer_out', '轉出'),
    ]
    
    STOCK_TYPE_CHOICES = [
        ('common', '普通股'),
        ('preferred', '特別股'),
    ]

    company_holding = models.ForeignKey(
        CompanyShareholding,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='持股關係'
    )
    transaction_date = models.DateField(
        verbose_name='交易日期'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='交易說明'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='交易類型'
    )
    stock_type = models.CharField(
        max_length=20,
        choices=STOCK_TYPE_CHOICES,
        default='common',
        verbose_name='股票類型'
    )
    par_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10.00,
        verbose_name='每股面額'
    )
    quantity = models.IntegerField(
        verbose_name='股數'
    )
    stock_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name='股票金額',
        help_text='每股面額 × 股數'
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='交易金額',
        help_text='實際交易價格（可能不等於股票金額）'
    )
    note = models.TextField(
        blank=True,
        verbose_name='備註'
    )

    class Meta:
        db_table = 'stock_transaction'
        verbose_name = '股權交易記錄'
        verbose_name_plural = '股權交易記錄'
        ordering = ['transaction_date', 'created_at']

    def __str__(self):
        return f"{self.company_holding.shareholder.name} - {self.get_transaction_type_display()} ({self.quantity}股) - {self.transaction_date}"


class BoardMember(SmartFirmBaseModel):
    """董監事模型"""
    TITLE_CHOICES = [
        ('chairman', '董事長'),
        ('director', '董事'),
        ('supervisor', '監察人'),
    ]

    company = models.ForeignKey(
        BasicInformation,
        on_delete=models.CASCADE,
        related_name='board_members',
        verbose_name='公司'
    )
    person = models.ForeignKey(
        Shareholder,
        on_delete=models.CASCADE,
        related_name='board_positions',
        verbose_name='姓名'
    )
    title = models.CharField(
        max_length=20,
        choices=TITLE_CHOICES,
        verbose_name='職稱'
    )
    representative_of = models.ForeignKey(
        Shareholder,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='represented_by',
        verbose_name='所代表法人',
        help_text='若此人為法人代表，請選擇所代表之法人'
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='生日'
    )

    class Meta:
        db_table = 'board_member'
        verbose_name = '董監事'
        verbose_name_plural = '董監事'
        ordering = ['company', 'title', 'person']

    def __str__(self):
        return f"{self.company.companyName} - {self.get_title_display()}: {self.person.name}"
