// incoming_mail.js - 收文系統 JavaScript 邏輯
// ⚠️ 注意：此檔案完全不使用 template literals (`${}`)，以避免與 Django template 衝突

// 從 HTML data 屬性讀取 Django 資料
let customers = [];
let contentTypes = [];
let itemCounter = 0;

// 初始化
document.addEventListener('DOMContentLoaded', function () {
    loadDjangoData();
    initializeForm();
    attachEventListeners();
});

function loadDjangoData() {
    // 從隱藏的 div 的 data 屬性中讀取 Django 傳遞的資料
    const dataElement = document.getElementById('djangoData');
    if (dataElement) {
        const customersData = dataElement.getAttribute('data-customers');
        const contentTypesData = dataElement.getAttribute('data-content-types');

        if (customersData) {
            try {
                customers = JSON.parse(customersData);
            } catch (e) {
                console.error('無法解析客戶資料:', e);
                customers = [];
            }
        }

        if (contentTypesData) {
            try {
                contentTypes = JSON.parse(contentTypesData);
            } catch (e) {
                console.error('無法解析內容類型資料:', e);
                contentTypes = [];
            }
        }
    }
}

function initializeForm() {
    // 初始化計數器
    const existingItems = document.querySelectorAll('.item-row');
    itemCounter = existingItems.length;
}

function attachEventListeners() {
    // 新增明細按鈕
    const addItemBtn = document.getElementById('addItemBtn');
    if (addItemBtn) {
        addItemBtn.addEventListener('click', addItem);
    }
}

// 新增明細項目
function addItem() {
    itemCounter++;

    const itemsContainer = document.getElementById('itemsContainer');
    const itemDiv = document.createElement('div');
    itemDiv.className = 'item-row border rounded p-3 mb-3';
    itemDiv.setAttribute('data-item-index', itemCounter);

    // ✅ 使用字串拼接，不使用 template literals
    let html = '<div class="row">';
    html += '<div class="col-12 d-flex justify-content-between align-items-center mb-2">';
    html += '<h6 class="mb-0">明細 #' + itemCounter + '</h6>';
    html += '<button type="button" class="btn btn-sm btn-danger" onclick="removeItem(this)">刪除</button>';
    html += '</div>';

    // 發文者
    html += '<div class="col-md-6 mb-3">';
    html += '<label class="form-label">發文者</label>';
    html += '<input type="text" class="form-control item-sender" placeholder="請輸入發文者">';
    html += '</div>';

    // 統一編號
    html += '<div class="col-md-6 mb-3">';
    html += '<label class="form-label">統一編號</label>';
    html += '<input type="text" class="form-control item-company-id" placeholder="請輸入統一編號">';
    html += '</div>';

    // 客戶名稱
    html += '<div class="col-md-6 mb-3">';
    html += '<label class="form-label">客戶名稱</label>';
    html += '<select class="form-select item-customer-select">';
    html += '<option value="">請選擇客戶</option>';

    // 動態生成客戶選項
    if (typeof customers !== 'undefined') {
        for (let i = 0; i < customers.length; i++) {
            const customer = customers[i];
            html += '<option value="' + customer.id + '" ';
            html += 'data-company-id="' + customer.companyId + '" ';
            html += 'data-company-name="' + customer.companyName + '">';
            html += customer.companyName + ' (' + customer.companyId + ')';
            html += '</option>';
        }
    }

    html += '</select>';
    html += '</div>';

    // 內容性質
    html += '<div class="col-md-6 mb-3">';
    html += '<label class="form-label">內容性質</label>';
    html += '<select class="form-control item-content-type">';
    html += '<option value="">請選擇內容性質</option>';

    // 動態生成內容性質選項
    if (typeof contentTypes !== 'undefined') {
        for (let i = 0; i < contentTypes.length; i++) {
            const ct = contentTypes[i];
            html += '<option value="' + ct.value + '">' + ct.display + '</option>';
        }
    }

    html += '</select>';
    html += '</div>';

    // 是否通知客戶
    html += '<div class="col-md-12 mb-3">';
    html += '<div class="form-check">';
    html += '<input type="checkbox" class="form-check-input item-notify-customer" id="notify_' + itemCounter + '">';
    html += '<label class="form-check-label" for="notify_' + itemCounter + '">是否通知客戶</label>';
    html += '</div>';
    html += '</div>';

    // 留言內容
    html += '<div class="col-md-12 mb-3">';
    html += '<label class="form-label">留言內容</label>';
    html += '<textarea class="form-control item-message" rows="3" placeholder="請輸入留言內容"></textarea>';
    html += '</div>';

    // 隱藏欄位（用於提交）
    html += '<input type="hidden" class="item-data" name="items">';

    html += '</div>';

    itemDiv.innerHTML = html;
    itemsContainer.appendChild(itemDiv);

    // 綁定客戶選擇事件
    const customerSelect = itemDiv.querySelector('.item-customer-select');
    if (customerSelect) {
        customerSelect.addEventListener('change', function () {
            onCustomerSelect(this);
        });
    }
}

// 移除明細項目
function removeItem(button) {
    const itemRow = button.closest('.item-row');
    if (itemRow) {
        itemRow.remove();
    }
}

// 客戶選擇變更事件
function onCustomerSelect(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const itemRow = selectElement.closest('.item-row');

    if (selectedOption && itemRow) {
        const companyId = selectedOption.getAttribute('data-company-id');
        const companyName = selectedOption.getAttribute('data-company-name');

        // 填入統一編號
        const companyIdInput = itemRow.querySelector('.item-company-id');
        if (companyIdInput && companyId) {
            companyIdInput.value = companyId;
        }
    }
}

// 表單提交前收集所有明細資料
function collectItemsData() {
    const itemRows = document.querySelectorAll('.item-row');
    const itemsData = [];

    itemRows.forEach(function (row) {
        const itemData = {
            sender: row.querySelector('.item-sender').value || '',
            company_id: row.querySelector('.item-company-id').value || '',
            customer_name: row.querySelector('.item-customer-select option:checked').text || '',
            content_type: row.querySelector('.item-content-type').value || '',
            notify_customer: row.querySelector('.item-notify-customer').checked,
            message_content: row.querySelector('.item-message').value || ''
        };

        // 將資料存入隱藏欄位
        const hiddenInput = row.querySelector('.item-data');
        if (hiddenInput) {
            hiddenInput.value = JSON.stringify(itemData);
        }

        itemsData.push(itemData);
    });

    return itemsData;
}

// 表單提交處理
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            collectItemsData();
        });
    }
});

console.log('incoming_mail.js 已載入');
