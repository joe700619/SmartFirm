from django import forms
from .models import BookingCustomer, TaxAuditRecord, TaxAuditHistory


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
            # 繳稅及通知
            'tax_payment', 'notification_method',
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
            # 繳稅及通知
            'tax_payment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notification_method': forms.Select(attrs={
                'class': 'form-select'
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

