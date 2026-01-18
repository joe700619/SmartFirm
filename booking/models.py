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


class VATRecord(models.Model):
    """營業稅申報記錄模型"""
    
    # ==================== (1) 基本資料（來自客戶，不可編輯） ====================
    customer = models.ForeignKey(
        BookingCustomer,
        on_delete=models.PROTECT,
        verbose_name='客戶',
        help_text='選擇客戶以自動帶入基本資料'
    )
    
    # ==================== (2) 本期資料（可編輯） ====================
    FILING_PERIOD_CHOICES = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]
    
    filing_year = models.CharField(
        max_length=4,
        verbose_name='申報年度',
        help_text='例如: 113'
    )
    
    filing_period = models.CharField(
        max_length=2,
        choices=FILING_PERIOD_CHOICES,
        verbose_name='申報期別'
    )
    
    TAX_PAYABLE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    tax_payable = models.CharField(
        max_length=3,
        choices=TAX_PAYABLE_CHOICES,
        blank=True,
        null=True,
        verbose_name='是否繳稅'
    )
    
    tax_deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name='繳稅截止日'
    )
    
    invoice_received_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='收到發票日期'
    )
    
    TAX_PAYMENT_STATUS_CHOICES = [
        ('customer_paid', '客戶自己繳納'),
        ('office_paid', '事務所代繳'),
        ('not_replied', '還沒回覆'),
    ]
    
    tax_payment_completed = models.CharField(
        max_length=20,
        choices=TAX_PAYMENT_STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='繳稅完成否'
    )
    
    SOURCE_CHOICES = [
        ('google', 'Google'),
        ('manual', '自行輸入'),
        ('na', 'NA'),
    ]
    
    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True,
        verbose_name='來源'
    )
    
    reply_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='回覆時間'
    )
    
    # ==================== 稅額資料 ====================
    sales_amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='銷項金額',
        help_text='輸入整數金額'
    )
    
    purchase_amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='進項金額',
        help_text='輸入整數金額'
    )
    
    credit_carryforward = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='留底抵稅額',
        help_text='輸入整數金額'
    )
    
    tax_payable_amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='應納稅額',
        help_text='輸入整數金額'
    )
    
    tax_refund_amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='應退稅額',
        help_text='輸入整數金額'
    )
    
    # ==================== 完成狀態 ====================
    COMPLETION_STATUS_CHOICES = [
        ('completed', '已完成'),
        ('not_started', '尚未開始'),
    ]
    
    completion_status = models.CharField(
        max_length=20,
        choices=COMPLETION_STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='完成狀態'
    )
    
    declaration_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='申報書網址'
    )
    
    payment_slip_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='繳款書網址'
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
        db_table = 'vat_record'
        verbose_name = '營業稅申報記錄'
        verbose_name_plural = '營業稅申報記錄'
        ordering = ['-filing_year', '-filing_period', '-created_at']
        # 確保同一客戶的同一年度同一期別只有一筆記錄
        unique_together = [['customer', 'filing_year', 'filing_period']]
    
    def __str__(self):
        return f"{self.customer.company_name} - {self.filing_year}年{self.get_filing_period_display()}"


# ==================== 所得稅申報記錄模型 ====================

class IncomeTaxRecord(models.Model):
    """所得稅申報記錄"""
    
    # ==================== 申報類別選項 ====================
    FILING_TYPE_CHOICES = [
        ('book_review', '書審'),
        ('income_standard', '所標'),
        ('account_audit', '查帳'),
        ('accounting_sign', '會簽'),
        ('other', '其他'),
    ]
    
    # ==================== 客戶關聯 ====================
    customer = models.ForeignKey(
        BookingCustomer,
        on_delete=models.PROTECT,
        related_name='income_tax_records',
        verbose_name='客戶'
    )
    
    # ==================== 申報基本資訊 ====================
    filing_year = models.IntegerField(
        verbose_name='申報年度',
        help_text='例如：113'
    )
    
    important_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='重要提醒事項',
        help_text='顯示在表單頂部的重要提醒'
    )
    
    # ==================== 暫繳區塊 ====================
    provisional_payment = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='暫繳金額',
        help_text='輸入整數金額，此金額會自動填入本稅區塊的暫繳-62欄'
    )
    
    # ==================== 未分配區塊 ====================
    dividend_distribution = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='股利分配金額',
        help_text='輸入整數金額'
    )
    
    # ==================== 本稅區塊 ====================
    receipt_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='收件編號'
    )
    
    filing_type = models.CharField(
        max_length=20,
        choices=FILING_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='申報類別'
    )
    
    # 應納稅額-60欄 (c)
    tax_payable_col60 = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='應納稅額(60欄)',
        help_text='輸入整數金額'
    )
    
    # 暫繳-62欄 (d) - 自動從 provisional_payment 填入
    provisional_col62 = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='暫繳(62欄)',
        help_text='自動從暫繳金額填入，唯讀'
    )
    
    # 扣繳-63欄 (e)
    withholding_col63 = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='扣繳(63欄)',
        help_text='輸入整數金額'
    )
    
    # 房地合一-65欄 (f)
    land_building_col65 = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='房地合一(65欄)',
        help_text='輸入整數金額'
    )
    
    # 其他 (g)
    other_amount = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='其他',
        help_text='輸入整數金額'
    )
    
    # 補繳金額(64)應退(65) (h) - 自動計算：c - d - e + f - g
    refund_or_payment = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='補繳金額(64)應退(65)',
        help_text='自動計算：應納稅額 - 暫繳 - 扣繳 + 房地合一 - 其他'
    )
    
    # 未分加徵稅額 (i)
    unallocated_surtax = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='未分加徵稅額',
        help_text='輸入整數金額'
    )
    
    # 抵完後應補(退) (j) - 自動計算
    final_refund_or_payment = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='抵完後應補(退)',
        help_text='自動計算'
    )
    
    # 總計稅款 (k) - 自動計算
    total_tax = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='總計稅款',
        help_text='自動計算'
    )
    
    # ==================== 文件網址 ====================
    declaration_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='申報書網址',
        help_text='輸入申報書的完整網址'
    )
    
    payment_slip_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='繳款書網址',
        help_text='輸入繳款書的完整網址'
    )
    
    # ==================== 檢查清單 (Check List) ====================
    INCOME_401_CHOICES = [
        ('reconciled', '調節相符申報'),
        ('zero', '申報0'),
        ('not_applicable', '無此情形'),
    ]
    
    income_401_reconciliation = models.CharField(
        max_length=20,
        choices=INCOME_401_CHOICES,
        blank=True,
        null=True,
        verbose_name='收入與401調節相符'
    )
    
    INCOME_EXPENSE_CHOICES = [
        ('confirmed', '確認無誤'),
        ('no_tax_expense', '無所得稅費用'),
    ]
    
    income_expense_match = models.CharField(
        max_length=20,
        choices=INCOME_EXPENSE_CHOICES,
        blank=True,
        null=True,
        verbose_name='所得費用相符'
    )
    
    bad_debt_expense = models.CharField(
        max_length=20,
        choices=[('confirmed', '確認未超限')],
        blank=True,
        null=True,
        verbose_name='壞帳費用'
    )
    
    entertainment_expense = models.CharField(
        max_length=20,
        choices=[('confirmed', '確認未超限')],
        blank=True,
        null=True,
        verbose_name='交際費'
    )
    
    employee_welfare = models.CharField(
        max_length=20,
        choices=[('confirmed', '確認未超限')],
        blank=True,
        null=True,
        verbose_name='職工福利'
    )
    
    UNDISTRIBUTED_EARNINGS_CHOICES = [
        ('no_earnings', '沒有未分配盈餘'),
        ('surtax_correct', '加徵稅額計算無誤'),
    ]
    
    undistributed_earnings_surtax = models.CharField(
        max_length=20,
        choices=UNDISTRIBUTED_EARNINGS_CHOICES,
        blank=True,
        null=True,
        verbose_name='未分配盈餘加徵'
    )
    
    COST_STATEMENT_CHOICES = [
        ('matched', '成本表相符'),
        ('not_prepared', '無編制成本表'),
    ]
    
    cost_statement = models.CharField(
        max_length=20,
        choices=COST_STATEMENT_CHOICES,
        blank=True,
        null=True,
        verbose_name='成本表'
    )
    
    PROVISIONAL_WITHHOLDING_CHOICES = [
        ('deducted', '已扣除'),
        ('not_applicable', '無暫繳或扣繳'),
    ]
    
    provisional_withholding_deduction = models.CharField(
        max_length=20,
        choices=PROVISIONAL_WITHHOLDING_CHOICES,
        blank=True,
        null=True,
        verbose_name='暫繳及扣繳要扣除'
    )
    
    LAND_TRANSACTION_CHOICES = [
        ('c4_filled', 'C4表已填'),
        ('no_transaction', '無土地交易'),
    ]
    
    land_transaction = models.CharField(
        max_length=20,
        choices=LAND_TRANSACTION_CHOICES,
        blank=True,
        null=True,
        verbose_name='土地交易'
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
        db_table = 'income_tax_record'
        verbose_name = '所得稅申報記錄'
        verbose_name_plural = '所得稅申報記錄'
        ordering = ['-filing_year', '-created_at']
        # 確保同一客戶的同一年度只有一筆記錄
        unique_together = [['customer', 'filing_year']]
    
    def __str__(self):
        return f"{self.customer.company_name} - {self.filing_year}年所得稅"
    
    def save(self, *args, **kwargs):
        """儲存前自動同步暫繳金額到 provisional_col62"""
        if self.provisional_payment is not None:
            self.provisional_col62 = self.provisional_payment
        super().save(*args, **kwargs)


# ==================== 下載資料管理模型 ====================

class DownloadData(models.Model):
    """下載資料管理"""
    
    # ==================== 選項定義 ====================
    PAYMENT_METHOD_CHOICES = [
        ('customer', '客戶自己繳'),
        ('office', '事務所代繳'),
        ('no_reply', '還沒回覆'),
    ]
    
    SOURCE_CHOICES = [
        ('google', 'Google'),
        ('manual', '自行輸入'),
        ('na', 'NA'),
    ]
    
    STATUS_CHOICES = [
        ('current', '當期'),
        ('previous', '上期'),
    ]
    
    CATEGORY_CHOICES = [
        ('vat', '營業稅'),
        ('income_tax', '所得稅'),
        ('provisional', '暫繳'),
    ]
    
    # ==================== 資料欄位 ====================
    file_number = models.CharField(
        max_length=50,
        verbose_name='檔案編號',
        help_text='資料檔案編號'
    )
    
    year = models.IntegerField(
        verbose_name='年度',
        help_text='申報年度'
    )
    
    period = models.CharField(
        max_length=20,
        verbose_name='期別',
        help_text='申報期別'
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        verbose_name='種類',
        help_text='資料種類'
    )
    
    company_id = models.CharField(
        max_length=8,
        verbose_name='統一編號',
        help_text='公司統一編號'
    )
    
    company_name = models.CharField(
        max_length=200,
        verbose_name='公司名稱'
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    
    invoice_received_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='收到發票日期'
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name='繳稅方式'
    )
    
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True,
        verbose_name='來源'
    )
    
    reply_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='回覆時間'
    )
    
    declaration_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='申報書網址'
    )
    
    payment_slip_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='繳款書網址'
    )
    
    tax_deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name='繳稅截止日'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='current',
        verbose_name='狀態'
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
        db_table = 'download_data'
        verbose_name = '下載資料'
        verbose_name_plural = '下載資料'
        ordering = ['-year', '-period', '-created_at']
    
    def __str__(self):
        return f"{self.file_number} - {self.company_name} ({self.year}年{self.period})"
