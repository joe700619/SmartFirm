from django.urls import path
from .views import SystemParameterUpdateView

urlpatterns = [
    path('', SystemParameterUpdateView.as_view(), name='system_parameters'),
]
