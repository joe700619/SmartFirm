/**
 * Registration Progress Form Logic
 * Handles calculations, dynamic formsets, and interaction logic.
 */

$(document).ready(function () {
    // --- 0. Initialize Scripts ---

    // Init Bootstrap Multiselect
    if ($('#case-type-multiselect').length) {
        $('#case-type-multiselect').multiselect({
            buttonWidth: '100%',
            nonSelectedText: '請選擇案件類別',
            allSelectedText: '全選',
            nSelectedText: '項已選',
            numberDisplayed: 3,
            templates: {
                button: '<button type="button" class="multiselect dropdown-toggle btn btn-outline-secondary w-100 text-start d-flex justify-content-between align-items-center" data-bs-toggle="dropdown" aria-expanded="false"><span class="multiselect-selected-text"></span></button>',
            }
        });
    }

    // Init Thousand Separator for currency inputs
    // Fields with class 'currency-input' will be formatted
    if (typeof ThousandSeparator !== 'undefined') {
        ThousandSeparator.init('.currency-input', { maxDecimals: 0 });
        ThousandSeparator.init('.percentage-input', { maxDecimals: 2 });
        // Prepare form submit (strip commas)
        ThousandSeparator.prepareFormSubmit('#progressForm');
    } else {
        console.error("ThousandSeparator module is missing!");
    }


    // Helper: Parse float from formatted string
    function parseVal(val) {
        if (!val) return 0;
        if (typeof ThousandSeparator !== 'undefined') {
            return parseFloat(ThousandSeparator.parseNumber(val)) || 0;
        }
        return parseFloat(val.replace(/,/g, '')) || 0;
    }

    // Helper: Format number
    function formatVal(num) {
        let rounded = Math.round(num);
        if (typeof ThousandSeparator !== 'undefined') {
            return ThousandSeparator.formatNumber(rounded);
        }
        return rounded.toLocaleString();
    }

    // --- 1. Date Defaults ---
    var acceptanceDate = $('#id_acceptance_date');
    if (acceptanceDate.length && !acceptanceDate.val()) {
        var today = new Date();
        acceptanceDate.val(today.toISOString().split('T')[0]);
    }
    $('#id_status').on('change', function () {
        var status = $(this).val();
        var dueDate = $('#id_due_date');
        if (['closed', 'none'].includes(status) && !dueDate.val()) {
            var today = new Date();
            dueDate.val(today.toISOString().split('T')[0]);
        }
    });

    // --- 2. Calculations ---

    function calculateServiceTotals() {
        var serviceTotal = 0;
        var advanceTotal = 0;

        $('#service-tbody tr').each(function () {
            // Skip if marked for deletion
            if ($(this).find('input[name$="-DELETE"]').is(':checked')) return;

            var nameInput = $(this).find('input[name$="-service_name"]');
            var feeInput = $(this).find('input[name$="-fee"]');

            var name = nameInput.val() || '';
            var fee = parseVal(feeInput.val());

            if (name.trim().startsWith('9')) {
                advanceTotal += fee;
            } else {
                serviceTotal += fee;
            }
        });

        var grandTotal = serviceTotal + advanceTotal;

        $('#total-fee').text(formatVal(serviceTotal));
        $('#total-advance').text(formatVal(advanceTotal));
        $('#grand-total').text(formatVal(grandTotal));

        return serviceTotal; // Return for cost split calc
    }

    function calculateCostTotals() {
        var totalSplit = 0;
        $('#cost-tbody tr').each(function () {
            // Skip if marked for deletion
            if ($(this).find('input[name$="-DELETE"]').is(':checked')) return;

            var amountInput = $(this).find('input[name$="-amount"]');
            totalSplit += parseVal(amountInput.val());
        });
        $('#total-cost-amount').text(formatVal(totalSplit));
    }

    // Trigger Calcs
    $(document).on('input change', '#service-tbody input', function () {
        calculateServiceTotals();
        // Re-calc split amounts if they are percentage based? 
        // User requirement: "Apportioned Amount = Service Fee Total * Ratio"
        // So if Service Fee changes, we should update splits.
        updateSplitAmounts();
    });

    $(document).on('input change', '#cost-tbody input[name$="-ratio"]', function () {
        var row = $(this).closest('tr');
        var ratio = parseVal($(this).val());
        var serviceTotal = calculateServiceTotals(); // Get current total

        var amount = Math.round(serviceTotal * (ratio / 100));
        var amountInput = row.find('input[name$="-amount"]');

        // Set formatted value
        if (typeof ThousandSeparator !== 'undefined') {
            amountInput.val(ThousandSeparator.formatNumber(amount));
        } else {
            amountInput.val(amount);
        }
        calculateCostTotals();
    });

    $(document).on('input change', '#cost-tbody input[name$="-amount"]', function () {
        calculateCostTotals();
    });

    function updateSplitAmounts() {
        var serviceTotal = calculateServiceTotals();
        $('#cost-tbody tr').each(function () {
            // Skip if marked for deletion
            if ($(this).find('input[name$="-DELETE"]').is(':checked')) return;

            var ratioInput = $(this).find('input[name$="-ratio"]');
            var amountInput = $(this).find('input[name$="-amount"]');
            var ratio = parseVal(ratioInput.val());

            if (ratio > 0) {
                var amount = Math.round(serviceTotal * (ratio / 100));
                if (typeof ThousandSeparator !== 'undefined') {
                    amountInput.val(ThousandSeparator.formatNumber(amount));
                } else {
                    amountInput.val(amount);
                }
            }
        });
        calculateCostTotals();
    }

    // Initial Calc on Load
    calculateServiceTotals();
    calculateCostTotals();


    // --- 3. Dynamic Formset: SERVICES ---
    // Note: total_form_count needs to be passed from the template usually,
    // or we can read it from the hidden management form input.

    function getFormCount(prefix) {
        var input = $('#id_' + prefix + '-TOTAL_FORMS');
        if (input.length) {
            return parseInt(input.val()) || 0;
        }
        return 0;
    }

    function setFormCount(prefix, count) {
        $('#id_' + prefix + '-TOTAL_FORMS').val(count);
    }

    $('#add-service-row').off('click').on('click', function () {
        var serviceFormIdx = getFormCount('services');
        var rowHtml = $('#service-empty-form table tr').first()[0].outerHTML;
        if (!rowHtml) { console.error("Service row template not found"); return; }

        var newFormHtml = rowHtml.replace(/__prefix__/g, serviceFormIdx);
        var newRow = $(newFormHtml);
        $('#service-tbody').append(newRow);

        // Init Separator for new row
        if (typeof ThousandSeparator !== 'undefined') {
            ThousandSeparator.initElement(newRow.find('.currency-input')[0], { maxDecimals: 0 });
        }

        setFormCount('services', serviceFormIdx + 1);
        calculateServiceTotals();
    });

    $(document).on('click', '.delete-row-btn', function () {
        var row = $(this).closest('tr');
        var deleteInput = row.find('input[name$="-DELETE"]');
        if (deleteInput.length > 0) {
            deleteInput.prop('checked', true);
            row.hide();
        } else {
            row.remove();
        }
        calculateServiceTotals();
        updateSplitAmounts();
    });

    // --- 4. Dynamic Formset: COST SPLITS ---
    $('#add-cost-row').off('click').on('click', function () {
        var costFormIdx = getFormCount('cost_splits');
        var rowHtml = $('#cost-empty-form table tr').first()[0].outerHTML;
        if (!rowHtml) { console.error("Cost row template not found"); return; }

        var newFormHtml = rowHtml.replace(/__prefix__/g, costFormIdx);
        var newRow = $(newFormHtml);
        $('#cost-tbody').append(newRow);

        // Init Separator
        if (typeof ThousandSeparator !== 'undefined') {
            ThousandSeparator.initElement(newRow.find('.percentage-input')[0], { maxDecimals: 2 });
            ThousandSeparator.initElement(newRow.find('.currency-input')[0], { maxDecimals: 0 });
        }

        setFormCount('cost_splits', costFormIdx + 1);
        calculateCostTotals();
    });

    $(document).on('click', '.delete-cost-row-btn', function () {
        var row = $(this).closest('tr');
        var deleteInput = row.find('input[name$="-DELETE"]');
        if (deleteInput.length > 0) {
            deleteInput.prop('checked', true);
            row.hide();
        } else {
            row.remove();
        }
        calculateCostTotals();
    });

    // --- 5. Knowledge Note Integration ---

    // Auto-fill logic when modal opens
    $('#btn-add-knowledge').on('click', function () {
        // Gathering data from the main form
        // Since JS is external, we can't use {{ }} directly for all fields unless passed params.
        // We will read from the DOM elements.

        var caseNoText = $('small.text-muted:contains("#")').text().replace('#', '').trim();
        var companyName = $('#id_customer option:selected').text();
        if (!companyName || companyName.match('-------')) companyName = $('#id_customer').val() || '';

        var caseTypeRaw = $('#case-type-multiselect option:selected').map(function () {
            return $(this).text();
        }).get();
        var caseTypes = caseTypeRaw.join(', ');

        // --- 1. Determine Organization Type ---
        // Rule: 
        // If not ends with "公司" -> "行號"
        // If ends with "公司" -> Check if ends with "股份有限公司" -> "股份有限公司", else "有限公司"
        var orgType = "行號";
        var cleanName = companyName.trim();
        if (cleanName.endsWith("公司")) {
            if (cleanName.endsWith("股份有限公司")) {
                orgType = "股份有限公司";
            } else {
                orgType = "有限公司";
            }
        }

        // --- 2. Build Title ---
        // Title: [OrgType] + [CaseType] 
        // Example: 有限公司變更登記
        var title = "";
        if (orgType && caseTypes) {
            title = `${orgType}_${caseTypes}`;
        } else {
            // Fallback if no case type selected
            title = `案件 ${caseNoText || 'New'} - ${companyName}`;
        }

        // --- 3. Build Checklist (Empty as requested) ---
        // User requested Checklist to be EMPTY

        $('#kn_title').val(title);
        $('#kn_tags').val(caseTypes); // Context = CaseType
        $('#kn_checklist').val('');   // Empty
        $('#kn_steps').val('');       // Empty
        $('#kn_warnings').val('');    // Empty

        // Show Modal
        var myModal = new bootstrap.Modal(document.getElementById('knowledgeModal'));
        myModal.show();
    });

    $('#btn-save-knowledge').on('click', function () {
        var data = {
            title: $('#kn_title').val(),
            tags: $('#kn_tags').val(),
            checklist: $('#kn_checklist').val(),
            steps: $('#kn_steps').val(),
            warnings: $('#kn_warnings').val()
        };

        if (!data.title) {
            alert('標題為必填項目');
            return;
        }

        // Send to Backend
        fetch('/registration/api/knowledge/create/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('成功加入知識庫！');
                    var modalEl = document.getElementById('knowledgeModal');
                    var modal = bootstrap.Modal.getInstance(modalEl);
                    modal.hide();
                } else {
                    alert('錯誤：' + result.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('發生錯誤');
            });
    });

});
