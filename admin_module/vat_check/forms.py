from django import forms
from admin_module.models import VATCheck, VATCheckItem


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
