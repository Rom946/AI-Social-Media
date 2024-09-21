function generatePost() {
    const prompt = document.getElementById('promptInput').value;
    fetch('/generate_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => response.json())
    .then(post => {
        const postsContainer = document.getElementById('posts');
        const newPost = createPostElement(post);
        if (postsContainer.children.length >= 3) {
            postsContainer.removeChild(postsContainer.firstChild);
        }
        postsContainer.appendChild(newPost);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.id = `post-${post.id}`;
    postElement.innerHTML = `
        <img src="${post.image}" alt="${post.caption}">
        <p class="caption">${post.caption}</p>
        <div class="post-actions">
            <button onclick="likePost(${post.id})">Like (<span class="likes-count">${post.likes}</span>)</button>
            <input type="text" placeholder="Add a comment" onkeypress="addComment(event, ${post.id})">
        </div>
        <div class="comments"></div>
    `;
    return postElement;
}

function likePost(postId) {
    fetch(`/like_post/${postId}`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        const likesCount = document.querySelector(`#post-${postId} .likes-count`);
        likesCount.textContent = data.likes;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function addComment(event, postId) {
    if (event.key === 'Enter') {
        const commentInput = event.target;
        const comment = commentInput.value;
        fetch(`/add_comment/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment: comment }),
        })
        .then(response => response.json())
        .then(data => {
            const commentsContainer = document.querySelector(`#post-${postId} .comments`);
            commentsContainer.innerHTML = data.comments.map(c => `<p>${c}</p>`).join('');
            commentInput.value = '';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}
