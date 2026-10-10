// static/api.js

// Private helper to extract cookies
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
};

// Generic fetch wrapper to attach CSRF and handle JSON parsing uniformly
async function fetchAPI(endpoint, options = {}) {
    const headers = {
        'X-CSRFToken': getCookie('csrftoken'),
        ...options.headers,
    };

    const response = await fetch(endpoint, { ...options, headers });

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    // Avoid parsing JSON on 204 No Content
    return response.status !== 204 ? await response.json() : null;
}

export const AuthService = {
    checkStatus: () => fetchAPI('/api/auth/me/'),
    login: (credentials) => fetchAPI('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
    })
};

export const PhotoService = {
    getFeed: () => fetchAPI('/api/feed/'),
    getPhoto: (id) => fetchAPI(`/api/photos/${id}/`),
    deletePhoto: (id) => fetchAPI(`/api/photos/${id}/delete/`, {
        method: 'DELETE'
    }),
    upload: (formData) => fetchAPI('/api/photos/upload/', {
        method: 'POST',
        body: formData
    }),
    toggleLike: (photoId) => fetchAPI(`/api/photos/${photoId}/like/`, {
        method: 'POST'
    })
};