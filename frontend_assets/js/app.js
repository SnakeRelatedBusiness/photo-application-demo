// static/js/app.js
import { PhotoService } from './api.js';
import { handleLike , createTagList, createLikeControls, initialiseAuth} from './common.js';

// DOM Elements
const UI = {
    loginForm: document.getElementById('login-form'),
    welcomeSection: document.getElementById('welcome-section'),
    uploadSection: document.getElementById('upload-section'),
    welcomeMessage: document.getElementById('welcome-message'),
    feedContainer: document.getElementById('feed-container'),
    uploadForm: document.getElementById('upload-form')
};

async function initApp() {
    bindUploadEvent();

    const params = new URLSearchParams(window.location.search);
    const tagFromUrl = params.get('tag');

    await initialiseAuth(UI.loginForm, async (user) => {
        const isAuth = user.is_authenticated;

        UI.loginForm.classList.toggle('hidden', isAuth);
        UI.welcomeSection.classList.toggle('hidden', !isAuth);
        UI.uploadSection.classList.toggle('hidden', !isAuth);

        if (isAuth) {
            UI.welcomeMessage.textContent = `Welcome back, ${user.username}!`;
            await loadFeed(tagFromUrl)
        } else {
            UI.feedContainer.textContent = 'Please log in to view the feed.';
        }
    })
}


async function loadFeed(tagFilter = null) {
    const endPointQuery = tagFilter ? `?tag=${tagFilter}` : '';
    UI.feedContainer.textContent = 'Loading...';

    try {
        const photos = await PhotoService.getFeed(endPointQuery);
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

            const tagList = createTagList(photo.tags);
            const controls = createLikeControls(photo);


            card.append(caption, author, imgLink, tagList, controls);
            UI.feedContainer.appendChild(card);
        });
    } catch (error) {
        UI.feedContainer.textContent = 'Failed to load feed.';
        console.error(error)
    }
}

// --- Event Handlers ---
function bindUploadEvent() {
    UI.uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData(e.target);

            const tagString = formData.get('tags');
            formData.delete('tags') // remove string from payload

            if (tagString) {
                const tagList = tagString.split(',').map(t => t.trim()).filter(Boolean);
                console.log(tagList);
                tagList.forEach(tag => formData.append('tags', tag));
            }

            await PhotoService.upload(formData);
            e.target.reset();
            await loadFeed();
        } catch (error) {
            console.error(error)
            alert('Upload failed.');
        }
    });
}

// Boot the application once HTML has fully loaded
document.addEventListener('DOMContentLoaded', initApp);