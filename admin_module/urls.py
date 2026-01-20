from django.urls import path
from . import views

app_name = 'admin_module'

urlpatterns = [
    # 客戶管理功能
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # 聯絡人管理功能
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/update/', views.contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # API
    path('api/contacts/', views.api_contacts, name='api_contacts'),
    path('api/customer-info/', views.api_customer_info, name='api_customer_info'),
    path('api/search-companies/', views.search_companies_api, name='api_search_companies'),
    
    # 收文系統
    path('incoming-mails/', views.incoming_mail_list, name='incoming_mail_list'),
    path('incoming-mails/create/', views.incoming_mail_create, name='incoming_mail_create'),
    path('incoming-mails/<int:pk>/update/', views.incoming_mail_update, name='incoming_mail_update'),
    path('incoming-mails/<int:pk>/delete/', views.incoming_mail_delete, name='incoming_mail_delete'),
    
    # 客戶增減管理
    path('customer-changes/', views.customer_change_list, name='customer_change_list'),
    path('customer-changes/create/', views.customer_change_create, name='customer_change_create'),
    path('customer-changes/<int:pk>/update/', views.customer_change_update, name='customer_change_update'),
    path('customer-changes/<int:pk>/delete/', views.customer_change_delete, name='customer_change_delete'),
    
    # 營業稅檢查管理
    path('vat-checks/', views.vat_check_list, name='vat_check_list'),
    path('vat-checks/create/', views.vat_check_create, name='vat_check_create'),
    path('vat-checks/<int:pk>/update/', views.vat_check_update, name='vat_check_update'),
    path('vat-checks/<int:pk>/delete/', views.vat_check_delete, name='vat_check_delete'),
    
    # 記帳進度檢查管理
    path('bookkeeping-checklists/', views.bookkeeping_checklist_list, name='bookkeeping_checklist_list'),
    path('bookkeeping-checklists/create/', views.bookkeeping_checklist_create, name='bookkeeping_checklist_create'),
    path('bookkeeping-checklists/<int:pk>/update/', views.bookkeeping_checklist_update, name='bookkeeping_checklist_update'),
    path('bookkeeping-checklists/<int:pk>/delete/', views.bookkeeping_checklist_delete, name='bookkeeping_checklist_delete'),
]

