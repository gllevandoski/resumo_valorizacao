function upload(formData) {
    document.getElementById("loading").hidden = false;

    let request = new Request(window.location.href, {
                                        method: "POST",
                                        body: formData,
                                    });
    fetch(request)
    .then(response => {
        let raw_filename = response.headers.get("Content-Disposition");
        let filename = raw_filename.slice(22, raw_filename.lastIndexOf("."));
        let a = document.createElement("a");

        response.blob().then((blob) => {
            let objURL = window.URL.createObjectURL(blob);
            a.download = filename;
            a.href = objURL;
            a.click();
        });

        let download_button = document.getElementById("download");
        let loading = document.getElementById("loading");
        download_button.hidden = false;
        loading.hidden = true;

        download_button.addEventListener("click", () => a.click())
    });
}

function handle_upload() {
    let file_inputs = document.getElementsByTagName("input");
    let formData = new FormData();
    for(file in file_inputs) {
        formData.append("pdf_" + file, file_inputs[file].files[0]);
    upload(formData);
    }

}

window.addEventListener("DOMContentLoaded", () => {
    let submit_button = document.getElementById("submit");
    let file_input = document.getElementById("file");
    let download_button = document.getElementById("download");

    submit_button.addEventListener("click", (event) => {
        event.preventDefault();
        handle_upload();
    });

    file_input.addEventListener("change", () => {
        download_button.hidden = true;
    });
});
