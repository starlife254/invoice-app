from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from weasyprint import HTML
import io
import os

app = Flask(__name__)
CORS(app)   # Allow frontend to access backend

@app.route("/")
def home():
    return "Invoice Generator Backend is Running 🚀"

@app.route("/invoice", methods=["POST"])
def generate_invoice():
    data = request.json

    print("📥 Received data:", data, flush=True)  # Debug line

    if not data.get("invoice_no"):
        return {"error": "Invoice number is required"}, 400

    # Render invoice HTML with data
    html = render_template("invoice.html", data=data)

    # Convert HTML → PDF
    pdf_file = io.BytesIO()
    HTML(string=html).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(
        pdf_file,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"invoice_{data['invoice_no']}.pdf"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render requires dynamic port
    app.run(host="0.0.0.0", port=port)
