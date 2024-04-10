from flask import Blueprint, render_template, request, Response


resumo_blueprint = Blueprint("resumo_blueprint", __name__, url_prefix="/resumo")


@resumo_blueprint.get("/")
def main():
    return render_template("resumo/index.html")


@resumo_blueprint.post("/")
def receive_upload():
    from werkzeug.utils import secure_filename
    from modules.resumo.pdf import Pdf
    from modules.resumo.pdf import Workbook
    from io import BytesIO

    pdf_file_fs = request.files["pdf_0"]
    write_type = int(request.form["write_type"])
    coordinates = request.form["alignment_type"]
    filename = secure_filename(pdf_file_fs.filename)
    pdf_file = BytesIO()
    pdf_file_fs.save(pdf_file)

    pdf_file = Pdf(pdf_file, coordinates)
    wb = Workbook()
    download = wb.write(pdf_file, write_type)

    headers = {"Content-Disposition": f"attachment; filename*={filename}"}
    return Response(download, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
