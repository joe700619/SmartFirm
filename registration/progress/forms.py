from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from hr.models import Employee
from registration.models import RegistrationProgress, RegistrationService, RegistrationCostSplit

# ... (RegistrationProgressForm logic omitted, ensure it's kept or re-added if not scoped correctly by tool. 
# Tool replaces range, so I must include everything I replace.)

# Wait, tool replaces a chunk. I should just append if possible, but replace_file_content replaces a block.
# Let's replace the import section first and then append the new form at the end.
# Actually, I can do it in one go if I'm careful or multiple calls.
# I will use multi_replace for safer discrete edits.

from core.widgets import ModalSearchInput
from admin_module.models import BasicInformation, Contact
from master.models import ServiceItem

class RegistrationProgressForm(forms.ModelForm):
    class Meta:
        model = RegistrationProgress
        fields = [
            'mandate_status', 'status', 'case_type', 'delivery_method', # Block 1
            'customer', 'tax_id', 'line_id', 'room_id', 'acceptance_date', 'due_date',
            'main_contact', 'contact_email', 'contact_phone', 'contact_mobile', 'contact_address',
            'remarks' # Block 2
        ]
        widgets = {
            # Block 1
            'mandate_status': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            
            'case_type': forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'case-type-multiselect'}),
            
            # Block 2
            'customer': ModalSearchInput(
                api_url=reverse_lazy('booking:search_customers'),
                modal_title='搜尋客戶',
                display_field='companyName',
                value_field='id',
                results_key='data',
                related_fields={
                    'unified_business_number': 'tax_id',
                    'line_id': 'line_id',
                    'room_id': 'room_id'
                },
                model=BasicInformation
            ),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'line_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'room_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'acceptance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            
            'main_contact': ModalSearchInput(
                api_url=reverse_lazy('registration:progress:api_search_contacts'),
                modal_title='搜尋聯絡人',
                display_field='name',
                value_field='id',
                results_key='data',
                related_fields={
                    'email': 'contact_email',
                    'phone': 'contact_phone',
                    'mobile': 'contact_mobile',
                    'address': 'contact_address'
                },
                model=Contact
            ),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_address': forms.TextInput(attrs={'class': 'form-control'}),
            
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RegistrationServiceForm(forms.ModelForm):
    fee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control currency-input', 'style': 'text-align: right;'}))

    class Meta:
        model = RegistrationService
        fields = ['service', 'service_name', 'service_item', 'fee', 'remarks']
        widgets = {
            'service': ModalSearchInput(
                api_url=reverse_lazy('registration:progress:api_search_services'),
                modal_title='搜尋服務',
                display_field='service_code', 
                value_field='id',
                results_key='data',
                related_fields={
                    'name': 'service_name',
                    'remarks': 'service_item',
                    'price': 'fee'
                },
                model=ServiceItem
            ),
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'service_item': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee:
            if isinstance(fee, str):
                fee = fee.replace(',', '')
                try:
                    return int(float(fee))
                except ValueError:
                    raise forms.ValidationError('請輸入有效的數字')
        return 0


RegistrationServiceFormSet = inlineformset_factory(
    RegistrationProgress,
    RegistrationService,
    form=RegistrationServiceForm,
    extra=0,
    can_delete=True
)

class RegistrationCostSplitForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control currency-input bg-light', 'style': 'text-align: right;', 'readonly': 'readonly'}), required=False)

    class Meta:
        model = RegistrationCostSplit
        fields = ['assistant', 'ratio', 'amount']
        widgets = {
            'assistant': ModalSearchInput(
                api_url=reverse_lazy('registration:progress:api_search_employees'),
                modal_title='搜尋員工',
                display_field='name',
                value_field='id',
                results_key='data',
                model=Employee
            ),
            'ratio': forms.TextInput(attrs={'class': 'form-control percentage-input', 'style': 'text-align: right;'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount:
            if isinstance(amount, str):
                amount = amount.replace(',', '')
                try:
                    return int(float(amount))
                except ValueError:
                     return 0
        return 0

RegistrationCostSplitFormSet = inlineformset_factory(
    RegistrationProgress,
    RegistrationCostSplit,
    form=RegistrationCostSplitForm,
    extra=0,
    can_delete=True
)
