from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from weasyprint import HTML
import os

app = Flask(__name__)
CORS(app)   # Allow frontend to access backend

LAST_INVOICE_FILE = "last_invoice.txt"

def get_next_invoice_number():
    """Get the next invoice number starting at 1000"""
    if os.path.exists(LAST_INVOICE_FILE):
        with open(LAST_INVOICE_FILE, "r") as f:
            last = int(f.read().strip())
    else:
        last = 999
    next_num = last + 1
    with open(LAST_INVOICE_FILE, "w") as f:
        f.write(str(next_num))
    return next_num

@app.route("/")
def home():
    return "Invoice Generator Backend is Running 🚀"

@app.route("/invoice", methods=["POST"])
def generate_invoice():
    data = request.json

    # Auto-generate invoice number if not provided
    if not data.get("invoice_no"):
        data["invoice_no"] = get_next_invoice_number()

    # Render invoice template with customer data
    html = render_template("invoice.html", data=data)

    # Save PDF using WeasyPrint
    pdf_path = "invoice.pdf"
    HTML(string=html).write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render requires dynamic port
    app.run(host="0.0.0.0", port=port)
