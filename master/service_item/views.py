from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from master.models import ServiceItem
from .forms import ServiceItemForm

class ServiceItemListView(ListView):
    model = ServiceItem
    template_name = 'service_item/serviceitem_list.html'
    context_object_name = 'service_items'
    paginate_by = 20

class ServiceItemCreateView(CreateView):
    model = ServiceItem
    form_class = ServiceItemForm
    template_name = 'service_item/serviceitem_form.html'
    success_url = reverse_lazy('master:serviceitem_list')

class ServiceItemUpdateView(UpdateView):
    model = ServiceItem
    form_class = ServiceItemForm
    template_name = 'service_item/serviceitem_form.html'
    success_url = reverse_lazy('master:serviceitem_list')

class ServiceItemDeleteView(DeleteView):
    model = ServiceItem
    template_name = 'service_item/confirm_delete.html'
    success_url = reverse_lazy('master:serviceitem_list')
