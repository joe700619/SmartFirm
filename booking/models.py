from django.db import models


class BookingCustomer(models.Model):
    """記帳客戶資料模型"""
    
    # ==================== (1) 基本資料 ====================
    company_name = models.CharField(
        max_length=200,
        verbose_name='公司名稱'
    )
    company_id = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='統一編號',
        help_text='請輸入8位數統一編號'
    )
    tax_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='稅籍編號'
    )
    registration_address = models.TextField(
        verbose_name='登記地址'
    )
    mailing_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='通訊地址'
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='Email'
    )
    contact_person = models.CharField(
        max_length=100,
        verbose_name='聯絡人'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='電話'
    )
    line_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Line ID'
    )
    business_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='營業人密碼'
    )
    
    # ==================== (2) 承接資料 ====================
    CHARGE_STATUS_CHOICES = [
        ('charging', '收費中'),
        ('not_charging', '未收費'),
    ]
    charge_status = models.CharField(
        max_length=20,
        choices=CHARGE_STATUS_CHOICES,
        default='charging',
        verbose_name='收費狀態'
    )
    
    CHARGE_METHOD_CHOICES = [
        ('annual', '年繳'),
        ('prepaid', '預繳'),
        ('monthly', '月繳'),
        ('auto_debit', '自動扣繳'),
        ('semi_annual', '半年繳'),
    ]
    charge_method = models.CharField(
        max_length=20,
        choices=CHARGE_METHOD_CHOICES,
        default='annual',
        verbose_name='收費方式'
    )
    
    UNDERTAKING_STATUS_CHOICES = [
        ('undertaking', '承接中'),
        ('suspended', '停業'),
        ('transferred_out', '轉出'),
        ('dissolved', '解散'),
        ('pending_transfer_out', '待轉出'),
        ('pending_transfer_in', '待轉入'),
    ]
    undertaking_status = models.CharField(
        max_length=30,
        choices=UNDERTAKING_STATUS_CHOICES,
        default='undertaking',
        verbose_name='承接狀態'
    )
    
    # ==================== (3) 營業人資料 ====================
    industry_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='行業代碼'
    )
    industry_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='行業名稱'
    )
    
    BUSINESS_TYPE_CHOICES = [
        ('exclusive', '專營營業人'),
        ('concurrent_direct', '兼營(直扣)'),
        ('concurrent_proportion', '兼營(比例)'),
        ('professional_investment', '專業投資'),
        ('non_business', '非營業人'),
    ]
    business_type = models.CharField(
        max_length=30,
        choices=BUSINESS_TYPE_CHOICES,
        default='exclusive',
        verbose_name='營業人類型'
    )
    
    e_invoice_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='電子發票帳號'
    )
    e_invoice_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='電子發票密碼'
    )
    
    INVOICE_PURCHASE_METHOD_CHOICES = [
        ('unified_purchase', '統購'),
        ('customer_purchase', '客戶自己買'),
        ('no_purchase', '沒買'),
    ]
    invoice_purchase_method = models.CharField(
        max_length=30,
        choices=INVOICE_PURCHASE_METHOD_CHOICES,
        default='unified_purchase',
        verbose_name='買發票方式'
    )
    
    INVOICE_DELIVERY_METHOD_CHOICES = [
        ('mail', '郵寄'),
        ('office_keep', '事務所保留'),
        ('no_purchase', '沒買'),
    ]
    invoice_delivery_method = models.CharField(
        max_length=30,
        choices=INVOICE_DELIVERY_METHOD_CHOICES,
        default='mail',
        verbose_name='送發票方式'
    )
    
    INVOICE_RECEIVE_METHOD_CHOICES = [
        ('seven_eleven', '7-11便利待'),
        ('self_collect', '親收'),
        ('customer_send', '客戶送來'),
    ]
    invoice_receive_method = models.CharField(
        max_length=30,
        choices=INVOICE_RECEIVE_METHOD_CHOICES,
        default='seven_eleven',
        verbose_name='收發票方式'
    )
    
    # ==================== (4) 繳稅及通知 ====================
    TAX_PAYMENT_CHOICES = [
        ('self_pay', '自繳'),
        ('agent_pay', '代繳'),
        ('not_replied', '尚未回覆'),
        ('auto_debit', '自動扣款'),
    ]
    tax_payment = models.CharField(
        max_length=20,
        choices=TAX_PAYMENT_CHOICES,
        blank=True,
        null=True,
        verbose_name='繳稅'
    )
    
    NOTIFICATION_METHOD_CHOICES = [
        ('email', 'Email'),
        ('line', 'Line'),
        ('both', 'Both'),
    ]
    notification_method = models.CharField(
        max_length=20,
        choices=NOTIFICATION_METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name='通知方式'
    )
    
    # ==================== 發票數量（當買發票方式為"統購"時使用） ====================
    invoice_qty_2_copy = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='二聯'
    )
    invoice_qty_2_副copy = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='二聯副'
    )
    invoice_qty_3_copy = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='三聯'
    )
    invoice_qty_3_副copy = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='三聯副'
    )
    invoice_qty_special = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='特種'
    )
    invoice_qty_2_cashier = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='二收銀'
    )
    invoice_qty_3_cashier = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='三收銀'
    )
    invoice_qty_3_cashier_副 = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='三收銀副'
    )
    
    # ==================== (6) 記帳助理 ====================
    bookkeeping_assistant = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='記帳助理'
    )
    assistant_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='助理比例',
        help_text='請輸入0-100之間的數字'
    )
    group_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='集團窗口'
    )
    contact_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='窗口比例',
        help_text='請輸入0-100之間的數字'
    )
    reviewer = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='review人員'
    )
    reviewer_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='review比例',
        help_text='請輸入0-100之間的數字'
    )
    business_registration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='工商'
    )
    business_registration_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='工商比例',
        help_text='請輸入0-100之間的數字'
    )
    
    # ==================== (7) 其他 ====================
    important_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='重要備註'
    )
    
    # ==================== 系統欄位 ====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )
    
    class Meta:
        db_table = 'booking_customer'
        verbose_name = '記帳客戶'
        verbose_name_plural = '記帳客戶'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} ({self.company_id})"
    
    def save(self, *args, **kwargs):
        """如果未填寫通訊地址，則使用登記地址"""
        if not self.mailing_address:
            self.mailing_address = self.registration_address
        super().save(*args, **kwargs)


class TaxAuditRecord(models.Model):
    """國稅局查帳紀錄模型"""
    
    # ==================== (1) 基本資料 ====================
    customer = models.ForeignKey(
        BookingCustomer,
        on_delete=models.PROTECT,
        verbose_name='客戶',
        help_text='選擇客戶以自動帶入公司名稱和Email'
    )
    company_name = models.CharField(
        max_length=200,
        verbose_name='公司名稱',
        help_text='從客戶資料自動帶入'
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='Email',
        help_text='從客戶資料自動帶入'
    )
    
    # ==================== (2) 查帳紀錄 ====================
    year = models.CharField(
        max_length=4,
        verbose_name='年度'
    )
    
    TAX_TYPE_CHOICES = [
        ('vat', '營業稅'),
        ('income', '所得稅'),
        ('stamp', '印花稅'),
        ('personal_income', '個人綜所'),
        ('other', '其他'),
    ]
    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPE_CHOICES,
        verbose_name='稅種'
    )
    
    REASON_CHOICES = [
        ('audit', '查帳'),
        ('correction', '更正'),
    ]
    reason = models.CharField(
        max_length=20,
        choices=REASON_CHOICES,
        verbose_name='原因'
    )
    
    letter_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='來函/送件日期'
    )
    
    expected_reply_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='預計回覆日期'
    )
    
    PROGRESS_CHOICES = [
        ('discussing', '討論中'),
        ('closed', '結案'),
    ]
    progress = models.CharField(
        max_length=20,
        choices=PROGRESS_CHOICES,
        default='discussing',
        verbose_name='進度'
    )
    
    jurisdiction = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='轄區'
    )
    
    jurisdiction_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='轄區電話'
    )
    
    handler = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='承辦人'
    )
    
    handler_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='承辦人電話'
    )
    
    handler_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='承辦人Email'
    )
    
    fax = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='傳真'
    )
    
    summary = models.TextField(
        blank=True,
        null=True,
        verbose_name='摘要'
    )
    
    attachment = models.FileField(
        upload_to='tax_audit_records/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='上傳檔案'
    )
    
    # ==================== 系統欄位 ====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新時間'
    )
    
    class Meta:
        db_table = 'tax_audit_record'
        verbose_name = '國稅局查帳紀錄'
        verbose_name_plural = '國稅局查帳紀錄'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.year}年 - {self.get_tax_type_display()}"


class TaxAuditHistory(models.Model):
    """查帳紀錄歷程（子表）"""
    
    audit_record = models.ForeignKey(
        TaxAuditRecord,
        on_delete=models.CASCADE,
        related_name='histories',
        verbose_name='查帳紀錄'
    )
    
    contact_date = models.DateField(
        verbose_name='聯絡日期'
    )
    
    discussion_content = models.TextField(
        verbose_name='討論內容'
    )
    
    attachment = models.FileField(
        upload_to='tax_audit_histories/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='上傳附件'
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
        db_table = 'tax_audit_history'
        verbose_name = '查帳歷程'
        verbose_name_plural = '查帳歷程'
        ordering = ['audit_record', 'contact_date', 'order']
    
    def __str__(self):
        return f"{self.audit_record.company_name} - {self.contact_date}"

