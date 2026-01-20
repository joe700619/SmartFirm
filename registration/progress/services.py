"""
案件進度追蹤業務邏輯
"""
from datetime import date, timedelta
from django.core.mail import send_mail


def check_case_overdue(case_filing_date, expected_days):
    """
    檢查案件是否逾期
    
    Args:
        case_filing_date: 案件提交日期
        expected_days: 預計處理天數
    
    Returns:
        bool: True=逾期, False=未逾期
    """
    deadline = case_filing_date + timedelta(days=expected_days)
    return date.today() > deadline


def calculate_remaining_days(case_filing_date, expected_days):
    """
    計算案件剩餘處理天數
    
    Args:
        case_filing_date: 案件提交日期
        expected_days: 預計處理天數
    
    Returns:
        int: 剩餘天數（負數表示逾期）
    """
    deadline = case_filing_date + timedelta(days=expected_days)
    remaining = (deadline - date.today()).days
    return remaining


def send_progress_notification(case_id, recipient_email, message):
    """
    發送進度更新通知
    
    Args:
        case_id: 案件ID
        recipient_email: 收件人email
        message: 通知訊息
    """
    subject = f'案件進度更新通知 - 案號 #{case_id}'
    
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@smartfirm.com',
        recipient_list=[recipient_email],
        fail_silently=False,
    )


def get_case_statistics():
    """
    取得案件統計資料
    
    Returns:
        dict: 各狀態案件數量
    """
    # TODO: 實作從資料庫取得統計
    return {
        'pending': 0,
        'processing': 0,
        'review': 0,
        'approved': 0,
        'completed': 0,
    }
