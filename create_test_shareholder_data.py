"""
Test script to create sample shareholder data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartfirm_project.settings')
django.setup()

from datetime import date, timedelta
from admin_module.models import BasicInformation
from registration.models import Shareholder, StockTransaction

def create_test_data():
    """Create test data for shareholder registry"""
    
    # Get or create a test company
    company, created = BasicInformation.objects.get_or_create(
        companyId='12345678',
        defaults={
            'companyName': '測試股份有限公司',
            'contact': '張三',
            'registration_address': '台北市信義區信義路五段7號',
            'email': 'test@example.com',
            'phone': '02-2345-6789'
        }
    )
    
    if created:
        print(f"✓ Created test company: {company.companyName}")
    else:
        print(f"✓ Using existing company: {company.companyName}")
    
    # Create shareholders
    shareholders_data = [
        {
            'name': '王大明',
            'identifier': 'A123456789',
            'phone': '0912-345-678',
            'email': 'wang@example.com',
            'address': '台北市大安區敦化南路一段100號'
        },
        {
            'name': '李小華',
            'identifier': 'B987654321',
            'phone': '0923-456-789',
            'email': 'li@example.com',
            'address': '新北市板橋區文化路二段200號'
        },
        {
            'name': '陳美玲',
            'identifier': 'C147258369',
            'phone': '0934-567-890',
            'email': 'chen@example.com',
            'address': '台中市西屯區台灣大道三段300號'
        },
    ]
    
    shareholders = []
    for sh_data in shareholders_data:
        shareholder, created = Shareholder.objects.get_or_create(
            company=company,
            identifier=sh_data['identifier'],
            defaults={
                'name': sh_data['name'],
                'phone': sh_data['phone'],
                'email': sh_data['email'],
                'address': sh_data['address']
            }
        )
        shareholders.append(shareholder)
        if created:
            print(f"✓ Created shareholder: {shareholder.name}")
        else:
            print(f"✓ Using existing shareholder: {shareholder.name}")
    
    # Create transactions for each shareholder
    print("\nCreating transactions...")
    
    # Shareholder 1 (王大明) - Original founder with majority stake
    transactions = [
        {
            'shareholder': shareholders[0],
            'date': date(2024, 1, 1),
            'type': 'founding',
            'quantity': 50000,
            'amount': 500000,
            'note': '公司設立時原始股'
        },
        {
            'shareholder': shareholders[0],
            'date': date(2025, 6, 1),
            'type': 'capital_increase',
            'quantity': 10000,
            'amount': 100000,
            'note': '增資入股'
        },
    ]
    
    # Shareholder 2 (李小華) - Second founder
    transactions.extend([
        {
            'shareholder': shareholders[1],
            'date': date(2024, 1, 1),
            'type': 'founding',
            'quantity': 30000,
            'amount': 300000,
            'note': '公司設立時原始股'
        },
        {
            'shareholder': shareholders[1],
            'date': date(2025, 3, 15),
            'type': 'transfer_out',
            'quantity': -5000,
            'amount': 60000,
            'note': '轉讓給陳美玲'
        },
    ])
    
    # Shareholder 3 (陳美玲) - New investor
    transactions.extend([
        {
            'shareholder': shareholders[2],
            'date': date(2024, 1, 1),
            'type': 'founding',
            'quantity': 20000,
            'amount': 200000,
            'note': '公司設立時原始股'
        },
        {
            'shareholder': shareholders[2],
            'date': date(2025, 3, 15),
            'type': 'transfer_in',
            'quantity': 5000,
            'amount': 60000,
            'note': '從李小華受讓'
        },
    ])
    
    for trans in transactions:
        transaction, created = StockTransaction.objects.get_or_create(
            shareholder=trans['shareholder'],
            transaction_date=trans['date'],
            transaction_type=trans['type'],
            defaults={
                'quantity': trans['quantity'],
                'amount': trans['amount'],
                'note': trans['note']
            }
        )
        if created:
            print(f"✓ Created transaction: {transaction}")
    
    print("\n" + "="*60)
    print("Test data creation completed!")
    print("="*60)
    print(f"\nCompany: {company.companyName} ({company.companyId})")
    print(f"Total Shareholders: {Shareholder.objects.filter(company=company).count()}")
    print(f"Total Transactions: {StockTransaction.objects.filter(shareholder__company=company).count()}")
    
    # Calculate current positions
    print("\n" + "-"*60)
    print("Current shareholding positions:")
    print("-"*60)
    
    from registration.utils import get_shareholder_balance
    
    total_shares = 0
    for shareholder in shareholders:
        balance = get_shareholder_balance(shareholder.id)
        total_shares += balance
        print(f"{shareholder.name:10} : {balance:7,} shares")
    
    print("-"*60)
    print(f"{'Total':10} : {total_shares:7,} shares")
    print("\n✓ You can now test the system at: /registration/shareholder-roster/")

if __name__ == '__main__':
    create_test_data()
