from django.urls import path
from . import views
from .views import (
    RegistrationProgressListView,
    RegistrationProgressCreateView,
    RegistrationProgressUpdateView,
    RegistrationProgressDeleteView
)

app_name = 'progress'

urlpatterns = [
    path('list/', RegistrationProgressListView.as_view(), name='list'),
    path('add/', RegistrationProgressCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', RegistrationProgressUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', RegistrationProgressDeleteView.as_view(), name='delete'),
    
    # AJAX
    path('api/company-details/', views.get_company_details, name='api_company_details'),
    path('api/contact-details/', views.get_contact_details, name='api_contact_details'),
    path('api/service-details/', views.get_service_details, name='api_service_details'),
    path('api/search-services/', views.search_services, name='api_search_services'),
    path('api/search-contacts/', views.search_contacts, name='api_search_contacts'),
    path('api/search-employees/', views.search_employees, name='api_search_employees'),
    path('create-knowledge-note/', views.create_knowledge_note, name='create_knowledge_note'),
]
