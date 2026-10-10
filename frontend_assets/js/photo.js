// static/js/photo.js
import { AuthService, PhotoService } from './api.js';
import { handleLike } from './common.js';

// DOM Elements
const UI = {
    loginForm: document.getElementById('login-form'),
    photoContainer : document.getElementById('photo-container'),
    navContainer : document.getElementById('nav-container'),
}

// --- State & Initialization ---
async function initApp() {
    await checkAuthAndRender();
}

async function      checkAuthAndRender() {
    try {
        const user = await AuthService.checkStatus();
        toggleAuthState(user);

        if (user.is_authenticated) {
            await loadPhoto();
        } else {
            UI.photoContainer.textContent = 'Please log in to view the photo.';
        }
    } catch (error) {
        console.error("Initialization failed:", error);
    }
}

// --- UI Rendering ---
function toggleAuthState(user) {
    const isAuth = user.is_authenticated;
    UI.loginForm.classList.toggle('hidden', isAuth);
    UI.navContainer.classList.toggle('hidden', !isAuth);
}

async function loadPhoto() {
    UI.photoContainer.textContent = 'Loading...';

    const pattern = new URLPattern({pathname: '/photos/:id/'});
    const match = pattern.exec(window.location.href);
    const photoId = match?.pathname.groups.id;

    if (!photoId) {
        UI.photoContainer.textContent = 'Invalid Photo URL.';
        return;
    }

    try {
        const [user, photo] = await Promise.all([
            AuthService.checkStatus(),
            PhotoService.getPhoto(photoId)
        ])

        renderPhoto(photo, user)
    } catch(error) {
        console.log("error loading photo:", error)
        UI.photoContainer.textContent = 'Photo not found or failed to load'
    }
}

function renderPhoto(photo, user) {
    UI.photoContainer.innerHTML = ''// Clear loading text

    const caption = document.createElement('h1');
    caption.textContent = photo.caption || 'Untitled';

    const author = document.createElement('p')
    author.textContent = 'Uploaded by: ';
    const authorName = document.createElement('strong');
    authorName.textContent = photo.author;
    author.appendChild(authorName)

    const img = document.createElement('img');
    img.src = photo.image;
    img.style.width = '100%'
    img.style.maxHeight = '800px'

    const dateText = document.createElement('p');
    const smallDate = document.createElement('small');
    smallDate.textContent = `Uploaded at: ${photo.uploaded_at ? new Date(photo.uploaded_at).toLocaleString("en-US") : 'Unknown'}`;
    dateText.appendChild(smallDate);
    dateText.style.marginBottom = '15px';

    const controls = document.createElement('div');
    controls.style.display = 'flex';
    controls.style.gap = '15px';
    controls.style.alignItems = 'center';

    const isLiked = photo.is_liked_by_user;
    const likeBtn = document.createElement('button');
    likeBtn.textContent = isLiked ? 'Unlike 💔' : 'Like ❤️';
    if (isLiked) likeBtn.classList.add('liked-active');

    const likeCount = document.createElement('span');
    likeCount.id = `likes-count-${photo.id}`;
    likeCount.textContent = `${photo.total_likes} likes`;

    likeBtn.addEventListener('click', (e) => handleLike(photo.id, e.currentTarget));
    controls.append(likeBtn, likeCount);

    if (user.is_authenticated && photo.user_id === user.id) {
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete 🗑️';
        deleteBtn.style.backgroundColor = '#ef4444'; // Red styling from CSS
        deleteBtn.addEventListener('click', () => handleDelete(photo.id));
        controls.appendChild(deleteBtn);
    }

    UI.photoContainer.append(caption, author, img, dateText, controls);
}



async function handleDelete(photoId) {
    if (!confirm("Are you sure you want to delete this photo?")) return;

    try {
        await PhotoService.deletePhoto(photoId)
        window.location.href = '/'
    } catch (error) {
        alert("Failed to delete photo. Ensure you have permission.");
    }
}

document.addEventListener('DOMContentLoaded', initApp);