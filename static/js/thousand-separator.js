/**
 * 千分位格式化工具模組
 * 用於自動格式化數字輸入欄位，添加千分位逗號
 */

const ThousandSeparator = {
    /**
     * 格式化數字為千分位格式
     * @param {string|number} value - 要格式化的值
     * @returns {string} - 格式化後的字符串
     */
    formatNumber: function (value) {
        if (!value && value !== 0) return '';

        // 移除所有非數字字符（保留小數點和負號）
        let numStr = value.toString().replace(/[^\d.-]/g, '');

        // 分離整數和小數部分
        let parts = numStr.split('.');
        let integerPart = parts[0];
        let decimalPart = parts.length > 1 ? '.' + parts[1] : '';

        // 處理負號
        let isNegative = integerPart.startsWith('-');
        if (isNegative) {
            integerPart = integerPart.substring(1);
        }

        // 添加千分位逗號
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

        // 組合結果
        return (isNegative ? '-' : '') + integerPart + decimalPart;
    },

    /**
     * 移除千分位逗號，獲取純數字
     * @param {string} value - 格式化的字符串
     * @returns {string} - 純數字字符串
     */
    parseNumber: function (value) {
        if (!value) return '';
        return value.toString().replace(/,/g, '');
    },

    /**
     * 初始化輸入欄位的千分位格式化
     * @param {string} selector - CSS選擇器，用於選擇要應用格式化的輸入欄位
     * @param {Object} options - 選項配置
     * @param {number} options.maxDecimals - 最大小數位數（默認為2）
     */
    init: function (selector, options = {}) {
        const maxDecimals = options.maxDecimals || 2;
        const inputs = document.querySelectorAll(selector);

        inputs.forEach(input => {
            // 處理輸入事件
            input.addEventListener('input', function (e) {
                const cursorPosition = this.selectionStart;
                const oldValue = this.value;
                const oldLength = oldValue.length;

                // 移除逗號
                let rawValue = ThousandSeparator.parseNumber(this.value);

                // 限制小數位數
                if (rawValue.includes('.')) {
                    const parts = rawValue.split('.');
                    if (parts[1] && parts[1].length > maxDecimals) {
                        parts[1] = parts[1].substring(0, maxDecimals);
                        rawValue = parts.join('.');
                    }
                }

                // 格式化
                const formatted = ThousandSeparator.formatNumber(rawValue);
                this.value = formatted;

                // 調整光標位置
                const newLength = formatted.length;
                const diff = newLength - oldLength;
                this.setSelectionRange(cursorPosition + diff, cursorPosition + diff);
            });

            // 焦點離開時確保格式正確
            input.addEventListener('blur', function () {
                if (this.value) {
                    const rawValue = ThousandSeparator.parseNumber(this.value);
                    this.value = ThousandSeparator.formatNumber(rawValue);
                }
            });

            // 如果已有初始值，格式化它
            if (input.value) {
                input.value = ThousandSeparator.formatNumber(input.value);
            }
        });
    },

    /**
     * 為單個元素設置千分位格式化
     * @param {HTMLElement} element - 要格式化的輸入元素
     * @param {Object} options - 選項配置
     */
    initElement: function (element, options = {}) {
        if (!element) return;

        const maxDecimals = options.maxDecimals || 2;

        // 處理輸入事件
        element.addEventListener('input', function (e) {
            const cursorPosition = this.selectionStart;
            const oldValue = this.value;
            const oldLength = oldValue.length;

            // 移除逗號
            let rawValue = ThousandSeparator.parseNumber(this.value);

            // 限制小數位數
            if (rawValue.includes('.')) {
                const parts = rawValue.split('.');
                if (parts[1] && parts[1].length > maxDecimals) {
                    parts[1] = parts[1].substring(0, maxDecimals);
                    rawValue = parts.join('.');
                }
            }

            // 格式化
            const formatted = ThousandSeparator.formatNumber(rawValue);
            this.value = formatted;

            // 調整光標位置
            const newLength = formatted.length;
            const diff = newLength - oldLength;
            this.setSelectionRange(cursorPosition + diff, cursorPosition + diff);
        });

        // 焦點離開時確保格式正確
        element.addEventListener('blur', function () {
            if (this.value) {
                const rawValue = ThousandSeparator.parseNumber(this.value);
                this.value = ThousandSeparator.formatNumber(rawValue);
            }
        });

        // 如果已有初始值，格式化它
        if (element.value) {
            element.value = ThousandSeparator.formatNumber(element.value);
        }
    }
};

// 如果是模組環境，導出模組
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThousandSeparator;
}
