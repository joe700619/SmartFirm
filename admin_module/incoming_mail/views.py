"""
Incoming Mail Views with Soft Delete
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_module.models import IncomingMail, IncomingMailItem, BasicInformation
from .forms import IncomingMailForm, IncomingMailItemForm


def list(request):
    """收文列表頁面"""
    mails = IncomingMail.objects.filter(is_deleted=False).prefetch_related('items')
    
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
    return render(request, 'admin_module/incoming_mail/list.html', context)


def create(request):
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
            return redirect('admin_module:incoming_mail:list')
    else:
        form = IncomingMailForm()
    
    # 取得所有客戶列表供選擇
    customers = BasicInformation.objects.filter(is_deleted=False).order_by('companyName')
    
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
    return render(request, 'admin_module/incoming_mail/form.html', context)


def update(request, pk):
    """編輯收文"""
    import json
    
    incoming_mail = get_object_or_404(IncomingMail, pk=pk, is_deleted=False)
    
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
            return redirect('admin_module:incoming_mail:list')
    else:
        form = IncomingMailForm(instance=incoming_mail)
    
    # 取得所有客戶列表供選擇
    customers = BasicInformation.objects.filter(is_deleted=False).order_by('companyName')
    
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
    return render(request, 'admin_module/incoming_mail/form.html', context)


def delete(request, pk):
    """刪除收文 (軟刪除)"""
    incoming_mail = get_object_or_404(IncomingMail, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        serial_number = incoming_mail.serial_number
        incoming_mail.is_deleted = True
        incoming_mail.save()
        messages.success(request, f'收文「{serial_number}」已成功刪除！')
        return redirect('admin_module:incoming_mail:list')
    
    context = {
        'incoming_mail': incoming_mail
    }
    return render(request, 'admin_module/incoming_mail/confirm_delete.html', context)
