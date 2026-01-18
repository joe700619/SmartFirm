# booking/utils.py
"""
Utility functions for booking app
"""
from .models import DownloadData, VATRecord, IncomeTaxRecord
from django.utils import timezone


def create_or_update_download_data(record, record_type='vat'):
    """
    建立或更新下載資料
    
    Args:
        record: VATRecord 或 IncomeTaxRecord 實例
        record_type: 'vat' 或 'income_tax'
    
    Returns:
        DownloadData 實例
    """
    # 決定種類代碼
    category_code = 'V' if record_type == 'vat' else 'T'
    
    # 取得客戶資訊
    customer = record.customer
    
    # 建立檔案編號：統一編號+種類+年度+期別
    if record_type == 'vat':
        file_number = f"{customer.company_id}{category_code}{record.filing_year}{record.filing_period}"
        period = record.get_filing_period_display()
        category = 'vat'
    else:  # income_tax
        file_number = f"{customer.company_id}{category_code}{record.filing_year}"
        period = f"{record.filing_year}年度"
        category = 'income_tax'
    
    # 對應 Payment Method
    # VAT: customer_paid, office_paid, not_replied
    # Download: customer, office, no_reply
    payment_map = {
        'customer_paid': 'customer',
        'office_paid': 'office',
        'not_replied': 'no_reply'
    }
    
    payment_method = None
    if record_type == 'vat' and hasattr(record, 'tax_payment_completed'):
        # 嘗試直接對應
        payment_method = payment_map.get(record.tax_payment_completed)
        # 如果對應不到，可能是已經相同的代碼（使用者修改過），嘗試直接賦值
        if not payment_method and record.tax_payment_completed in payment_map.values():
            payment_method = record.tax_payment_completed

    # 對應 Source
    # 由於使用者已將 VATRecord 的選項修改為與 DownloadData 一致 (google, manual, na)
    # 我們優先嘗試直接賦值
    source = 'manual'
    if hasattr(record, 'source') and record.source:
        source = record.source
    
    # 為了調試日期問題，我們打印日誌
    print(f"Transferring Data for {file_number}:")
    print(f"Source: {source}")
    print(f"Payment Method: {payment_method}")
    if hasattr(record, 'invoice_received_date'):
        print(f"Invoice Date: {record.invoice_received_date}")
    if hasattr(record, 'reply_time'):
        print(f"Reply Time: {record.reply_time}")
    if hasattr(record, 'tax_deadline'):
        print(f"Tax Deadline: {record.tax_deadline}")

    # 檢查是否已存在
    download_data, created = DownloadData.objects.update_or_create(
        file_number=file_number,
        defaults={
            'year': record.filing_year,
            'period': period if record_type == 'vat' else str(record.filing_year),
            'category': category,
            'company_id': customer.company_id,
            'company_name': customer.company_name,
            'email': customer.email if hasattr(customer, 'email') else None,
            'status': 'current',
            'source': source,
            # 日期欄位
            'invoice_received_date': record.invoice_received_date if hasattr(record, 'invoice_received_date') else None,
            'reply_time': record.reply_time if hasattr(record, 'reply_time') else None,
            'tax_deadline': record.tax_deadline if hasattr(record, 'tax_deadline') else None,
            # 其他資訊欄位
            'payment_method': payment_method,
            'declaration_url': record.declaration_url if hasattr(record, 'declaration_url') else None,
            'payment_slip_url': record.payment_slip_url if hasattr(record, 'payment_slip_url') else None,
        }
    )
    
    return download_data, created


def notify_customer_and_save(record, record_type='vat'):
    """
    通知客戶並儲存到下載資料
    
    Args:
        record: VATRecord 或 IncomeTaxRecord 實例
        record_type: 'vat' 或 'income_tax'
    
    Returns:
        tuple: (success, message, download_data)
    """
    try:
        download_data, created = create_or_update_download_data(record, record_type)
        
        customer_name = record.customer.company_name
        action = "已建立" if created else "已更新"
        
        message = f"{customer_name} 本期資料已傳送（下載資料{action}）"
        
        return True, message, download_data
    
    except Exception as e:
        return False, f"傳送失敗：{str(e)}", None
