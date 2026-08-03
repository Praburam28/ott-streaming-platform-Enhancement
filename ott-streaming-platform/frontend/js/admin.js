redirectIfNotLoggedIn();

loadContents();

document
.getElementById("uploadForm")
.addEventListener("submit", uploadContent);

async function uploadContent(e){

e.preventDefault();

const formData = new FormData();

formData.append("title",
title.value);

formData.append("description",
description.value);

formData.append("content_type",
contentType.value);

formData.append("category",
category.value);

formData.append("duration",
duration.value);

formData.append("plan_id",
planId.value);

formData.append(
"thumbnail",
thumbnail.files[0]
);

formData.append(
"content_file",
contentFile.files[0]
);

const response=
await fetch(

`${API_BASE_URL}/content/upload`,

{

method:"POST",

headers:{

Authorization:

authHeaders().Authorization

},

body:formData

}

);

if(response.ok){

alert("Content Uploaded");

uploadForm.reset();

loadContents();

}else{

const err=
await response.json();

alert(err.detail);

}

}

async function loadContents(){

const response=
await fetch(

`${API_BASE_URL}/content`

);

const contents=
await response.json();

const container=
document.getElementById("contentList");

container.innerHTML="";

contents.forEach(content=>{

container.innerHTML+=`

<div class="content-item">

<div>

<h3>${content.title}</h3>

<p>${content.category}</p>

</div>

<img
src="${API_BASE_URL}/thumbnails/${content.thumbnail}">

</div>

`;

});

}