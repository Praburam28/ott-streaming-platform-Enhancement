function getToken() {
    return localStorage.getItem(STORAGE.TOKEN);
}

function getApiKey() {
    return localStorage.getItem(STORAGE.API_KEY);
}

function saveToken(token) {
    localStorage.setItem(STORAGE.TOKEN, token);
}

function saveApiKey(apiKey) {
    localStorage.setItem(STORAGE.API_KEY, apiKey);
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

function authHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`
    };
}

function streamHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`,
        "X-API-Key": getApiKey()
    };
}

function isLoggedIn() {
    return !!getToken();
}

function redirectIfNotLoggedIn() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
    }
}