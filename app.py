from flask import Flask, render_template, url_for

# Create the application instance
app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/split_pdf")
def split_pdf():
    return render_template("split_pdf.html")


if __name__ == '__main__':
    app.run(debug=True)
