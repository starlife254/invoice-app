import requests

data = {
    "invoice_no": "1202",
    "date": "11.09.2025",
    "customer_name": "Fr. Julius Muthamba",
    "customer_phone": "0722464268",
    "description": "Birthday Cake Deco",
    "amount": "32000"
}

response = requests.post("http://127.0.0.1:5000/invoice", json=data)

with open("invoice.pdf", "wb") as f:
    f.write(response.content)

print("Invoice saved as invoice.pdf ✅")
