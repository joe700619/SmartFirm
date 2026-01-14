from django.shortcuts import render

def index(request):
    """Dashboard 首頁視圖"""
    return render(request, 'dashboard/index.html')
