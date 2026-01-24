"""
Contact Views with Soft Delete
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_module.models import Contact
from .forms import ContactForm, ContactFilterForm


def list(request):
    """聯絡人列表頁面"""
    contacts = Contact.objects.filter(is_deleted=False)
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
    return render(request, 'admin_module/contact/list.html', context)


def create(request):
    """新增聯絡人"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'聯絡人「{contact.name}」已成功新增！')
            return redirect('admin_module:contact:list')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'action': '新增聯絡人'
    }
    return render(request, 'admin_module/contact/form.html', context)


def update(request, pk):
    """編輯聯絡人"""
    contact = get_object_or_404(Contact, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'聯絡人「{contact.name}」已成功更新！')
            return redirect('admin_module:contact:list')
    else:
        form = ContactForm(instance=contact)
    
    context = {
        'form': form,
        'action': '編輯聯絡人',
        'contact': contact
    }
    return render(request, 'admin_module/contact/form.html', context)


def delete(request, pk):
    """刪除聯絡人 (軟刪除)"""
    contact = get_object_or_404(Contact, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        name = contact.name
        contact.is_deleted = True
        contact.save()
        messages.success(request, f'聯絡人「{name}」已成功刪除！')
        return redirect('admin_module:contact:list')
    
    context = {
        'contact': contact
    }
    return render(request, 'admin_module/contact/confirm_delete.html', context)
