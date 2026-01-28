from django.urls import path
from .views import (
    ServiceItemListView,
    ServiceItemCreateView,
    ServiceItemUpdateView,
    ServiceItemDeleteView
)

urlpatterns = [
    path('service-items/', ServiceItemListView.as_view(), name='serviceitem_list'),
    path('service-items/add/', ServiceItemCreateView.as_view(), name='serviceitem_add'),
    path('service-items/<int:pk>/edit/', ServiceItemUpdateView.as_view(), name='serviceitem_edit'),
    path('service-items/<int:pk>/delete/', ServiceItemDeleteView.as_view(), name='serviceitem_delete'),
]
