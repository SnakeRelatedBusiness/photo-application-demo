import { PhotoService } from "./api.js";

export async function handleLike(photoId, btnElement) {
    const likeCountSpan = document.getElementById(`likes-count-${photoId}`);
    if (!likeCountSpan) return;

    btnElement.disabled = true;
    const currentLikes = parseInt(likeCountSpan.textContent.trim().split(' ')[0]);
    const isCurrentlyLiked = btnElement.classList.contains('liked-active');

    if (isCurrentlyLiked) {
        likeCountSpan.textContent = `${currentLikes - 1} likes`;
        btnElement.classList.remove('liked-active');
        btnElement.textContent = 'Like ❤️';
    } else {
        likeCountSpan.textContent = `${currentLikes + 1} likes`;
        btnElement.classList.add('liked-active');
        btnElement.textContent = 'Unlike 💔';
    }

    try {
        await PhotoService.toggleLike(photoId);
    } catch (error) {
        likeCountSpan.textContent = `${currentLikes} likes`;
        if (isCurrentlyLiked) {
            btnElement.classList.add('liked-active');
            btnElement.textContent = 'Unlike 💔';
        } else {
            btnElement.classList.remove('liked-active');
            btnElement.textContent = 'Like ❤️';
        }
        alert("Could not register like. Please try again.");
    } finally {
        btnElement.disabled = false;
    }
}
