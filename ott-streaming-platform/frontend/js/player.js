redirectIfNotLoggedIn();

const contentId = localStorage.getItem("content_id");

if (!contentId) {
    window.location.href = "dashboard.html";
}

window.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname.includes("music-player.html")) {
        loadMusic();
    } else {
        loadVideo();
    }

});

async function getContent() {

    const response = await fetch(
        `${API_BASE_URL}/content/${contentId}`
    );

    if (!response.ok) {
        throw new Error("Unable to load content.");
    }

    return await response.json();

}

async function loadVideo() {

    try {

        const content = await getContent();

        document.getElementById("videoTitle").textContent =
            content.title;

        document.getElementById("title").textContent =
            content.title;

        document.getElementById("description").textContent =
            content.description;

        document.getElementById("category").textContent =
            content.category;

        document.getElementById("duration").textContent =
            `${content.duration} mins`;

        const video =
            document.getElementById("videoPlayer");

        await streamMedia(
            video,
            `${API_BASE_URL}/stream/video/${content.id}`
        );

    }

    catch(error){

        console.error(error);

        alert(error.message);

    }

}

async function loadMusic(){

    try{

        const content = await getContent();

        document.getElementById("musicTitle").textContent =
            content.title;

        document.getElementById("title").textContent =
            content.title;

        document.getElementById("artist").textContent =
            content.category;

        document.getElementById("thumbnail").src =
            `${API_BASE_URL}/thumbnails/${content.thumbnail}`;

        const audio =
            document.getElementById("audioPlayer");

        await streamMedia(
            audio,
            `${API_BASE_URL}/stream/music/${content.id}`
        );

    }

    catch(error){

        console.error(error);

        alert(error.message);

    }

}

async function streamMedia(player, url){

    const token =
        localStorage.getItem(STORAGE.TOKEN);

    const apiKey =
        localStorage.getItem(STORAGE.API_KEY);

    console.log("TOKEN:", token);
    console.log("API KEY:", apiKey);

    const response = await fetch(

        url,

        {

            headers:{

                Authorization:`Bearer ${token}`,

                "X-API-Key":apiKey

            }

        }

    );

    if(!response.ok){

        const error = await response.json();

        throw new Error(error.detail);

    }

    const blob = await response.blob();

    const blobUrl = URL.createObjectURL(blob);

    player.src = blobUrl;

}