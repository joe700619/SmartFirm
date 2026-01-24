from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from hr.models import Employee
from .forms import EmployeeForm

class EmployeeListView(ListView):
    model = Employee
    template_name = 'hr/employee/list.html'
    context_object_name = 'employees'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        status = self.request.GET.get('status', 'active')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'active')
        return context

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/employee/form.html'
    success_url = reverse_lazy('hr:employee_list')
    
    def form_valid(self, form):
        messages.success(self.request, '員工資料已成功建立')
        return super().form_valid(form)

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/employee/form.html'
    success_url = reverse_lazy('hr:employee_list')

    def form_valid(self, form):
        messages.success(self.request, '員工資料已成功更新')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all employees ordered by employee_id as per model Meta
        employees = list(Employee.objects.filter(is_deleted=False).values_list('pk', flat=True))
        current_pk = self.object.pk
        try:
            index = employees.index(current_pk)
            previous_pk = employees[index - 1] if index > 0 else None
            next_pk = employees[index + 1] if index < len(employees) - 1 else None
        except ValueError:
            previous_pk = None
            next_pk = None
        
        context['previous_pk'] = previous_pk
        context['next_pk'] = next_pk
        return context

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'hr/employee/confirm_delete.html'
    success_url = reverse_lazy('hr:employee_list')
    context_object_name = 'employee'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        messages.success(self.request, '員工資料已刪除')
        # Fix: Use HttpResponseRedirect instead of returning proxy object directly
        return HttpResponseRedirect(self.success_url)
    
    # Override post to handle soft delete (DeleteView calls delete() inside post())
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
