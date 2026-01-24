"""
Backward Compatible Views - Redirects to new modular views
這些 views 保留用於向後相容舊的 URL 路徑
"""

# Import views from new modular structure
from .customer import views as customer_views
from .contact import views as contact_views
from .incoming_mail import views as incoming_mail_views
from .customer_change import views as customer_change_views
from .vat_check import views as vat_check_views
from .booking_check import views as booking_check_views

# Customer views (backward compatible)
customer_list = customer_views.list
customer_create = customer_views.create
customer_update = customer_views.update
customer_delete = customer_views.delete

# Contact views (backward compatible)
contact_list = contact_views.list
contact_create = contact_views.create
contact_update = contact_views.update
contact_delete = contact_views.delete

# API endpoints (still in old structure, will keep here)
from django.http import JsonResponse
from .models import Contact, BasicInformation
from django.db.models import Q

def api_contacts(request):
    """API: 根據公司統編取得聯絡人列表"""
    company_id = request.GET.get('company_id', '').strip()
    
    if not company_id:
        return JsonResponse([], safe=False)
    
    contacts = Contact.objects.filter(company_id=company_id, is_deleted=False).values(
        'id', 'name', 'position', 'email', 'phone', 'mobile', 'fax', 'address'
    )
    
    return JsonResponse(list(contacts), safe=False)


def api_customer_info(request):
    """API: 根據統一編號取得客戶資料"""
    company_id = request.GET.get('company_id', '').strip()
    
    if not company_id:
        return JsonResponse({'error': 'Missing company_id'}, status=400)
    
    try:
        customer = BasicInformation.objects.get(companyId=company_id, is_deleted=False)
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
        Q(companyName__icontains=query) | Q(companyId__icontains=query),
        is_deleted=False
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

# Incoming Mail views (backward compatible)
incoming_mail_list = incoming_mail_views.list
incoming_mail_create = incoming_mail_views.create
incoming_mail_update = incoming_mail_views.update
incoming_mail_delete = incoming_mail_views.delete

# Customer Change views (backward compatible)
customer_change_list = customer_change_views.list
customer_change_create = customer_change_views.create
customer_change_update = customer_change_views.update
customer_change_delete = customer_change_views.delete

# VAT Check views (backward compatible)
vat_check_list = vat_check_views.list
vat_check_create = vat_check_views.create
vat_check_update = vat_check_views.update
vat_check_delete = vat_check_views.delete

# Bookkeeping Checklist views (backward compatible)
bookkeeping_checklist_list = booking_check_views.list
bookkeeping_checklist_create = booking_check_views.create
bookkeeping_checklist_update = booking_check_views.update
bookkeeping_checklist_delete = booking_check_views.delete
