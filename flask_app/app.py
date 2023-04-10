from flask import Flask, render_template, request, json
import base64
import requests as req
from werkzeug.exceptions import HTTPException
app = Flask(__name__, template_folder='templates')
app.secret_key = "fake secret key for test purposes"


@app.route('/')
def health():
    return render_template("index.html", torch_status='unknown')


@app.route('/ping')
def ping_server():
    url = "http://127.0.0.1:8080/ping"
    response = req.post(url)
    return render_template("index.html", torch_status=response.json()['status'])


@app.route('/generate', methods=['POST'])
def get_prediction():
    if request.files:
        content_img = request.files['content'].read()
        style_img = request.files['style'].read()

        url = "http://localhost:8080/predictions/nst"

        response = req.post(url, data={'content': content_img, 'style': style_img})
        result = response.content
        return {'out_img': base64.b64encode(result).decode()}
    else:
        result = 'Please, select an image'
        return {'error': result}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)