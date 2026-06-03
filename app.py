from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'profile_data.json'
CONFIG_FILE = 'config.json'

DEFAULT_DATA = {
    "name": "你的名字",
    "title": "職稱 / 專長領域介紹",
    "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=default",
    "bio": "專注於數位工藝與永續技術。這裡是我在網路世界的數位棲地，歡迎瀏覽我的專案與連結。",
    "location": "台灣",
    "email": "your@email.com",
    "links": [
        {"platform": "GitHub", "url": "https://github.com/yourhandle", "icon": "github"},
        {"platform": "LinkedIn", "url": "https://linkedin.com/in/yourhandle", "icon": "linkedin"},
        {"platform": "Instagram", "url": "https://instagram.com/yourhandle", "icon": "instagram"},
        {"platform": "Twitter", "url": "https://twitter.com/yourhandle", "icon": "twitter"}
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 安全讀取外部 JSON 密碼
def get_admin_password():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                return config.get('edit_password', 'forest123')
            except json.JSONDecodeError:
                return 'forest123'
    return 'forest123'

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/api/profile', methods=['GET'])
def get_profile():
    return jsonify(load_data())

@app.route('/api/profile', methods=['POST'])
def update_profile():
    data = request.json
    save_data(data)
    return jsonify({"status": "ok"})

# 新增：後端密碼驗證 API
@app.route('/api/verify-password', methods=['POST'])
def verify_password():
    req_data = request.json or {}
    input_password = req_data.get('password')
    actual_password = get_admin_password()
    
    if input_password == actual_password:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)