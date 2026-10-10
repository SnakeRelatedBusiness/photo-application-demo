// static/js/app.js
import { AuthService, PhotoService } from './api.js';
import { handleLike } from './common.js';

// DOM Elements
const UI = {
    loginForm: document.getElementById('login-form'),
    welcomeSection: document.getElementById('welcome-section'),
    uploadSection: document.getElementById('upload-section'),
    welcomeMessage: document.getElementById('welcome-message'),
    feedContainer: document.getElementById('feed-container'),
    uploadForm: document.getElementById('upload-form')
};

// --- State & Initialization ---
async function initApp() {
    bindEvents();
    await checkAuthAndRender();
}

async function      checkAuthAndRender() {
    try {
        const user = await AuthService.checkStatus();
        toggleAuthState(user);

        if (user.is_authenticated) {
            await loadFeed();
        } else {
            UI.feedContainer.textContent = 'Please log in to view the feed.';
        }
    } catch (error) {
        console.error("Initialization failed:", error);
    }
}

// --- UI Rendering ---
function toggleAuthState(user) {
    const isAuth = user.is_authenticated;

    UI.loginForm.classList.toggle('hidden', isAuth);
    UI.welcomeSection.classList.toggle('hidden', !isAuth);
    UI.uploadSection.classList.toggle('hidden', !isAuth);

    if (isAuth) {
        // Safe injection via textContent
        UI.welcomeMessage.textContent = `Welcome back, ${user.username}!`;
    }
}

async function loadFeed() {
    UI.feedContainer.textContent = 'Loading...';
    try {
        const photos = await PhotoService.getFeed();
        UI.feedContainer.innerHTML = ''; // Clear loading text

        photos.forEach(photo => {
            const card = document.createElement('article');
            card.className = 'photo-card';

            const caption = document.createElement('h3');
            caption.textContent = photo.caption || 'Untitled';

            const author = document.createElement('p');
            author.textContent = 'By: ';
            const authorName = document.createElement('strong');
            authorName.textContent = photo.author;
            author.appendChild(authorName);

            const imgLink = document.createElement('a');
            imgLink.href = `/photos/${photo.id}/`;
            const img = document.createElement('img');
            img.src = photo.image_url;
            img.alt = photo.caption;
            imgLink.appendChild(img);

            const controls = document.createElement('div');
            const isLiked = photo.is_liked_by_user;

            const btnClass = isLiked ? 'liked-active' : '';
            const btnText = isLiked ? 'Unlike 💔' : 'Like ❤️';
            const likeBtn = document.createElement('button');
            likeBtn.textContent = btnText;
            if (btnClass) likeBtn.classList.add(btnClass);

            likeBtn.addEventListener('click', (e) => handleLike(photo.id, e.currentTarget));

            const likeCount = document.createElement('span');
            likeCount.classList.add('likes-count');
            likeCount.id = `likes-count-${photo.id}`; // Add this missing line
            likeCount.textContent = `  ${photo.total_likes} likes`;

            controls.append(likeBtn, likeCount);
            card.append(caption, author, imgLink, controls);
            UI.feedContainer.appendChild(card);
        });
    } catch (error) {
        UI.feedContainer.textContent = 'Failed to load feed.';
    }
}

// --- Event Handlers ---
function bindEvents() {
    UI.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData(e.target);
            await AuthService.login(Object.fromEntries(formData));
            e.target.reset();
            await checkAuthAndRender();
        } catch (error) {
            alert('Login failed. Please check your credentials.');
        }
    });

    UI.uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await PhotoService.upload(new FormData(e.target));
            e.target.reset();
            await loadFeed();
        } catch (error) {
            alert('Upload failed.');
        }
    });
}

// Boot the application once HTML has fully loaded
document.addEventListener('DOMContentLoaded', initApp);