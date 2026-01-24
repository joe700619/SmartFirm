"""
Customer (BasicInformation) Views

NOTE: This is a placeholder. The actual views from admin_module/views.py 
(lines 15-112) need to be copied here and adapted.

Views to migrate:
- customer_list
- customer_create
- customer_update
- customer_delete

Also include:
- api_customer_info
- search_companies_api
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from admin_module.models import BasicInformation
from .forms import BasicInformationForm, CustomerFilterForm


def list(request):
    """客戶列表頁面"""
    customers = BasicInformation.objects.filter(is_deleted=False)
    filter_form = CustomerFilterForm(request.GET or None)
    
    # 處理篩選
    if filter_form.is_valid():
        company_name = filter_form.cleaned_data.get('company_name')
        company_id = filter_form.cleaned_data.get('company_id')
        contact = filter_form.cleaned_data.get('contact')
        
        filters = Q()
        if company_name:
            filters &= Q(companyName__icontains=company_name)
        if company_id:
            filters &= Q(companyId__icontains=company_id)
        if contact:
            filters &= Q(contact__icontains=contact)
        
        if filters:
            customers = customers.filter(filters)
    
    # 分頁處理
    paginator = Paginator(customers, 50)
    page = request.GET.get('page')
    
    try:
        customers_page = paginator.page(page)
    except PageNotAnInteger:
        customers_page = paginator.page(1)
    except EmptyPage:
        customers_page = paginator.page(paginator.num_pages)
    
    context = {
        'customers': customers_page,
        'filter_form': filter_form,
        'paginator': paginator,
    }
    return render(request, 'admin_module/customer/list.html', context)


def create(request):
    """新增客戶"""
    if request.method == 'POST':
        form = BasicInformationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'客戶「{customer.companyName}」已成功新增！')
            return redirect('admin_module:customer:list')
    else:
        form = BasicInformationForm()
    
    context = {
        'form': form,
        'action': '新增客戶'
    }
    return render(request, 'admin_module/customer/form.html', context)


def update(request, pk):
    """編輯客戶"""
    customer = get_object_or_404(BasicInformation, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = BasicInformationForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'客戶「{customer.companyName}」已成功更新！')
            return redirect('admin_module:customer:list')
    else:
        form = BasicInformationForm(instance=customer)
    
    context = {
        'form': form,
        'action': '編輯客戶',
        'customer': customer
    }
    return render(request, 'admin_module/customer/form.html', context)


def delete(request, pk):
    """刪除客戶 (軟刪除)"""
    customer = get_object_or_404(BasicInformation, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        company_name = customer.companyName
        customer.is_deleted = True
        customer.save()
        messages.success(request, f'客戶「{company_name}」已成功刪除！')
        return redirect('admin_module:customer:list')
    
    context = {
        'customer': customer
    }
    return render(request, 'admin_module/customer/confirm_delete.html', context)
