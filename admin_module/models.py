from django.db import models


class BasicInformation(models.Model):
    """客戶基本資料模型"""
    companyId = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='公司統編',
        help_text='請輸入8位數公司統一編號'
    )
    companyName = models.CharField(
        max_length=200,
        verbose_name='公司名稱'
    )
    contact = models.CharField(
        max_length=100,
        verbose_name='聯絡人'
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='電子郵件'
    )
    phoneNumber = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='公司電話'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='聯絡人手機'
    )
    LineId = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Line ID'
    )
    fax_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='傳真號碼'
    )
    account_last_5 = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name='帳號後五碼'
    )
    registration_address = models.TextField(
        verbose_name='登記地址'
    )
    mailing_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='通訊地址',
        help_text='若未填寫，則與登記地址相同'
    )
    important_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='重要訊息描述'
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
        db_table = 'basic_information'
        verbose_name = '客戶基本資料'
        verbose_name_plural = '客戶基本資料'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.companyName} ({self.companyId})"

    def save(self, *args, **kwargs):
        """如果未填寫通訊地址，則使用登記地址"""
        if not self.mailing_address:
            self.mailing_address = self.registration_address
        super().save(*args, **kwargs)


class Contact(models.Model):
    """聯絡人資料模型"""
    company_name = models.CharField(
        max_length=200,
        verbose_name='公司名稱'
    )
    company_id = models.CharField(
        max_length=8,
        verbose_name='統一編號',
        help_text='請輸入8位數統一編號'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='聯絡人姓名'
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='職稱'
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='電話'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='手機'
    )
    fax = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='傳真'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='通訊地址'
    )
    notes = models.TextField(
        blank=True,
        null=True,
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
        db_table = 'contact'
        verbose_name = '聯絡人'
        verbose_name_plural = '聯絡人'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company_name}"


class IncomingMail(models.Model):
    """收文主記錄模型"""
    date = models.DateField(
        verbose_name='日期'
    )
    serial_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='序號'
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
        db_table = 'incoming_mail'
        verbose_name = '收文主記錄'
        verbose_name_plural = '收文主記錄'
        ordering = ['-date', '-serial_number']

    def __str__(self):
        return f"{self.serial_number}"

    def save(self, *args, **kwargs):
        """自動生成序號，格式：YYYYMMDD-XXX"""
        if not self.serial_number:
            date_prefix = self.date.strftime('%Y%m%d')
            # 查詢當天已有的最大序號
            existing = IncomingMail.objects.filter(
                serial_number__startswith=date_prefix
            ).order_by('-serial_number').first()
            
            if existing:
                # 取得最後三位數字並加1
                last_num = int(existing.serial_number[-3:])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.serial_number = f"{date_prefix}-{new_num:03d}"
        
        super().save(*args, **kwargs)


class IncomingMailItem(models.Model):
    """收文明細記錄模型"""
    CONTENT_TYPE_CHOICES = [
        ('accounting_voucher', '會計/營業憑證'),
        ('nta_chinese', '國稅局中文'),
    ]
    
    incoming_mail = models.ForeignKey(
        IncomingMail,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='收文主記錄'
    )
    sender = models.CharField(
        max_length=200,
        verbose_name='寄件人'
    )
    company = models.ForeignKey(
        BasicInformation,
        on_delete=models.PROTECT,
        verbose_name='統一編號',
        help_text='請從客戶基本資料中選取'
    )
    customer_name = models.CharField(
        max_length=200,
        verbose_name='歸屬客戶'
    )
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_TYPE_CHOICES,
        verbose_name='內容'
    )
    notify_customer = models.BooleanField(
        default=False,
        verbose_name='通知客戶'
    )
    message_content = models.TextField(
        blank=True,
        null=True,
        verbose_name='傳送訊息內容'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='排序順序'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )

    class Meta:
        db_table = 'incoming_mail_item'
        verbose_name = '收文明細記錄'
        verbose_name_plural = '收文明細記錄'
        ordering = ['incoming_mail', 'order']

    def __str__(self):
        return f"{self.incoming_mail.serial_number} - {self.sender}"


class CustomerChange(models.Model):
    """客戶增減模型"""
    CHANGE_TYPE_CHOICES = [
        ('new_establishment', '新設立'),
        ('transfer_in', '轉入'),
        ('transfer_out', '轉出'),
        ('dissolution', '解散'),
    ]
    
    company_id = models.CharField(
        max_length=8,
        verbose_name='統一編號',
        help_text='請輸入8位數統一編號'
    )
    company_name = models.CharField(
        max_length=200,
        verbose_name='客戶名稱'
    )
    accounting_assistant = models.CharField(
        max_length=100,
        verbose_name='記帳助理人員'
    )
    overdue_days = models.IntegerField(
        default=0,
        verbose_name='逾期天數'
    )
    establishment_date = models.DateField(
        verbose_name='立案日期'
    )
    change_type = models.CharField(
        max_length=20,
        choices=CHANGE_TYPE_CHOICES,
        verbose_name='種類'
    )
    
    # 檢查事項
    invoice_quantity = models.BooleanField(
        default=False,
        verbose_name='發票本數'
    )
    id_copy = models.BooleanField(
        default=False,
        verbose_name='負責人身分證影本'
    )
    lease_and_tax = models.BooleanField(
        default=False,
        verbose_name='租約及稅單'
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
        db_table = 'customer_change'
        verbose_name = '客戶增減'
        verbose_name_plural = '客戶增減'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} ({self.company_id}) - {self.get_change_type_display()}"


class VATCheck(models.Model):
    """營業稅檢查主記錄模型"""
    STATUS_CHOICES = [
        ('pending', '尚未完成'),
        ('completed', '已完成'),
    ]
    
    date = models.DateField(
        verbose_name='日期'
    )
    check_period = models.CharField(
        max_length=50,
        verbose_name='檢查期間',
        help_text='例如：113年1-2月'
    )
    inspector = models.CharField(
        max_length=100,
        verbose_name='檢查人員'
    )
    inspectee = models.CharField(
        max_length=100,
        verbose_name='受檢人員'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='完成狀態'
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
        db_table = 'vat_check'
        verbose_name = '營業稅檢查'
        verbose_name_plural = '營業稅檢查'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.check_period} - {self.inspector}"


class VATCheckItem(models.Model):
    """營業稅檢查明細記錄模型"""
    vat_check = models.ForeignKey(
        VATCheck,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='營業稅檢查主記錄'
    )
    
    # 基本資料
    company_id = models.CharField(
        max_length=8,
        verbose_name='統一編號',
        help_text='請輸入8位數統一編號'
    )
    company_name = models.CharField(
        max_length=200,
        verbose_name='公司名稱'
    )
    input_buyer = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='進項買受人'
    )
    
    # 檢查項目
    check_input_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='進項金額（檢查）'
    )
    input_duplicate = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='進項重複'
    )
    output_e_invoice = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='銷項電子發票'
    )
    
    # 401資料
    form401_output_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='銷項金額（401）'
    )
    form401_input_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='進項金額（401）'
    )
    tax_credit_carried_forward = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='留抵稅額'
    )
    tax_payable = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='應納稅額'
    )
    tax_refundable = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='應退稅額'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='排序順序'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    
    class Meta:
        db_table = 'vat_check_item'
        verbose_name = '營業稅檢查明細'
        verbose_name_plural = '營業稅檢查明細'
        ordering = ['vat_check', 'order']
    
    def __str__(self):
        return f"{self.vat_check.check_period} - {self.company_name}"


class BookkeepingChecklist(models.Model):
    """記帳進度檢查模型"""
    
    STATUS_CHOICES = [
        ('not_started', '尚未開始'),
        ('completed', '已完成'),
    ]
    
    # 基本資訊
    sequence_number = models.CharField(max_length=50, verbose_name='序號')
    check_period = models.CharField(max_length=50, verbose_name='檢查期別')
    company_id = models.CharField(max_length=8, verbose_name='統一編號')
    company_name = models.CharField(max_length=200, verbose_name='公司名稱')
    bookkeeper = models.CharField(max_length=100, verbose_name='記帳助理人員')
    industry_code = models.CharField(max_length=20, verbose_name='行業別代號')
    industry_name = models.CharField(max_length=200, verbose_name='行業別名稱')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='狀態')
    
    # 財務報表數據 - 收入
    revenue_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='收入帳列數')
    revenue_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='收入申報數')
    
    # 財務報表數據 - 成本
    cost_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='成本帳列數')
    cost_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='成本申報數')
    
    # 財務報表數據 - 毛利（自動計算）
    gross_profit_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='毛利帳列數')
    gross_profit_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='毛利申報數')
    
    # 財務報表數據 - 營業費用
    operating_expense_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='營業費用帳列數')
    operating_expense_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='營業費用申報數')
    
    # 財務報表數據 - 營業利益（自動計算）
    operating_profit_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='營業利益帳列數')
    operating_profit_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='營業利益申報數')
    
    # 財務報表數據 - 業外收入
    non_operating_income_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='業外收入帳列數')
    non_operating_income_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='業外收入申報數')
    
    # 財務報表數據 - 業外支出
    non_operating_expense_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='業外支出帳列數')
    non_operating_expense_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='業外支出申報數')
    
    # 財務報表數據 - 淨利（自動計算）
    net_profit_listed = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='淨利帳列數')
    net_profit_reported = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='淨利申報數')
    
    # 結論
    conclusion = models.TextField(blank=True, null=True, verbose_name='結論')
    
    # 系統欄位
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    class Meta:
        db_table = 'bookkeeping_checklist'
        verbose_name = '記帳進度檢查'
        verbose_name_plural = '記帳進度檢查'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.check_period} - {self.company_name}"
