from flask import Flask, render_template, request, url_for, redirect, session, flash
import requests as req
app = Flask(__name__, template_folder='templates')
app.secret_key = "fake secret key for test purposes"


@app.route('/')
def health():
    predicted_label = session.get('predicted_label') or "not executed"
    torch_status = session.get('torch_status') or "unknown"
    return render_template("index_no_ajax.html", torch_status=torch_status, predicted_label=predicted_label)


@app.route('/ping_model_server')
def ping_server():
    url = "http://127.0.0.1:8080/ping"
    response = req.post(url)
    predicted_label = session.get('predicted_label') or "not executed"
    session['torch_status'] = response.json()['status']
    return render_template("index_no_ajax.html", torch_status=response.json()['status'], predicted_label=predicted_label)


@app.route('/predictions/fmnist', methods=['POST'])
def get_prediction():
    image_path = request.form['selected_image']

    url = "http://127.0.0.1:8080/predictions/fmnist"
    if image_path:
        with open(image_path, 'rb') as f:
            img64 = f.read()

        response = req.post(url, data={'body': img64})
        session['predicted_label'] = response.text

    else:
        flash('Select an image')
    return redirect(url_for("health"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)