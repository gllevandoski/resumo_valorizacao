from flask import Flask, send_from_directory, request, render_template
from uuid import uuid4


app = Flask(__name__)


@app.get("/")
def main():
    return render_template("index.html")

@app.post("/")
def receive_upload():
    import pdf
    import shutil
    from main import Workbook

    pdf_file = request.files["pdf"]
    name = uuid4()
    pdf_file.save(f"pdf/{name}.pdf")

    web_pdf = {"internet": [pdf.Pdf(f"pdf/{name}.pdf")]}

    shutil.copy("assets/resumo.xlsx", f"generated/{name}.xlsx")
    wb = Workbook(f"generated/{name}.xlsx")
    wb.write(web_pdf, resumed=False)

    download_link = f"{name}.xlsx"
    return {"download_link": download_link}

@app.get("/download/<file_name>")
def download_file(file_name):
    return send_from_directory("generated", file_name)


if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=80)
