from django import forms
from admin_module.models import BookkeepingChecklist


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
