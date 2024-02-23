from flask import Blueprint, Response, request, render_template


traducao_blueprint = Blueprint("traducao_blueprint", __name__, url_prefix="/traducao", template_folder="templates")


@traducao_blueprint.get("/")
def main():
    return render_template("traducao/index.html")

@traducao_blueprint.post("/")
def receive_upload():
    from io import BytesIO
    from werkzeug.utils import secure_filename
    from translate.translate import Translate

    resumo_fs = request.files["pdf_0"]
    template_fs = request.files["pdf_1"]
    filename = secure_filename(template_fs.filename)
    
    resumo_file = BytesIO()
    resumo_fs.save(resumo_file)
    template_file = BytesIO()
    template_fs.save(template_file)

    ts = Translate(resumo_file, template_file)
    pdfs = ts.pdfs

    headers = {"Content-Disposition": "attachment; filename=%s" % filename}
    return Response(pdfs, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

