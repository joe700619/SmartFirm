from django import forms
from admin_module.models import IncomingMail, IncomingMailItem, BasicInformation


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
