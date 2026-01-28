from django import forms
from registration.models import RegistrationAML

class RegistrationAMLForm(forms.ModelForm):
    class Meta:
        model = RegistrationAML
        fields = ['risk_level', 'notes']
        widgets = {
            'risk_level': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
