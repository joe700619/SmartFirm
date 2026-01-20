"""
股東管理表單
"""
from django import forms
from registration.models import Shareholder, StockTransaction, CompanyShareholding
from admin_module.models import BasicInformation


class ShareholderForm(forms.ModelForm):
    """股東基本資料表單"""
    
    class Meta:
        model = Shareholder
        fields = ['identifier', 'name', 'phone', 'email', 'address']
        widgets = {
            'identifier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '身分證字號或統一編號',
                'maxlength': 20
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '股東姓名',
                'maxlength': 100
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '聯絡電話',
                'maxlength': 20
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '地址',
                'maxlength': 255
            }),
        }
        labels = {
            'identifier': '身分證字號/統一編號',
            'name': '股東姓名',
            'phone': '聯絡電話',
            'email': 'Email',
            'address': '地址',
        }
    
    def clean_identifier(self):
        """驗證身分證字號/統一編號格式"""
        identifier = self.cleaned_data.get('identifier')
        
        if not identifier:
            raise forms.ValidationError('身分證字號/統一編號為必填欄位')
        
        # 移除空白
        identifier = identifier.strip().upper()
        
        # 基本長度檢查
        if len(identifier) < 8:
            raise forms.ValidationError('身分證字號/統一編號長度不正確')
        
        # TODO: 可以加入更詳細的身分證或統編格式驗證
        
        return identifier
    
    def clean_name(self):
        """驗證姓名"""
        name = self.cleaned_data.get('name')
        
        if not name:
            raise forms.ValidationError('股東姓名為必填欄位')
        
        name = name.strip()
        
        if len(name) < 2:
            raise forms.ValidationError('姓名長度至少2個字元')
        
        return name


class StockTransactionForm(forms.ModelForm):
    """股權交易表單"""
    
    # 自定義欄位：公司選擇
    company = forms.ModelChoiceField(
        queryset=BasicInformation.objects.all(),
        label='公司',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control company-select'})
    )
    
    # 自定義欄位：股東選擇
    shareholder = forms.ModelChoiceField(
        queryset=Shareholder.objects.all(),
        label='股東',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control shareholder-select'})
    )
    
    # 身分證字號（只讀展示欄位）
    identifier_display = forms.CharField(
        label='身分證字號',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'id': 'identifier_display'
        })
    )
    
    class Meta:
        model = StockTransaction
        fields = [
            'transaction_date', 'description', 'transaction_type',
            'stock_type', 'par_value', 'quantity', 'stock_amount',
            'amount', 'note'
        ]
        widgets = {
            'transaction_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '交易說明'
            }),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'stock_type': forms.Select(attrs={'class': 'form-control'}),
            'par_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1'
            }),
            'stock_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'readonly': 'readonly'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '備註'
            }),
        }
        labels = {
            'transaction_date': '交易日期',
            'description': '交易說明',
            'transaction_type': '交易類型',
            'stock_type': '股票類型',
            'par_value': '每股面額',
            'quantity': '股數',
            'stock_amount': '股票金額',
            'amount': '交易金額',
            'note': '備註',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果是編輯現有交易，填入公司和股東
        if self.instance and self.instance.pk:
            self.fields['company'].initial = self.instance.company_holding.company
            self.fields['shareholder'].initial = self.instance.company_holding.shareholder
            self.fields['identifier_display'].initial = self.instance.company_holding.shareholder.identifier
