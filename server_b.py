from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'my-flask-api.db'

# Setup database (creates table if it doesn't exist)
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inquiry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            gender TEXT,
            subject TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call init on startup
init_db()

# Route to receive data (API)
@app.route('/api/receive', methods=['POST'])
def receive_data():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    gender = data.get('gender')
    subject = data.get('subject')
    message = data.get('message')

    # Save to database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO inquiry (name, email, phone, gender, subject, message) VALUES (?, ?, ?, ?, ?, ?)',
              (name, email, phone, gender, subject, message))
    conn.commit()
    conn.close()

    print("✅ Received and saved:", data)
    return {"status": "ok", "received": data}, 200

# Route to view all records as JSON
@app.route('/inquiry', methods=['GET'])
def list_records():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM inquiry')
    rows = c.fetchall()
    conn.close()

    results = [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "phone": r[3],
            "gender": r[4],
            "subject": r[5],
            "message": r[6]
        } for r in rows
    ]
    return jsonify(results)

# Route to view all records as HTML
@app.route('/view', methods=['GET'])
def view_records():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM inquiry')
    rows = c.fetchall()
    conn.close()

    html = "<h1>All Inquiries</h1><ul>"
    for row in rows:
        html += f"<li>{row}</li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
