from django.urls import path
from . import views

app_name = 'misc'

urlpatterns = [
    path('name-precheck/', views.NamePreCheckView.as_view(), name='name_precheck'),
    path('seal-management/', views.SealManagementView.as_view(), name='seal_management'),
]
