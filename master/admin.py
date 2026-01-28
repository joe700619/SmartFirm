from django.contrib import admin
from .models import ServiceItem, KnowledgeNote, CaseType

@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('service_code', 'service_name', 'reference_price', 'department')
    search_fields = ('service_code', 'service_name')

@admin.register(KnowledgeNote)
class KnowledgeNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'created_at')
    search_fields = ('title', 'tags')
    list_filter = ('created_at',)

@admin.register(CaseType)
class CaseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
