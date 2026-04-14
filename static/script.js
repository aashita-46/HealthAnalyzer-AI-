function upload() {
    const file = document.getElementById("file").files[0];

    const formData = new FormData();
    formData.append("image", file);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
    });
}