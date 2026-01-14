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
    
    # 查帳紀錄管理
    path('tax-audit/', views.tax_audit_list, name='tax_audit_list'),
    path('tax-audit/create/', views.tax_audit_create, name='tax_audit_create'),
    path('tax-audit/<int:pk>/update/', views.tax_audit_update, name='tax_audit_update'),
    path('tax-audit/<int:pk>/delete/', views.tax_audit_delete, name='tax_audit_delete'),
]
