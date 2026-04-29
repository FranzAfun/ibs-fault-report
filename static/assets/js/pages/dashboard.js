// X-axis labels: Day 1 to Day 15
const xLabels = Array.from({ length: 15 }, (_, index) => `Day ${index + 1}`);

// Generate random percentage data for donut charts
function generateRandomData() {
    const charities = ["Charity A", "Charity B", "Charity C"];
    let data = charities.map(name => ({
        name,
        value: Math.floor(Math.random() * 100) + 1
    }));

    // Calculate total to convert values into percentages
    const total = data.reduce((sum, item) => sum + item.value, 0);

    // Normalize to percentages
    data.forEach(item => {
        item.value = (item.value / total) * 100;
    });

    return data;
}

// Initialize a single donut chart
function initDonutChart(selector) {
    const data = generateRandomData();

    new CustomEChart({
        selector,
        options: () => ({
            tooltip: { show: false },
            series: [{
                type: "pie",
                radius: ["60%", "100%"],
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

// Revenue & Orders Line Chart (15-day trend)
new CustomEChart({
    selector: "#revenue-chart",
    options: () => ({
        textStyle: {
            fontFamily: getComputedStyle(document.body).fontFamily
        },
        tooltip: {
            trigger: "axis",
            padding: [5, 0],
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
                const day = params[0].name;
                let html = `
                    <div style="font-size: 14px; font-weight: 600; text-transform: uppercase; 
                                border-bottom: 1px solid ${ins("border-color")}; 
                                margin-bottom: 8px; padding: 3px 10px 8px;">
                        ${day}
                    </div>
                `;

                params.forEach(p => {
                    const value = p.seriesName === "Total Revenue" 
                        ? "$" + p.value 
                        : p.value + " sales";

                    html += `
                        <div style="margin-top: 4px; padding: 3px 15px;">
                            <span style="display:inline-block; margin-right:5px; 
                                        border-radius:50%; width:10px; height:10px; 
                                        background-color:${p.color};"></span>
                            ${p.seriesName}: <strong>${value}</strong>
                        </div>
                    `;
                });

                return html;
            }
        },
        xAxis: {
            type: "category",
            data: xLabels,
            boundaryGap: false,
            axisLine: { show: false },
            axisTick: { show: false },
            axisLabel: { color: ins("secondary-color"), margin: 15 },
            splitLine: { show: false }
        },
        yAxis: {
            type: "value",
            splitLine: { lineStyle: { color: "#676b891f", type: "dashed" } },
            boundaryGap: false,
            axisLabel: {
                show: true,
                color: ins("secondary-color"),
                margin: 15,
                formatter: value => "$" + value
            },
            axisTick: { show: false },
            axisLine: { show: false }
        },
        series: [
            {
                name: "Total Revenue",
                type: "line",
                smooth: true,
                symbolSize: 2,
                itemStyle: { color: ins("primary"), borderColor: ins("primary"), borderWidth: 2 },
                areaStyle: { opacity: 0.2, color: ins("primary") },
                lineStyle: { color: ins("primary") },
                symbol: "circle",
                stack: "data",
                data: [45, 88, 120, 160, 210, 240, 350, 420, 380, 500, 640, 710, 890, 1150, 1200]
            },
            {
                name: "Orders",
                type: "line",
                smooth: true,
                symbolSize: 2,
                itemStyle: { color: ins("secondary"), borderColor: ins("secondary"), borderWidth: 2 },
                areaStyle: { opacity: 0.2, color: ins("secondary") },
                lineStyle: { color: ins("secondary") },
                symbol: "circle",
                stack: "data",
                data: [15, 30, 35, 50, 55, 75, 95, 120, 135, 160, 180, 210, 250, 390, 450]
            }
        ],
        grid: {
            right: 20,
            left: 5,
            bottom: 5,
            top: 8,
            containLabel: true
        }
    })
});

// Project Progress Rose Chart (Nightingale-style)
new CustomEChart({
    selector: "#project-progress-chart",
    options: () => ({
        tooltip: {
            trigger: "item",
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
            shadowOffsetY: 1
        },
        textStyle: {
            fontFamily: getComputedStyle(document.body).fontFamily
        },
        series: [{
            name: "Project Progress",
            type: "pie",
            radius: [60, 100],
            center: ["50%", "50%"],
            roseType: "area",
            itemStyle: { borderRadius: 8 },
            label: { color: ins("secondary-color") },
            data: [
                { value: 85, name: "Website Redesign", itemStyle: { color: ins("primary") } },
                { value: 70, name: "Mobile App", itemStyle: { color: ins("secondary") } },
                { value: 55, name: "CRM Integration", itemStyle: { color: ins("info") } },
                { value: 60, name: "Product Launch", itemStyle: { color: ins("success") } },
                { value: 75, name: "Backend Refactor", itemStyle: { color: ins("light") } },
                { value: 50, name: "Client Dashboard", itemStyle: { color: ins("warning") } }
            ]
        }]
    })
});

// Initialize all donut charts on the page
const donutCharts = document.querySelectorAll(".donut-chart");
if (donutCharts.length > 0) {
    donutCharts.forEach(initDonutChart);
}