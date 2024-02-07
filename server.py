from flask import Flask, render_template
from blueprints.resumo.server import resumo_blueprint
from blueprints.traducao.server import traducao_blueprint


app = Flask(__name__)
app.register_blueprint(resumo_blueprint)
app.register_blueprint(traducao_blueprint)


@app.get("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=80)
