
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'cloud_data.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            info TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add', methods=['POST'])
def add_data():
    new_data = request.json.get('info')
    if not new_data:
        return jsonify({"error": "No data provided"}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM data WHERE info = ?", (new_data,))
    if c.fetchone():
        conn.close()
        return jsonify({"message": "Duplicate entry. Data already exists."}), 409

    try:
        c.execute("INSERT INTO data (info) VALUES (?)", (new_data,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Data added successfully."}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Data insertion failed."}), 500

@app.route('/all', methods=['GET'])
def get_all_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    rows = c.fetchall()
    conn.close()
    return jsonify({"data": rows})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
