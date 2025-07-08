from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Setup database (creates table if it doesn't exist)
def init_db():
    conn = sqlite3.connect('my-flask-api.db')
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

# Route to receive data
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
    conn = sqlite3.connect('my-flask-api.db')
    c = conn.cursor()
    c.execute('INSERT INTO inquiry (name, email, phone, gender, subject, message) VALUES (?, ?, ?, ?, ?, ?)', (name, email, phone, gender, subject, message))
    conn.commit()
    conn.close()

    print("✅ Received and saved:", data)
    return {"status": "ok", "received": data}, 200

# Route to view all records
@app.route('/inquiry', methods=['GET'])
def list_records():
    conn = sqlite3.connect('my-flask-api.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inquiry')
    rows = c.fetchall()
    conn.close()

    results = [
        {"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "gender": r[4], "subject": r[5], "message": r[6]}
        for r in rows
    ]
    return jsonify(results)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


