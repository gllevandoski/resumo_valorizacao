function upload() {
    document.getElementById("loading").hidden = false;
    let formData = new FormData();
    formData.append("pdf", document.getElementById("file").files[0]);

    let promise = http_request(formData);
    promise.then((resolved) => {
        let download_button = document.getElementById("download");
        let loading = document.getElementById("loading");
        download_button.hidden = false;
        loading.hidden = true;
        
        download_button.addEventListener("click", () => {
            window.location.href = "download/" + JSON.parse(resolved)["download_link"];
        })
    });
}

window.addEventListener("DOMContentLoaded", () => {
    let submit_button = document.getElementById("submit");
    let file_input = document.getElementById("file");
    let download_button = document.getElementById("download");

    submit_button.addEventListener("click", upload);
    
    file_input.addEventListener("change", () => {
        download_button.hidden = true;
    });
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