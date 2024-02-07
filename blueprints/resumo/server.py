from flask import Blueprint, render_template, request, send_from_directory
from uuid import uuid4
import pdf
from main import Workbook


resumo_blueprint = Blueprint("resumo", __name__, url_prefix="/resumo")


@resumo_blueprint.get("/")
def main():
    return render_template("resumo.html")


@resumo_blueprint.post("/")
def receive_upload():
    pdf_file = request.files["pdf"]
    name = uuid4()
    pdf_file.save(f"pdf/{name}.pdf")

    web_pdf = [pdf.Pdf(f"pdf/{name}.pdf")]
    wb = Workbook(output_name=name)
    wb.write(web_pdf, resumed=False)

    download_link = f"{name}.xlsx"
    return {"download_link": download_link}


@resumo_blueprint.get("/download/<file_name>")
def download_file(file_name):
    return send_from_directory("generated", file_name)
