from django.contrib import admin
from .models import (
    BasicInformation, Contact, IncomingMail, IncomingMailItem, 
    CustomerChange, VATCheck, VATCheckItem, BookkeepingChecklist
)


@admin.register(BasicInformation)
class BasicInformationAdmin(admin.ModelAdmin):
    list_display = ['companyName', 'companyId', 'contact', 'phone', 'is_deleted', 'created_at']
    search_fields = ['companyName', 'companyId', 'contact', 'phone']
    list_filter = ['is_deleted', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'phone', 'email', 'is_deleted', 'created_at']
    search_fields = ['name', 'company_name', 'phone', 'email']
    list_filter = ['is_deleted', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


class IncomingMailItemInline(admin.TabularInline):
    model = IncomingMailItem
    extra = 1


@admin.register(IncomingMail)
class IncomingMailAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'date', 'is_deleted', 'created_at']
    search_fields = ['serial_number', 'date']
    list_filter = ['is_deleted', 'date', 'created_at']
    inlines = [IncomingMailItemInline]
    readonly_fields = ['serial_number', 'created_at', 'updated_at']


@admin.register(CustomerChange)
class CustomerChangeAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_id', 'change_type', 'establishment_date', 'is_deleted', 'created_at']
    search_fields = ['company_name', 'company_id']
    list_filter = ['is_deleted', 'change_type', 'establishment_date', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


class VATCheckItemInline(admin.TabularInline):
    model = VATCheckItem
    extra = 1


@admin.register(VATCheck)
class VATCheckAdmin(admin.ModelAdmin):
    list_display = ['check_period', 'inspector', 'inspectee', 'status', 'is_deleted', 'date']
    search_fields = ['check_period', 'inspector', 'inspectee']
    list_filter = ['is_deleted', 'status', 'date', 'created_at']
    inlines = [VATCheckItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BookkeepingChecklist)
class BookkeepingChecklistAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_id', 'check_period', 'status', 'is_deleted', 'bookkeeper']
    search_fields = ['company_name', 'company_id', 'check_period', 'bookkeeper']
    list_filter = ['is_deleted', 'status', 'check_period', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
