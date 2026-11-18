import { AuthService, PhotoService } from './api.js';

const UI = {
    profileContainer: document.getElementById('profile-container')
};

async function initProfileView() {
    try {
        const user = await AuthService.checkStatus();
        if (user.is_authenticated) {
            await loadProfileFeed();
        } else {
            window.location.href = '/';
        }
    } catch (error) {
        console.error("Initialization failed:", error);
    }
}

async function loadProfileFeed() {
    UI.profileContainer.textContent = 'Loading your photos...';
    try {
        const photos = await PhotoService.getProfileFeed();
        UI.profileContainer.innerHTML = '';

        if (photos.length === 0) {
            UI.profileContainer.textContent = "Upload some photos to your profile.";
            return;
        }

        UI.profileContainer.style.display = 'grid';
        UI.profileContainer.style.gridTemplateColumns = 'repeat(auto-fill, minmax(200px, 1fr))';
        UI.profileContainer.style.gap = '15px';

        photos.forEach(photo => {
            const card = document.createElement('article');
            card.className = 'photo-card';
            card.style.display = 'flex';
            card.style.flexDirection = 'column';

            const imgLink = document.createElement('a');
            imgLink.href = `/photos/${photo.id}/`;

            const img = document.createElement('img');
            img.src = photo.thumbnail_url || photo.image_url;
            img.alt = photo.title || 'Photo';
            img.style.width = '100%';
            img.style.aspectRatio = '1 / 1';
            img.style.objectFit = 'cover';

            imgLink.appendChild(img);

            const statsContainer = document.createElement('div');
            statsContainer.style.padding = '4px 4px';
            statsContainer.style.fontSize = '0.9rem';
            statsContainer.style.color = '#555';
            statsContainer.textContent = `❤️ ${photo.total_likes}`;

            card.append(imgLink, statsContainer);
            UI.profileContainer.appendChild(card);
        });
    } catch (error) {
        UI.profileContainer.textContent = 'Failed to load profile feed.';
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', initProfileView);