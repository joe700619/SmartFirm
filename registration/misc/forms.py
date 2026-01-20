"""
雜項功能表單
"""
from django import forms


class NamePreCheckForm(forms.Form):
    """公司名稱預查表單"""
    
    company_name = forms.CharField(
        max_length=100,
        label='公司名稱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入擬查詢之公司名稱'
        })
    )
    
    company_type = forms.ChoiceField(
        choices=[
            ('limited', '有限公司'),
            ('stock', '股份有限公司'),
        ],
        label='公司類型',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SealRegistrationForm(forms.Form):
    """印鑑登記表單"""
    
    seal_type = forms.ChoiceField(
        choices=[
            ('company', '公司印鑑'),
            ('representative', '代表人印鑑'),
        ],
        label='印鑑類型',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    seal_image = forms.ImageField(
        label='印鑑圖檔',
        help_text='請上傳清晰的印鑑圖檔',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
