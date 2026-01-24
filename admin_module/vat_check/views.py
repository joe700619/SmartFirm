"""
VAT Check Views with Soft Delete
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_module.models import VATCheck, VATCheckItem
from .forms import VATCheckForm, VATCheckItemForm, VATCheckFilterForm


def list(request):
    """營業稅檢查列表頁面"""
    vat_checks = VATCheck.objects.filter(is_deleted=False)
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
    
    # 分頁處理
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
    return render(request, 'admin_module/vat_check/list.html', context)


def create(request):
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
            return redirect('admin_module:vat_check:list')
    else:
        form = VATCheckForm()
    
    context = {
        'form': form,
        'action': '新增營業稅檢查',
    }
    return render(request, 'admin_module/vat_check/form.html', context)


def update(request, pk):
    """編輯營業稅檢查"""
    import json
    
    vat_check = get_object_or_404(VATCheck, pk=pk, is_deleted=False)
    
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
            return redirect('admin_module:vat_check:list')
    else:
        form = VATCheckForm(instance=vat_check)
    
    context = {
        'form': form,
        'vat_check': vat_check,
        'action': '編輯營業稅檢查',
    }
    return render(request, 'admin_module/vat_check/form.html', context)


def delete(request, pk):
    """刪除營業稅檢查 (軟刪除)"""
    vat_check = get_object_or_404(VATCheck, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        check_period = vat_check.check_period
        vat_check.is_deleted = True
        vat_check.save()
        messages.success(request, f'營業稅檢查「{check_period}」已成功刪除！')
        return redirect('admin_module:vat_check:list')
    
    context = {
        'vat_check': vat_check
    }
    return render(request, 'admin_module/vat_check/confirm_delete.html', context)
