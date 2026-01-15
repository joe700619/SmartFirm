from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import BookingCustomer, TaxAuditRecord, TaxAuditHistory
from .forms import BookingCustomerForm, BookingCustomerFilterForm, TaxAuditRecordForm, TaxAuditHistoryForm
from admin_module.models import BasicInformation


def search_customers(request):
    """搜尋客戶API（從管理系統的BasicInformation）"""
    search_term = request.GET.get('q', '')
    
    if not search_term or len(search_term) < 1:
        return JsonResponse({'customers': []})
    
    # 搜尋公司名稱或統一編號（使用正確的欄位名稱）
    customers = BasicInformation.objects.filter(
        Q(companyName__icontains=search_term) | 
        Q(companyId__icontains=search_term)
    )[:20]  # 限制最多返回20筆結果
    
    results = []
    for customer in customers:
        results.append({
            'id': customer.id,
            'company_name': customer.companyName,
            'unified_business_number': customer.companyId or '',
            'tax_id_number': '',  # BasicInformation沒有稅籍編號欄位
            'registration_address': customer.registration_address or '',
            'contact_person': customer.contact or '',
            'phone': customer.phone or customer.phoneNumber or '',
            'email': customer.email or '',
        })
    
    return JsonResponse({'customers': results})


def customer_list(request):
    """客戶列表視圖"""
    # 獲取篩選條件
    filter_form = BookingCustomerFilterForm(request.GET)
    
    # 查詢所有客戶
    customers = BookingCustomer.objects.all()
    
    # 應用篩選條件
    if filter_form.is_valid():
        company_name = filter_form.cleaned_data.get('company_name')
        company_id = filter_form.cleaned_data.get('company_id')
        contact_person = filter_form.cleaned_data.get('contact_person')
        charge_status = filter_form.cleaned_data.get('charge_status')
        undertaking_status = filter_form.cleaned_data.get('undertaking_status')
        
        if company_name:
            customers = customers.filter(company_name__icontains=company_name)
        if company_id:
            customers = customers.filter(company_id__icontains=company_id)
        if contact_person:
            customers = customers.filter(contact_person__icontains=contact_person)
        if charge_status:
            customers = customers.filter(charge_status=charge_status)
        if undertaking_status:
            customers = customers.filter(undertaking_status=undertaking_status)
    
    # 分頁
    paginator = Paginator(customers, 20)  # 每頁20筆
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'filter_form': filter_form,
        'paginator': paginator,
    }
    return render(request, 'booking/customer_list.html', context)


def customer_create(request):
    """新增客戶視圖"""
    if request.method == 'POST':
        form = BookingCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '客戶資料已成功新增！')
            return redirect('booking:customer_list')
    else:
        form = BookingCustomerForm()
    
    context = {
        'form': form,
        'action': '新增客戶'
    }
    return render(request, 'booking/customer_form.html', context)


def customer_update(request, pk):
    """編輯客戶視圖"""
    customer = get_object_or_404(BookingCustomer, pk=pk)
    
    if request.method == 'POST':
        form = BookingCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, '客戶資料已成功更新！')
            return redirect('booking:customer_list')
    else:
        form = BookingCustomerForm(instance=customer)
    
    context = {
        'form': form,
        'action': '編輯客戶',
        'customer': customer
    }
    return render(request, 'booking/customer_form.html', context)


def customer_delete(request, pk):
    """刪除客戶視圖"""
    customer = get_object_or_404(BookingCustomer, pk=pk)
    
    if request.method == 'POST':
        customer_name = customer.company_name
        customer.delete()
        messages.success(request, f'客戶「{customer_name}」已成功刪除！')
        return redirect('booking:customer_list')
    
    context = {
        'customer': customer
    }
    return render(request, 'booking/customer_confirm_delete.html', context)


# ==================== 查帳紀錄相關視圖 ====================

def get_customer_data(request):
    """API: 根據客戶ID獲取客戶資料"""
    customer_id = request.GET.get('customer_id')
    
    if customer_id:
        try:
            customer = BookingCustomer.objects.get(pk=customer_id)
            data = {
                'success': True,
                'company_name': customer.company_name,
                'email': customer.email or '',
            }
        except BookingCustomer.DoesNotExist:
            data = {'success': False, 'error': '客戶不存在'}
    else:
        data = {'success': False, 'error': '未提供客戶ID'}
    
    return JsonResponse(data)


def tax_audit_list(request):
    """查帳紀錄列表視圖"""
    records = TaxAuditRecord.objects.select_related('customer').all()
    
    # 分頁
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'records': page_obj,
        'paginator': paginator,
    }
    return render(request, 'booking/tax_audit_list.html', context)


def tax_audit_create(request):
    """新增查帳紀錄視圖"""
    HistoryFormSet = inlineformset_factory(
        TaxAuditRecord, TaxAuditHistory,
        form=TaxAuditHistoryForm,
        extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        form = TaxAuditRecordForm(request.POST, request.FILES)
        formset = HistoryFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            audit_record = form.save()
            formset.instance = audit_record
            formset.save()
            messages.success(request, '查帳紀錄已成功新增！')
            return redirect('booking:tax_audit_list')
    else:
        form = TaxAuditRecordForm()
        formset = HistoryFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'action': '新增查帳紀錄'
    }
    return render(request, 'booking/tax_audit_form.html', context)


def tax_audit_update(request, pk):
    """編輯查帳紀錄視圖"""
    audit_record = get_object_or_404(TaxAuditRecord, pk=pk)
    HistoryFormSet = inlineformset_factory(
        TaxAuditRecord, TaxAuditHistory,
        form=TaxAuditHistoryForm,
        extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        form = TaxAuditRecordForm(request.POST, request.FILES, instance=audit_record)
        formset = HistoryFormSet(request.POST, request.FILES, instance=audit_record)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, '查帳紀錄已成功更新！')
            return redirect('booking:tax_audit_list')
    else:
        form = TaxAuditRecordForm(instance=audit_record)
        formset = HistoryFormSet(instance=audit_record)
    
    context = {
        'form': form,
        'formset': formset,
        'action': '編輯查帳紀錄',
        'audit_record': audit_record
    }
    return render(request, 'booking/tax_audit_form.html', context)


def tax_audit_delete(request, pk):
    """刪除查帳紀錄視圖"""
    audit_record = get_object_or_404(TaxAuditRecord, pk=pk)
    
    if request.method == 'POST':
        record_name = f"{audit_record.company_name} - {audit_record.year}年"
        audit_record.delete()
        messages.success(request, f'查帳紀錄「{record_name}」已成功刪除！')
        return redirect('booking:tax_audit_list')
    
    context = {
        'audit_record': audit_record
    }
    return render(request, 'booking/tax_audit_confirm_delete.html', context)

