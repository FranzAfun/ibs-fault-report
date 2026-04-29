document.addEventListener("DOMContentLoaded", () => {

    function initComplexDataTable(selector) {
        const tableElement = document.querySelector(selector);
        
        if (!tableElement) {
            console.warn(`DataTable element not found for selector: ${selector}`);
            return null;
        }

        // Extract column names (only needed if you use column search inputs)
        const headerRow = tableElement.querySelector("thead tr");
        if (!headerRow) {
            console.error(`Table header not found in table: ${selector}`);
            return null;
        }

        const columnNames = Array.from(headerRow.querySelectorAll("th"))
            .map(th => th.textContent.trim())
            .filter(name => name);

        if (columnNames.length === 0) {
            console.error(`No column names found in table: ${selector}`);
            return null;
        }

        // Export buttons collection
        const exportButtonCollection = {
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
        };

        // Initialize DataTable WITHOUT the column visibility button
        const tableInstance = new DataTable(tableElement, {
            responsive: true,
            pageLength: 7,
            lengthMenu: [7, 10, 25, 50, -1],
            select: { style: "single" },
            dom: "<'d-md-flex justify-content-between align-items-center mt-2 mb-3'Bf>rt<'d-md-flex justify-content-between align-items-center mt-2'ip>",
            buttons: [
                exportButtonCollection   // Only Export button now
            ],
            language: {
                paginate: {
                    first: '<i class="ti ti-chevrons-left"></i>',
                    previous: '<i class="ti ti-chevron-left"></i>',
                    next: '<i class="ti ti-chevron-right"></i>',
                    last: '<i class="ti ti-chevrons-right"></i>'
                },
                lengthMenu: "_MENU_ Items per page",
                info: 'Showing <span class="fw-semibold">_START_</span> to <span class="fw-semibold">_END_</span> of <span class="fw-semibold">_TOTAL_</span> Items'
            },
            initComplete: function () {
                const api = this.api();

                // Column search inputs (if you have a row with id="column-search-inputs")
                const searchInputsRow = tableElement.querySelector("#column-search-inputs");
                if (searchInputsRow) {
                    searchInputsRow.querySelectorAll("th").forEach((th, columnIndex) => {
                        th.addEventListener("click", (e) => e.stopPropagation());
                        const input = th.querySelector("input");
                        if (input) {
                            input.addEventListener("click", (e) => e.stopPropagation());
                            input.addEventListener("keyup", function () {
                                if (api.column(columnIndex).search() !== this.value) {
                                    api.column(columnIndex).search(this.value).draw();
                                }
                            });
                        }
                    });
                }

                // No column visibility logic anymore — completely removed
            }
        });

        return tableInstance;
    }

    // Initialize all your tables — all will work perfectly now
    initComplexDataTable("#table-1");
    initComplexDataTable("#table-2");
    initComplexDataTable("#table-3");
    initComplexDataTable("#table-4");
    initComplexDataTable("#table-5");
    initComplexDataTable("#table-6");
    initComplexDataTable("#table-7");
    initComplexDataTable("#table-8");
    initComplexDataTable("#table-9");
    initComplexDataTable("#table-10");
});