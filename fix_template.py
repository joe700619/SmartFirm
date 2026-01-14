import sys

filepath = r'c:\Users\joe70\PythonProject\SmartFirm\admin_module\templates\admin_module\vat_check_form.html'

# Read the file
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 166-169 (index 165-168) - put template tags on single lines
lines[165] = '                                <td class="checkbox-cell"><input type="checkbox" class="form-check-input input-buyer" {% if item.input_buyer %}checked{% endif %}></td>\r\n'
lines[166] = '                                <td class="checkbox-cell"><input type="checkbox" class="form-check-input check-input-amount" {% if item.check_input_amount %}checked{% endif %}></td>\r\n'  
lines[167] = '                                <td class="checkbox-cell"><input type="checkbox" class="form-check-input input-duplicate" {% if item.input_duplicate %}checked{% endif %}></td>\r\n'
lines[168] = '                                <td class="checkbox-cell"><input type="checkbox" class="form-check-input output-e-invoice" {% if item.output_e_invoice %}checked{% endif %}></td>\r\n'

# Delete the old multi-line versions (lines 167-175, which are now indices 169-175 after we fixed 165-168)
# We need to delete 7 lines
del lines[169:176]

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print('File fixed successfully!')
print('Lines 166-169 are now single-line checkbox definitions')
