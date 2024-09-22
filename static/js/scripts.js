function generatePost() {
    const prompt = document.getElementById('promptInput').value;
    axios.post('/generate_post', { prompt })
        .then(response => {
            addPostToDOM(response.data);
        })
        .catch(error => {
            console.error('Error generating post:', error);
        });
}

function generateRandomPost() {
    axios.post('/generate_random_post')
        .then(response => {
            addPostToDOM(response.data);
        })
        .catch(error => {
            console.error('Error generating random post:', error);
        });
}

function likePost(postId) {
    const likeCount = document.querySelector(`#post-${postId} .likes-count`);
    const currentLikes = parseInt(likeCount.textContent);
    likeCount.textContent = currentLikes + 1;
    // You can add an API call here to update the like count on the server
}

function dislikePost(postId) {
    const dislikeCount = document.querySelector(`#post-${postId} .dislikes-count`);
    const currentDislikes = parseInt(dislikeCount.textContent);
    dislikeCount.textContent = currentDislikes + 1;
    // You can add an API call here to update the dislike count on the server
}

function generateRandomComment(postId) {
    axios.post(`/generate_random_comment/${postId}`)
        .then(response => {
            const newComment = response.data.comments[response.data.comments.length - 1];
            addCommentToDOM(postId, newComment);
        })
        .catch(error => {
            console.error('Error generating random comment:', error);
            if (error.response) {
                console.error(error.response.data);
                console.error(error.response.status);
            }
        });
}

function addComment(event, postId) {
    if (event.key === 'Enter') {
        const comment = event.target.value;
        // Add the comment to the DOM
        addCommentToDOM(postId, `User: ${comment}`);
        // Clear the input field
        event.target.value = '';
        // You can add an API call here to save the comment on the server
    }
}

function addPostToDOM(post) {
    const postsContainer = document.getElementById('posts');
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.id = `post-${post.id}`;
    postElement.innerHTML = `
        <div class="post-header">
            <img src="https://via.placeholder.com/30" alt="Profile Picture" class="profile-pic">
            <span class="username">${post.username}</span>
        </div>
        <img src="${post.image}" alt="${post.caption}" class="post-image">
        <div class="post-actions">
            <button onclick="likePost(${post.id})"><i class="far fa-heart"></i> <span class="likes-count">${post.likes}</span></button>
            <button onclick="dislikePost(${post.id})"><i class="far fa-thumbs-down"></i> <span class="dislikes-count">${post.dislikes}</span></button>
            <button onclick="generateRandomComment(${post.id})"><i class="far fa-comment"></i></button>
        </div>
        <div class="post-caption">
            <span class="username">${post.username}</span> ${post.caption}
        </div>
        <div class="comments"></div>
        <div class="add-comment">
            <input type="text" placeholder="Add a comment..." onkeypress="addComment(event, ${post.id})">
        </div>
    `;
    postsContainer.insertBefore(postElement, postsContainer.firstChild);
}

function addCommentToDOM(postId, comment) {
    const commentsContainer = document.querySelector(`#post-${postId} .comments`);
    const commentElement = document.createElement('p');
    const [username, commentText] = comment.split(':');
    commentElement.innerHTML = `<strong>${username}</strong>: ${commentText}`;
    commentsContainer.appendChild(commentElement);
}
