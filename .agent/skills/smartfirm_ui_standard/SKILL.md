---
name: SmartFirm UI Standard
description: Official UI/UX guidelines for SmartFirm application. Includes standards for List Views (DataTables), Form Layouts, and Action Buttons.
---

# SmartFirm UI/UX Standard

Use this skill when creating or modifying views in the SmartFirm application to ensure consistency with the established design language.

## 1. List Views (DataTables)

### HTML Structure
- **Table Classes**: Use `table table-hover align-middle`.
- **Header (`thead`)**: MUST use `class="table-light border-bottom border-2 fw-bold"`.
    - Light gray background.
    - Thick bottom border.
    - Bold text.
- **Action Buttons**: Use **borderless icon buttons**.
    - Edit: `<a class="btn btn-sm border-0 text-primary"><i class="bi bi-pencil-fill"></i></a>`
    - Delete: `<a class="btn btn-sm border-0 text-danger"><i class="bi bi-trash-fill"></i></a>`
- **Selection**: Include a "Select All" checkbox in the first column.

### DataTables Configuration
Always use the following **Chinese Localization** and configuration:

```javascript
$('#tableName').DataTable({
    "language": {
        "processing": "處理中...",
        "loadingRecords": "載入中...",
        "lengthMenu": "顯示 _MENU_ 項結果",
        "zeroRecords": "沒有符合的結果",
        "info": "顯示第 _START_ 至 _END_ 項結果，共 _TOTAL_ 項",
        "infoEmpty": "顯示第 0 至 0 項結果，共 0 項",
        "infoFiltered": "(從 _MAX_ 項結果中過濾)",
        "infoPostFix": "",
        "search": "搜尋:",
        "paginate": {
            "first": "第一頁",
            "previous": "上一頁",
            "next": "下一頁",
            "last": "最後一頁"
        },
        "aria": {
            "sortAscending": ": 升冪排列",
            "sortDescending": ": 降冪排列"
        }
    },
    "columnDefs": [
        { "orderable": false, "targets": [0, -1] } // Disable sorting on Checkbox (first) and Actions (last)
    ],
    // ... other settings
});
```

## 2. Form Views (Edit/Create)

### Layout Structure
Use a **2-Column Layout** with a dedicated Action Sidebar.

```html
<div class="row">
    <!-- Left Sidebar: Action Zone -->
    <div class="col-md-2">
        <div class="card mb-2">
            <div class="card-header bg-light">
                <h5 class="mb-0 card-title">動作專區</h5>
            </div>
            <div class="card-body">
                <!-- Action Buttons Stack -->
                 <div class="d-grid gap-2">...</div>
            </div>
        </div>
    </div>

    <!-- Right Main Content: Form -->
    <div class="col-md-10">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">基本資料</h5>
            </div>
            <div class="card-body">
                <!-- Form Fields -->
            </div>
        </div>
    </div>
</div>
```

### Action Bar (Navigation)
Do **NOT** place navigation buttons in the page header. Place them in a **dedicated row above the columns**:

- **Location**: Inside `{% block content %}`, before the main `.row`.
- **Alignment**: Right-aligned (`d-flex justify-content-end`).
- **Standard Buttons**:
    1.  **New** (`btn-primary`): "新增 [Model]"
    2.  **Back to List** (`btn-outline-secondary`): "回到列表"
    3.  **Prev/Next** (`btn-group`): "上一筆" / "下一筆"

### Field Styling
- **Labels**: Always add `fw-bold` class.
- **Required Asterisk**: `<span class="text-danger">*</span>`.
- **Validation Errors**: **MUST** be displayed in Red.
    - Use `{% if form.field.errors %}<div class="text-danger small">{{ form.field.errors }}</div>{% endif %}`.

## 3. General Implementation Details
- **Soft Delete**: Models should implement `is_deleted`. Deletion URLs should perform soft delete (set flag) rather than database delete.
- **Base Template**: All pages extend `base.html`.
- **Authentication**: Header displays user name and Logout button (conditionally rendered).
