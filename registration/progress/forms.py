"""
案件進度管理表單
"""
from django import forms


class CaseStatusUpdateForm(forms.Form):
    """案件狀態更新表單"""
    
    STATUS_CHOICES = [
        ('pending', '待處理'),
        ('processing', '處理中'),
        ('review', '審核中'),
        ('approved', '已核准'),
        ('rejected', '已駁回'),
        ('completed', '已完成'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='案件狀態',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    note = forms.CharField(
        required=False,
        label='備註',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '請輸入狀態更新說明'
        })
    )
