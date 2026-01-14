from django import forms
from .models import (BasicInformation, Contact, IncomingMail, IncomingMailItem, 
                     CustomerChange, VATCheck, VATCheckItem, BookkeepingChecklist)




class BasicInformationForm(forms.ModelForm):
    """客戶基本資料表單"""
    
    class Meta:
        model = BasicInformation
        fields = [
            'companyId',
            'companyName',
            'contact',
            'email',
            'phoneNumber',
            'phone',
            'LineId',
            'fax_number',
            'account_last_5',
            'registration_address',
            'mailing_address',
            'important_notes',
        ]
        widgets = {
            'companyId': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入8位數公司統編',
                'maxlength': '8',
            }),
            'companyName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入公司名稱',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入聯絡人姓名',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@company.com',
            }),
            'phoneNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：02-12345678',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：0912-345678',
            }),
            'LineId': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入 Line ID',
            }),
            'fax_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：02-87654321',
            }),
            'account_last_5': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入帳號後5碼',
                'maxlength': '5',
            }),
            'registration_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入公司登記地址',
            }),
            'mailing_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入通訊地址（若未填寫，則與登記地址相同）',
            }),
            'important_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入重要訊息或備註',
            }),
        }


class CustomerFilterForm(forms.Form):
    """客戶篩選表單"""
    company_name = forms.CharField(
        required=False,
        label='公司名稱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入公司名稱',
        })
    )
    company_id = forms.CharField(
        required=False,
        label='公司統編',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入公司統編',
        })
    )
    contact = forms.CharField(
        required=False,
        label='聯絡人',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入聯絡人姓名',
        })
    )


class ContactForm(forms.ModelForm):
    """聯絡人表單"""
    
    class Meta:
        model = Contact
        fields = [
            'company_name',
            'company_id',
            'name',
            'position',
            'email',
            'phone',
            'mobile',
            'fax',
            'address',
            'notes',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入公司名稱',
            }),
            'company_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入8位數統編',
                'maxlength': '8',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入聯絡人姓名',
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入職稱',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@company.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：02-12345678',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：0912-345678',
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例：02-87654321',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入通訊地址',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入備註',
            }),
        }


class ContactFilterForm(forms.Form):
    """聯絡人篩選表單"""
    email = forms.CharField(
        required=False,
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入 Email',
        })
    )
    company_name = forms.CharField(
        required=False,
        label='公司名稱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入公司名稱',
        })
    )
    name = forms.CharField(
        required=False,
        label='聯絡人姓名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入聯絡人姓名',
        })
    )


class IncomingMailForm(forms.ModelForm):
    """收文主記錄表單"""
    
    class Meta:
        model = IncomingMail
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class IncomingMailItemForm(forms.ModelForm):
    """收文明細記錄表單"""
    
    class Meta:
        model = IncomingMailItem
        fields = [
            'sender',
            'company',
            'customer_name',
            'content_type',
            'notify_customer',
            'message_content',
            'order',
        ]
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入寄件人',
            }),
            'company': forms.Select(attrs={
                'class': 'form-control company-select',
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control customer-name-field',
                'readonly': 'readonly',
            }),
            'content_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'notify_customer': forms.CheckboxInput(attrs={
                'class': 'form-check-input notify-checkbox',
            }),
            'message_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入傳送訊息內容',
            }),
            'order': forms.HiddenInput(),
        }


class CustomerChangeForm(forms.ModelForm):
    """客戶增減表單"""
    
    class Meta:
        model = CustomerChange
        fields = [
            'company_id',
            'company_name',
            'accounting_assistant',
            'overdue_days',
            'establishment_date',
            'change_type',
            'invoice_quantity',
            'id_copy',
            'lease_and_tax',
        ]
        widgets = {
            'company_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入8位數統一編號',
                'maxlength': '8',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入客戶名稱',
            }),
            'accounting_assistant': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入記帳助理人員',
            }),
            'overdue_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '請輸入逾期天數',
            }),
            'establishment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'change_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'invoice_quantity': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'id_copy': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'lease_and_tax': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class VATCheckForm(forms.ModelForm):
    """營業稅檢查主記錄表單"""
    
    class Meta:
        model = VATCheck
        fields = [
            'date',
            'check_period',
            'inspector',
            'inspectee',
            'status',
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'check_period': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：113年1-2月',
            }),
            'inspector': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入檢查人員',
            }),
            'inspectee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '請輸入受檢人員',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class VATCheckItemForm(forms.ModelForm):
    """營業稅檢查明細記錄表單"""
    
    class Meta:
        model = VATCheckItem
        fields = [
            'company_id',
            'company_name',
            'input_buyer',
            'check_input_amount',
            'input_duplicate',
            'output_e_invoice',
            'form401_output_amount',
            'form401_input_amount',
            'tax_credit_carried_forward',
            'tax_payable',
            'tax_refundable',
            'order',
        ]
        widgets = {
            'company_id': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '統編',
                'maxlength': '8',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '公司名稱',
            }),
            'input_buyer': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '買受人',
            }),
            'check_input_amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '進項金額',
                'step': '0.01',
            }),
            'input_duplicate': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '重複',
            }),
            'output_e_invoice': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '電子發票',
            }),
            'form401_output_amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '銷項',
                'step': '0.01',
            }),
            'form401_input_amount': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '進項',
                'step': '0.01',
            }),
            'tax_credit_carried_forward': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '留抵',
                'step': '0.01',
            }),
            'tax_payable': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '應納',
                'step': '0.01',
            }),
            'tax_refundable': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '應退',
                'step': '0.01',
            }),
            'order': forms.HiddenInput(),
        }


class VATCheckFilterForm(forms.Form):
    """營業稅檢查篩選表單"""
    check_period = forms.CharField(
        required=False,
        label='檢查期別',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入檢查期別',
        })
    )
    status = forms.ChoiceField(
        required=False,
        label='完成狀態',
        choices=[('', '全部')] + VATCheck.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    inspector = forms.CharField(
        required=False,
        label='檢查人員',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入檢查人員',
        })
    )


class BookkeepingChecklistForm(forms.ModelForm):
    """記帳進度檢查表單"""
    
    class Meta:
        model = BookkeepingChecklist
        fields = [
            'sequence_number', 'check_period', 'company_id', 'company_name',
            'bookkeeper', 'industry_code', 'industry_name', 'status',
            'revenue_listed', 'revenue_reported',
            'cost_listed', 'cost_reported',
            'gross_profit_listed', 'gross_profit_reported',
            'operating_expense_listed', 'operating_expense_reported',
            'operating_profit_listed', 'operating_profit_reported',
            'non_operating_income_listed', 'non_operating_income_reported',
            'non_operating_expense_listed', 'non_operating_expense_reported',
            'net_profit_listed', 'net_profit_reported',
            'conclusion'
        ]
        widgets = {
            'sequence_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '序號'}),
            'check_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如：113年1-2月'}),
            'company_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '統一編號', 'maxlength': '8'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '公司名稱'}),
            'bookkeeper': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '記帳助理人員'}),
            'industry_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '行業別代號'}),
            'industry_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '行業別名稱'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            
            # 金額欄位 - 添加 amount-field class 以支持千分位格式化
            'revenue_listed': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'revenue_reported': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'cost_listed': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'cost_reported': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'gross_profit_listed': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            'gross_profit_reported': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            'operating_expense_listed': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'operating_expense_reported': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'operating_profit_listed': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            'operating_profit_reported': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            'non_operating_income_listed': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'non_operating_income_reported': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'non_operating_expense_listed': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'non_operating_expense_reported': forms.TextInput(attrs={'class': 'form-control amount-field', 'placeholder': '0'}),
            'net_profit_listed': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            'net_profit_reported': forms.TextInput(attrs={'class': 'form-control amount-field calculated-field', 'placeholder': '0', 'readonly': 'readonly'}),
            
            'conclusion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '結論內容（目前空白）'}),
        }


class BookkeepingChecklistFilterForm(forms.Form):
    """記帳進度檢查篩選表單"""
    
    check_period = forms.CharField(
        required=False,
        label='檢查期別',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入檢查期別',
        })
    )
    status = forms.ChoiceField(
        required=False,
        label='狀態',
        choices=[('', '全部')] + BookkeepingChecklist.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    bookkeeper = forms.CharField(
        required=False,
        label='記帳助理',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入記帳助理人員',
        })
    )
