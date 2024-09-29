// Function to generate a post with a given or random prompt
async function generatePost(prompt = null) {
    try {
        const response = await fetch('/generate_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });
        const post = await response.json();
        addPostToDOM(post);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to generate a random post
async function generateRandomPost() {
    try {
        const response = await fetch('/generate_random_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const post = await response.json();
        addPostToDOM(post);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to add a post to the DOM
function addPostToDOM(post) {
    const postsContainer = document.getElementById('posts');
    if (postsContainer.children.length >= 10) {
        postsContainer.removeChild(postsContainer.firstChild);
    }
    const newPost = createPostElement(post);
    postsContainer.insertBefore(newPost, postsContainer.firstChild);  // Insert new post at the top
}

// Function to create a post element
function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.id = `post-${post.id}`;
    postElement.innerHTML = `
        <h2>${post.caption}</h2>
        <p>Posted by ${post.username} on ${post.date}</p>
        <img src="${post.image}" alt="${post.caption}">
        <div class="post-actions">
            <button onclick="likePost(${post.id})">Like (<span class="likes-count">${post.likes}</span>)</button>
            <button onclick="dislikePost(${post.id})">Dislike (<span class="dislikes-count">${post.dislikes}</span>)</button>
            <button onclick="generateRandomComment(${post.id})">Generate Random Comment</button>
            <input type="text" placeholder="Add a comment" onkeypress="addComment(event, ${post.id})">
        </div>
        <div class="comments"></div>
    `;
    return postElement;
}

// Function to handle liking a post
async function likePost(postId) {
    try {
        const response = await fetch(`/like_post/${postId}`, { method: 'POST' });
        const data = await response.json();
        const likesCount = document.querySelector(`#post-${postId} .likes-count`);
        likesCount.textContent = data.likes;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to handle disliking a post
async function dislikePost(postId) {
    try {
        const response = await fetch(`/dislike_post/${postId}`, { method: 'POST' });
        const data = await response.json();
        const dislikesCount = document.querySelector(`#post-${postId} .dislikes-count`);
        dislikesCount.textContent = data.dislikes;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to add a comment to a post when the Enter key is pressed
async function addComment(event, postId) {
    if (event.key === 'Enter') {
        const commentInput = event.target;
        const comment = commentInput.value;
        try {
            const response = await fetch(`/add_comment/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment: comment }),
            });
            const data = await response.json();
            const commentsContainer = document.querySelector(`#post-${postId} .comments`);
            commentsContainer.innerHTML = data.comments.map(c => `<p>${c}</p>`).join('');
            commentInput.value = '';
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// Function to generate a random comment for a post
async function generateRandomComment(postId) {
    try {
        const response = await fetch(`/generate_random_comment/${postId}`, { method: 'POST' });
        const data = await response.json();
        const commentsContainer = document.querySelector(`#post-${postId} .comments`);
        commentsContainer.innerHTML = data.comments.map(c => `<p>${c}</p>`).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}