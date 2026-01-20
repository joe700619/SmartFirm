"""
案件進度追蹤視圖
"""
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ProgressDashboardView(LoginRequiredMixin, View):
    """案件進度看板 (Kanban)"""
    
    def get(self, request):
        """顯示案件看板"""
        context = {
            'title': '案件進度追蹤',
        }
        return render(request, 'progress/dashboard.html', context)


class CaseListView(LoginRequiredMixin, View):
    """案件列表視圖"""
    
    def get(self, request):
        """顯示所有案件"""
        # TODO: 從models獲取案件資料
        context = {
            'title': '案件列表',
            'cases': [],  # 待實作
        }
        return render(request, 'progress/list.html', context)
