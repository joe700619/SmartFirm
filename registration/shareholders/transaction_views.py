"""
股權交易管理視圖
"""
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction as db_transaction
from django.db.models import Q
from registration.models import StockTransaction, Shareholder, CompanyShareholding
from admin_module.models import BasicInformation


class StockTransactionListView(LoginRequiredMixin, View):
    """股權交易列表視圖"""
    
    def get(self, request):
        """顯示所有股權交易"""
        transactions = StockTransaction.objects.all().select_related(
            'company_holding__shareholder',
            'company_holding__company'
        ).order_by('-transaction_date', '-created_at')
        
        # 準備數據
        transaction_data = []
        for trans in transactions:
            transaction_data.append({
                'id': trans.id,
                'date': trans.transaction_date,
                'description': trans.description,
                'type': trans.get_transaction_type_display(),
                'company_name': trans.company_holding.company.companyName,
                'company_id': trans.company_holding.company.companyId,
                'shareholder_name': trans.company_holding.shareholder.name,
                'identifier': trans.company_holding.shareholder.identifier,
                'stock_type': trans.get_stock_type_display(),
                'par_value': trans.par_value,
                'quantity': trans.quantity,
                'stock_amount': trans.stock_amount,
                'amount': trans.amount if trans.amount else '',
                'note': trans.note or '',
            })
        
        context = {
            'transactions': transaction_data,
            'companies': BasicInformation.objects.all(),
            'shareholders': Shareholder.objects.all(),
        }
        
        return render(request, 'shareholders/transaction_list.html', context)


@require_http_methods(["GET"])
def get_transaction_api(request, pk):
    """API: 取得單筆交易"""
    try:
        trans = StockTransaction.objects.select_related(
            'company_holding__shareholder',
            'company_holding__company'
        ).get(pk=pk)
        
        data = {
            'success': True,
            'transaction': {
                'id': trans.id,
                'transaction_date': trans.transaction_date.isoformat(),
                'description': trans.description,
                'transaction_type': trans.transaction_type,
                'stock_type': trans.stock_type,
                'par_value': str(trans.par_value),
                'quantity': trans.quantity,
                'stock_amount': str(trans.stock_amount),
                'amount': str(trans.amount) if trans.amount else '',
                'note': trans.note or '',
                'company_id': trans.company_holding.company.id,
                'company_name': trans.company_holding.company.companyName,
                'shareholder_id': trans.company_holding.shareholder.id,
                'shareholder_name': trans.company_holding.shareholder.name,
                'identifier': trans.company_holding.shareholder.identifier,
            }
        }
        return JsonResponse(data)
    except StockTransaction.DoesNotExist:
        return JsonResponse({'success': False, 'error': '交易記錄不存在'}, status=404)


@require_http_methods(["POST"])
def create_transaction_api(request):
    """API: 新增交易"""
    try:
        with db_transaction.atomic():
            company_id = request.POST.get('company_id')
            shareholder_id = request.POST.get('shareholder_id')
            
            # 獲取或創建公司持股關係
            company_holding, created = CompanyShareholding.objects.get_or_create(
                company_id=company_id,
                shareholder_id=shareholder_id
            )
            
            # 創建交易
            trans = StockTransaction.objects.create(
                company_holding=company_holding,
                transaction_date=request.POST.get('transaction_date'),
                description=request.POST.get('description', ''),
                transaction_type=request.POST.get('transaction_type'),
                stock_type=request.POST.get('stock_type', 'common'),
                par_value=request.POST.get('par_value', 10),
                quantity=request.POST.get('quantity'),
                stock_amount=request.POST.get('stock_amount', 0),
                amount=request.POST.get('amount') or None,
                note=request.POST.get('note', '')
            )
            
            return JsonResponse({
                'success': True,
                'message': '交易記錄已成功新增',
                'transaction_id': trans.id
            })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def update_transaction_api(request, pk):
    """API: 更新交易"""
    try:
        trans = StockTransaction.objects.get(pk=pk)
        
        with db_transaction.atomic():
            # 更新持股關係（如果公司或股東改變）
            company_id = request.POST.get('company_id')
            shareholder_id = request.POST.get('shareholder_id')
            
            if (str(trans.company_holding.company.id) != company_id or 
                str(trans.company_holding.shareholder.id) != shareholder_id):
                company_holding, created = CompanyShareholding.objects.get_or_create(
                    company_id=company_id,
                    shareholder_id=shareholder_id
                )
                trans.company_holding = company_holding
            
            # 更新其他欄位
            trans.transaction_date = request.POST.get('transaction_date')
            trans.description = request.POST.get('description', '')
            trans.transaction_type = request.POST.get('transaction_type')
            trans.stock_type = request.POST.get('stock_type', 'common')
            trans.par_value = request.POST.get('par_value', 10)
            trans.quantity = request.POST.get('quantity')
            trans.stock_amount = request.POST.get('stock_amount', 0)
            trans.amount = request.POST.get('amount') or None
            trans.note = request.POST.get('note', '')
            
            trans.save()
            
            return JsonResponse({
                'success': True,
                'message': '交易記錄已更新'
            })
    except StockTransaction.DoesNotExist:
        return JsonResponse({'success': False, 'error': '交易記錄不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def search_shareholders_api(request):
    """API: 搜尋股東"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'shareholders': []})
    
    # Search by name or identifier
    shareholders = Shareholder.objects.filter(
        Q(name__icontains=query) | Q(identifier__icontains=query)
    )[:20]  # Limit to 20 results
    
    data = {
        'shareholders': [
            {
                'id': s.id,
                'name': s.name,
                'identifier': s.identifier,
            }
            for s in shareholders
        ]
    }
    
    return JsonResponse(data)

