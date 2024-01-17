function upload() {
    let pdf = document.getElementById("file").files[0];
    let formData = new FormData();
    formData.append("pdf", pdf);
    let promise = http_request(formData);
    promise.then((resolved) => {
        let download_link = JSON.parse(resolved)["download_link"];
        window.location.href = "download/" + download_link;
    });
}

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("submit").addEventListener("click", upload);
});

function http_request(data) {
    let promise = new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/");

        xhr.onload = () => {
            if (xhr.status >= 400) {
                reject(xhr.response);
            }
            resolve(xhr.response);
        };
            xhr.send(data);
    });
    return promise;
}