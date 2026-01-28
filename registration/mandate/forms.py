from django import forms
from registration.models import RegistrationMandate

class RegistrationMandateForm(forms.ModelForm):
    class Meta:
        model = RegistrationMandate
        fields = ['mandate_date', 'remarks']
        widgets = {
            'mandate_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
