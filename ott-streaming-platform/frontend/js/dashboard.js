redirectIfNotLoggedIn();

const loading = document.getElementById("loading");
const emptyMessage = document.getElementById("emptyMessage");
const searchInput = document.getElementById("searchInput");

let allContents = [];

document
    .getElementById("logoutBtn")
    .addEventListener("click", logout);

window.addEventListener("DOMContentLoaded", async () => {

    await loadProfile();
    await loadUsageMetrics();
    await loadContents();

});

searchInput.addEventListener("input", () => {

    const keyword = searchInput.value.trim().toLowerCase();

    const filtered = allContents.filter(content =>

        content.title.toLowerCase().includes(keyword) ||
        content.category.toLowerCase().includes(keyword) ||
        content.content_type.toLowerCase().includes(keyword)

    );

    renderContents(filtered);

});

async function loadProfile() {

    try {

        const response = await fetch(

            `${API_BASE_URL}/profile`,

            {

                headers: authHeaders()

            }

        );

        if (!response.ok) {

            logout();

            return;

        }

        const user = await response.json();

        document.getElementById("welcomeUser").textContent =
            `Hi, ${user.full_name}`;

    }

    catch (error) {

        console.error(error);

    }

}

async function loadContents() {

    loading.style.display = "block";

    emptyMessage.style.display = "none";

    try {

        const response = await fetch(

            `${API_BASE_URL}/content`

        );

        if (!response.ok)

            throw new Error("Unable to load contents.");

        allContents = await response.json();

        renderContents(allContents);

    }

    catch (error) {

        console.error(error);

        emptyMessage.style.display = "block";

        emptyMessage.textContent =
            "Unable to load contents.";

    }

    finally {

        loading.style.display = "none";

    }

}

function renderContents(contents) {

    const movieContainer =
        document.getElementById("movieContainer");

    const seriesContainer =
        document.getElementById("seriesContainer");

    const musicContainer =
        document.getElementById("musicContainer");

    movieContainer.innerHTML = "";

    seriesContainer.innerHTML = "";

    musicContainer.innerHTML = "";

    if (contents.length === 0) {

        emptyMessage.style.display = "block";

        return;

    }

    emptyMessage.style.display = "none";

    contents.forEach(content => {

        const card = createCard(content);

        switch (content.content_type) {

            case "MOVIE":

                movieContainer.appendChild(card);

                break;

            case "SERIES":

                seriesContainer.appendChild(card);

                break;

            case "MUSIC":

                musicContainer.appendChild(card);

                break;

        }

    });

}

function createCard(content) {

    const card = document.createElement("div");

    card.className = "movie-card";

    const plan =

        content.plan_name ||

        content.plan ||

        "Free";

    card.innerHTML = `

        <img
            src="${API_BASE_URL}/thumbnails/${content.thumbnail}"
            alt="${content.title}">

        <h3>${content.title}</h3>

        <p>${content.category}</p>

        <p>

            <strong>${plan}</strong>

        </p>

        <div class="card-buttons">

            <button
                class="primary-btn play-btn">

                ▶ Play

            </button>

            <button
                class="favorite-btn"
                title="Add to Favorites">

                ❤️

            </button>

        </div>

    `;

    card.querySelector(".play-btn")
        .addEventListener("click", () => {

            playContent(

                content.id,

                content.content_type

            );

        });

    card.querySelector(".favorite-btn")
        .addEventListener("click", () => {

            addFavorite(content.id);

        });

    return card;

}

function playContent(id, type) {

    localStorage.setItem("content_id", id);

    if (type === "MUSIC") {

        window.location.href = "music-player.html";

    }

    else {

        window.location.href = "video-player.html";

    }

}

async function addFavorite(contentId) {

    try {

        const response = await fetch(

            `${API_BASE_URL}/profile/favorites/${contentId}`,

            {

                method: "POST",

                headers: authHeaders()

            }

        );

        if (response.ok) {

            alert("❤️ Added to Favorites");

        }

        else {

            const error = await response.json();

            alert(error.detail);

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to add to Favorites.");

    }

}

// ======================================
// Usage Metrics
// ======================================

async function loadUsageMetrics() {

    try {

        const response = await fetch(

            `${API_BASE_URL}/profile/usage`,

            {

                headers: authHeaders()

            }

        );

        if (!response.ok) {

            throw new Error("Unable to load usage metrics.");

        }

        const usage = await response.json();

        renderUsageMetrics(usage);

    }

    catch (error) {

        console.error(error);

    }

}

function renderUsageMetrics(usage) {

    const container = document.getElementById("usageMetrics");

    container.innerHTML = "";

    container.appendChild(
        createUsageCard(
            "Movies",
            usage.movies_used,
            usage.movies_limit
        )
    );

    container.appendChild(
        createUsageCard(
            "Series",
            usage.series_used,
            usage.series_limit
        )
    );

    container.appendChild(
        createUsageCard(
            "Music",
            usage.music_used,
            usage.music_limit
        )
    );

}

function createUsageCard(
    title,
    used,
    limit
) {

    const percentage = Math.min(
        Math.round((used / limit) * 100),
        100
    );

    let warning = "";

    if (percentage >= 100) {

        warning =
            `<p class="usage-danger">
                ❌ Usage limit exceeded
            </p>`;

    }

    else if (percentage >= 80) {

        warning =
            `<p class="usage-warning">
                ⚠ Approaching limit
            </p>`;

    }

    const card = document.createElement("div");

    card.className = "usage-card";

    card.innerHTML = `

        <h3>${title}</h3>

        <progress
            value="${used}"
            max="${limit}">
        </progress>

        <p>

            ${used} / ${limit}

            (${percentage}%)

        </p>

        ${warning}

    `;

    return card;

}