from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Nota: Untuk Vercel, lebih baik guna Database sebenar (seperti MongoDB atau Vercel KV) 
# Tapi untuk permulaan, kita guna JSON file.
DB_FILE = 'users_db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {"maintenance": False, "keys": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint untuk Admin Dashboard
@app.route('/admin')
def admin():
    db = load_db()
    return render_template('admin.html', db=db)

# API untuk skrip drag.py panggil (Verify)
@app.route('/api/verify', methods=['GET'])
def verify():
    db = load_db()
    client_ip = request.remote_addr
    
    if db.get("maintenance"):
        return jsonify({"status": "maintenance", "msg": "MAINTENANCE, WAIT FOR UPDATE"}), 403[span_1](start_span)[span_1](end_span)
    
    # Logik semakan IP
    for key, data in db['keys'].items():
        if data['ip'] == client_ip:
            return jsonify({"status": "success", "key": key})
            
    return jsonify({"status": "denied"}), 403[span_2](start_span)[span_2](end_span)

# API untuk Admin Toggle Maintenance
@app.route('/api/admin/maintenance', methods=['POST'])
def toggle_maintenance():
    db = load_db()
    db['maintenance'] = not db['maintenance']
    save_db(db)
    return jsonify({"new_status": db['maintenance']})

if __name__ == '__main__':
    app.run()
