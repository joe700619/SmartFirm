from django.urls import path, include
from django.views.generic import RedirectView

app_name = 'registration'

urlpatterns = [
    # Sub-modules
    path('shareholders/', include('registration.shareholders.urls')),
    path('progress/', include('registration.progress.urls')),
    path('board/', include('registration.board.urls')),
    path('misc/', include('registration.misc.urls')),
    
    # Redirects for old URLs (backward compatibility)
    path('shareholder-roster/', RedirectView.as_view(
        pattern_name='registration:shareholders:roster', 
        permanent=True
    ), name='shareholder_roster'),
    
    path('shareholder-edit/', RedirectView.as_view(
        pattern_name='registration:shareholders:list',
        permanent=True
    ), name='shareholder_edit'),
    
    path('shareholder/<int:shareholder_id>/', RedirectView.as_view(
        pattern_name='registration:shareholders:detail',
        permanent=True
    ), name='shareholder_detail'),
    
    # Old API endpoints redirects
    path('api/shareholder/<int:pk>/', RedirectView.as_view(
        pattern_name='registration:shareholders:api_get',
        permanent=True
    ), name='get_shareholder_api'),
    
    path('api/shareholder/update/<int:pk>/', RedirectView.as_view(
        pattern_name='registration:shareholders:api_update',
        permanent=True
    ), name='update_shareholder_api'),
    
    path('api/shareholder/create/', RedirectView.as_view(
        pattern_name='registration:shareholders:api_create',
        permanent=True
    ), name='create_shareholder_api'),
]
