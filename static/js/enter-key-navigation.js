/**
 * Enter 鍵導航工具模組
 * 用於實現按 Enter 鍵自動跳到下一個輸入欄位的功能
 */

const EnterKeyNavigation = {
    /**
     * 初始化 Enter 鍵導航功能
     * @param {string} containerSelector - 容器選擇器（可選，默認為 document）
     * @param {Object} options - 選項配置
     * @param {string} options.inputSelector - 輸入欄位選擇器（默認為 'input, select, textarea'）
     * @param {boolean} options.excludeTextarea - 是否排除 textarea（默認為 true，因為 textarea 通常需要 Enter 換行）
     * @param {Function} options.onEnter - Enter 鍵按下時的回調函數
     */
    init: function (containerSelector = null, options = {}) {
        const container = containerSelector ? document.querySelector(containerSelector) : document;
        if (!container) {
            console.warn('EnterKeyNavigation: Container not found');
            return;
        }

        const inputSelector = options.inputSelector || 'input:not([type=hidden]), select';
        const excludeTextarea = options.excludeTextarea !== false; // 默認排除 textarea

        // 如果不排除 textarea，添加到選擇器
        const finalSelector = excludeTextarea ? inputSelector : inputSelector + ', textarea';

        container.addEventListener('keydown', function (e) {
            // 檢查是否按下 Enter 鍵
            if (e.key === 'Enter' || e.keyCode === 13) {
                const target = e.target;

                // 確認是輸入欄位
                if (target.matches(finalSelector)) {
                    // 如果是 textarea 且沒有按 Shift，允許換行
                    if (target.tagName === 'TEXTAREA' && !e.shiftKey) {
                        return; // 允許 textarea 換行
                    }

                    // 執行回調（如果有）
                    if (options.onEnter && typeof options.onEnter === 'function') {
                        const shouldContinue = options.onEnter(e, target);
                        if (shouldContinue === false) {
                            return;
                        }
                    }

                    e.preventDefault();

                    // 獲取所有可聚焦的輸入欄位
                    const inputs = Array.from(container.querySelectorAll(finalSelector))
                        .filter(input => {
                            // 過濾掉隱藏的和禁用的欄位
                            return !input.disabled &&
                                input.type !== 'hidden' &&
                                input.offsetParent !== null; // 檢查是否可見
                        });

                    // 找到當前輸入欄位的索引
                    const currentIndex = inputs.indexOf(target);

                    if (currentIndex > -1 && currentIndex < inputs.length - 1) {
                        // 跳到下一個欄位
                        const nextInput = inputs[currentIndex + 1];
                        nextInput.focus();

                        // 如果是 text 或 number 類型，選擇全部內容
                        if (nextInput.select && (nextInput.type === 'text' || nextInput.type === 'number')) {
                            nextInput.select();
                        }
                    } else if (currentIndex === inputs.length - 1) {
                        // 如果是最後一個欄位，可以選擇跳到第一個或觸發提交
                        if (options.loopToFirst) {
                            inputs[0].focus();
                            if (inputs[0].select) {
                                inputs[0].select();
                            }
                        } else if (options.submitOnLast) {
                            // 尋找最近的 form 並提交
                            const form = target.closest('form');
                            if (form) {
                                form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
                            }
                        }
                    }
                }
            }
        });
    },

    /**
     * 為特定表格初始化行內 Enter 鍵導航
     * @param {string} tableSelector - 表格選擇器
     * @param {Object} options - 選項配置
     */
    initTable: function (tableSelector, options = {}) {
        const table = document.querySelector(tableSelector);
        if (!table) {
            console.warn('EnterKeyNavigation: Table not found');
            return;
        }

        table.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.keyCode === 13) {
                const target = e.target;

                // 確認是輸入欄位
                if (target.matches('input, select, textarea')) {
                    // 如果是 textarea 且沒有按 Shift，允許換行
                    if (target.tagName === 'TEXTAREA' && !e.shiftKey) {
                        return;
                    }

                    e.preventDefault();

                    // 找到當前儲存格
                    const currentCell = target.closest('td, th');
                    if (!currentCell) return;

                    const currentRow = currentCell.parentElement;
                    const cells = Array.from(currentRow.cells);
                    const currentCellIndex = cells.indexOf(currentCell);

                    // 嘗試移動到同一行的下一個儲存格
                    if (currentCellIndex < cells.length - 1) {
                        const nextCell = cells[currentCellIndex + 1];
                        const nextInput = nextCell.querySelector('input, select, textarea');
                        if (nextInput) {
                            nextInput.focus();
                            if (nextInput.select) nextInput.select();
                            return;
                        }
                    }

                    // 如果是行的最後一個儲存格，移動到下一行的第一個輸入欄位
                    const nextRow = currentRow.nextElementSibling;
                    if (nextRow) {
                        const firstInputInNextRow = nextRow.querySelector('input, select, textarea');
                        if (firstInputInNextRow) {
                            firstInputInNextRow.focus();
                            if (firstInputInNextRow.select) firstInputInNextRow.select();
                        }
                    } else if (options.addRowOnLast) {
                        // 如果是最後一行，可以觸發新增行的功能
                        if (typeof options.addRowCallback === 'function') {
                            options.addRowCallback();
                        }
                    }
                }
            }
        });
    },

    /**
     * 移除 Enter 鍵導航功能
     * @param {string} containerSelector - 容器選擇器
     */
    destroy: function (containerSelector = null) {
        const container = containerSelector ? document.querySelector(containerSelector) : document;
        if (!container) return;

        // 移除所有相關的事件監聽器
        // 注意：這需要存儲原始的處理函數引用，這裡提供一個簡化版本
        console.log('EnterKeyNavigation: destroy() called. You may need to reload the page to fully remove listeners.');
    }
};

// 如果是模組環境，導出模組
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EnterKeyNavigation;
}
