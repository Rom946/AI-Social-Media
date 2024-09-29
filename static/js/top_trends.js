document.getElementById('update-trends-button').addEventListener('click', async function() {
    try {
        const response = await fetch('/update_trends', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            location.reload();  // Reload the page to reflect updated trends
        } else {
            alert('Failed to update trends');
        }
    } catch (error) {
        console.error('Error updating trends:', error);
    }
});
