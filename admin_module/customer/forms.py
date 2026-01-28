from django import forms
from admin_module.models import BasicInformation


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
            'room_id',
            'fax_number',
            'account_last_5',
            'registration_zip_code',
            'registration_address',
            'mailing_zip_code',
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
            'room_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room ID',
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
            'registration_zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '郵遞區號',
                'maxlength': '10',
            }),
            'registration_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '請輸入公司登記地址',
            }),
            'mailing_zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '郵遞區號',
                'maxlength': '10',
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
