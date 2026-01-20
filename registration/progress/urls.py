from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('dashboard/', views.ProgressDashboardView.as_view(), name='dashboard'),
    path('list/', views.CaseListView.as_view(), name='list'),
]
