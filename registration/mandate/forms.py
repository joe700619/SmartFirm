from django import forms
from registration.models import RegistrationMandate

class RegistrationMandateForm(forms.ModelForm):
    class Meta:
        model = RegistrationMandate
        fields = ['mandate_date', 'remarks', 'is_drafting_agreed', 'is_seal_authorized', 'delivery_method', 'address']
        widgets = {
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_drafting_agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_seal_authorized': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_method'].required = True
        self.fields['address'].required = True
        self.fields['delivery_method'].choices = [('', '---------')] + list(RegistrationMandate.DELIVERY_CHOICES)
