"""
雜項功能視圖
"""
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class NamePreCheckView(LoginRequiredMixin, View):
    """公司名稱預查視圖"""
    
    def get(self, request):
        """顯示名稱預查表單"""
        context = {
            'title': '公司名稱預查',
        }
        return render(request, 'misc/name_precheck.html', context)


class SealManagementView(LoginRequiredMixin, View):
    """印鑑管理視圖"""
    
    def get(self, request):
        """顯示印鑑管理頁面"""
        context = {
            'title': '印鑑管理',
        }
        return render(request, 'misc/seal_management.html', context)
