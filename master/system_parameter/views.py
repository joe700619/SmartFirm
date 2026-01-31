from django.views.generic.edit import UpdateView
from django.contrib import messages
from master.models import SystemParameter
from .forms import SystemParameterForm

class SystemParameterUpdateView(UpdateView):
    model = SystemParameter
    form_class = SystemParameterForm
    template_name = 'master/system_parameter_form.html'

    def get_object(self, queryset=None):
        return SystemParameter.load()

    def get_success_url(self):
        messages.success(self.request, '系統參數已更新')
        return self.request.path
