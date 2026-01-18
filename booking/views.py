from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import BookingCustomer, TaxAuditRecord, TaxAuditHistory, VATRecord, IncomeTaxRecord, DownloadData
from .forms import BookingCustomerForm, BookingCustomerFilterForm, TaxAuditRecordForm, TaxAuditHistoryForm, VATRecordForm, VATRecordFilterForm, IncomeTaxRecordForm, DownloadDataForm
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
    
    
    # 不使用 Django 分頁，讓 DataTables 處理
    context = {
        'customers': customers,  # 傳遞所有篩選後的客戶，不分頁
        'filter_form': filter_form,
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


# ==================== VAT 申報記錄相關視圖 ====================

def vat_record_list(request):
    """營業稅申報記錄列表視圖"""
    # 獲取篩選條件
    filter_form = VATRecordFilterForm(request.GET)
    
    # 查詢所有客戶，排除非營業人
    customers = BookingCustomer.objects.exclude(business_type='non_business')
    
    # 快速篩選：完成狀態
    completion_status = request.GET.get('completion_status')
    if completion_status:
        customers = customers.filter(
            vatrecord__completion_status=completion_status
        ).distinct()
    
    # 快速篩選：繳稅完成否
    tax_payment_completed = request.GET.get('tax_payment_completed')
    if tax_payment_completed:
        customers = customers.filter(
            vatrecord__tax_payment_completed=tax_payment_completed
        ).distinct()
    
    # 應用篩選條件
    if filter_form.is_valid():
        bookkeeping_assistant = filter_form.cleaned_data.get('bookkeeping_assistant')
        company_name = filter_form.cleaned_data.get('company_name')
        company_id = filter_form.cleaned_data.get('company_id')
        undertaking_status = filter_form.cleaned_data.get('undertaking_status')
        business_type = filter_form.cleaned_data.get('business_type')
        tax_payment = filter_form.cleaned_data.get('tax_payment')
        
        if bookkeeping_assistant:
            customers = customers.filter(bookkeeping_assistant__icontains=bookkeeping_assistant)
        if company_name:
            customers = customers.filter(company_name__icontains=company_name)
        if company_id:
            customers = customers.filter(company_id__icontains=company_id)
        if undertaking_status:
            customers = customers.filter(undertaking_status=undertaking_status)
        if business_type:
            customers = customers.filter(business_type=business_type)
        if tax_payment:
            customers = customers.filter(tax_payment=tax_payment)
    
    # 計算統計數據（基於所有非營業人客戶）
    all_customers = BookingCustomer.objects.exclude(business_type='non_business')
    from django.db.models import Q
    
    # 完成狀態統計
    completed_count = all_customers.filter(
        vatrecord__completion_status='completed'
    ).distinct().count()
    
    not_started_count = all_customers.filter(
        vatrecord__completion_status='not_started'
    ).distinct().count()
    
    # 繳稅狀態統計
    customer_paid_count = all_customers.filter(
        vatrecord__tax_payment_completed='customer_paid'
    ).distinct().count()
    
    office_paid_count = all_customers.filter(
        vatrecord__tax_payment_completed='office_paid'
    ).distinct().count()
    
    not_replied_count = all_customers.filter(
        vatrecord__tax_payment_completed='not_replied'
    ).distinct().count()
    
    # 不使用 Django 分頁，讓 DataTables 處理
    context = {
        'customers': customers,  # 傳遞所有篩選後的客戶，不分頁
        'filter_form': filter_form,
        # 統計數據
        'completed_count': completed_count,
        'not_started_count': not_started_count,
        'customer_paid_count': customer_paid_count,
        'office_paid_count': office_paid_count,
        'not_replied_count': not_replied_count,
        # 當前篩選狀態
        'current_completion_status': completion_status,
        'current_tax_payment_completed': tax_payment_completed,
    }
    return render(request, 'booking/vat_record_list.html', context)




def vat_record_create(request):
    """新增VAT申報記錄視圖"""
    if request.method == 'POST':
        form = VATRecordForm(request.POST)
        if form.is_valid():
            # 檢查客戶是否為非營業人
            customer = form.cleaned_data['customer']
            if customer.business_type == 'non_business':
                messages.error(request, '非營業人不需要申報營業稅！')
            else:
                form.save()
                messages.success(request, 'VAT申報記錄已成功新增！')
                return redirect('booking:vat_record_list')
    else:
        form = VATRecordForm()
    
    # 只提供非「非營業人」的客戶選項
    form.fields['customer'].queryset = BookingCustomer.objects.exclude(business_type='non_business')
    
    context = {
        'form': form,
        'action': '新增VAT申報記錄'
    }
    return render(request, 'booking/vat_record_form.html', context)


def vat_record_edit(request, pk=None, customer_id=None):
    """編輯VAT申報記錄視圖"""
    # 如果提供 customer_id，嘗試獲取或創建 VAT 記錄
    if customer_id:
        customer = get_object_or_404(BookingCustomer, pk=customer_id)
        # 獲取最新的 VAT 記錄，如果沒有則為 None
        vat_record = VATRecord.objects.filter(customer=customer).order_by('-filing_year', '-filing_period').first()
    else:
        vat_record = get_object_or_404(VATRecord, pk=pk) if pk else None
        customer = vat_record.customer if vat_record else None
    
    if request.method == 'POST':
        if vat_record:
            form = VATRecordForm(request.POST, instance=vat_record)
        else:
            form = VATRecordForm(request.POST)
            # 如果是新建，設置客戶
            if customer_id:
                form.instance.customer = customer
        
        if form.is_valid():
            vat_record = form.save()
            messages.success(request, 'VAT申報記錄已成功更新！')
            # 留在編輯頁面，而不是跳轉到列表
            return redirect('booking:vat_record_edit', pk=vat_record.pk)
    else:
        if vat_record:
            form = VATRecordForm(instance=vat_record)
        else:
            form = VATRecordForm(initial={'customer': customer} if customer else {})
    
    # 客戶選擇欄位設為唯讀（透過模板控制）
    context = {
        'form': form,
        'action': '編輯VAT申報記錄',
        'vat_record': vat_record,
        'customer': customer,
        'is_edit': True
    }
    return render(request, 'booking/vat_record_form.html', context)



def vat_record_delete(request, pk):
    """刪除VAT申報記錄視圖"""
    vat_record = get_object_or_404(VATRecord, pk=pk)
    
    if request.method == 'POST':
        record_name = str(vat_record)
        vat_record.delete()
        messages.success(request, f'VAT申報記錄「{record_name}」已成功刪除！')
        return redirect('booking:vat_record_list')
    
    context = {
        'vat_record': vat_record
    }
    return render(request, 'booking/vat_record_confirm_delete.html', context)


# ==================== 所得稅申報相關視圖 ====================

def income_tax_list(request):
    """所得稅申報記錄列表視圖"""
    # 查詢所有客戶
    customers = BookingCustomer.objects.all()
    
    # 不使用 Django 分頁，讓 DataTables 處理
    context = {
        'customers': customers,
    }
    return render(request, 'booking/income_tax_list.html', context)


def income_tax_edit_by_customer(request, customer_id):
    """編輯客戶的所得稅申報記錄（根據客戶ID）"""
    customer = get_object_or_404(BookingCustomer, pk=customer_id)
    
    # 嘗試取得該客戶的所得稅記錄，若沒有則建立新的
    try:
        income_record = IncomeTaxRecord.objects.get(customer=customer)
        action = '編輯所得稅申報記錄'
    except IncomeTaxRecord.DoesNotExist:
        income_record = None
        action = '新增所得稅申報記錄'
    
    if request.method == 'POST':
        if income_record:
            form = IncomeTaxRecordForm(request.POST, instance=income_record)
        else:
            form = IncomeTaxRecordForm(request.POST)
        
        if form.is_valid():
            income_record = form.save(commit=False)
            income_record.customer = customer
            income_record.save()
            messages.success(request, '所得稅申報記錄已成功儲存！')
            return redirect('booking:income_tax_list')
    else:
        if income_record:
            form = IncomeTaxRecordForm(instance=income_record)
        else:
            # 建立新表單時預設 customer
            form = IncomeTaxRecordForm(initial={'customer': customer})
    
    context = {
        'form': form,
        'customer': customer,
        'income_record': income_record,
        'action': action,
    }
    return render(request, 'booking/income_tax_form.html', context)


# ==================== 下載資料相關視圖 ====================

def download_data_list(request):
    """下載資料列表視圖"""
    download_data = DownloadData.objects.all()
    
    context = {
        'download_data': download_data,
    }
    return render(request, 'booking/download_data_list.html', context)


def download_data_create(request):
    """新增下載資料"""
    if request.method == 'POST':
        form = DownloadDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '下載資料已成功建立！')
            return redirect('booking:download_data_list')
    else:
        form = DownloadDataForm()
    
    context = {
        'form': form,
        'action': '新增下載資料',
    }
    return render(request, 'booking/download_data_form.html', context)


def download_data_edit(request, pk):
    """編輯下載資料"""
    data = get_object_or_404(DownloadData, pk=pk)
    
    if request.method == 'POST':
        form = DownloadDataForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, '下載資料已成功更新！')
            return redirect('booking:download_data_list')
    else:
        form = DownloadDataForm(instance=data)
    
    context = {
        'form': form,
        'data': data,
        'action': '編輯下載資料',
    }
    return render(request, 'booking/download_data_form.html', context)


def download_data_delete(request, pk):
    """刪除下載資料"""
    data = get_object_or_404(DownloadData, pk=pk)
    
    if request.method == 'POST':
        data.delete()
        messages.success(request, '下載資料已成功刪除！')
        return redirect('booking:download_data_list')
    
    context = {
        'data': data
    }
    return render(request, 'booking/download_data_confirm_delete.html', context)


# ==================== 客戶通知功能 ====================

from .utils import notify_customer_and_save

def notify_customer(request, record_type, pk):
    """
    通知客戶並將資料轉移到下載資料
    
    Args:
        record_type: 'vat' 或 'income_tax'
        pk: 記錄的主鍵
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '無效的請求方法'}, status=405)
    
    try:
        # 根據類型取得記錄
        if record_type == 'vat':
            record = get_object_or_404(VATRecord, pk=pk)
        elif record_type == 'income_tax':
            record = get_object_or_404(IncomeTaxRecord, pk=pk)
        else:
            return JsonResponse({'success': False, 'message': '無效的記錄類型'}, status=400)
        
        # 執行通知並儲存
        success, message, download_data = notify_customer_and_save(record, record_type)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': message,
                'file_number': download_data.file_number if download_data else None
            })
        else:
            return JsonResponse({'success': False, 'message': message}, status=500)
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'系統錯誤：{str(e)}'}, status=500)
