from django import forms
from master.models import SystemParameter

class SystemParameterForm(forms.ModelForm):
    class Meta:
        model = SystemParameter
        fields = '__all__'
        widgets = {
            'gemini_api_key': forms.PasswordInput(render_value=True),
            'line_access_token': forms.PasswordInput(render_value=True),
            'ecpay_hash_key': forms.PasswordInput(render_value=True),
            'ecpay_hash_iv': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add form-control class to all fields
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} form-control'.strip()
            
            # Special handling for checkboxes if needed, though form-control usually fine
            # If using custom checkbox style from AdminLTE, might need 'custom-control-input'
