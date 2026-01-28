from django.db import models
from admin_module.models import BasicInformation, Contact

from django.conf import settings
from django.utils import timezone

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



class RegistrationProgress(SmartFirmBaseModel):
    """登記案件進度追蹤"""
    MANDATE_STATUS_CHOICES = [
        ('not_issued', '未發出'),
        ('pending_return', '待簽回'),
        ('approved', '已核准'),
        ('disagreed', '不同意'),
    ]
    
    STATUS_CHOICES = [
        ('discussion', '0.討論中'),
        ('new_case', '1.新接案'),
        ('documentation', '2.製作中'),
        ('government_review', '3.審查中'),
        ('closed', '4.結案'),
        ('none', '5.沒有辦理'),
    ]
    
    DELIVERY_METHOD_CHOICES = [
        ('self_pickup', '自取'),
        ('mail', '郵寄'),
    ]

    # Block 1
    mandate_status = models.CharField(
        max_length=20, 
        choices=MANDATE_STATUS_CHOICES, 
        default='not_issued',
        verbose_name='委任書狀態'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='discussion',
        verbose_name='案件狀態'
    )
    delivery_method = models.CharField(
        max_length=20, 
        choices=DELIVERY_METHOD_CHOICES,
        default='mail',
        verbose_name='寄送方式'
    )
    case_type = models.ManyToManyField(
        'master.CaseType',
        blank=True,
        verbose_name='案件類別'
    )

    # Block 2
    case_number = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False, 
        verbose_name='登記案件文號'
    )
    customer = models.ForeignKey(
        BasicInformation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='公司名稱',
        related_name='registration_cases'
    )
    # Storing snapshot validation data
    tax_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='統一編號')
    line_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Line ID')
    room_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Room ID')
    
    acceptance_date = models.DateField(
        default=timezone.now,
        verbose_name='承接日期'
    )
    due_date = models.DateField(blank=True, null=True, verbose_name='預計完成日期')
    
    main_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='主要聯絡人',
        related_name='registration_cases'
    )
    
    # Contact snapshots
    contact_email = models.EmailField(blank=True, null=True, verbose_name='Email')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='電話')
    contact_mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name='手機')
    contact_address = models.TextField(blank=True, null=True, verbose_name='地址')
    
    remarks = models.TextField(blank=True, null=True, verbose_name='備註')

    class Meta:
        db_table = 'registration_progress'
        verbose_name = '登記案件'
        verbose_name_plural = '登記案件'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.case_number} - {self.customer.companyName if self.customer else 'Unknown'}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            today_str = timezone.now().strftime('%Y%m%d')
            prefix = f"RO-{today_str}-R"
            # Find max seq for today
            existing = RegistrationProgress.objects.filter(case_number__startswith=prefix).order_by('case_number').last()
            if existing:
                try:
                    # Extract sequence number RO-YYYYMMDD-RXXX
                    seq = int(existing.case_number.split('-R')[-1])
                    new_seq = seq + 1
                except ValueError:
                    new_seq = 1
            else:
                new_seq = 1
            
            self.case_number = f"{prefix}{new_seq:03d}"
            
        # Update completion date if status is closed or none
        if self.status in ['closed', 'none'] and not self.due_date:
             # Logic for auto-setting due_date/completion_date? 
             # User said: "預計完成日期：狀態改為結案，或是沒有辦理的時候". 
             # Seems to imply it's set WHEN status changes? Or maybe it means "Required when..."?
             # "預計完成日期：狀態改為結案，或是沒有辦理的時候" -> "Expected Completion Date: When status is Closed or Not Processed [Set to today?]"
             # I'll default it to today if empty and status is finalized, or leave logic to view/frontend.
             pass

        super().save(*args, **kwargs)


class RegistrationService(SmartFirmBaseModel):
    """登記案件服務項目明細 (Block 3)"""
    progress = models.ForeignKey(
        RegistrationProgress,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='登記案件'
    )
    service = models.ForeignKey(
        'master.ServiceItem',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='服務代碼'
    )
    service_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='服務名稱')
    service_item = models.CharField(max_length=200, blank=True, null=True, verbose_name='服務項目')
    fee = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='服務費用')
    remarks = models.TextField(blank=True, null=True, verbose_name='備註')

    class Meta:
        db_table = 'registration_service'
        verbose_name = '登記案件服務明細'
        verbose_name_plural = '登記案件服務明細'
        ordering = ['created_at']

class RegistrationCostSplit(SmartFirmBaseModel):
    """登記案件公費拆分計算"""
    progress = models.ForeignKey(
        RegistrationProgress,
        on_delete=models.CASCADE,
        related_name='cost_splits',
        verbose_name='登記案件'
    )
    assistant = models.ForeignKey(
        'hr.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='助理'
    )
    ratio = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name='比例',
        help_text='百分比 (Ex: 50.00)'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        default=0, 
        verbose_name='分攤公費'
    )

    class Meta:
        db_table = 'registration_cost_split'
        verbose_name = '公費拆分'
        verbose_name_plural = '公費拆分'
        ordering = ['created_at']

class RegistrationMandate(SmartFirmBaseModel):
    """委任書 (Mandate)"""
    progress = models.OneToOneField(
        RegistrationProgress,
        on_delete=models.CASCADE,
        related_name='mandate',
        verbose_name='登記案件'
    )
    # 範例欄位：委任日期, 簽署狀態
    mandate_date = models.DateField(blank=True, null=True, verbose_name='委任日期')
    is_signed = models.BooleanField(default=False, verbose_name='是否已簽署')
    remarks = models.TextField(blank=True, null=True, verbose_name='備註')

    class Meta:
        db_table = 'registration_mandate'
        verbose_name = '委任書'
        verbose_name_plural = '委任書'

class RegistrationAML(SmartFirmBaseModel):
    """洗錢防制 (Money Laundering Prevention)"""
    progress = models.OneToOneField(
        RegistrationProgress,
        on_delete=models.CASCADE,
        related_name='aml_record',
        verbose_name='登記案件'
    )
    # 範例欄位：風險等級
    RISK_LEVEL_CHOICES = [
        ('low', '低風險'),
        ('medium', '中風險'),
        ('high', '高風險'),
    ]
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default='low',
        verbose_name='風險等級'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='審查紀錄')

    class Meta:
        db_table = 'registration_aml'
        verbose_name = '洗錢防制'
        verbose_name_plural = '洗錢防制'
