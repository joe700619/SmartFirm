from django import forms
from .models import BookingCustomer, TaxAuditRecord, TaxAuditHistory, VATRecord, IncomeTaxRecord, DownloadData
from admin_module.models import BasicInformation


class BookingCustomerForm(forms.ModelForm):
    """記帳客戶表單"""
    
    class Meta:
        model = BookingCustomer
        fields = [
            # 基本資料
            'company_name', 'company_id', 'tax_id', 'registration_address',
            'mailing_address', 'email', 'contact_person', 'phone', 'line_id',
            'business_password',
            # 承接資料
            'charge_status', 'charge_method', 'undertaking_status',
            # 營業人資料
            'industry_code', 'industry_name', 'business_type',
            'e_invoice_account', 'e_invoice_password',
            'invoice_purchase_method', 'invoice_delivery_method',
            'invoice_receive_method',
            # 發票數量
            'invoice_qty_2_copy', 'invoice_qty_2_副copy', 'invoice_qty_3_copy',
            'invoice_qty_3_副copy', 'invoice_qty_special', 'invoice_qty_2_cashier',
            'invoice_qty_3_cashier', 'invoice_qty_3_cashier_副',
            # 繳稅及通知
            'tax_payment', 'notification_method',
            # 記帳助理
            'bookkeeping_assistant', 'assistant_ratio', 'group_contact', 'contact_ratio',
            'reviewer', 'reviewer_ratio', 'business_registration', 'business_registration_ratio',
            # 其他
            'important_notes',
        ]
        widgets = {
            # 基本資料
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入公司名稱'
            }),
            'company_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入8位數統一編號',
                'maxlength': '8'
            }),
            'tax_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入稅籍編號'
            }),
            'registration_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '請輸入登記地址'
            }),
            'mailing_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '若未填寫，則與登記地址相同'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入Email'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入聯絡人'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入電話'
            }),
            'line_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入Line ID'
            }),
            'business_password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入營業人密碼'
            }),
            # 承接資料
            'charge_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'charge_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'undertaking_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            # 營業人資料
            'industry_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入行業代碼'
            }),
            'industry_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入行業名稱'
            }),
            'business_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'e_invoice_account': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入電子發票帳號'
            }),
            'e_invoice_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入電子發票密碼'
            }),
            'invoice_purchase_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'invoice_delivery_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'invoice_receive_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            # 發票數量
            'invoice_qty_2_copy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_2_副copy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_3_copy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_3_副copy': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_special': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_2_cashier': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_3_cashier': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'invoice_qty_3_cashier_副': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            # 繳稅及通知
            'tax_payment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notification_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            # 記帳助理
            'bookkeeping_assistant': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入記帳助理姓名'
            }),
            'assistant_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'group_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入集團窗口姓名'
            }),
            'contact_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'reviewer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入review人員姓名'
            }),
            'reviewer_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'business_registration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入工商人員姓名'
            }),
            'business_registration_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            # 其他
            'important_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入重要備註'
            }),
        }


class BookingCustomerFilterForm(forms.Form):
    """記帳客戶篩選表單"""
    
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '公司名稱'
        })
    )
    company_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '統一編號'
        })
    )
    contact_person = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '聯絡人'
        })
    )
    charge_status = forms.ChoiceField(
        required=False,
        choices=[('', '全部')] + BookingCustomer.CHARGE_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    undertaking_status = forms.ChoiceField(
        required=False,
        choices=[('', '全部')] + BookingCustomer.UNDERTAKING_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class TaxAuditRecordForm(forms.ModelForm):
    """國稅局查帳紀錄表單"""
    
    class Meta:
        model = TaxAuditRecord
        fields = [
            'customer', 'company_name', 'email',
            'year', 'tax_type', 'reason', 'letter_date', 'expected_reply_date',
            'progress', 'jurisdiction', 'jurisdiction_phone', 'handler',
            'handler_phone', 'handler_email', 'fax', 'summary', 'attachment'
        ]
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_customer'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': '從統編自動帶入'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': '從統編自動帶入'
            }),
            'year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如: 113'
            }),
            'tax_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'reason': forms.Select(attrs={
                'class': 'form-select'
            }),
            'letter_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expected_reply_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'progress': forms.Select(attrs={
                'class': 'form-select'
            }),
            'jurisdiction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入轄區'
            }),
            'jurisdiction_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入轄區電話'
            }),
            'handler': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入承辦人'
            }),
            'handler_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入承辦人電話'
            }),
            'handler_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入承辦人Email'
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入傳真號碼'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入摘要'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class TaxAuditHistoryForm(forms.ModelForm):
    """查帳歷程表單"""
    
    class Meta:
        model = TaxAuditHistory
        fields = ['contact_date', 'discussion_content', 'attachment']
        widgets = {
            'contact_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'discussion_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入討論內容'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class VATRecordForm(forms.ModelForm):
    """營業稅申報記錄表單"""
    
    class Meta:
        model = VATRecord
        fields = [
            'customer',
            'filing_year', 'filing_period', 'tax_payable', 'tax_deadline',
            'invoice_received_date', 'tax_payment_completed', 'source',
            'reply_time', 'declaration_url', 'payment_slip_url',
            # 新增稅額欄位
            'sales_amount', 'purchase_amount', 'credit_carryforward',
            'tax_payable_amount', 'tax_refund_amount',
            # 完成狀態
            'completion_status'
        ]
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_vat_customer'
            }),
            'filing_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如: 113',
                'maxlength': '4'
            }),
            'filing_period': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tax_payable': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tax_deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'invoice_received_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'tax_payment_completed': forms.Select(attrs={
                'class': 'form-select'
            }),
            'source': forms.Select(attrs={
                'class': 'form-select'
            }),
            'reply_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
            'declaration_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'payment_slip_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            # 稅額欄位 - 使用 TextInput 以支援千分位逗號
            'sales_amount': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'purchase_amount': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'credit_carryforward': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'tax_payable_amount': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'tax_refund_amount': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            # 完成狀態
            'completion_status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class VATRecordFilterForm(forms.Form):
    """營業稅申報記錄篩選表單"""
    
    bookkeeping_assistant = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '記帳助理'
        })
    )
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '公司名稱'
        })
    )
    company_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '統一編號'
        })
    )
    undertaking_status = forms.ChoiceField(
        required=False,
        choices=[('', '全部')] + BookingCustomer.UNDERTAKING_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    business_type = forms.ChoiceField(
        required=False,
        choices=[('', '全部')] + BookingCustomer.BUSINESS_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    tax_payment = forms.ChoiceField(
        required=False,
        choices=[('', '全部')] + BookingCustomer.TAX_PAYMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class IncomeTaxRecordForm(forms.ModelForm):
    """所得稅申報記錄表單"""
    
    class Meta:
        model = IncomeTaxRecord
        fields = [
            'customer', 'filing_year', 'important_notes',
            'provisional_payment', 'dividend_distribution',
            'receipt_number', 'filing_type',
            'tax_payable_col60', 'provisional_col62', 'withholding_col63',
            'land_building_col65', 'other_amount',
            'refund_or_payment', 'unallocated_surtax',
            'final_refund_or_payment', 'total_tax',
            'declaration_url', 'payment_slip_url',
            # Checklist fields
            'income_401_reconciliation', 'income_expense_match',
            'bad_debt_expense', 'entertainment_expense', 'employee_welfare',
            'undistributed_earnings_surtax', 'cost_statement',
            'provisional_withholding_deduction', 'land_transaction'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'filing_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '113'}),
            'important_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'provisional_payment': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric',
                'id': 'id_provisional_payment'
            }),
            'dividend_distribution': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'filing_type': forms.Select(attrs={'class': 'form-select'}),
            'tax_payable_col60': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'provisional_col62': forms.TextInput(attrs={
                'class': 'form-control amount-field',
                'placeholder': '0',
                'readonly': 'readonly',
                'inputmode': 'numeric'
            }),
            'withholding_col63': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'land_building_col65': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'other_amount': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'refund_or_payment': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-result',
                'placeholder': '0',
                'readonly': 'readonly',
                'inputmode': 'numeric'
            }),
            'unallocated_surtax': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-field',
                'placeholder': '0',
                'inputmode': 'numeric'
            }),
            'final_refund_or_payment': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-result',
                'placeholder': '0',
                'readonly': 'readonly',
                'inputmode': 'numeric'
            }),
            'total_tax': forms.TextInput(attrs={
                'class': 'form-control amount-field calc-result',
                'placeholder': '0',
                'readonly': 'readonly',
                'inputmode': 'numeric'
            }),
            'declaration_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/declaration.pdf'
            }),
            'payment_slip_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/payment_slip.pdf'
            }),
            # Checklist fields
            'income_401_reconciliation': forms.Select(attrs={'class': 'form-select'}),
            'income_expense_match': forms.Select(attrs={'class': 'form-select'}),
            'bad_debt_expense': forms.Select(attrs={'class': 'form-select'}),
            'entertainment_expense': forms.Select(attrs={'class': 'form-select'}),
            'employee_welfare': forms.Select(attrs={'class': 'form-select'}),
            'undistributed_earnings_surtax': forms.Select(attrs={'class': 'form-select'}),
            'cost_statement': forms.Select(attrs={'class': 'form-select'}),
            'provisional_withholding_deduction': forms.Select(attrs={'class': 'form-select'}),
            'land_transaction': forms.Select(attrs={'class': 'form-select'}),
        }


class DownloadDataForm(forms.ModelForm):
    """下載資料表單"""
    
    class Meta:
        model = DownloadData
        fields = [
            'file_number', 'year', 'period', 'category',
            'company_id', 'company_name', 'email',
            'invoice_received_date', 'payment_method', 'source',
            'reply_time', 'declaration_url', 'payment_slip_url',
            'tax_deadline', 'status'
        ]
        widgets = {
            'file_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '113'}),
            'period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01-02'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'company_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'invoice_received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'reply_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'declaration_url': forms.URLInput(attrs={'class': 'form-control'}),
            'payment_slip_url': forms.URLInput(attrs={'class': 'form-control'}),
            'tax_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
