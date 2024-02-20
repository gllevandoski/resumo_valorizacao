from flask import Flask, send_file, request
from io import BytesIO
from werkzeug.wsgi import wrap_file


app = Flask(__name__)


@app.route("/")
def main():
    bf = BytesIO(b"123123123")
    return send_file(bf, as_attachment=True, download_name="abcbc")

if __name__ == "__main__":
    app.run(debug=True, port=80)
