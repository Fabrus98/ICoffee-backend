import json
from pathlib import Path
from datetime import datetime, timedelta
from django.utils.timezone import now

SESSION_DATA_FILE = Path(__file__).resolve().parent / "session.json"
MENU_DATA_FILE = Path(__file__).resolve().parent / "menu.json"
BOOKINGS_DATA_FILE = Path(__file__).resolve().parent / "bookings.json"

def format_italian_date(data):
    return data.strftime("%d-%m-%Y")

def update_session_date():
    data = load_session_data()
    current_time = now()
    cutoff = current_time.replace(hour=8, minute=0, second=0, microsecond=0)

    if current_time < cutoff:
        booking_date = current_time.date()
    else:
        booking_date = (current_time + timedelta(days=1)).date()

    italian_booking_date = format_italian_date(booking_date)
    data["currentSession"] = italian_booking_date
    save_general_data(data, SESSION_DATA_FILE)
    print(italian_booking_date)

def load_session_data():
    if not SESSION_DATA_FILE.exists():
        return {"currentSession": format_italian_date(now().date())}
    with open(SESSION_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_menu_data():
    if not MENU_DATA_FILE.exists():
        return {"itemsTemplate": [], "items": []}
    with open(MENU_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_booking_data():
    if not BOOKINGS_DATA_FILE.exists():
        return []
    with open(BOOKINGS_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_general_data(data, DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def find_item_by_id(item_id):
    items = load_menu_data()

    for category in items:
        for item in category["items"]:
            if item["id"] == item_id:
                return item
    return None
