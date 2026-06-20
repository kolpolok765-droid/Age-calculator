import os
import calendar
from datetime import date
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def add_years(sourcedate, years):
    try:
        return sourcedate.replace(year=sourcedate.year + years)
    except ValueError:
        # Handle Leap Year (Feb 29) to non-leap year mapping to Feb 28
        return sourcedate.replace(year=sourcedate.year + years, month=2, day=28)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def get_zodiac_info(month, day):
    # Zodiac signs limits: (start_date_threshold, sign_name, sign_emoji)
    if month == 1:
        return ("Capricorn", "♑") if day < 20 else ("Aquarius", "♒")
    elif month == 2:
        return ("Aquarius", "♒") if day < 19 else ("Pisces", "♓")
    elif month == 3:
        return ("Pisces", "♓") if day < 21 else ("Aries", "♈")
    elif month == 4:
        return ("Aries", "♈") if day < 20 else ("Taurus", "♉")
    elif month == 5:
        return ("Taurus", "♉") if day < 21 else ("Gemini", "♊")
    elif month == 6:
        return ("Gemini", "♊") if day < 21 else ("Cancer", "♋")
    elif month == 7:
        return ("Cancer", "♋") if day < 23 else ("Leo", "♌")
    elif month == 8:
        return ("Leo", "♌") if day < 23 else ("Virgo", "♍")
    elif month == 9:
        return ("Virgo", "♍") if day < 23 else ("Libra", "♎")
    elif month == 10:
        return ("Libra", "♎") if day < 23 else ("Scorpio", "♏")
    elif month == 11:
        return ("Scorpio", "♏") if day < 22 else ("Sagittarius", "♐")
    elif month == 12:
        return ("Sagittarius", "♐") if day < 22 else ("Capricorn", "♑")
    return ("Unknown", "❓")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate_age():
    data = request.get_json() or {}
    birthdate_str = data.get("birthdate")

    if not birthdate_str:
        return jsonify({"error": "Please select your birthdate"}), 400

    targetdate_str = data.get("targetdate")

    try:
        birthdate = date.fromisoformat(birthdate_str)
    except ValueError:
        return jsonify({"error": "Invalid birthdate format. Use YYYY-MM-DD"}), 400

    if targetdate_str:
        try:
            target_date = date.fromisoformat(targetdate_str)
        except ValueError:
            return jsonify({"error": "Invalid target date format. Use YYYY-MM-DD"}), 400
    else:
        target_date = date.today()

    if birthdate > target_date:
        return jsonify({"error": "Birthdate cannot be after target date"}), 400

    # Age math calculations
    # Find years
    years = target_date.year - birthdate.year
    if add_years(birthdate, years) > target_date:
        years -= 1
    
    anchor = add_years(birthdate, years)
    
    # Find months
    months = 0
    while add_months(anchor, months + 1) <= target_date:
        months += 1
        
    anchor = add_months(anchor, months)
    
    # Find days
    days = (target_date - anchor).days

    zodiac_name, zodiac_emoji = get_zodiac_info(birthdate.month, birthdate.day)

    return jsonify({
        "years": years,
        "months": months,
        "days": days,
        "zodiac_name": zodiac_name,
        "zodiac_emoji": zodiac_emoji
    })

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug)
