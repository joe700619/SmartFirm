from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from admin_module.models import BasicInformation
from registration.models import Shareholder, BoardMember
from datetime import datetime

class BoardMemberListView(View):
    """董監事名單視圖"""
    def get(self, request):
        # 取得所有董監事資料，包含關聯的公司和人員
        members = BoardMember.objects.select_related(
            'company', 'person', 'representative_of'
        ).order_by('company__companyId', 'title')

        context = {
            'members': members,
        }
        return render(request, 'board/list.html', context)

@require_http_methods(["GET"])
def get_board_member_api(request, pk):
    """API: 取得單一董監事資料"""
    try:
        member = BoardMember.objects.get(pk=pk)
        data = {
            'success': True,
            'member': {
                'id': member.id,
                'company_id': member.company.id,
                'company_name': member.company.companyName,
                'shareholder_id': member.person.id,
                'shareholder_name': member.person.name,
                'identifier': member.person.identifier,
                'title': member.title,
                'birthday': member.birthday.isoformat() if member.birthday else '',
                'representative_of_id': member.representative_of.id if member.representative_of else '',
                'representative_of_name': member.representative_of.name if member.representative_of else '',
            }
        }
        return JsonResponse(data)
    except BoardMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': '資料不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
def create_board_member_api(request):
    """API: 新增董監事"""
    try:
        # 必填欄位
        company_id = request.POST.get('company_id')
        shareholder_id = request.POST.get('shareholder_id')
        title = request.POST.get('title')
        
        if not all([company_id, shareholder_id, title]):
            return JsonResponse({'success': False, 'error': '請填寫所有必填欄位'}, status=400)

        # 處理日期
        birthday = request.POST.get('birthday') or None
        
        # 處理代表法人
        rep_id = request.POST.get('representative_of_id') or None
        representative_of = None
        if rep_id:
            representative_of = Shareholder.objects.get(id=rep_id)

        member = BoardMember.objects.create(
            company_id=company_id,
            person_id=shareholder_id,
            title=title,
            birthday=birthday,
            representative_of=representative_of
        )

        return JsonResponse({
            'success': True, 
            'message': '新增成功',
            'id': member.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
def update_board_member_api(request, pk):
    """API: 更新董監事"""
    try:
        member = BoardMember.objects.get(pk=pk)
        
        # 更新基本欄位
        member.company_id = request.POST.get('company_id')
        member.person_id = request.POST.get('shareholder_id')
        member.title = request.POST.get('title')
        
        # 更新選填欄位
        member.birthday = request.POST.get('birthday') or None
        
        rep_id = request.POST.get('representative_of_id') or None
        if rep_id:
            member.representative_of = Shareholder.objects.get(id=rep_id)
        else:
            member.representative_of = None
            
        member.save()

        return JsonResponse({
            'success': True, 
            'message': '更新成功'
        })
    except BoardMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': '資料不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
