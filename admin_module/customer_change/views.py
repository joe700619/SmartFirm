"""
Customer Change Views with Soft Delete
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_module.models import CustomerChange
from .forms import CustomerChangeForm


def list(request):
    """客戶增減列表頁面"""
    changes = CustomerChange.objects.filter(is_deleted=False)
    
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
    return render(request, 'admin_module/customer_change/list.html', context)


def create(request):
    """新增客戶增減"""
    if request.method == 'POST':
        form = CustomerChangeForm(request.POST)
        if form.is_valid():
            customer_change = form.save()
            messages.success(request, f'客戶增減「{customer_change.company_name}」已成功新增！')
            return redirect('admin_module:customer_change:list')
    else:
        form = CustomerChangeForm()
    
    context = {
        'form': form,
        'action': '新增客戶增減'
    }
    return render(request, 'admin_module/customer_change/form.html', context)


def update(request, pk):
    """編輯客戶增減"""
    customer_change = get_object_or_404(CustomerChange, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = CustomerChangeForm(request.POST, instance=customer_change)
        if form.is_valid():
            customer_change = form.save()
            messages.success(request, f'客戶增減「{customer_change.company_name}」已成功更新！')
            return redirect('admin_module:customer_change:list')
    else:
        form = CustomerChangeForm(instance=customer_change)
    
    context = {
        'form': form,
        'action': '編輯客戶增減',
        'customer_change': customer_change
    }
    return render(request, 'admin_module/customer_change/form.html', context)


def delete(request, pk):
    """刪除客戶增減 (軟刪除)"""
    customer_change = get_object_or_404(CustomerChange, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        company_name = customer_change.company_name
        customer_change.is_deleted = True
        customer_change.save()
        messages.success(request, f'客戶增減「{company_name}」已成功刪除！')
        return redirect('admin_module:customer_change:list')
    
    context = {
        'customer_change': customer_change
    }
    return render(request, 'admin_module/customer_change/confirm_delete.html', context)
