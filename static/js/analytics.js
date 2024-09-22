document.addEventListener('DOMContentLoaded', function() {
    // Global Metrics Chart
    const globalMetricsCtx = document.getElementById('globalMetricsChart').getContext('2d');
    const globalMetricsChart = new Chart(globalMetricsCtx, {
        type: 'bar',
        data: {
            labels: ['Likes', 'Dislikes', 'Comments'],
            datasets: [{
                label: 'Global Metrics',
                data: [globalLikes, globalDislikes, globalComments],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Individual Post Metrics Charts
    postsData.forEach(post => {
        const postMetricsCtx = document.getElementById(`postMetricsChart-${post.id}`).getContext('2d');
        const postMetricsChart = new Chart(postMetricsCtx, {
            type: 'bar',
            data: {
                labels: ['Likes', 'Dislikes', 'Comments'],
                datasets: [{
                    label: `Post ${post.id} Metrics`,
                    data: [post.likes, post.dislikes, post.comments.length],
                    backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
});