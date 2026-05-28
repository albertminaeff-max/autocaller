from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

GOOGLE_SHEET_ID   = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE", "google_creds.json")

def get_sheet():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds  = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet  = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    # Заголовки если таблица пустая
    if not sheet.get_all_values():
        sheet.append_row(["Дата", "Номер телефона", "Компания"])
    return sheet

@app.route("/save", methods=["POST"])
def save():
    data    = request.get_json(force=True)
    phone   = data.get("phone", "unknown")
    company = data.get("company", "не распознано")

    sheet = get_sheet()
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        phone,
        company
    ])
    print(f"✅ Записано: {phone} — {company}")
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def index():
    return {"status": "running"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
