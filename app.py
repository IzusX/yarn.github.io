from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    with sqlite3.connect('yarn.db') as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS yarns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                color TEXT,
                length REAL
            )
        """)
        conn.commit()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/add', methods=['POST'])
def add_yarn():
    data = request.json
    with sqlite3.connect('yarn.db') as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO yarns (type, color, length) VALUES (?, ?, ?)
        """, (data['type'], data['color'], data['length']))
        conn.commit()
    return jsonify({"status": "ok"})

@app.route('/api/list', methods=['GET'])
def list_yarns():
    with sqlite3.connect('yarn.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM yarns")
        rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080)