from flask import Blueprint, render_template, request, send_file, Response
from werkzeug.wsgi import wrap_file


resumo_blueprint = Blueprint("resumo_blueprint", __name__, url_prefix="/resumo")


@resumo_blueprint.get("/")
def main():
    return render_template("resumo/index.html")


@resumo_blueprint.post("/")
def receive_upload():
    from werkzeug.utils import secure_filename
    from resumo.pdf import Pdf
    from resumo.pdf2xlsx import Workbook
    from io import BytesIO

    pdf_file_fs = request.files["pdf_0"]
    filename = secure_filename(pdf_file_fs.filename)
    pdf_file = BytesIO()
    pdf_file_fs.save(pdf_file)

    pdf_file = Pdf(pdf_file)
    wb = Workbook()
    download = wb.write(pdf_file, resumed=False)
    download.seek(0)

    headers = {"Content-Disposition": f"attachment; filename*={filename}"}
    return Response(download, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
