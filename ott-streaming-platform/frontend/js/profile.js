redirectIfNotLoggedIn();

loadProfile();
loadHistory();
loadFavorites();

async function loadProfile() {

    const response = await fetch(
        `${API_BASE_URL}/profile`,
        {
            headers: authHeaders()
        }
    );

    const user = await response.json();

    document.getElementById("fullName").innerText = user.full_name;
    document.getElementById("email").innerText = user.email;
    document.getElementById("role").innerText = user.role;
    document.getElementById("subscription").innerText = user.subscription;
    document.getElementById("apiKey").value = user.api_key;
}

async function loadHistory() {

    const response = await fetch(
        `${API_BASE_URL}/profile/history`,
        {
            headers: authHeaders()
        }
    );

    const data = await response.json();

    const container = document.getElementById("historyContainer");

    container.innerHTML = "";

    if (data.length === 0) {
        container.innerHTML = "<p>No watch history found.</p>";
        return;
    }

    data.forEach(item => {

        container.innerHTML += `
            <div class="history-card">

                <img
                    src="${API_BASE_URL}/thumbnails/${item.thumbnail}"
                    alt="${item.title}"
                    class="favorite-thumbnail"
                >

                <div class="history-info">
                    <h3>${item.title}</h3>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Type:</strong> ${item.content_type}</p>
                </div>

            </div>
        `;

    });

}

async function loadFavorites() {

    const response = await fetch(
        `${API_BASE_URL}/profile/favorites`,
        {
            headers: authHeaders()
        }
    );

    const data = await response.json();

    const container = document.getElementById("favoriteContainer");

    container.innerHTML = "";

    if (data.length === 0) {
        container.innerHTML = "<p>No favorites added.</p>";
        return;
    }

    data.forEach(item => {

        container.innerHTML += `
            <div class="history-card">

                <img
                    src="${API_BASE_URL}/thumbnails/${item.thumbnail}"
                    alt="${item.title}"
                    class="favorite-thumbnail"
                >

                <div class="history-info">
                    <h3>${item.title}</h3>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Type:</strong> ${item.content_type}</p>
                </div>

            </div>
        `;

    });

}