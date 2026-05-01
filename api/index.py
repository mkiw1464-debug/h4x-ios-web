from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>H4X IOS Web is Running!</h1>"

@app.route('/api/verify')
def verify():
    return jsonify({"status": "ready"})

# Ini wajib untuk Vercel
app.debug = True
