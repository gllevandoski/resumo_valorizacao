function upload(formData) {
    let download_button = document.getElementById("download");
    let loading = document.getElementById("loading");
    let file_input = document.querySelector(".file_input");
    let submit_button = document.querySelector(".submit_button");

    download_button.hidden = true;
    loading.hidden = false;
    file_input.disabled = true;
    submit_button.disabled = true;


    let request = new Request(window.location.href, {method: "POST", body: formData});
    fetch(request)
    .then(response => {
        let raw_filename = response.headers.get("Content-Disposition");
        let filename = raw_filename.slice(22, raw_filename.lastIndexOf("."));

        response.blob().then((blob) => {
            download_button.href = window.URL.createObjectURL(blob);
            download_button.download = filename;
            download_button.click();
        });


        download_button.hidden = false;
        loading.hidden = true;
        file_input.disabled = false;
        submit_button.disabled = false;

        addListeners();
    });
}

function handle_upload(file_input) {
    let formData = new FormData();

    formData.append(String(file_input.id), file_input.files[0]);

    upload(formData);
}

function addListeners() {
    document.querySelector(".submit_button").addEventListener("click", () => {
        let file_input = document.querySelector(".file_input");

        if (file_input.files.length != 1) {
            return
        }

        handle_upload(file_input);
    });
    document.querySelector(".file_input").addEventListener("change", () => {
        document.querySelector(".download_button").hidden = true;
    })
}

window.addEventListener("DOMContentLoaded", addListeners);
