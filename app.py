from flask import Flask, redirect, url_for, render_template, request, send_from_directory, flash, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
from db_stuff.db_actions import get_files, save_file, get_user, del_file, add_users


app = Flask(__name__)
auth = HTTPBasicAuth()
ALLOWED_EXTENSION = "xlsx"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")


app_data = {
    "name":         "Peter's Starter Template for a Flask Web App",
    "description":  "A basic Flask app using bootstrap for layout",
    "author":       "Peter Simeth",
    "html_title":   "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords":     "flask, webapp, template, basic"
}


@app.route("/")
@auth.login_required
def start():
    return redirect(url_for("index"))


@auth.verify_password
def verify_password(username, password):
    if get_user(username, password):
        return username


@app.route("/overview")
@auth.login_required
def index():
    return render_template("index.html", files=get_files())


@app.route("/up", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("upload"))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("upload"))
        if file:
            filename = secure_filename(file.filename)
            save_file(filename, auth.current_user())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("index"))

    return render_template("upload.html", app_data=app_data)


@app.route("/delete_file/<name>")
@auth.login_required
def delete_file(name: str):
    if del_file(name):
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], name))

    return redirect(url_for("index"))


@app.route("/download_file/<name>")
@auth.login_required
def download_file(name: str):
    return send_file(
        os.path.join(app.config["UPLOAD_FOLDER"], name),
        as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
