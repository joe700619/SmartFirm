from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from registration.models import RegistrationProgress, RegistrationService, RegistrationCostSplit, RegistrationMandate, RegistrationAML
from .forms import RegistrationProgressForm, RegistrationServiceFormSet, RegistrationCostSplitFormSet
from registration.mandate.forms import RegistrationMandateForm
from registration.aml.forms import RegistrationAMLForm

class RegistrationProgressListView(LoginRequiredMixin, ListView):
    model = RegistrationProgress
    template_name = 'progress/list.html'
    context_object_name = 'cases'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class RegistrationProgressCreateView(LoginRequiredMixin, CreateView):
    model = RegistrationProgress
    form_class = RegistrationProgressForm
    template_name = 'progress/form.html'
    def get_success_url(self):
        return reverse_lazy('registration:progress:edit', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['services'] = RegistrationServiceFormSet(self.request.POST, prefix='services')
            data['cost_splits'] = RegistrationCostSplitFormSet(self.request.POST, prefix='cost_splits')
        else:
            data['services'] = RegistrationServiceFormSet(queryset=RegistrationService.objects.none(), prefix='services')
            data['cost_splits'] = RegistrationCostSplitFormSet(queryset=RegistrationCostSplit.objects.none(), prefix='cost_splits')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        services = context['services']
        cost_splits = context['cost_splits']
        if services.is_valid() and cost_splits.is_valid():
            with transaction.atomic():
                self.object = form.save()
                services.instance = self.object
                services.save()
                cost_splits.instance = self.object
                cost_splits.save()
            return super().form_valid(form)
        else:
            print("Services Formset Errors (Create):", services.errors)
            return self.render_to_response(self.get_context_data(form=form))

class RegistrationProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistrationProgress
    form_class = RegistrationProgressForm
    template_name = 'progress/form.html'
    
    def get_success_url(self):
        return reverse_lazy('registration:progress:edit', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['services'] = RegistrationServiceFormSet(self.request.POST, instance=self.object, prefix='services')
            data['cost_splits'] = RegistrationCostSplitFormSet(self.request.POST, instance=self.object, prefix='cost_splits')
        else:
            data['services'] = RegistrationServiceFormSet(
                instance=self.object,
                queryset=self.object.services.filter(is_deleted=False),
                prefix='services'
            )
            data['cost_splits'] = RegistrationCostSplitFormSet(
                instance=self.object,
                queryset=self.object.cost_splits.filter(is_deleted=False),
                prefix='cost_splits'
            )
        
        # Navigation logic (Prev/Next)
        cases = RegistrationProgress.objects.filter(is_deleted=False).order_by('-created_at')
        cases_list = list(cases.values_list('pk', flat=True))
        try:
            current_idx = cases_list.index(self.object.pk)
            # Previous (newer in time desc list)
            if current_idx > 0:
                data['previous_case'] = cases_list[current_idx - 1]
            # Next (older in time desc list)
            if current_idx < len(cases_list) - 1:
                data['next_case'] = cases_list[current_idx + 1]
        except ValueError:
            pass

        # Load Mandate Form
        mandate, _ = RegistrationMandate.objects.get_or_create(progress=self.object)
        data['mandate_form'] = RegistrationMandateForm(self.request.POST or None, instance=mandate, prefix='mandate')

        # Load AML Form
        aml, _ = RegistrationAML.objects.get_or_create(progress=self.object)
        data['aml_form'] = RegistrationAMLForm(self.request.POST or None, instance=aml, prefix='aml')
        
        # Check if AML is required based on Services
        is_aml_required = self.object.services.filter(service__is_aml_required=True).exists()
        data['is_aml_required'] = is_aml_required

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        services = context['services']
        cost_splits = context['cost_splits']
        mandate_form = context['mandate_form']
        aml_form = context['aml_form']
        
        # Check validity (AML is conditional, but here we init form always. 
        # If prefix data is missing, empty form might be valid if fields are optional? 
        # But we should only save if valid.
        # Actually, we should check if is_aml_required is true before validating/saving AML?
        # For simplicity, if form is posted with prefix, we save it.
        
        if services.is_valid() and cost_splits.is_valid() and mandate_form.is_valid() and aml_form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                services.save()
                cost_splits.save()
                mandate_form.save()
                aml_form.save()
            return super().form_valid(form)
        else:
            print("Services Formset Errors (Update):", services.errors)
            print("Cost Splits Formset Errors (Update):", cost_splits.errors)
            return self.render_to_response(self.get_context_data(form=form))

class RegistrationProgressDeleteView(LoginRequiredMixin, DeleteView):
    model = RegistrationProgress
    template_name = 'progress/confirm_delete.html'
    success_url = reverse_lazy('registration:progress:list')

# AJAX Views
from django.http import JsonResponse
from django.db import models # for Q objects
from admin_module.models import BasicInformation, Contact
from master.models import ServiceItem
from hr.models import Employee

def get_company_details(request):
    company_id = request.GET.get('id')
    data = {}
    if company_id:
        try:
            company = BasicInformation.objects.get(pk=company_id)
            data = {
                'tax_id': company.companyId,
            }
        except BasicInformation.DoesNotExist:
            pass
    return JsonResponse(data)

def get_contact_details(request):
    contact_id = request.GET.get('id')
    data = {}
    if contact_id:
        try:
            contact = Contact.objects.get(pk=contact_id)
            data = {
                'email': contact.email,
                'phone': contact.phone,
                'mobile': contact.mobile,
                'address': contact.address,
            }
        except Contact.DoesNotExist:
            pass
    return JsonResponse(data)

def get_service_details(request):
    service_id = request.GET.get('id')
    data = {}
    if service_id:
        try:
            service = ServiceItem.objects.get(pk=service_id)
            data = {
                'service_name': service.service_name,
                'service_item': service.remarks, 
                'fee': service.reference_price,
            }
        except ServiceItem.DoesNotExist:
            pass
    return JsonResponse(data)

def search_services(request):
    """API: Search Service Items"""
    term = request.GET.get('q', '')
    if len(term) < 1:
        return JsonResponse({'config': {}, 'data': []})
    
    services = ServiceItem.objects.filter(
        models.Q(service_code__icontains=term) |
        models.Q(service_name__icontains=term)
    )[:20]
    
    results = []
    for s in services:
        results.append({
            'id': s.id,
            'code': s.service_code,
            'name': s.service_name,
            'price': s.reference_price,
            'remarks': s.remarks or ''
        })
        
    response_data = {
        'config': {
            'value_field': 'id',
            'display_field': 'code', # Service uses code as display in the input usually, or name? Let's check form usage.
                                     # Looking at form: display_field='code' was set in RegistrationServiceForm.
            'columns': [
                {'title': '服務代碼', 'data': 'code'},
                {'title': '服務名稱', 'data': 'name'},
                {'title': '參考價格', 'data': 'price'},
            ]
        },
        'data': results
    }
    return JsonResponse(response_data)

def search_contacts(request):
    """API: Search Contacts"""
    term = request.GET.get('q', '')
    if len(term) < 1:
        return JsonResponse({'config': {}, 'data': []})
    
    contacts = Contact.objects.filter(
        models.Q(name__icontains=term) |
        models.Q(email__icontains=term) | 
        models.Q(phone__icontains=term)
    )[:20]
    
    results = []
    for c in contacts:
        results.append({
            'id': c.id,
            'name': c.name,
            'email': c.email or '',
            'phone': c.phone or '',
            'mobile': c.mobile or '',
            'address': c.address or '',
        })
        
    response_data = {
        'config': {
            'value_field': 'id',
            'display_field': 'name',
            'columns': [
                {'title': '姓名', 'data': 'name'},
                {'title': '電話', 'data': 'phone'},
                {'title': 'Email', 'data': 'email'},
            ]
        },
        'data': results
    }
    return JsonResponse(response_data)

def search_employees(request):
    """API: Search Employees"""
    term = request.GET.get('q', '')
    if len(term) < 1:
        return JsonResponse({'config': {}, 'data': []})
    
    employees = Employee.objects.filter(
        models.Q(name__icontains=term) |
        models.Q(employee_id__icontains=term)
    )[:20]
    
    results = []
    for e in employees:
        results.append({
            'id': e.id, # Using ID as value
            'name': e.name,
            'emp_id': e.employee_id,
            'job_title': e.get_job_title_display(),
        })
        
    response_data = {
        'config': {
            'value_field': 'id',
            'display_field': 'name',
            'columns': [
                {'title': '姓名', 'data': 'name'},
                {'title': '員工編號', 'data': 'emp_id'},
                {'title': '職稱', 'data': 'job_title'},
            ]
        },
        'data': results
    }
    return JsonResponse(response_data)

# Knowledge Note Creation
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from master.models import KnowledgeNote

@login_required
@require_POST
def create_knowledge_note(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        tags = data.get('tags')
        checklist = data.get('checklist')
        steps = data.get('steps')
        warnings = data.get('warnings')
        
        if not title:
            return JsonResponse({'success': False, 'message': '標題為必填項目'}, status=400)
            
        note = KnowledgeNote.objects.create(
            title=title,
            tags=tags,
            checklist=checklist,
            steps=steps,
            warnings=warnings
        )
        return JsonResponse({'success': True, 'message': '成功加入知識庫', 'id': note.id})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
