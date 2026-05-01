from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import time
import uuid
from functools import wraps

app = Flask(__name__, template_folder='../templates')
DB_FILE = 'users_db.json'

# Fungsi untuk memuatkan data dari JSON[span_1](start_span)[span_1](end_span)
def load_db():
    if not os.path.exists(DB_FILE):
        return {"maintenance": False, "keys": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Fungsi untuk menyimpan data ke JSON[span_2](start_span)[span_2](end_span)
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Security: Basic Auth untuk Admin Dashboard[span_3](start_span)[span_3](end_span)
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # Sila tukar password 'AKMAL_H4X' kepada yang lebih selamat[span_4](start_span)[span_4](end_span)
        if not auth or (auth.username != 'admin' or auth.password != 'AKMAL_H4X'):
            return jsonify({"error": "Unauthorized Access"}), 401
        return f(*args, **kwargs)
    return decorated

# --- ROUTES UNTUK USER ---

@app.route('/')
def home():
    # Paparan branding H4X IOS[span_5](start_span)[span_5](end_span)
    return render_template('index.html')

@app.route('/api/verify', methods=['GET'])
def verify():
    db = load_db()
    client_ip = request.args.get('ip') or request.remote_addr
    
    # 1. Semak jika Maintenance aktif[span_6](start_span)[span_6](end_span)
    if db.get("maintenance", False):
        return jsonify({"status": "maintenance", "msg": "MAINTENANCE, WAIT FOR UPDATE"}), 403[span_7](start_span)[span_7](end_span)
    
    # 2. Semak jika IP berdaftar dan belum tamat tempoh[span_8](start_span)[span_8](end_span)
    for key, data in db.get('keys', {}).items():
        if data.get('ip') == client_ip:
            if time.time() < data.get('expiry', 0):
                return jsonify({"status": "success", "key": key})
            else:
                return jsonify({"status": "expired", "msg": "Key has expired"}), 403[span_9](start_span)[span_9](end_span)
                
    return jsonify({"status": "denied", "msg": "Access Denied by H4X IOS"}), 403[span_10](start_span)[span_10](end_span)

# --- ROUTES UNTUK ADMIN (H4X IOS CONTROL) ---

@app.route('/admin')
@admin_required
def admin_panel():
    db = load_db()
    return render_template('admin.html', db=db)

@app.route('/api/admin/maintenance', methods=['POST'])
@admin_required
def toggle_maintenance():
    db = load_db()
    db['maintenance'] = not db.get('maintenance', False)
    save_db(db)
    return jsonify({"new_status": db['maintenance']})

@app.route('/api/admin/generate', methods=['POST'])
@admin_required
def generate_key():
    db = load_db()
    # Jana key unik dengan prefix H4X[span_11](start_span)[span_11](end_span)
    new_key = f"H4X-{str(uuid.uuid4())[:8].upper()}"
    
    # Default 30 hari (2,592,000 saat)[span_12](start_span)[span_12](end_span)
    expiry_date = int(time.time()) + 2592000
    
    db['keys'][new_key] = {
        "ip": None, # Akan di-lock secara automatik pada login pertama[span_13](start_span)[span_13](end_span)
        "expiry": expiry_date,
        "status": "Active"
    }
    save_db(db)
    return jsonify({"status": "success", "key": new_key})

@app.route('/api/admin/delete', methods=['POST'])
@admin_required
def delete_key():
    data = request.json
    key_to_del = data.get('key')
    db = load_db()
    if key_to_del in db['keys']:
        del db['keys'][key_to_del]
        save_db(db)
        return jsonify({"status": "deleted"})
    return jsonify({"status": "not_found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
