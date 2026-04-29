class UnifiedDataView {
    constructor() {
        this.container = document.querySelector('[data-custom-table-container]');
        if (!this.container) return;

        this.gridItems = Array.from(this.container.querySelectorAll('[data-project-item]'));
        this.tableRows = Array.from(this.container.querySelectorAll('[data-table] tbody tr'));
        this.allItems = [...this.gridItems.map(el => ({ el, type: 'grid' })), 
                         ...this.tableRows.map(el => ({ el, type: 'table' }))];

        this.searchInput = document.getElementById('search-input');
        this.statusFilter = document.querySelector('select[data-filter="status"]') || 
                           document.querySelector('select option[value="On Track"]').closest('select');
        this.deadlineFilter = document.querySelector('select option[value="This Week"]').closest('select');

        this.init();
    }

    init() {
        // Search
        if (this.searchInput) {
            this.searchInput.addEventListener('keyup', () => this.applyFilters());
        }

        // Filters
        document.querySelectorAll('#filter-form select').forEach(select => {
            select.addEventListener('change', () => this.applyFilters());
        });

        // Apply button
        document.querySelector('#filter-form button[type="submit"]')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.applyFilters();
        });

        // Initial filter
        this.applyFilters();
    }

    getProjectData(element) {
        if (element.hasAttribute('data-project-name')) {
            // Grid item
            return {
                name: element.dataset.projectName || '',
                status: element.dataset.projectStatus || '',
                deadline: element.dataset.projectDeadline || ''
            };
        } else {
            // Table row
            const cells = element.querySelectorAll('td');
            return {
                name: cells[1]?.querySelector('a')?.textContent?.trim().toLowerCase() || '',
                status: cells[3]?.querySelector('.badge')?.textContent?.trim().toLowerCase() || '',
                deadline: cells[8]?.textContent?.trim() || ''
            };
        }
    }

    matchesSearch(project, term) {
        return project.name.includes(term);
    }

    matchesStatus(project, statusValue) {
        if (!statusValue || statusValue === 'Status') return true;
        const statusMap = {
            'on track': 'on track',
            'delayed': 'delayed',
            'at risk': 'at risk',
            'completed': 'completed'
        };
        return project.status === (statusMap[statusValue.toLowerCase()] || statusValue.toLowerCase());
    }

    matchesDeadline(project, deadlineValue) {
        if (!deadlineValue || deadlineValue === 'Deadline') return true;

        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const projectDate = new Date(project.deadline);
        if (isNaN(projectDate)) return deadlineValue === 'No Deadline';

        const isThisWeek = projectDate >= new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay())
            && projectDate <= new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay() + 6);
        const isThisMonth = projectDate.getMonth() === today.getMonth() && projectDate.getFullYear() === today.getFullYear();
        const isNextMonth = projectDate.getMonth() === (today.getMonth() + 1) % 12 && projectDate.getFullYear() === (today.getMonth() === 11 ? today.getFullYear() + 1 : today.getFullYear());

        switch (deadlineValue) {
            case 'This Week': return isThisWeek;
            case 'This Month': return isThisMonth;
            case 'Next Month': return isNextMonth;
            case 'No Deadline': return isNaN(projectDate);
            default: return true;
        }
    }

    applyFilters() {
        const searchTerm = (this.searchInput?.value || '').toLowerCase();
        const statusFilter = (this.statusFilter?.value || '');
        const deadlineFilter = (this.deadlineFilter?.value || '');

        let visibleCount = 0;

        this.allItems.forEach(item => {
            const project = this.getProjectData(item.el);
            const matchesSearch = this.matchesSearch(project, searchTerm);
            const matchesStatus = this.matchesStatus(project, statusFilter);
            const matchesDeadline = this.matchesDeadline(project, deadlineFilter);

            const shouldShow = matchesSearch && matchesStatus && matchesDeadline;

            if (shouldShow) visibleCount++;

            if (item.type === 'grid') {
                item.el.style.display = shouldShow ? '' : 'none';
            } else {
                item.el.style.display = shouldShow ? '' : 'none';
            }
        });

        // Update "No results" message in grid
        const gridContainer = document.getElementById('employee-list-container');
        let noResultsMsg = gridContainer.querySelector('.no-results-msg');
        if (!noResultsMsg && visibleCount === 0) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.className = 'col-12 text-center py-5 no-results-msg';
            noResultsMsg.innerHTML = '<p class="text-muted">No projects found matching your filters.</p>';
            gridContainer.appendChild(noResultsMsg);
        } else if (noResultsMsg && visibleCount > 0) {
            noResultsMsg.remove();
        }
    }
}

// Keep your original Table class for list view sorting/pagination (optional)
// But now filtering is handled globally above

// Initialize unified filtering
document.addEventListener("DOMContentLoaded", () => {
    new UnifiedDataView();

    // Initialize original table features (sorting, pagination, etc.) only on list view
    new CustomTable({
        tableSelector: '[data-table]',
        rowsPerPage: 10
    });
});