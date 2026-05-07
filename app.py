from flask import Flask, render_template, request, jsonify
import sqlite3
import math
import random
import string
from datetime import datetime

app = Flask(__name__)

COMMON_PASSWORDS = {
    "123456", "password", "qwerty", "admin", "letmein", "welcome"
}

S
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            entropy REAL,
            crack_time TEXT,
            breached INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def analyze_password(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        suggestions.append("Add special characters")

    breached = password.lower() in COMMON_PASSWORDS
    if breached:
        suggestions.append("This is a common password")

    entropy = round(len(password) * math.log2(94), 2) if password else 0

    if entropy > 60:
        crack_time = "Years"
    elif entropy > 40:
        crack_time = "Months"
    elif entropy > 25:
        crack_time = "Days"
    else:
        crack_time = "Instant"

    return {
        "score": score,
        "entropy": entropy,
        "crack_time": crack_time,
        "breached": breached,
        "suggestions": suggestions
    }


def save_log(result):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO password_logs (score, entropy, crack_time, breached, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        result["score"],
        result["entropy"],
        result["crack_time"],
        int(result["breached"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/generator')
def generator():
    return render_template('generator.html')


@app.route('/analytics')
def analytics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT score, COUNT(*) FROM password_logs GROUP BY score")
    data = cursor.fetchall()

    conn.close()

    scores = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template('analytics.html', scores=scores, counts=counts)


# ✅ NEW ROUTE (ENTER → REDIRECT → RESULT PAGE)
@app.route('/analyze-page', methods=['POST'])
def analyze_page():
    password = request.form.get("password", "")

    result = analyze_password(password)
    save_log(result)

    return render_template(
        "result.html",
        password=password,
        result=result
    )


# Existing API route (for JS live checking)
@app.route('/analyze', methods=['POST'])
def analyze():
    password = request.json.get("password", "")
    result = analyze_password(password)
    save_log(result)
    return jsonify(result)


@app.route('/generate-password')
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(14))
    return jsonify({"password": password})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)