from django.contrib import admin
from .models import Shareholder, CompanyShareholding, StockTransaction


@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ['name', 'identifier', 'phone', 'email', 'created_at']
    search_fields = ['name', 'identifier', 'phone', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CompanyShareholding)
class CompanyShareholdingAdmin(admin.ModelAdmin):
    list_display = ['shareholder', 'company', 'created_at']
    search_fields = ['shareholder__name', 'shareholder__identifier', 'company__companyName']
    list_filter = ['company', 'created_at']
    readonly_fields = ['created_at']


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['company_holding', 'transaction_date', 'transaction_type', 'quantity', 'amount']
    search_fields = ['company_holding__shareholder__name', 'company_holding__company__companyName']
    list_filter = ['transaction_type', 'transaction_date']
    readonly_fields = ['created_at', 'updated_at']
