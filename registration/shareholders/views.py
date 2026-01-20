from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from datetime import date
from admin_module.models import BasicInformation
from registration.models import Shareholder, CompanyShareholding, StockTransaction
from .services import get_company_roster, get_shareholder_transaction_history


class ShareholderRosterView(View):
    """股東名冊查詢視圖"""
    
    def get(self, request):
        """顯示查詢表單和結果"""
        companies = BasicInformation.objects.all().order_by('companyName')
        
        context = {
            'companies': companies,
        }
        
        return render(request, 'shareholders/roster.html', context)


class ShareholderDetailView(View):
    """股東明細查詢視圖（交易歷史）"""
    
    def get(self, request, shareholder_id):
        """顯示股東交易歷史"""
        # Note: This needs to be updated to work with new model structure
        # For now, redirecting to shareholder list
        return redirect('registration:shareholders:list')


class ShareholderListView(View):
    """股東管理列表視圖"""
    
    def get(self, request):
        """顯示所有股東列表"""
        shareholders = Shareholder.objects.all().order_by('name')
        
        context = {
            'shareholders': shareholders,
        }
        
        return render(request, 'shareholders/list.html', context)


@require_http_methods(["GET"])
def get_company_transactions_api(request, company_id):
    """API: 取得公司的股權交易歷史 (Timeline)，合併同一天同一類型的交易"""
    try:
        # Get all transactions for this company
        transactions = StockTransaction.objects.filter(
            company_holding__company_id=company_id
        ).select_related('company_holding__shareholder').order_by('-transaction_date', '-created_at')
        
        # Group transactions by date and type
        timeline_data = []
        seen_events = set()
        
        for tx in transactions:
            event_key = f"{tx.transaction_date}_{tx.transaction_type}"
            
            if event_key not in seen_events:
                timeline_data.append({
                    'id': f"group_{tx.transaction_date}_{tx.transaction_type}", # Use a group key
                    'date': tx.transaction_date.isoformat(),
                    'type': tx.get_transaction_type_display(),
                    # 'amount': tx.amount, # Amount might be ambiguous if summed, showing basic info
                    'description': tx.transaction_type
                })
                seen_events.add(event_key)
            
        return JsonResponse({
            'success': True,
            'timeline': timeline_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def get_roster_snapshot_api(request, company_id, target_date):
    """API: 取得特定日期的股東名冊快照"""
    try:
        date_obj = date.fromisoformat(target_date)
        roster = get_company_roster(company_id, date_obj)
        
        # Serialize for JSON
        roster_data = []
        for item in roster:
            roster_data.append({
                'id': item['shareholder'].id,
                'name': item['shareholder'].name,
                'identifier': item['shareholder'].identifier,
                'phone': item['shareholder'].phone,
                'email': item['shareholder'].email,
                'stock_type': item['stock_type_display'], 
                'balance': item['balance'],
                'amount': item['amount'],
                'percentage': item['percentage']
            })
            
        total_shares = sum(item['balance'] for item in roster_data)
        total_capital = sum(item['amount'] for item in roster_data)
        
        return JsonResponse({
            'success': True,
            'roster': roster_data,
            'total_shares': total_shares,
            'total_capital': total_capital,
            'target_date': target_date
        })
    except ValueError:
        return JsonResponse({'success': False, 'error': '無效的日期格式'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def get_shareholder_api(request, pk):
    """API: 取得單一股東資料"""
    try:
        shareholder = Shareholder.objects.get(pk=pk)
        data = {
            'success': True,
            'shareholder': {
                'id': shareholder.id,
                'name': shareholder.name,
                'identifier': shareholder.identifier,
                'phone': shareholder.phone or '',
                'email': shareholder.email or '',
                'address': shareholder.address or '',
            }
        }
        return JsonResponse(data)
    except Shareholder.DoesNotExist:
        return JsonResponse({'success': False, 'error': '股東不存在'}, status=404)


@require_http_methods(["POST"])
def update_shareholder_api(request, pk):
    """API: 更新股東資料"""
    try:
        shareholder = Shareholder.objects.get(pk=pk)
        
        # Update fields
        shareholder.name = request.POST.get('name', shareholder.name)
        shareholder.phone = request.POST.get('phone', '')
        shareholder.email = request.POST.get('email', '')
        shareholder.address = request.POST.get('address', '')
        
        shareholder.save()
        
        return JsonResponse({
            'success': True,
            'message': '股東資料已更新'
        })
    except Shareholder.DoesNotExist:
        return JsonResponse({'success': False, 'error': '股東不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def create_shareholder_api(request):
    """API: 新增股東"""
    try:
        # Validate required fields
        name = request.POST.get('name')
        identifier = request.POST.get('identifier')
        
        if not all([name, identifier]):
            return JsonResponse({
                'success': False,
                'error': '請填寫所有必填欄位（姓名、身分證字號/統一編號）'
            }, status=400)
        
        # Create shareholder
        shareholder = Shareholder.objects.create(
            identifier=identifier,
            name=name,
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': '股東已成功新增',
            'shareholder_id': shareholder.id
        })
    except IntegrityError:
        return JsonResponse({
            'success': False, 
            'error': '此身分證字號/統一編號已存在'
        }, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
