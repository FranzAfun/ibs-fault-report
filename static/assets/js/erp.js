// Generate random data for donut charts
function generateRandomData() {
    const labels = ["A", "B", "C"];
    let data = labels.map(label => ({
        name: label,
        value: Math.floor(Math.random() * 100) + 1
    }));

    // Calculate total for percentage conversion
    const total = data.reduce((sum, item) => sum + item.value, 0);

    // Convert values to percentages
    data.forEach(item => {
        item.value = (item.value / total) * 100;
    });

    return data;
}
$.fn.dataTable.ext.errMode = 'none';
$(document).ready(function() {

    const STORAGE_KEY = 'smartystorage';

    // 1. On Load: Check if we need to open a Tab OR a Modal
    const savedId = localStorage.getItem(STORAGE_KEY);
    if (savedId) {
        const element = document.querySelector(`[href="${savedId}"], [data-bs-target="${savedId}"], [id="${savedId.replace('#', '')}"]`);

        if (element) {
            // Check if it's a tab trigger
            if (element.hasAttribute('data-bs-toggle') && element.getAttribute('data-bs-toggle') === 'tab') {
                const tab = new bootstrap.Tab(element);
                tab.show();
            } 
            // Check if the saved ID is a Modal itself
            // else if (savedId.startsWith('#')) {
            //     const modalEl = document.querySelector(savedId);
            //     if (modalEl && modalEl.classList.contains('modal')) {
            //         const modal = new bootstrap.Modal(modalEl);
            //         modal.show();
            //     }
            // }
        }
    }

    // 2. Listen for Tab Changes
    $(document).on('shown.bs.tab', '[data-bs-toggle="tab"]', function (e) {
        let target = $(e.target).attr('data-bs-target') || $(e.target).attr('href');
        localStorage.setItem(STORAGE_KEY, target);
    });

    // 3. Listen for Modal Opening
    // $(document).on('shown.bs.modal', '.modal', function (e) {
    //     localStorage.setItem(STORAGE_KEY, '#' + $(e.target).attr('id'));
    // });

    // 4. Clear storage when Modal Closes (Optional)
    // If you don't do this, the modal will pop up EVERY time you refresh.
    // $(document).on('hidden.bs.modal', '.modal', function () {
    //     localStorage.removeItem(STORAGE_KEY);
    // });
});
// Initialize a single donut chart
function initDonutChart(selector) {
    const data = generateRandomData();

    new CustomEChart({
        selector: selector,
        options: () => ({
            tooltip: { show: false },
            series: [{
                type: "pie",
                radius: ["65%", "100%"],
                hoverAnimation: false,
                label: { show: false },
                labelLine: { show: false },
                data: data.map((item, index) => ({
                    value: item.value,
                    itemStyle: {
                        color: index === 0 ? ins("primary") :
                               index === 1 ? ins("secondary") : "#bbcae14d"
                    }
                }))
            }]
        })
    });
}

// Initialize all donut charts
const donutCharts = document.querySelectorAll(".donut-chart");
if (donutCharts) {
    donutCharts.forEach(initDonutChart);
}

// Prepare data for the orders line/bar chart (last 15 days)
var category = [];
var completeProjects = [];
var activeProjects = [];
var heldProjects = [];

fetch('/engine/dashboard_project_status/')
.then(response => response.json())
.then(data => {
        category=data.dates;
        completeProjects=data.completed;
        activeProjects=data.active;
        heldProjects=data.held;
        new CustomEChart({
            selector: "#projects_update",
            options: () => ({
                tooltip: {
                    trigger: "axis",
                    padding: [8, 15],
                    backgroundColor: ins("secondary-bg"),
                    borderColor: ins("border-color"),
                    textStyle: { color: ins("light-text-emphasis") },
                    borderWidth: 1,
                    transitionDuration: 0.125,
                    axisPointer: { type: "none" },
                    shadowBlur: 2,
                    shadowColor: "rgba(76, 76, 92, 0.15)",
                    shadowOffsetX: 0,
                    shadowOffsetY: 1,
                    formatter: function (params) {
                        const date = new Date();
                        date.setDate(today.getDate() - 14 + params[0].dataIndex);
                        const formatted = date.toLocaleDateString("en-GB", {
                            day: "2-digit",
                            month: "short",
                            year: "numeric"
                        });
        
                        return `
                            <div class="mb-1 text-body">${formatted}</div>
                            ${params.map(p => `${p.marker} ${p.seriesName}: <span class="fw-bold">${p.value}</span> Orders`).join("<br/>")}
                        `;
                    }
                },
                legend: {
                    data: ["Completed", "Active", "On Hold"],
                    top: 15,
                    textStyle: { color: ins("body-color") }
                },
                textStyle: {
                    fontFamily: getComputedStyle(document.body).fontFamily
                },
                xAxis: {
                    data: category,
                    axisLine: { lineStyle: { type: "dashed", color: ins("border-color") } },
                    axisLabel: { show: true, color: ins("secondary-color") },
                    splitLine: { lineStyle: { color: ins("border-color"), type: "dashed" } }
                },
                yAxis: {
                    axisLine: { lineStyle: { type: "dashed", color: ins("border-color") } },
                    axisLabel: { show: true, color: ins("secondary-color") },
                    splitLine: { show: false, lineStyle: { color: ins("border-color"), type: "dashed" } }
                },
                grid: {
                    left: 25,
                    right: 25,
                    bottom: 25,
                    top: 60,
                    containLabel: true
                },
                series: [
                    {
                        name: "Completed",
                        type: "line",
                        smooth: true,
                        itemStyle: { color: ins("success") },
                        showAllSymbol: true,
                        symbol: "emptyCircle",
                        symbolSize: 5,
                        data: completeProjects
                    },
                    {
                        name: "Active",
                        type: "bar",
                        barWidth: 14,
                        itemStyle: {
                            borderRadius: [5, 5, 0, 0],
                            color: ins("secondary")
                        },
                        data: activeProjects
                    },
                    {
                        name: "On Hold",
                        type: "bar",
                        barWidth: 14,
                        itemStyle: {
                            borderRadius: [5, 5, 0, 0],
                            color: "#bbcae14d"
                        },
                        data: heldProjects
                    }
                ]
            })
        });

    })
    .catch(error => console.error('Error fetching project status:', error));
// Toast notification system
function showToast(title, message, color = "primary", icon = "", timestamp = "", time_since = "", link = "") {
    let container = document.getElementById("toast-container");
    // Create container if it doesn't exist
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        // Positioning to top-0 end-0 for top-right corner
        container.className = "toast-container position-fixed top-0 end-0 p-3";
        container.style.zIndex = 1100;
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    // Ensure the text color is correct for the background
    const textColorClass = ['warning', 'info', 'light'].includes(color) ? 'text-dark' : 'text-white';
    
    toast.className = `toast text-bg-${color} border-0 fade`;
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");
    toast.id = `liveToast-${Date.now()}`;

    // Generate the "view" link HTML if the link variable is provided
    const linkHtml = link
        ? `<a href="${link}" class="link-light link-underline-opacity-0 link-underline-opacity-100-hover me-2" target="_blank">View</a>`
        : '';
    

    const iconHtml = icon
        ? `<span class="${icon} text-center me-2 ${textColorClass} bg-${color}" style="width:18px;height:18px;font-size:10px;padding:3px;border-radius:2px;" aria-hidden="true"></span>` 
        : '';


    toast.innerHTML = `
        <div class="toast-header">
            ${iconHtml}
            <strong class="me-auto ">${title}</strong>
            <small>${time_since || timestamp || 'Just now'}</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body d-flex justify-content-between align-items-center">
            <span>${message}</span>
            ${linkHtml}
        </div>
    `;
    

    container.appendChild(toast);

    // Initializing and showing the toast
    const bsToast = new bootstrap.Toast(toast, { delay: 30000 });
    bsToast.show();

    // Clean up after hide
    toast.addEventListener("hidden.bs.toast", () => {
        toast.remove();
    });
}
function hidenotification(id){
    fetch('/system/notifications/hide/'+id+'/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 'notification_id': id })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        
        if(data.status==='ok'){
            console.log('Notification hidden successfully:', data);
            unread_count=document.querySelectorAll('[identifier="notif_unread"]');
            unread_count.forEach(function(element){
                current_count=parseInt(element.textContent.trim());
                new_count=current_count-1;
                if(new_count>0){
                    element.textContent=new_count;
                }
                else{
                    element.style.display='none';
                }   
            });
        }
    }).catch(error => {
        console.error('Error hiding notification:', error);
    });
}
function readnotif(id){
    var url ='/system/notifications/read/'+id+'/';
    window.location.href = url;
    
}

// Debounce utility
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
function printDiv(div){
    var printContents = document.getElementById(div).innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
    window.location.reload();
}

/* --------------------------------------------------------------
   3. Show Chrome-only reminder (optional but nice UX)
   -------------------------------------------------------------- */
function showChromeReminder() {
  if (!isChrome) return;

  const toast = document.createElement('div');
  toast.textContent = 'Chrome tip: Open Print → More settings → Check “Background graphics” for full colour.';
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    background: '#333',
    color: '#fff',
    padding: '10px 20px',
    borderRadius: '6px',
    fontFamily: 'sans-serif',
    fontSize: '14px',
    zIndex: 9999,
    boxShadow: '0 4px 12px rgba(0,0,0,.3)',
    transition: 'opacity .3s',
    opacity: 0
  });
  document.body.appendChild(toast);

  // Fade-in
  setTimeout(() => toast.style.opacity = 1, 100);

  // Auto-hide after 6 s (or user can close)
  const hide = () => {
    toast.style.opacity = 0;
    setTimeout(() => toast.remove(), 300);
  };
  setTimeout(hide, 6000);
  toast.onclick = hide;
}

/* --------------------------------------------------------------
   4. Hook into the print process
   -------------------------------------------------------------- */
window.addEventListener('beforeprint', () => {
  forcePrintBackgrounds();
  showChromeReminder();
});

/* --------------------------------------------------------------
   5. (Optional) Run once on load – useful for “Print” buttons
   -------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  
});


document.addEventListener('submit', function (event) {
    const submitButton = event.target.querySelector('button[type="submit"], input[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>  Please wait...
        `;
    }
});