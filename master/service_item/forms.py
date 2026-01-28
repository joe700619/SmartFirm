from django import forms
from master.models import ServiceItem

class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = ['service_code', 'service_name', 'reference_price', 'department', 'is_aml_required', 'remarks']
        widgets = {
            'service_code': forms.TextInput(attrs={'class': 'form-control'}),
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'is_aml_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
