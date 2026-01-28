from django import forms
import json

class ModalSearchInput(forms.Widget):
    template_name = 'core/widgets/modal_search_input.html'

    class Media:
        css = {
            'all': (
                'https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.7.1.min.js',
            'https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js',
            'https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js',
        )

    def __init__(self, attrs=None, api_url='', modal_title='Search', 
                 display_field='name', value_field='id', related_fields=None, results_key='results', model=None):
        """
        api_url: URL to fetch search results.
        modal_title: Title shown in the modal header.
        display_field: JSON key from API result AND model attribute to show in the text input.
        value_field: JSON key from API result to allow form submission.
        related_fields: Dictionary mapping API response keys to other form field names for auto-fill.
                        Example: {'tax_id': 'tax_id', 'address': 'contact_address'}
        results_key: The key in the JSON response containing the list of items. Default 'results'.
        model: The Django Model class. Used to fetch the display value (name) for a given ID (value) upon initial render.
        """
        super().__init__(attrs)
        self.api_url = api_url
        self.modal_title = modal_title
        self.display_field = display_field
        self.value_field = value_field
        self.related_fields = related_fields or {}
        self.results_key = results_key
        self.model = model

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['api_url'] = self.api_url
        context['widget']['modal_title'] = self.modal_title
        context['widget']['display_field'] = self.display_field
        context['widget']['value_field'] = self.value_field
        context['widget']['related_fields'] = json.dumps(self.related_fields)
        context['widget']['results_key'] = self.results_key
        
        # Calculate Display Value for Server-Side Render
        display_val = ''
        if value and self.model:
            try:
                # Assuming value is the PK
                obj = self.model.objects.get(pk=value)
                # Get attribute dynamically, strict or fallback?
                display_val = getattr(obj, self.display_field, str(obj))
            except (self.model.DoesNotExist, ValueError, TypeError):
                # value might be invalid or None
                pass
        
        # Allow override from attrs if needed (e.g. invalid form post)
        if attrs and 'data-display-value' in attrs:
             display_val = attrs['data-display-value']
             
        context['widget']['display_value'] = display_val
        
        return context
