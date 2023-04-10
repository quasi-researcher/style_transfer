from flask import Flask, render_template, request, url_for, redirect, session, flash
import requests as req
app = Flask(__name__, template_folder='templates')
app.secret_key = "fake secret key for test purposes"


@app.route('/')
def health():
    predicted_label = session.get('predicted_label') or "not executed"
    torch_status = session.get('torch_status') or "unknown"
    return render_template("index.html", torch_status=torch_status)


@app.route('/ping')
def ping_server():
    url = "http://127.0.0.1:8080/ping"
    response = req.post(url)
    predicted_label = session.get('predicted_label') or "not executed"
    session['torch_status'] = response.json()['status']
    return render_template("index.html", torch_status=response.json()['status'], predicted_label=predicted_label)


@app.route('/classify', methods=['POST'])
def get_prediction():
    image = request.files['selected_image'].read()

    url = "http://127.0.0.1:8080/predictions/fmnist"
    if image:
        response = req.post(url, data={'body': image})
        session['predicted_label'] = response.text
        return render_template("result.html", predicted_label=response.text)
    else:
        flash('Select an image')
    return redirect(url_for("health"))


@app.route('/back')
def back_to_main():
    session['predicted_label'] = 'not executed'
    return redirect(url_for("health"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)