from django import forms
from admin_module.models import Contact


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
