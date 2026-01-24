from django.contrib import admin
from .models import Shareholder, CompanyShareholding, StockTransaction, BoardMember


class SoftDeleteAdmin(admin.ModelAdmin):
    """支援軟刪除的 Admin"""
    list_filter = ['is_deleted']
    actions = ['restore_deleted_items']

    def get_queryset(self, request):
        """顯示所有項目（包含已刪除），以便從垃圾桶救回"""
        # 使用 un-filtered 的 manager (如果有的話)，這裡直接用 objects 
        # 因為我們還沒在 Model 層強制過濾 objects，所以這裡預設會看到全部
        return super().get_queryset(request)

    @admin.action(description='還原已刪除的項目')
    def restore_deleted_items(self, request, queryset):
        # 批量還原
        updated_count = queryset.update(is_deleted=False)
        self.message_user(request, f"已成功還原 {updated_count} 筆資料。")


@admin.register(Shareholder)
class ShareholderAdmin(SoftDeleteAdmin):
    list_display = ['name', 'identifier', 'phone', 'email', 'created_at', 'is_deleted']
    search_fields = ['name', 'identifier', 'phone', 'email']
    list_filter = ['is_deleted', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by']


@admin.register(CompanyShareholding)
class CompanyShareholdingAdmin(SoftDeleteAdmin):
    list_display = ['shareholder', 'company', 'created_at', 'is_deleted']
    search_fields = ['shareholder__name', 'shareholder__identifier', 'company__companyName']
    list_filter = ['is_deleted', 'company', 'created_at']
    readonly_fields = ['created_at', 'created_by']


@admin.register(StockTransaction)
class StockTransactionAdmin(SoftDeleteAdmin):
    list_display = ['company_holding', 'transaction_date', 'transaction_type', 'quantity', 'amount', 'is_deleted']
    search_fields = ['company_holding__shareholder__name', 'company_holding__company__companyName']
    list_filter = ['is_deleted', 'transaction_type', 'transaction_date']
    readonly_fields = ['created_at', 'updated_at', 'created_by']


@admin.register(BoardMember)
class BoardMemberAdmin(SoftDeleteAdmin):
    list_display = ['company', 'title', 'person', 'representative_of', 'is_deleted']
    search_fields = ['company__companyName', 'person__name', 'person__identifier']
    list_filter = ['is_deleted', 'title', 'company']
    # autocomplete_fields = ['person', 'representative_of', 'company']
    raw_id_fields = ['person', 'representative_of', 'company']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
