from django.db import models
from admin_module.models import BasicInformation


class Shareholder(models.Model):
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )

    class Meta:
        db_table = 'shareholder'
        verbose_name = '股東'
        verbose_name_plural = '股東'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.identifier})"


class CompanyShareholding(models.Model):
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )

    class Meta:
        db_table = 'company_shareholding'
        verbose_name = '持股關係'
        verbose_name_plural = '持股關係'
        unique_together = [['shareholder', 'company']]
        ordering = ['company', 'shareholder']

    def __str__(self):
        return f"{self.shareholder.name} - {self.company.companyName}"


class StockTransaction(models.Model):
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )

    class Meta:
        db_table = 'stock_transaction'
        verbose_name = '股權交易記錄'
        verbose_name_plural = '股權交易記錄'
        ordering = ['transaction_date', 'created_at']

    def __str__(self):
        return f"{self.company_holding.shareholder.name} - {self.get_transaction_type_display()} ({self.quantity}股) - {self.transaction_date}"
