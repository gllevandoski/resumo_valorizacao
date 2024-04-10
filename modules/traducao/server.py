from flask import Blueprint, Response, request, render_template


traducao_blueprint = Blueprint("traducao_blueprint", __name__, url_prefix="/traducao", template_folder="templates")


@traducao_blueprint.get("/")
def main():
    return render_template("traducao/index.html")


@traducao_blueprint.post("/")
def receive_upload():
    from io import BytesIO
    from werkzeug.utils import secure_filename
    from modules.traducao.traducao import Translate

    resumo_fs = request.files["resumo"]
    filename = secure_filename(resumo_fs.filename)
    resumo_file = BytesIO()
    resumo_fs.save(resumo_file)

    translation = Translate(resumo_file)
    merged = translation.merged_pdf
    merged.seek(0)

    headers = {"Content-Disposition": f"attachment; filename*={filename}"}
    return Response(merged, content_type="application/pdf", headers=headers)
