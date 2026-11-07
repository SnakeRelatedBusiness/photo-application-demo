import { AuthService, PhotoService } from "./api.js";

export async function initialiseAuth(loginFormElement, onAuthStateChange) {
    try {
        const user = await AuthService.checkStatus();
        onAuthStateChange(user)
    } catch (error) {
        console.error("Auth initialisation failed: ", error)
        onAuthStateChange({"is_authenticated": false})
    }

    if (loginFormElement) {
        loginFormElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            try {
                const formData = new FormData(e.target);
                await AuthService.login(Object.fromEntries(formData));
                e.target.reset();

                const user = await AuthService.checkStatus();
                onAuthStateChange(user);
            } catch (error) {
                console.error(error)
                alert('Login failed. Please check your credentials.');
            }
        });
    }

}

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

export function createLikeButton(photo) {
    const controls = document.createElement('div');
    controls.style.display = 'flex';
    controls.style.gap = '15px';
    controls.style.alignItems = 'centre';

    const isLiked = photo.is_liked_by_user;
    const likeBtn = document.createElement('button')
    likeBtn.textContent = isLiked ? 'Unlike 💔' : 'Like ❤️';
    if (isLiked) {
        likeBtn.classList.add('liked-active');
    }

    likeBtn.addEventListener('click', (e) => handleLike(photo.id, e.currentTarget));

    const likeCount = document.createElement('span');
    likeCount.id = `likes-count-${photo.id}`;
    likeCount.classList.add('likes-count');
    likeCount.textContent = ` ${photo.total_likes} likes`;

    controls.append(likeBtn, likeCount);

    return controls;
}
