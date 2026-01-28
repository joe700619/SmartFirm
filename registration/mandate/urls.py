from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:pk>/', views.mandate_update, name='update'),
]
