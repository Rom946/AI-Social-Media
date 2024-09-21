// Add your JavaScript code here
function generatePost() {
    const prompt = document.getElementById('promptInput').value;
    axios.post('/generate_post', { prompt })
        .then(response => {
            location.reload();
        })
        .catch(error => {
            console.error('Error generating post:', error);
        });
}

function generateRandomPost() {
    axios.post('/generate_random_post')
        .then(response => {
            location.reload();
        })
        .catch(error => {
            console.error('Error generating random post:', error);
        });
}

function likePost(postId) {
    // Implement like functionality
}

function dislikePost(postId) {
    // Implement dislike functionality
}

function generateRandomComment(postId) {
    axios.post(`/generate_random_comment/${postId}`)
        .then(response => {
            location.reload();
        })
        .catch(error => {
            console.error('Error generating random comment:', error);
        });
}

function addComment(event, postId) {
    if (event.key === 'Enter') {
        const comment = event.target.value;
        // Implement add comment functionality
    }
}