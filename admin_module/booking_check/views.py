"""
Booking Check (BookkeepingChecklist) Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from admin_module.models import BookkeepingChecklist
from .forms import BookkeepingChecklistForm, BookkeepingChecklistFilterForm


def list(request):
    """記帳進度檢查列表"""
    checklists = BookkeepingChecklist.objects.filter(is_deleted=False)
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
    return render(request, 'admin_module/booking_check/list.html', context)


def create(request):
    """新增記帳進度檢查"""
    if request.method == 'POST':
        form = BookkeepingChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            messages.success(request, f'記帳進度檢查「{checklist.check_period} - {checklist.company_name}」已成功新增！')
            return redirect('admin_module:booking_check:list')
    else:
        form = BookkeepingChecklistForm()
    
    context = {
        'form': form,
        'action': '新增記帳進度檢查',
    }
    return render(request, 'admin_module/booking_check/form.html', context)


def update(request, pk):
    """編輯記帳進度檢查"""
    checklist = get_object_or_404(BookkeepingChecklist, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        form = BookkeepingChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            checklist = form.save()
            messages.success(request, f'記帳進度檢查「{checklist.check_period} - {checklist.company_name}」已成功更新！')
            return redirect('admin_module:booking_check:list')
    else:
        form = BookkeepingChecklistForm(instance=checklist)
    
    context = {
        'form': form,
        'checklist': checklist,
        'action': '編輯記帳進度檢查',
    }
    return render(request, 'admin_module/booking_check/form.html', context)


def delete(request, pk):
    """刪除記帳進度檢查 (軟刪除)"""
    checklist = get_object_or_404(BookkeepingChecklist, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        check_period = checklist.check_period
        company_name = checklist.company_name
        checklist.is_deleted = True
        checklist.save()
        messages.success(request, f'記帳進度檢查「{check_period} - {company_name}」已成功刪除！')
        return redirect('admin_module:booking_check:list')
    
    context = {
        'checklist': checklist
    }
    return render(request, 'admin_module/booking_check/confirm_delete.html', context)
