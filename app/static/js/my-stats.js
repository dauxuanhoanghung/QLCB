function revenueChart(labels, data) {
    const ctx = document.getElementById('revenueChart');

    revenue = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Doanh thu',
                data: data,
                borderWidth: 1,
                backgroundColor: ['red', 'green', 'blue', 'gold', 'brown']
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Doanh thu theo tháng'
                }
            }
        }
    });
}

function percentChart(labels, data) {
    const ctx = document.getElementById('percentChart');

    cha = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Chuyến bay',
                data: data,
                borderWidth: 1,
                backgroundColor: ['red', 'green', 'blue', 'gold', 'brown']
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tỉ lệ chuyến bay'
                }
            }
        }
    });
}