from flask import Blueprint, render_template, request, send_file, Response
from werkzeug.wsgi import wrap_file


resumo_blueprint = Blueprint("resumo_blueprint", __name__, url_prefix="/resumo")


@resumo_blueprint.get("/")
def main():
    return render_template("resumo/index.html")


@resumo_blueprint.post("/")
def receive_upload():
    from werkzeug.utils import secure_filename
    from calc.pdf import Pdf
    from calc.pdf2xlsx import Workbook
    from io import BytesIO

    pdf_file_fs = request.files["pdf"]
    filename = secure_filename(pdf_file_fs.filename)
    pdf_file = BytesIO()
    pdf_file_fs.save(pdf_file)

    pdf_file = Pdf(pdf_file)
    wb = Workbook()
    download = wb.write(pdf_file, resumed=False)
    download = wrap_file(request.environ, file=download)

    print(download)
    print("sent")

    return Response(download, direct_passthrough=True, mimetype="pdf")
    # return send_file(download, mimetype="pdf", as_attachment=True, download_name=filename)
