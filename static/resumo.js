function upload() {
    document.getElementById("loading").hidden = false;
    let formData = new FormData();
    formData.append("pdf", document.getElementById("file").files[0]);

    let request = new Request("/resumo", {
                                        method: "POST",
                                        body: formData,
                                    });
    fetch(request).then(response => response.blob()).then(blob => {
        let objURL = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = objURL;
        a.download = "download" || "download";
        a.click();

        let download_button = document.getElementById("download");
        let loading = document.getElementById("loading");
        download_button.hidden = false;
        loading.hidden = true;

        download_button.addEventListener("click", () => a.click())
    });
}

window.addEventListener("DOMContentLoaded", () => {
    let submit_button = document.getElementById("submit");
    let file_input = document.getElementById("file");
    let download_button = document.getElementById("download");

    submit_button.addEventListener("click", (event) => {
        event.preventDefault();
        upload();
    });

    file_input.addEventListener("change", () => {
        download_button.hidden = true;
    });
});
