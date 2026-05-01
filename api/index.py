from flask import Flask, render_template, request, jsonify
import json
import os
import time
import uuid
from functools import wraps

app = Flask(__name__)
DB_FILE = 'users_db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {"maintenance": False, "keys": {}}
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# Security untuk Admin Dashboard[span_2](start_span)[span_2](end_span)
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or (auth.username != 'admin' or auth.password != 'AKMAL_H4X'):
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html', db=load_db())

@app.route('/api/verify', methods=['GET'])
def verify():
    db = load_db()
    client_ip = request.args.get('ip')
    
    if db.get("maintenance"):
        return jsonify({"status": "maintenance"}), 403[span_3](start_span)[span_3](end_span)
    
    for key, data in db['keys'].items():
        if data['ip'] == client_ip:
            if time.time() < data['expiry']:
                return jsonify({"status": "success"})
    return jsonify({"status": "denied"}), 403[span_4](start_span)[span_4](end_span)

@app.route('/api/admin/maintenance', methods=['POST'])
@admin_required
def toggle_maint():
    db = load_db()
    db['maintenance'] = not db['maintenance']
    save_db(db)
    return jsonify({"status": db['maintenance']})

@app.route('/api/admin/generate', methods=['POST'])
@admin_required
def generate():
    db = load_db()
    new_key = f"H4X-{str(uuid.uuid4())[:8].upper()}"
    db['keys'][new_key] = {"ip": None, "expiry": int(time.time()) + 2592000} # 30 Hari[span_5](start_span)[span_5](end_span)
    save_db(db)
    return jsonify({"key": new_key})
