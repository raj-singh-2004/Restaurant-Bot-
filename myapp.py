import requests

url = "http://127.0.0.1:8000/accounts/registerVendor/"
files = {"vendor_license": open(r"C:\Users\rajdeep\Pictures\WhatsApp Image 2024-12-22 at 05.07.15_f9557d63.jpg", "rb")}
data = {
  "first_name": "Riya",
  "last_name": "Sharma",
  "username": "riya1rest",
  "email": "riya@acme.in",
  "phone_number": "912345678901",
  "password": "Str0ng&Spicy1!",
  "confirm_password": "Str0ng&Spicy1!",
  "vendor_name": "ACME Biryani House"
}
r = requests.post(url, data=data, files=files)
print(r.status_code, r.json())

