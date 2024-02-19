from flask import Blueprint, request, send_from_directory, render_template
from uuid import uuid4


traducao_blueprint = Blueprint("traducao_blueprint", __name__, url_prefix="/traducao", template_folder="templates")


@traducao_blueprint.get("/")
def main():
    return render_template("traducao/index.html")

@traducao_blueprint.post("/")
def receive_upload():
    pdf_file = request.files["pdf"]
    name = uuid4()
    pdf_file.save(f"pdf/{name}.pdf")

    # precisa de uma planilha para enviar


    download_link = f"{name}.xlsx"
    return {"download_link": download_link}


@traducao_blueprint.get("/download/<file_name>")
def download_file(file_name):
    return send_from_directory("generated", file_name)
