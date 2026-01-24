from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('employee_id', 'name', 'status', 'group', 'job_title', 'is_deleted')
    
    # Filter options
    list_filter = ('is_deleted', 'status', 'group')
    
    # Search fields
    search_fields = ('name', 'employee_id', 'id_number')
    
    # Allow editable fields directly in list view (optional, useful for quick restore)
    list_editable = ('is_deleted', 'status')
    
    # Ordering
    ordering = ('employee_id',)
