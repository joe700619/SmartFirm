from django.urls import path, include

app_name = 'master'

urlpatterns = [
    path('', include('master.service_item.urls')),
]
