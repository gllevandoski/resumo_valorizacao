function upload(formData) {
    let download_button = document.getElementById("download");
    let loading = document.getElementById("loading");
    let file_input = document.querySelector(".file_input");
    let fieldsets = document.querySelectorAll("fieldset");
    let submit_button = document.querySelector(".submit_button");

    download_button.hidden = true;
    loading.hidden = false;
    file_input.disabled = true;
    for(fs of fieldsets){fs.disabled = true}
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
        for(fs of fieldsets) {fs.disabled = false}
        submit_button.disabled = false;

        addListeners();
    });
}

function handle_upload(file_input, selected_write_type, selected_alignment_type) {
    let formData = new FormData();

    formData.append(String(file_input.id), file_input.files[0]);
    formData.append(selected_write_type.name, selected_write_type.value);
    formData.append(selected_alignment_type.name, selected_alignment_type.value);

    upload(formData);
}

function addListeners() {
    document.querySelector(".submit_button").addEventListener("click", () => {
        let file_input = document.querySelector(".file_input");
        let selected_write_type = document.querySelector(".write_types input:checked");
        let selected_alignment_type = document.querySelector(".alignment_type input:checked");

        if (file_input.files.length != 1 || !selected_write_type || !selected_alignment_type) {
            return
        }

        handle_upload(file_input, selected_write_type, selected_alignment_type);
    });
    document.querySelector(".file_input").addEventListener("change", () => {
        document.querySelector(".download_button").hidden = true;
    })
}

window.addEventListener("DOMContentLoaded", addListeners);
