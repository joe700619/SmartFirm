"""
Shareholder utilities for calculations and roster generation
"""
from django.db.models import Sum
from datetime import date
from registration.models import Shareholder, StockTransaction, CompanyShareholding


def get_shareholder_balance(company_holding_id, target_date=None, stock_type=None):
    """
    Calculate the shareholding balance and stock amount for a company holding as of a specific date.
    
    Args:
        company_holding_id: ID of the CompanyShareholding
        target_date: Date to calculate balance as of (default: today)
        stock_type: Optional stock type filter ('common' or 'preferred')
    
    Returns:
        Dict: {'shares': int, 'amount': Decimal}
    """
    if target_date is None:
        target_date = date.today()
    
    filters = {
        'company_holding_id': company_holding_id,
        'transaction_date__lte': target_date
    }
    
    if stock_type:
        filters['stock_type'] = stock_type
    
    transactions = StockTransaction.objects.filter(**filters)
    
    result = transactions.aggregate(
        total_shares=Sum('quantity'),
        total_amount=Sum('stock_amount')
    )
    
    return {
        'shares': result['total_shares'] or 0,
        'amount': result['total_amount'] or 0
    }


def get_company_roster(company_id, target_date=None):
    """
    Get the shareholder roster for a company as of a specific date, broken down by stock type.
    
    Args:
        company_id: ID of the company (BasicInformation)
        target_date: Date to calculate roster as of (default: today)
    
    Returns:
        List of dicts with shareholder info and their balance per stock type:
        [
            {
                'shareholder': Shareholder object,
                'stock_type': 'common',
                'stock_type_display': '普通股',
                'balance': int (shares held),
                'amount': Decimal (stock amount),
                'percentage': float (ownership percentage)
            },
            ...
        ]
    """
    if target_date is None:
        target_date = date.today()
    
    # Get all shareholdings for this company
    company_holdings = CompanyShareholding.objects.filter(
        company_id=company_id
    ).select_related('shareholder')
    
    roster = []
    total_shares = 0
    
    # Define stock types to check
    stock_types = [
        ('common', '普通股'),
        ('preferred', '特別股')
    ]
    
    for holding in company_holdings:
        for s_type, s_type_display in stock_types:
            result = get_shareholder_balance(holding.id, target_date, stock_type=s_type)
            balance = result['shares']
            amount = result['amount']
            
            if balance > 0:
                roster.append({
                    'shareholder': holding.shareholder,
                    'stock_type': s_type,
                    'stock_type_display': s_type_display,
                    'balance': balance,
                    'amount': amount,
                    'percentage': 0  # Will calculate after we know total
                })
                total_shares += balance
    
    # Calculate percentages
    if total_shares > 0:
        for item in roster:
            item['percentage'] = round((item['balance'] / total_shares) * 100, 2)
    
    # Sort by balance (descending)
    roster.sort(key=lambda x: x['balance'], reverse=True)
    
    return roster


def get_shareholder_transaction_history(company_holding_id):
    """
    Get transaction history for a company holding with running balance.
    
    Args:
        company_holding_id: ID of the CompanyShareholding
    
    Returns:
        List of dicts with transaction info and running balance:
        [
            {
                'transaction': StockTransaction object,
                'running_balance': int (cumulative shares)
            },
            ...
        ]
    """
    transactions = StockTransaction.objects.filter(
        company_holding_id=company_holding_id
    ).order_by('transaction_date', 'created_at')
    
    history = []
    running_balance = 0
    
    for transaction in transactions:
        running_balance += transaction.quantity
        history.append({
            'transaction': transaction,
            'running_balance': running_balance
        })
    
    return history
