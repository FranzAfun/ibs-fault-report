document.addEventListener("DOMContentLoaded", () => {
    // Export and pagination table
    const exportDropdownTable = document.querySelector('[data-tables="export-data-dropdown"]');
    if (exportDropdownTable) {
        new DataTable(exportDropdownTable, {
            dom: "<'d-md-flex justify-content-between align-items-center my-2'<'dropdown'B>f>rt<'d-md-flex justify-content-between align-items-center mt-2'ip>",
            responsive: true,
            pageLength: 7,
            lengthMenu: [7, 10, 25, 50, -1],
            select: {
                style: "single" // Default value, can be changed
            },
            buttons: [
                {
                    extend: "collection",
                    text: '<i class="ti ti-download me-1"></i> Export',
                    className: "btn btn-sm btn-secondary dropdown-toggle",
                    autoClose: true,
                    buttons: [
                        { extend: "copy", text: '<i class="ti ti-copy me-1 fs-lg align-middle"></i> Copy', className: "dropdown-item" },
                        { extend: "csv", text: '<i class="ti ti-file-type-csv me-1 fs-lg align-middle"></i> CSV', className: "dropdown-item" },
                        { extend: "excel", text: '<i class="ti ti-file-spreadsheet me-1 fs-lg align-middle"></i> Excel', className: "dropdown-item" },
                        { extend: "print", text: '<i class="ti ti-printer me-1 fs-lg align-middle"></i> Print', className: "dropdown-item" },
                        { extend: "pdf", text: '<i class="ti ti-file-text me-1 fs-lg align-middle"></i> PDF', className: "dropdown-item" }
                    ]
                }
            ],
            language: {
                paginate: {
                    first: '<i class="ti ti-chevrons-left"></i>',
                    previous: '<i class="ti ti-chevron-left"></i>',
                    next: '<i class="ti ti-chevron-right"></i>',
                    last: '<i class="ti ti-chevrons-right"></i>'
                },
                lengthMenu: "_MENU_ Companies per page",
                info: 'Showing <span class="fw-semibold">_START_</span> to <span class="fw-semibold">_END_</span> of <span class="fw-semibold">_TOTAL_</span> Companies'
            }
        });
    }

    // Selectable table
    function initSelectableDataTable(e, t = {}) {
        e = document.querySelector(e);
        e && new DataTable(e, {
            pageLength: 7,
            lengthMenu: [7, 10, 25, 50, -1],
            select: t,
            language: {
                paginate: {
                    first: '<i class="ti ti-chevrons-left"></i>',
                    previous: '<i class="ti ti-chevron-left"></i>',
                    next: '<i class="ti ti-chevron-right"></i>',
                    last: '<i class="ti ti-chevrons-right"></i>'
                },
                lengthMenu: "_MENU_ Companies per page",
                info: 'Showing <span class="fw-semibold">_START_</span> to <span class="fw-semibold">_END_</span> of <span class="fw-semibold">_TOTAL_</span> Companies'
            }
        });
    }

    initSelectableDataTable("#single-select", { style: "single" });
    initSelectableDataTable("#multi-select", { style: "multi" });
    initSelectableDataTable("#cell-select", { style: "os", items: "cell" });

    // Show/hide columns table
    var showHideTable = document.getElementById("show-hide-column");
    if (showHideTable) {
        let tableInstance = new DataTable(showHideTable, {
            responsive: true,
            dom: "<'d-md-flex justify-content-between align-items-center mt-2 mb-3'<'columnToggleWrapper'B>f>rt<'d-md-flex justify-content-between align-items-center mt-2'lp>",
            language: {
                paginate: {
                    first: '<i class="ti ti-chevrons-left"></i>',
                    previous: '<i class="ti ti-chevron-left"></i>',
                    next: '<i class="ti ti-chevron-right"></i>',
                    last: '<i class="ti ti-chevrons-right"></i>'
                }
            }
        });

        let columns = ["Company", "Symbol", "Price", "Change", "Volume", "Market Cap", "Rating", "Status"];
        let columnToggleWrapper = document.querySelector(".columnToggleWrapper");

        if (columnToggleWrapper) {
            let dropdownDiv = document.createElement("div");
            dropdownDiv.className = "dropdown";
            dropdownDiv.innerHTML = `
                <button class="btn btn-sm btn-secondary" type="button" data-bs-toggle="dropdown" data-bs-auto-close="outside">
                    Show/Hide Columns
                </button>
                <ul class="dropdown-menu" id="columnToggleMenu">
                    ${columns.map((column, index) => `
                        <li class="dropdown-item">
                            <div class="form-check">
                                <input class="form-check-input form-check-input-light fs-14 mt-0 toggle-vis" 
                                       type="checkbox" data-column="${index}" id="colToggle${index}" checked>
                                <label class="form-check-label fw-medium" for="colToggle${index}">
                                    ${column}
                                </label>
                            </div>
                        </li>
                    `).join("")}
                </ul>
            `;
            columnToggleWrapper.appendChild(dropdownDiv);
            document.getElementById("columnToggleMenu").addEventListener("change", function(event) {
                if (event.target.classList.contains("toggle-vis")) {
                    let columnIndex = parseInt(event.target.dataset.column, 10);
                    tableInstance.column(columnIndex).visible(event.target.checked);
                }
            });
        }
    }
});