import os

# Fix shareholder_roster.html
roster_content = r'''{% extends 'base.html' %}
{% load static %}

{% block title %}股東名冊查詢{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>股東名冊查詢</h2>
    
    <div class="card mb-4">
        <div class="card-body">
            <form method="get" action="{% url 'registration:shareholder_roster' %}">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="company_id">公司名稱</label>
                            <select name="company_id" id="company_id" class="form-control" required>
                                <option value="">請選擇公司</option>
                                {% for company in companies %}
                                <option value="{{ company.id }}" {% if selected_company_id == company.id|stringformat:"s" %}selected{% endif %}>{{ company.companyName }} ({{ company.companyId }})</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label for="target_date">查詢日期</label>
                            <input type="date" name="target_date" id="target_date" class="form-control" value="{{ target_date }}" required>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="form-group">
                            <label>&nbsp;</label>
                            <button type="submit" class="btn btn-primary btn-block">查詢</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>

    {% if error %}
    <div class="alert alert-danger">{{ error }}</div>
    {% endif %}

    {% if roster %}
    <div class="card">
        <div class="card-header">
            <h4>{{ company.companyName }} ({{ company.companyId }}) - 股東名冊</h4>
            <p class="mb-0">查詢日期：{{ target_date }} | 總股數：{{ total_shares|floatformat:0 }}</p>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead class="thead-light">
                        <tr>
                            <th>股東姓名</th>
                            <th>身分證字號/統一編號</th>
                            <th>聯絡電話</th>
                            <th>Email</th>
                            <th class="text-right">持股股數</th>
                            <th class="text-right">持股比例</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in roster %}
                        <tr>
                            <td>{{ item.shareholder.name }}</td>
                            <td>{{ item.shareholder.identifier }}</td>
                            <td>{{ item.shareholder.phone|default:"-" }}</td>
                            <td>{{ item.shareholder.email|default:"-" }}</td>
                            <td class="text-right">{{ item.balance|floatformat:0 }}</td>
                            <td class="text-right">{{ item.percentage }}%</td>
                            <td><a href="{% url 'registration:shareholder_detail' item.shareholder.id %}" class="btn btn-sm btn-info">查看交易明細</a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr class="font-weight-bold">
                            <td colspan="4">合計</td>
                            <td class="text-right">{{ total_shares|floatformat:0 }}</td>
                            <td class="text-right">100.00%</td>
                            <td></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
    {% elif selected_company_id %}
    <div class="alert alert-info">此公司尚無股東資料</div>
    {% endif %}
</div>
{% endblock %}
'''

# Fix shareholder_detail.html
detail_content = r'''{% extends 'base.html' %}
{% load static %}

{% block title %}股東交易明細 - {{ shareholder.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="mb-3">
        <a href="{% url 'registration:shareholder_roster' %}?company_id={{ shareholder.company.id }}" class="btn btn-secondary">← 返回股東名冊</a>
    </div>

    <h2>股東交易明細</h2>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h4 class="mb-0">股東資料</h4>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>股東姓名：</strong>{{ shareholder.name }}</p>
                    <p><strong>身分證字號/統一編號：</strong>{{ shareholder.identifier }}</p>
                    <p><strong>公司：</strong>{{ shareholder.company.companyName }} ({{ shareholder.company.companyId }})</p>
                </div>
                <div class="col-md-6">
                    <p><strong>聯絡電話：</strong>{{ shareholder.phone|default:"-" }}</p>
                    <p><strong>Email：</strong>{{ shareholder.email|default:"-" }}</p>
                    <p><strong>地址：</strong>{{ shareholder.address|default:"-" }}</p>
                </div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h4>股權交易歷史</h4>
        </div>
        <div class="card-body">
            {% if history %}
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead class="thead-light">
                        <tr>
                            <th>交易日期</th>
                            <th>交易類型</th>
                            <th class="text-right">變動股數</th>
                            <th class="text-right">交易金額</th>
                            <th class="text-right">累計持股</th>
                            <th>備註</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in history %}
                        <tr>
                            <td>{{ item.transaction.transaction_date }}</td>
                            <td>
                                {% if item.transaction.transaction_type == 'founding' %}
                                <span class="badge badge-primary">{{ item.transaction.get_transaction_type_display }}</span>
                                {% elif item.transaction.transaction_type == 'transfer_in' or item.transaction.transaction_type == 'capital_increase' %}
                                <span class="badge badge-success">{{ item.transaction.get_transaction_type_display }}</span>
                                {% elif item.transaction.transaction_type == 'transfer_out' or item.transaction.transaction_type == 'capital_reduction' %}
                                <span class="badge badge-danger">{{ item.transaction.get_transaction_type_display }}</span>
                                {% else %}
                                <span class="badge badge-secondary">{{ item.transaction.get_transaction_type_display }}</span>
                                {% endif %}
                            </td>
                            <td class="text-right {% if item.transaction.quantity > 0 %}text-success{% elif item.transaction.quantity < 0 %}text-danger{% endif %}">{% if item.transaction.quantity > 0 %}+{% endif %}{{ item.transaction.quantity|floatformat:0 }}</td>
                            <td class="text-right">{% if item.transaction.amount %}${{ item.transaction.amount|floatformat:0 }}{% else %}-{% endif %}</td>
                            <td class="text-right font-weight-bold">{{ item.running_balance|floatformat:0 }}</td>
                            <td>{{ item.transaction.note|default:"-" }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                    <tfoot>
                        <tr class="font-weight-bold bg-light">
                            <td colspan="4">目前持股總計</td>
                            <td class="text-right">{% if history %}{{ history.last.running_balance|floatformat:0 }}{% else %}0{% endif %}</td>
                            <td></td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">此股東尚無交易記錄</div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''

# Write files
with open(r'c:\Users\joe70\PythonProject\SmartFirm\registration\templates\registration\shareholder_roster.html', 'w', encoding='utf-8') as f:
    f.write(roster_content)

with open(r'c:\Users\joe70\PythonProject\SmartFirm\registration\templates\registration\shareholder_detail.html', 'w', encoding='utf-8') as f:
    f.write(detail_content)

print("✓ Templates fixed successfully!")
