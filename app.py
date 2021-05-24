import os

from flask import Flask, render_template, request, flash, redirect, send_file
from werkzeug.utils import secure_filename

from utils import allowed_file, pdf_split

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "files")

# Create the application instance
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route("/", methods=['GET', 'POST'])
# def upload_file_home():
#     return render_template("upload_file.html")


@app.route("/")
def home():
    print(UPLOAD_FOLDER)
    return render_template("home.html")


@app.route("/split_pdf")
def split_pdf():
    return render_template("split_pdf.html", filename=None)


@app.route('/split_pdf', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_split(app.config['UPLOAD_FOLDER'], filename)
            return render_template('split_pdf.html', filename=filename.replace("pdf", "zip"))


@app.route('/download', methods=['GET'])
def download():
    fn = request.args.get('fn')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], fn)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
