import codecs

html_content = '''{% extends 'base.html' %}
{% load static %}

{% block title %}股東管理 - SmartFirm{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="bi bi-people-fill"></i> 股東管理</h2>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createShareholderModal">
            <i class="bi bi-plus-circle"></i> 新增股東
        </button>
    </div>

    {% if messages %}
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}
    {% endif %}

    {% if shareholders %}
    <div class="table-responsive">
        <table class="table table-striped table-hover" id="shareholdersTable">
            <thead class="table-secondary">
                <tr>
                    <th>股東姓名</th>
                    <th>身分證字號/統一編號</th>
                    <th>聯絡電話</th>
                    <th>Email</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {% for shareholder in shareholders %}
                <tr>
                    <td>{{ shareholder.name }}</td>
                    <td>{{ shareholder.identifier }}</td>
                    <td>{{ shareholder.phone|default:"—" }}</td>
                    <td>{{ shareholder.email|default:"—" }}</td>
                    <td>
                        <button type="button" class="btn btn-sm btn-warning edit-btn" data-id="{{ shareholder.id }}">
                            <i class="bi bi-pencil"></i> 編輯
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="alert alert-info" role="alert">
        <i class="bi bi-info-circle"></i> 目前尚無股東資料。
    </div>
    {% endif %}
</div>

<!-- 編輯股東 Modal -->
<div class="modal fade" id="editShareholderModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title"><i class="bi bi-pencil-square"></i> 編輯股東資料</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="editAlertArea"></div>
                
                <form id="editShareholderForm">
                    {% csrf_token %}
                    <input type="hidden" id="edit_shareholder_id" name="shareholder_id">

                    <div class="mb-3">
                        <label for="edit_identifier" class="form-label">身分證字號/統一編號</label>
                        <input type="text" class="form-control" id="edit_identifier" name="identifier" readonly>
                        <small class="form-text text-muted">身分證字號/統一編號不可修改</small>
                    </div>

                    <div class="mb-3">
                        <label for="edit_name" class="form-label">股東姓名 <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="edit_name" name="name" required>
                    </div>

                    <div class="mb-3">
                        <label for="edit_phone" class="form-label">聯絡電話</label>
                        <input type="text" class="form-control" id="edit_phone" name="phone">
                    </div>

                    <div class="mb-3">
                        <label for="edit_email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="edit_email" name="email">
                    </div>

                    <div class="mb-3">
                        <label for="edit_address" class="form-label">地址</label>
                        <input type="text" class="form-control" id="edit_address" name="address">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" id="saveEditBtn">儲存</button>
            </div>
        </div>
    </div>
</div>

<!-- 新增股東 Modal -->
<div class="modal fade" id="createShareholderModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title"><i class="bi bi-plus-circle"></i> 新增股東</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="createAlertArea"></div>
                
                <form id="createShareholderForm">
                    {% csrf_token %}

                    <div class="mb-3">
                        <label for="create_identifier" class="form-label">身分證字號/統一編號 <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="create_identifier" name="identifier" required>
                        <small class="form-text text-muted">每個身分證字號/統一編號在系統中必須唯一</small>
                    </div>

                    <div class="mb-3">
                        <label for="create_name" class="form-label">股東姓名 <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="create_name" name="name" required>
                    </div>

                    <div class="mb-3">
                        <label for="create_phone" class="form-label">聯絡電話</label>
                        <input type="text" class="form-control" id="create_phone" name="phone">
                    </div>

                    <div class="mb-3">
                        <label for="create_email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="create_email" name="email">
                    </div>

                    <div class="mb-3">
                        <label for="create_address" class="form-label">地址</label>
                        <input type="text" class="form-control" id="create_address" name="address">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" id="saveCreateBtn">新增</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css">
{% endblock %}

{% block extra_js %}
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>

<script>
$(document).ready(function() {
    function showAlert(elementId, message, type = 'danger') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        $('#' + elementId).html(alertHtml);
        $('#' + elementId)[0].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    $('#shareholdersTable').DataTable({
        language: {
            "sProcessing": "處理中...",
            "sLengthMenu": "顯示 _MENU_ 筆資料",
            "sZeroRecords": "沒有符合的資料",
            "sInfo": "顯示第 _START_ 至 _END_ 筆資料，共 _TOTAL_ 筆",
            "sInfoEmpty": "顯示第 0 至 0 筆資料，共 0 筆",
            "sInfoFiltered": "(從 _MAX_ 筆資料中篩選)",
            "sSearch": "搜尋:",
            "oPaginate": {
                "sFirst": "第一頁",
                "sPrevious": "上一頁",
                "sNext": "下一頁",
                "sLast": "最後一頁"
            }
        },
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "全部"]],
        order: [[0, 'asc']],
        columnDefs: [{ orderable: false, targets: [4] }],
        responsive: true
    });

    $('.edit-btn').on('click', function() {
        const shareholderId = $(this).data('id');
        $('#editAlertArea').html('');

        $.ajax({
            url: `/registration/api/shareholder/${shareholderId}/`,
            method: 'GET',
            success: function(response) {
                if (response.success) {
                    const s = response.shareholder;
                    $('#edit_shareholder_id').val(s.id);
                    $('#edit_identifier').val(s.identifier);
                    $('#edit_name').val(s.name);
                    $('#edit_phone').val(s.phone);
                    $('#edit_email').val(s.email);
                    $('#edit_address').val(s.address);
                    $('#editShareholderModal').modal('show');
                } else {
                    showAlert('editAlertArea', '❌ 取得股東資料失敗：' + response.error);
                }
            },
            error: function() {
                showAlert('editAlertArea', '❌ 取得股東資料時發生錯誤');
            }
        });
    });

    $('#saveEditBtn').on('click', function() {
        const form = document.getElementById('editShareholderForm');
        $('#editAlertArea').html('');
        
        if (!form.reportValidity()) {
            return;
        }
        
        const shareholderId = $('#edit_shareholder_id').val();
        const formData = $('#editShareholderForm').serialize();
        
        $.ajax({
            url: `/registration/api/shareholder/update/${shareholderId}/`,
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    showAlert('editAlertArea', '✅ 股東資料已更新', 'success');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    showAlert('edit AlertArea', '❌ 更新失敗：' + response.error);
                }
            },
            error: function() {
                showAlert('editAlertArea', '❌ 更新時發生錯誤');
            }
        });
    });

    $('#saveCreateBtn').on('click', function() {
        const form = document.getElementById('createShareholderForm');
        $('#createAlertArea').html('');
        
        if (!form.reportValidity()) {
            return;
        }
        
        const formData = $('#createShareholderForm').serialize();
        
        $.ajax({
            url: '/registration/api/shareholder/create/',
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    showAlert('createAlertArea', '✅ 股東已成功新增', 'success');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    showAlert('createAlertArea', '❌ 新增失敗：' + response.error);
                }
            },
            error: function(xhr) {
                const response = xhr.responseJSON;
                if (response && response.error) {
                    showAlert('createAlertArea', '❌ ' + response.error);
                } else {
                    showAlert('createAlertArea', '❌ 新增時發生錯誤：未知錯誤');
                }
            }
        });
    });
    
    $('#createShareholderModal').on('hidden.bs.modal', function() {
        $('#createAlertArea').html('');
        $('#createShareholderForm')[0].reset();
    });
    
    $('#editShareholderModal').on('hidden.bs.modal', function() {
        $('#editAlertArea').html('');
    });
});
</script>
{% endblock %}
'''

# Write with UTF-8 encoding
with codecs.open(r'c:\Users\joe70\PythonProject\SmartFirm\registration\templates\registration\shareholder_list.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ shareholder_list.html written successfully with UTF-8 encoding!")
