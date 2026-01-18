from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # 客戶管理
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # API
    path('api/customer-data/', views.get_customer_data, name='get_customer_data'),
    path('api/search-customers/', views.search_customers, name='search_customers'),
    
    # 查帳紀錄管理
    path('tax-audit/', views.tax_audit_list, name='tax_audit_list'),
    path('tax-audit/create/', views.tax_audit_create, name='tax_audit_create'),
    path('tax-audit/<int:pk>/update/', views.tax_audit_update, name='tax_audit_update'),
    path('tax-audit/<int:pk>/delete/', views.tax_audit_delete, name='tax_audit_delete'),
    
    # VAT 申報記錄管理
    path('vat/', views.vat_record_list, name='vat_record_list'),
    path('vat/customer/<int:customer_id>/edit/', views.vat_record_edit, name='vat_record_edit_by_customer'),
    path('vat/<int:pk>/edit/', views.vat_record_edit, name='vat_record_edit'),
    path('vat/<int:pk>/delete/', views.vat_record_delete, name='vat_record_delete'),
    
    # 所得稅申報記錄管理
    path('income-tax/', views.income_tax_list, name='income_tax_list'),
    path('income-tax/customer/<int:customer_id>/edit/', views.income_tax_edit_by_customer, name='income_tax_edit_by_customer'),
    
    # 下載資料管理
    path('download-data/', views.download_data_list, name='download_data_list'),
    path('download-data/create/', views.download_data_create, name='download_data_create'),
    path('download-data/<int:pk>/edit/', views.download_data_edit, name='download_data_edit'),
    path('download-data/<int:pk>/delete/', views.download_data_delete, name='download_data_delete'),
    
    # 客戶通知API
    path('api/notify-customer/<str:record_type>/<int:pk>/', views.notify_customer, name='notify_customer'),
]
