from django.urls import path, include

app_name = 'hr'

urlpatterns = [
    path('', include('hr.employee.urls')),
]
