from django.urls import path
from . import views
from . import transaction_views

app_name = 'shareholders'

urlpatterns = [
    # Shareholder roster and management
    path('roster/', views.ShareholderRosterView.as_view(), name='roster'),
    path('detail/<int:shareholder_id>/', views.ShareholderDetailView.as_view(), name='detail'),
    path('list/', views.ShareholderListView.as_view(), name='list'),
    
    # Shareholder API endpoints
    path('api/get/<int:pk>/', views.get_shareholder_api, name='api_get'),
    path('api/update/<int:pk>/', views.update_shareholder_api, name='api_update'),
    path('api/create/', views.create_shareholder_api, name='api_create'),
    path('api/search/', transaction_views.search_shareholders_api, name='api_search'),
    
    # New Roster Timeline APIs
    path('api/company/<int:company_id>/transactions/', views.get_company_transactions_api, name='api_company_transactions'),
    path('api/company/<int:company_id>/roster/<str:target_date>/', views.get_roster_snapshot_api, name='api_roster_snapshot'),

    # Stock Transaction management
    path('transactions/', transaction_views.StockTransactionListView.as_view(), name='transaction_list'),
    path('api/transaction/get/<int:pk>/', transaction_views.get_transaction_api, name='api_get_transaction'),
    path('api/transaction/create/', transaction_views.create_transaction_api, name='api_create_transaction'),
    path('api/transaction/update/<int:pk>/', transaction_views.update_transaction_api, name='api_update_transaction'),
]
