from django import forms
from admin_module.models import CustomerChange


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
