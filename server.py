from flask import Flask, render_template
from resumo.pdf2xlsx_server import resumo_blueprint
from translate.translate_server import traducao_blueprint
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(resumo_blueprint)
app.register_blueprint(traducao_blueprint)
CORS(app, resources={r"/*": {"origins" : "*", "Access-Control-Allow-Headers": "*"}})


@app.get("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True, port=80)
