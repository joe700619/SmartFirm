from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:pk>/', views.mandate_update, name='update'),
    path('detail/<int:pk>/', views.MandateDetailView.as_view(), name='detail'),
]
