---
name: SmartFirm UI Standard
description: Official UI/UX guidelines for SmartFirm application (AdminLTE v4 Edition). Includes standards for List Views (Cards), Form Layouts, and Action Buttons.
---

# SmartFirm UI/UX Standard (AdminLTE v4)

Use this skill when creating or modifying views in the SmartFirm application to ensure consistency with the **AdminLTE v4** design language.

## 1. List Views (Standard Table)

### Layout Structure (Card Pattern)
All list views MUST be wrapped in an **AdminLTE Card** component.

```html
<div class="row">
    <div class="col-12">
        <div class="card">
            <!-- Card Header: Title & Actions -->
            <div class="card-header">
                <h3 class="card-title">List Title (e.g., Customer List)</h3>
                <div class="card-tools">
                    <!-- Global Actions go here -->
                    <a href="..." class="btn btn-primary btn-sm">
                        <i class="bi bi-plus-circle"></i> Add New
                    </a>
                </div>
            </div>
            
            <!-- Card Body: Table -->
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0">
                        <thead>...</thead>
                        <tbody>...</tbody>
                    </table>
                </div>
            </div>
            
            <!-- Card Footer: Pagination (Optional) -->
            <div class="card-footer clearfix">
                <!-- Pagination links -->
            </div>
        </div>
    </div>
</div>
```

### Table Style
- **Classes**: `table table-striped table-hover mb-0`
- **Header**: Standard `<thead>` (AdminLTE handles theme).
- **Body**: standard `<tbody>`.
- **Action Column**:
    - Use `btn-sm` buttons with icons.
    - Edit: `btn-warning` (Yellow)
    - Delete: `btn-danger` (Red)

## 2. Form Views (Edit/Create)

### Layout Structure
Use standard AdminLTE card layout for forms.
- **Card Header**: Form title (`<h3 class="card-title">...</h3>`).
- **Card Body**: Form fields (`.mb-3`).
- **Card Footer**: Submit (`btn-primary`) and Cancel (`btn-secondary`) buttons.

### Field Styling
- **Labels**: `<label class="form-label">`.
- **Inputs**: `<input class="form-control">`.
- **Cancel Button**: `btn-secondary` or `btn-default`.

## 3. Dashboard Widgets

### Info Boxes
Use for high-level summary metrics.

```html
<div class="info-box">
    <span class="info-box-icon text-bg-primary shadow-sm">
        <i class="bi bi-gear-fill"></i>
    </span>
    <div class="info-box-content">
        <span class="info-box-text">Label</span>
        <span class="info-box-number">Value</span>
    </div>
</div>
```

### General Cards
Use for charts or content blocks.
- **Collapsible**: Add `<button data-lte-toggle="card-collapse">` in `.card-tools`.
- **Removable**: Add `<button data-lte-toggle="card-remove">` in `.card-tools`.

## 4. General
- **Icons**: Use **Bootstrap Icons** (`bi bi-...`).
- **Colors**: Use Bootstrap 5 utility classes (`text-primary`, `bg-warning`, etc.).
- **Base Template**: Always extend `base.html`.
