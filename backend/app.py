from flask import Flask, render_template, request, send_file
from flask_cors import CORS   # <-- add this
import pdfkit

app = Flask(__name__)
CORS(app)   # <-- allow frontend to access backend


# Configure path to wkhtmltopdf (important for Windows)
PDFKIT_CONFIG = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

@app.route("/")
def home():
    return "Invoice Generator Backend is Running 🚀"

@app.route("/invoice", methods=["POST"])
def generate_invoice():
    data = request.json

    # Render invoice template with customer data
    html = render_template("invoice.html", data=data)

    # Save PDF
    pdf_path = "invoice.pdf"
    pdfkit.from_string(html, pdf_path, configuration=PDFKIT_CONFIG)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

