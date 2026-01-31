from django.contrib import admin
from .models import PaymentProvider, PaymentTransaction

@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('merchant_trade_no', 'provider', 'amount', 'currency', 'status', 'payment_time')
    list_filter = ('status', 'provider', 'currency')
    search_fields = ('merchant_trade_no', 'trade_no')
    readonly_fields = ('created_at', 'updated_at')
