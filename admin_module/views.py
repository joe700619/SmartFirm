from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (BasicInformation, Contact, IncomingMail, IncomingMailItem, 
                     CustomerChange, VATCheck, VATCheckItem, BookkeepingChecklist)
from .forms import (BasicInformationForm, CustomerFilterForm, ContactForm, ContactFilterForm, 
                    IncomingMailForm, IncomingMailItemForm, CustomerChangeForm,
                    VATCheckForm, VATCheckItemForm, VATCheckFilterForm,
                    BookkeepingChecklistForm, BookkeepingChecklistFilterForm)



def customer_list(request):
    """客戶列表頁面"""
    customers = BasicInformation.objects.all()
    filter_form = CustomerFilterForm(request.GET or None)
    
    # 處理篩選
    if filter_form.is_valid():
        company_name = filter_form.cleaned_data.get('company_name')
        company_id = filter_form.cleaned_data.get('company_id')
        contact = filter_form.cleaned_data.get('contact')
        
        # 建立篩選條件
        filters = Q()
        if company_name:
            filters &= Q(companyName__icontains=company_name)
        if company_id:
            filters &= Q(companyId__icontains=company_id)
        if contact:
            filters &= Q(contact__icontains=contact)
        
        # 應用篩選
        if filters:
            customers = customers.filter(filters)
    
    # 分頁處理 - 每頁顯示 50 筆
    paginator = Paginator(customers, 50)
    page = request.GET.get('page')
    
    try:
        customers_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果頁碼不是整數，顯示第一頁
        customers_page = paginator.page(1)
    except EmptyPage:
        # 如果頁碼超出範圍，顯示最後一頁
        customers_page = paginator.page(paginator.num_pages)
    
    context = {
        'customers': customers_page,
        'filter_form': filter_form,
        'paginator': paginator,
    }
    return render(request, 'admin_module/customer_list.html', context)


def customer_create(request):
    """新增客戶"""
    if request.method == 'POST':
        form = BasicInformationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'客戶「{customer.companyName}」已成功新增！')
            return redirect('admin_module:customer_list')
    else:
        form = BasicInformationForm()
    
    context = {
        'form': form,
        'action': '新增客戶'
    }
    return render(request, 'admin_module/customer_form.html', context)


def customer_update(request, pk):
    """編輯客戶"""
    customer = get_object_or_404(BasicInformation, pk=pk)
    
    if request.method == 'POST':
        form = BasicInformationForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'客戶「{customer.companyName}」已成功更新！')
            return redirect('admin_module:customer_list')
    else:
        form = BasicInformationForm(instance=customer)
    
    context = {
        'form': form,
        'action': '編輯客戶',
        'customer': customer
    }
    return render(request, 'admin_module/customer_form.html', context)


def customer_delete(request, pk):
    """刪除客戶"""
    customer = get_object_or_404(BasicInformation, pk=pk)
    
    if request.method == 'POST':
        company_name = customer.companyName
        customer.delete()
        messages.success(request, f'客戶「{company_name}」已成功刪除！')
        return redirect('admin_module:customer_list')
    
    context = {
        'customer': customer
    }
    return render(request, 'admin_module/customer_confirm_delete.html', context)


# ========== 聯絡人管理 ==========

def contact_list(request):
    """聯絡人列表頁面"""
    contacts = Contact.objects.all()
    filter_form = ContactFilterForm(request.GET or None)
    
    # 處理篩選
    if filter_form.is_valid():
        email = filter_form.cleaned_data.get('email')
        company_name = filter_form.cleaned_data.get('company_name')
        name = filter_form.cleaned_data.get('name')
        
        # 建立篩選條件
        filters = Q()
        if email:
            filters &= Q(email__icontains=email)
        if company_name:
            filters &= Q(company_name__icontains=company_name)
        if name:
            filters &= Q(name__icontains=name)
        
        # 應用篩選
        if filters:
            contacts = contacts.filter(filters)
    
    # 分頁處理 - 每頁顯示 50 筆
    paginator = Paginator(contacts, 50)
    page = request.GET.get('page')
    
    try:
        contacts_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_page = paginator.page(1)
    except EmptyPage:
        contacts_page = paginator.page(paginator.num_pages)
    
    context = {
        'contacts': contacts_page,
        'filter_form': filter_form,
        'paginator': paginator,
    }
    return render(request, 'admin_module/contact_list.html', context)


def contact_create(request):
    """新增聯絡人"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'聯絡人「{contact.name}」已成功新增！')
            return redirect('admin_module:contact_list')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'action': '新增聯絡人'
    }
    return render(request, 'admin_module/contact_form.html', context)


def contact_update(request, pk):
    """編輯聯絡人"""
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'聯絡人「{contact.name}」已成功更新！')
            return redirect('admin_module:contact_list')
    else:
        form = ContactForm(instance=contact)
    
    context = {
        'form': form,
        'action': '編輯聯絡人',
        'contact': contact
    }
    return render(request, 'admin_module/contact_form.html', context)


def contact_delete(request, pk):
    """刪除聯絡人"""
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        name = contact.name
        contact.delete()
        messages.success(request, f'聯絡人「{name}」已成功刪除！')
        return redirect('admin_module:contact_list')
    
    context = {
        'contact': contact
    }
    return render(request, 'admin_module/contact_confirm_delete.html', context)


# ========== API ==========

from django.http import JsonResponse

def api_contacts(request):
    """API: 根據公司統編取得聯絡人列表"""
    company_id = request.GET.get('company_id', '').strip()
    
    if not company_id:
        return JsonResponse([], safe=False)
    
    contacts = Contact.objects.filter(company_id=company_id).values(
        'id', 'name', 'position', 'email', 'phone', 'mobile', 'fax', 'address'
    )
    
    return JsonResponse(list(contacts), safe=False)


def api_customer_info(request):
    """API: 根據統一編號取得客戶資料"""
    company_id = request.GET.get('company_id', '').strip()
    
    if not company_id:
        return JsonResponse({'error': 'Missing company_id'}, status=400)
    
    try:
        customer = BasicInformation.objects.get(companyId=company_id)
        return JsonResponse({
            'id': customer.id,
            'companyName': customer.companyName,
            'contact': customer.contact,
        })
    except BasicInformation.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


def search_companies_api(request):
    """API: 搜尋公司"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'companies': []})
    
    # Search by company name or company ID
    companies = BasicInformation.objects.filter(
        Q(companyName__icontains=query) | Q(companyId__icontains=query)
    )[:20]  # Limit to 20 results
    
    data = {
        'companies': [
            {
                'id': c.id,
                'companyName': c.companyName,
                'companyId': c.companyId,
            }
            for c in companies
        ]
    }
    
    return JsonResponse(data)



# ========== 收文系統 ==========

def incoming_mail_list(request):
    """收文列表頁面"""
    mails = IncomingMail.objects.all().prefetch_related('items')
    
    # 分頁處理
    paginator = Paginator(mails, 50)
    page = request.GET.get('page')
    
    try:
        mails_page = paginator.page(page)
    except PageNotAnInteger:
        mails_page = paginator.page(1)
    except EmptyPage:
        mails_page = paginator.page(paginator.num_pages)
    
    context = {
        'mails': mails_page,
        'paginator': paginator,
    }
    return render(request, 'admin_module/incoming_mail_list.html', context)


def incoming_mail_create(request):
    """新增收文"""
    import json
    
    if request.method == 'POST':
        form = IncomingMailForm(request.POST)
        if form.is_valid():
            incoming_mail = form.save()
            
            # 處理明細項目
            items_data = request.POST.getlist('items')
            for idx, item_json in enumerate(items_data):
                if item_json:
                    item_data = json.loads(item_json)
                    IncomingMailItem.objects.create(
                        incoming_mail=incoming_mail,
                        sender=item_data.get('sender', ''),
                        company_id=item_data.get('company_id'),
                        customer_name=item_data.get('customer_name', ''),
                        content_type=item_data.get('content_type', ''),
                        notify_customer=item_data.get('notify_customer', False),
                        message_content=item_data.get('message_content', ''),
                        order=idx
                    )
            
            messages.success(request, f'收文「{incoming_mail.serial_number}」已成功新增！')
            return redirect('admin_module:incoming_mail_list')
    else:
        form = IncomingMailForm()
    
    # 取得所有客戶列表供選擇
    customers = BasicInformation.objects.all().order_by('companyName')
    
    # 序列化為 JSON 供 JavaScript 使用
    customers_json = mark_safe(json.dumps(list(customers.values('id', 'companyId', 'companyName', 'contact'))))
    content_types_json = mark_safe(json.dumps([{'value': ct[0], 'display': ct[1]} for ct in IncomingMailItem.CONTENT_TYPE_CHOICES]))
    
    context = {
        'form': form,
        'customers': customers,
        'customers_json': customers_json,
        'content_types_json': content_types_json,
        'action': '新增收文',
        'content_type_choices': IncomingMailItem.CONTENT_TYPE_CHOICES,
    }
    return render(request, 'admin_module/incoming_mail_form.html', context)


def incoming_mail_update(request, pk):
    """編輯收文"""
    import json
    
    incoming_mail = get_object_or_404(IncomingMail, pk=pk)
    
    if request.method == 'POST':
        form = IncomingMailForm(request.POST, instance=incoming_mail)
        if form.is_valid():
            incoming_mail = form.save()
            
            # 刪除舊的明細項目
            incoming_mail.items.all().delete()
            
            # 重新建立明細項目
            items_data = request.POST.getlist('items')
            for idx, item_json in enumerate(items_data):
                if item_json:
                    item_data = json.loads(item_json)
                    IncomingMailItem.objects.create(
                        incoming_mail=incoming_mail,
                        sender=item_data.get('sender', ''),
                        company_id=item_data.get('company_id'),
                        customer_name=item_data.get('customer_name', ''),
                        content_type=item_data.get('content_type', ''),
                        notify_customer=item_data.get('notify_customer', False),
                        message_content=item_data.get('message_content', ''),
                        order=idx
                    )
            
            messages.success(request, f'收文「{incoming_mail.serial_number}」已成功更新！')
            return redirect('admin_module:incoming_mail_list')
    else:
        form = IncomingMailForm(instance=incoming_mail)
    
    # 取得所有客戶列表供選擇
    customers = BasicInformation.objects.all().order_by('companyName')
    
    # 序列化為 JSON 供 JavaScript 使用
    customers_json = mark_safe(json.dumps(list(customers.values('id', 'companyId', 'companyName', 'contact'))))
    content_types_json = mark_safe(json.dumps([{'value': ct[0], 'display': ct[1]} for ct in IncomingMailItem.CONTENT_TYPE_CHOICES]))
    
    context = {
        'form': form,
        'incoming_mail': incoming_mail,
        'customers': customers,
        'customers_json': customers_json,
        'content_types_json': content_types_json,
        'action': '編輯收文',
        'content_type_choices': IncomingMailItem.CONTENT_TYPE_CHOICES,
    }
    return render(request, 'admin_module/incoming_mail_form.html', context)


def incoming_mail_delete(request, pk):
    """刪除收文"""
    incoming_mail = get_object_or_404(IncomingMail, pk=pk)
    
    if request.method == 'POST':
        serial_number = incoming_mail.serial_number
        incoming_mail.delete()
        messages.success(request, f'收文「{serial_number}」已成功刪除！')
        return redirect('admin_module:incoming_mail_list')
    
    context = {
        'incoming_mail': incoming_mail
    }
    return render(request, 'admin_module/incoming_mail_confirm_delete.html', context)


# ========== 客戶增減管理 ==========

def customer_change_list(request):
    """客戶增減列表頁面"""
    changes = CustomerChange.objects.all()
    
    # 分頁處理
    paginator = Paginator(changes, 50)
    page = request.GET.get('page')
    
    try:
        changes_page = paginator.page(page)
    except PageNotAnInteger:
        changes_page = paginator.page(1)
    except EmptyPage:
        changes_page = paginator.page(paginator.num_pages)
    
    context = {
        'changes': changes_page,
        'paginator': paginator,
    }
    return render(request, 'admin_module/customer_change_list.html', context)


def customer_change_create(request):
    """新增客戶增減"""
    if request.method == 'POST':
        form = CustomerChangeForm(request.POST)
        if form.is_valid():
            customer_change = form.save()
            messages.success(request, f'客戶增減「{customer_change.company_name}」已成功新增！')
            return redirect('admin_module:customer_change_list')
    else:
        form = CustomerChangeForm()
    
    context = {
        'form': form,
        'action': '新增客戶增減'
    }
    return render(request, 'admin_module/customer_change_form.html', context)


def customer_change_update(request, pk):
    """編輯客戶增減"""
    customer_change = get_object_or_404(CustomerChange, pk=pk)
    
    if request.method == 'POST':
        form = CustomerChangeForm(request.POST, instance=customer_change)
        if form.is_valid():
            customer_change = form.save()
            messages.success(request, f'客戶增減「{customer_change.company_name}」已成功更新！')
            return redirect('admin_module:customer_change_list')
    else:
        form = CustomerChangeForm(instance=customer_change)
    
    context = {
        'form': form,
        'action': '編輯客戶增減',
        'customer_change': customer_change
    }
    return render(request, 'admin_module/customer_change_form.html', context)


def customer_change_delete(request, pk):
    """刪除客戶增減"""
    customer_change = get_object_or_404(CustomerChange, pk=pk)
    
    if request.method == 'POST':
        company_name = customer_change.company_name
        customer_change.delete()
        messages.success(request, f'客戶增減「{company_name}」已成功刪除！')
        return redirect('admin_module:customer_change_list')
    
    context = {
        'customer_change': customer_change
    }
    return render(request, 'admin_module/customer_change_confirm_delete.html', context)


# ========== 營業稅檢查管理 ==========

def vat_check_list(request):
    """營業稅檢查列表頁面"""
    vat_checks = VATCheck.objects.all()
    filter_form = VATCheckFilterForm(request.GET or None)
    
    # 處理篩選
    if filter_form.is_valid():
        check_period = filter_form.cleaned_data.get('check_period')
        status = filter_form.cleaned_data.get('status')
        inspector = filter_form.cleaned_data.get('inspector')
        
        # 建立篩選條件
        filters = Q()
        if check_period:
            filters &= Q(check_period__icontains=check_period)
        if status:
            filters &= Q(status=status)
        if inspector:
            filters &= Q(inspector__icontains=inspector)
        
        # 應用篩選
        if filters:
            vat_checks = vat_checks.filter(filters)
    
    # 分頁處理 - 每頁顯示 50 筆
    paginator = Paginator(vat_checks, 50)
    page = request.GET.get('page')
    
    try:
        vat_checks_page = paginator.page(page)
    except PageNotAnInteger:
        vat_checks_page = paginator.page(1)
    except EmptyPage:
        vat_checks_page = paginator.page(paginator.num_pages)
    
    context = {
        'vat_checks': vat_checks_page,
        'filter_form': filter_form,
        'paginator': paginator,
    }
    return render(request, 'admin_module/vat_check_list.html', context)


def vat_check_create(request):
    """新增營業稅檢查"""
    import json
    
    if request.method == 'POST':
        form = VATCheckForm(request.POST)
        if form.is_valid():
            vat_check = form.save()
            
            # 處理明細項目
            items_data = request.POST.getlist('items')
            for idx, item_json in enumerate(items_data):
                if item_json:
                    item_data = json.loads(item_json)
                    VATCheckItem.objects.create(
                        vat_check=vat_check,
                        company_id=item_data.get('company_id', ''),
                        company_name=item_data.get('company_name', ''),
                        input_buyer=item_data.get('input_buyer', ''),
                        check_input_amount=item_data.get('check_input_amount') or None,
                        input_duplicate=item_data.get('input_duplicate', ''),
                        output_e_invoice=item_data.get('output_e_invoice', ''),
                        form401_output_amount=item_data.get('form401_output_amount') or None,
                        form401_input_amount=item_data.get('form401_input_amount') or None,
                        tax_credit_carried_forward=item_data.get('tax_credit_carried_forward') or None,
                        tax_payable=item_data.get('tax_payable') or None,
                        tax_refundable=item_data.get('tax_refundable') or None,
                        order=idx
                    )
            
            messages.success(request, f'營業稅檢查「{vat_check.check_period}」已成功新增！')
            return redirect('admin_module:vat_check_list')
    else:
        form = VATCheckForm()
    
    context = {
        'form': form,
        'action': '新增營業稅檢查',
    }
    return render(request, 'admin_module/vat_check_form.html', context)


def vat_check_update(request, pk):
    """編輯營業稅檢查"""
    import json
    
    vat_check = get_object_or_404(VATCheck, pk=pk)
    
    if request.method == 'POST':
        form = VATCheckForm(request.POST, instance=vat_check)
        if form.is_valid():
            vat_check = form.save()
            
            # 刪除舊的明細項目
            vat_check.items.all().delete()
            
            # 重新建立明細項目
            items_data = request.POST.getlist('items')
            for idx, item_json in enumerate(items_data):
                if item_json:
                    item_data = json.loads(item_json)
                    VATCheckItem.objects.create(
                        vat_check=vat_check,
                        company_id=item_data.get('company_id', ''),
                        company_name=item_data.get('company_name', ''),
                        input_buyer=item_data.get('input_buyer', ''),
                        check_input_amount=item_data.get('check_input_amount') or None,
                        input_duplicate=item_data.get('input_duplicate', ''),
                        output_e_invoice=item_data.get('output_e_invoice', ''),
                        form401_output_amount=item_data.get('form401_output_amount') or None,
                        form401_input_amount=item_data.get('form401_input_amount') or None,
                        tax_credit_carried_forward=item_data.get('tax_credit_carried_forward') or None,
                        tax_payable=item_data.get('tax_payable') or None,
                        tax_refundable=item_data.get('tax_refundable') or None,
                        order=idx
                    )
            
            messages.success(request, f'營業稅檢查「{vat_check.check_period}」已成功更新！')
            return redirect('admin_module:vat_check_list')
    else:
        form = VATCheckForm(instance=vat_check)
    
    context = {
        'form': form,
        'vat_check': vat_check,
        'action': '編輯營業稅檢查',
    }
    return render(request, 'admin_module/vat_check_form.html', context)


def vat_check_delete(request, pk):
    """刪除營業稅檢查"""
    vat_check = get_object_or_404(VATCheck, pk=pk)
    
    if request.method == 'POST':
        check_period = vat_check.check_period
        vat_check.delete()
        messages.success(request, f'營業稅檢查「{check_period}」已成功刪除！')
        return redirect('admin_module:vat_check_list')
    
    context = {
        'vat_check': vat_check
    }
    return render(request, 'admin_module/vat_check_confirm_delete.html', context)


# ==================== 記帳進度檢查 ====================

def bookkeeping_checklist_list(request):
    """記帳進度檢查列表"""
    checklists = BookkeepingChecklist.objects.all()
    filter_form = BookkeepingChecklistFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        check_period = filter_form.cleaned_data.get('check_period')
        status = filter_form.cleaned_data.get('status')
        bookkeeper = filter_form.cleaned_data.get('bookkeeper')
        
        filters = Q()
        if check_period:
            filters &= Q(check_period__icontains=check_period)
        if status:
            filters &= Q(status=status)
        if bookkeeper:
            filters &= Q(bookkeeper__icontains=bookkeeper)
        
        if filters:
            checklists = checklists.filter(filters)
    
    paginator = Paginator(checklists, 50)
    page = request.GET.get('page')
    
    try:
        checklists_page = paginator.page(page)
    except PageNotAnInteger:
        checklists_page = paginator.page(1)
    except EmptyPage:
        checklists_page = paginator.page(paginator.num_pages)
    
    context = {
        'checklists': checklists_page,
        'filter_form': filter_form,
    }
    return render(request, 'admin_module/bookkeeping_checklist_list.html', context)


def bookkeeping_checklist_create(request):
    """新增記帳進度檢查"""
    if request.method == 'POST':
        form = BookkeepingChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            messages.success(request, f'記帳進度檢查「{checklist.check_period} - {checklist.company_name}」已成功新增！')
            return redirect('admin_module:bookkeeping_checklist_list')
    else:
        form = BookkeepingChecklistForm()
    
    context = {
        'form': form,
        'action': '新增記帳進度檢查',
    }
    return render(request, 'admin_module/bookkeeping_checklist_form.html', context)


def bookkeeping_checklist_update(request, pk):
    """編輯記帳進度檢查"""
    checklist = get_object_or_404(BookkeepingChecklist, pk=pk)
    
    if request.method == 'POST':
        form = BookkeepingChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            checklist = form.save()
            messages.success(request, f'記帳進度檢查「{checklist.check_period} - {checklist.company_name}」已成功更新！')
            return redirect('admin_module:bookkeeping_checklist_list')
    else:
        form = BookkeepingChecklistForm(instance=checklist)
    
    context = {
        'form': form,
        'checklist': checklist,
        'action': '編輯記帳進度檢查',
    }
    return render(request, 'admin_module/bookkeeping_checklist_form.html', context)


def bookkeeping_checklist_delete(request, pk):
    """刪除記帳進度檢查"""
    checklist = get_object_or_404(BookkeepingChecklist, pk=pk)
    
    if request.method == 'POST':
        check_period = checklist.check_period
        company_name = checklist.company_name
        checklist.delete()
        messages.success(request, f'記帳進度檢查「{check_period} - {company_name}」已成功刪除！')
        return redirect('admin_module:bookkeeping_checklist_list')
    
    context = {
        'checklist': checklist
    }
    return render(request, 'admin_module/bookkeeping_checklist_confirm_delete.html', context)
