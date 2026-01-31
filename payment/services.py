import hashlib
import urllib.parse
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from master.models import SystemParameter
from .models import PaymentTransaction, PaymentProvider

class ECPayAdapter:
    def __init__(self):
        params = SystemParameter.load()
        self.merchant_id = params.ecpay_merchant_id
        self.hash_key = params.ecpay_hash_key
        self.hash_iv = params.ecpay_hash_iv
        # Use ECPay staging URL by default, or prod if configured?
        # For now hardcode staging, user can change later or we can add a config flag.
        # User requested: "MerchantTradeNo is case number", suggesting this is live or near-live.
        # But usually we need a flag. Let's assume production URL if 'PaymentProvider' says so, 
        # but since we use SystemParameter, let's stick to the standard URL 
        # https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5 (Prod)
        # https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5 (Stage)
        # We will default to PROD if not specified, or checks length of MerchantID?
        # ECPay Stage MerchantID is '2000132'.
        if self.merchant_id == '2000132':
             self.action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
        else:
             self.action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5'

    def generate_check_mac_value(self, params):
        # 1. Sort alphabetically
        sorted_keys = sorted(params.keys())
        
        # 2. Key1=Value1&Key2=Value2...
        raw = []
        for k in sorted_keys:
            raw.append(f"{k}={params[k]}")
        qs = "&".join(raw)
        
        # 3. Add HashKey and HashIV
        qs = f"HashKey={self.hash_key}&{qs}&HashIV={self.hash_iv}"
        
        # 4. Urlencode (must use quote_plus but logic is specific for .NET compatibility)
        # ECPay requires specific encoding: space -> +, but some chars unencoded.
        # Python quote_plus is close, but we need to lowercase first? 
        # Spec: "Urlencode" -> "Lowercase" -> "SHA256" -> "Uppercase"
        
        encoded = urllib.parse.quote_plus(qs).lower()
        
        # 5. Fix specific characters to match ECPay .NET encoding if needed
        # (Standard quote_plus usually works for ECPay if we just lower() it)
        # HOWEVER, ECPay spec often says: replace %2d -> -, %5f -> _, %2e -> ., %21 -> !, %2a -> *, %28 -> (, %29 -> )
        # But since we lower() everything, %2D becomes %2d.
        
        # 6. SHA256
        m = hashlib.sha256()
        m.update(encoded.encode('utf-8'))
        return m.hexdigest().upper()

    def create_payment_html(self, transaction, return_url, client_back_url=None):
        """
        Generates the HTML form to auto-submit to ECPay.
        """
        # Prepare parameters
        now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # ItemName logic: ECPay requires strict formatting.
        # User logic: "工商費用及郵資65元" or "工商服務費用"
        # We can pass this in, or derive from transaction.
        # For now, generic name.
        item_name = "工商服務費用" 

        params = {
            'MerchantID': self.merchant_id,
            'MerchantTradeNo': transaction.merchant_trade_no,
            'MerchantTradeDate': now_str,
            'PaymentType': 'aio',
            'TotalAmount': int(transaction.amount),
            'TradeDesc': 'SmartFirm Service Fee',
            'ItemName': item_name,
            'ReturnURL': return_url,  # Server-side callback
            'ChoosePayment': 'ALL',
            'EncryptType': '1',
        }
        
        if client_back_url:
            params['ClientBackURL'] = client_back_url # Button "Back to Store"
            params['OrderResultURL'] = client_back_url # Redirect after payment (if ClientRedirect is on)

        # Calculate CheckMacValue
        params['CheckMacValue'] = self.generate_check_mac_value(params)

        # Build HTML Form
        form_fields = []
        for k, v in params.items():
            form_fields.append(f'<input type="hidden" name="{k}" value="{v}" />')
        
        # Mobile-friendly redirect page with manual button fallback
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Redirecting to Payment...</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f8f9fa;
                }}
                .container {{
                    text-align: center;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    max-width: 90%;
                    width: 400px;
                }}
                .loader {{
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #3498db;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
                h3 {{ color: #333; margin-bottom: 10px; }}
                p {{ color: #666; margin-bottom: 20px; }}
                button {{
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    font-size: 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                }}
                button:hover {{ background-color: #218838; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="loader"></div>
                <h3>正在轉導至綠界支付...</h3>
                <p>請稍候，如果不自動跳轉，請點擊下方按鈕。</p>
                <form id="ecpay-form" action="{self.action_url}" method="POST">
                    {''.join(form_fields)}
                    <button type="submit">前往付款</button>
                </form>
            </div>
            <script>
                // Auto submit after a short delay to ensure UI renders
                setTimeout(function() {{
                    document.getElementById('ecpay-form').submit();
                }}, 100);
            </script>
        </body>
        </html>
        """
        return html

def create_payment(source_obj, amount, merchant_trade_no, return_url, client_back_url=None):
    """
    Facade to create transaction and return HTML.
    
    Args:
        merchant_trade_no: The base Identifier (e.g. Case Number).
                           This function will sanitize it and append a suffix to ensure
                           uniqueness for ECPay (Max 20 chars).
    """
    import re
    import random
    import string
    import time
    
    # 1. Sanitize: Remove non-alphanumeric characters
    # e.g. "RO-20260127-R001" -> "RO20260127R001"
    safe_base_no = re.sub(r'[^a-zA-Z0-9]', '', merchant_trade_no)
    
    # 2. Append Unique Suffix
    # ECPay max length is 20.
    # We reserve 6 chars for uniqueness suffix (enough for timestamp tail + random)
    # 4 chars random hex/alphanumeric allows 1.6M combinations, sufficient for retries.
    # Let's use 4 chars suffix -> Max base length = 16.
    
    max_base_len = 16
    truncated_base = safe_base_no[:max_base_len]
    
    # Generate suffix: e.g. last 2 digits of timestamp + 2 random chars
    # Or just 4 random chars.
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    final_trade_no = f"{truncated_base}{suffix}"
    
    # 3. Create Transaction Record
    provider, _ = PaymentProvider.objects.get_or_create(code='ecpay', defaults={'name': 'ECPay'})

    # Since we generate a unique suffix every time, we use .create()
    # This allows multiple attempts for the same case (history of attempts).
    tx = PaymentTransaction.objects.create(
        provider=provider,
        merchant_trade_no=final_trade_no, # Unique for ECPay
        amount=amount,
        content_type=ContentType.objects.get_for_model(source_obj),
        object_id=source_obj.pk,
        status=PaymentTransaction.Status.PENDING,
        trade_no = merchant_trade_no,  # Store the ORIGINAL case number locally
        response_data={'original_merchant_trade_no': merchant_trade_no}
    )

    # 2. Get Adapter
    adapter = ECPayAdapter()
    
    # 3. Generate HTML
    return adapter.create_payment_html(tx, return_url, client_back_url)
