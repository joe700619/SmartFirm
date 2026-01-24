from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('list/', views.BoardMemberListView.as_view(), name='list'),
    path('api/create/', views.create_board_member_api, name='api_create'),
    path('api/update/<int:pk>/', views.update_board_member_api, name='api_update'),
    path('api/get/<int:pk>/', views.get_board_member_api, name='api_get'),
]
