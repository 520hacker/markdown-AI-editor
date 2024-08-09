import datetime
import json
import os
import random
import re
import sqlite3
import string
import time
from config import Config
import requests
from flask import (Flask, Response, jsonify, redirect, render_template,
                   request, send_from_directory, stream_with_context, url_for)

from flask_cors import CORS
from upload import Uploader

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # Replace '/api/*' with your endpoint and '*' with the allowed origin

app.config["UPLOAD_FOLDER"] = os.path.join("files", "note")
app.config["DATABASE_PATH"] = os.path.join(os.getcwd(), "files", "db", "histories.db")
app.config["PROXY_DOMAIN"] = "https://api.yunzhu.info"
app.uploader = Uploader()


@app.route("/upload/test", methods=["GET"])
def upload_test():
    return render_template("upload.html")


@app.route("/api/upload", methods=["POST"])
def handle_upload():
    res = app.uploader.upload(request)
    return res


@app.route("/api/fetch", methods=["POST"])
def handle_fetch():
    res = app.uploader.fetch(request)
    return res


@app.route("/images/<filename>")
def images_files(filename):
    allowed_files = ["logo.png"]
    if filename not in allowed_files:
        return ""
    return send_from_directory("templates/images", filename)


@app.route("/static/<filename>")
def static_files(filename):
    allowed_files = [
        "vue.js",
        "axios.js",
        "vditor.js",
        "base.css",
        "index.css",
        "light.css",
        "dark.css",
        "wechat.css",
        "ant-design.css",
        "favicon.ico",
        "qrcode.js",
        "site.js",
        "en_US.js",
        "zh_CN.js",
        "zh_TW.js",
        "lute.min.js"
    ]
    if filename not in allowed_files:
        return ""
    return send_from_directory("templates/static", filename)


@app.route("/scripts/<filename>")
def scripts_files(filename):
    allowed_files = [
        "background.js",
        "content.js",
        "style.css",
    ]
    if filename not in allowed_files:
        return ""
    return send_from_directory("templates/scripts", filename)


@app.route("/scripts/set/<filename>")
def scripts_set_files(filename):
    allowed_files = [
        "set.js",
        "style.css",
    ]
    if filename not in allowed_files:
        return ""
    return send_from_directory("templates/scripts/set", filename)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/setting", methods=["GET"])
def setting():
    return render_template("set.html")


@app.route("/<key>", methods=["GET"])
def single_page(key):
    return render_template("index.html", key=key)


def generate_key(length):
    min_length = 4
    length = max(min_length, length)

    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.route("/new", methods=["GET"])
def new_page():
    conn = sqlite3.connect(app.config["DATABASE_PATH"])
    cursor = conn.cursor()
    key_length = 4
    start_time = time.time() * 1000  # 毫秒时间戳
    while True:
        key = generate_key(key_length)
        cursor.execute("SELECT * FROM keys WHERE key=?", (key,))
        result = cursor.fetchone()

        if not result:
            # 插入新的key到keys表中
            cursor.execute("INSERT OR IGNORE INTO keys (key) VALUES (?)", (key,))
            conn.commit()
            break
        else:
            end_time = time.time() * 1000
            elapsed = end_time - start_time
            if elapsed >= 1000:
                key_length += int(elapsed / 1000)

    conn.close()

    # 跳转到对应的/{key}页面
    return redirect(url_for("single_page", key=key))

@app.route("/api/key", methods=["GET"])
def new_key():
    conn = sqlite3.connect(app.config["DATABASE_PATH"])
    cursor = conn.cursor()
    key_length = 4
    start_time = time.time() * 1000  # Millisecond timestamp

    while True:
        key = generate_key(key_length)
        cursor.execute("SELECT * FROM keys WHERE key=?", (key,))
        result = cursor.fetchone()

        if not result:
            # Insert the new key into the keys table
            cursor.execute("INSERT INTO keys (key) VALUES (?)", (key,))
            conn.commit()
            break
        else:
            # If a key collision occurs, try again after a short pause
            time.sleep(0.01)  # Sleep for 10ms to avoid tight loop

        # Increment key length if it takes too long to find a unique key
        end_time = time.time() * 1000
        if end_time - start_time >= 1000:
            key_length += 1
            start_time = end_time  # Reset the timer for the new key length

    conn.close()

    # Return the key as a JSON response
    return jsonify({"key": key})

@app.route("/api/get/<key>", methods=["GET"])
def get_content(key):
    """获取指定key的内容"""
    if not re.match("^[a-zA-Z0-9]+$", key):
        return "Invalid key"

    filename = f"{key}.md"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(filepath):
        return ""

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except Exception as e:
        return str(e)


@app.route("/api/update/<key>", methods=["POST"])
def update_content(key):
    """更新指定key的内容"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"})

    content = data.get("content")

    if not content:
        return jsonify({"error": "Missing content field"})

    # 保存内容到文件
    filename = f"{key}.md"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    # 保存历史记录到sqlite数据库
    conn = sqlite3.connect(app.config["DATABASE_PATH"])
    c = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    c.execute("INSERT OR IGNORE INTO keys (key) VALUES (?)", (key,))
    c.execute(
        "INSERT INTO histories (key, update_time, content, ip, user_agent) VALUES (?, ?, ?, ?, ?)",
        (key, now, content, ip, user_agent),
    )
    history_id = c.lastrowid
    conn.commit()
    conn.close()

    return jsonify({"history_id": history_id})


@app.route("/api/refresh/<key>/<int:id>", methods=["GET"])
def refresh_content(key, id):
    """获取指定key和id的最新历史记录"""
    conn = sqlite3.connect(app.config["DATABASE_PATH"])
    c = conn.cursor()
    c.execute(
        "SELECT * FROM histories WHERE key = ? AND id > ? ORDER BY id DESC LIMIT 1",
        (key, id),
    )
    result = c.fetchone()
    conn.close()

    if result:
        history_id, _, _, content, _, _ = result
        return jsonify({"history_id": history_id, "content": content})
    else:
        return jsonify({})


def extract_cookies_from_header(cookie_header):
    cookies = {}
    if cookie_header:
        # Split the header by semicolon to get the individual parts
        cookie_parts = cookie_header.split(';')
        # print(cookie_parts[0])
        # Only consider the first part for the actual cookie key-value pair
        # key, value = cookie_parts[0].strip().split('=')
        # cookies[key] = value
        # 使用正则表达式匹配键值对
        pattern = r'([^=]+)=([^;]+)'

        # 匹配所有的键值对
        matches = re.findall(pattern, cookie_parts[0])

        # 创建一个字典来存储解析后的键值对
        cookies = {}

        # 将匹配到的键值对添加到字典中
        for match in matches:
            key = match[0]
            value = match[1]
            cookies[key] = value
    return cookies
        
@app.route("/api/ai/user/currentUser", methods=["GET"])
def currentUser():
    default_user_info = {"status": 1, "success": False, "message": ""}
    cookies = request.headers.get("Cookie")
    if cookies:
        # Send request with existing cookies
        url = "https://api.yunzhu.info/user/currentUser"
        headers = {"Cookie": cookies}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            try:
                user_info['data']['userName'] = '共享用户'
            except Exception as ex:
                pass
            return jsonify(user_info)

    # Load cookies from cookies.json
    with open("cookies.json", "r") as file:
        cookies_data = json.load(file)

    # Send request with cookies from cookies.json
    url = "https://api.yunzhu.info/user/currentUser"
    headers = {"Cookie": f"EGG_SESS={cookies_data['EGG_SESS']}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        if user_info.get("status") == 0:
            try:
                user_info['data']['userName'] = '共享用户'
            except Exception as ex:
                pass
            return jsonify(user_info) 

    url = "https://api.yunzhu.info/user/loginByPwd"
    config = Config()
    username = config['echo']['username']
    password = config['echo']['password']
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        login_response = response.json()
        if login_response.get("status") == 0:
            set_cookie_header = response.headers.get("Set-Cookie")
            new_cookies = extract_cookies_from_header(set_cookie_header)
            cookies_data = {}
            cookies_data["EGG_SESS"] = new_cookies.get("EGG_SESS", "")
            
            with open("cookies.json", "w") as file:
                json.dump(cookies_data, file) 

            # Send request with new cookies
            headers = {"Cookie": f"EGG_SESS={cookies_data['EGG_SESS']}"} 
            url = "https://api.yunzhu.info/user/currentUser"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                try:
                    user_info['data']['userName'] = '共享用户'
                except Exception as ex:
                    pass
                return jsonify(user_info)

    return jsonify(default_user_info)

@app.route("/api/ai/<path:url>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(url):
    headers = {key: value for (key, value) in request.headers if key != "Host"}

    headers["Origin"] = app.config["PROXY_DOMAIN"]
    headers["Referer"] = app.config["PROXY_DOMAIN"]
    headers["Host"] = app.config["PROXY_DOMAIN"].replace("https://", "")

    url = f'{app.config["PROXY_DOMAIN"]}/{url}'
    data = {} 

    cookies = request.headers.get("Cookie")
    if cookies == None: 
        with open("cookies.json", "r") as file:
            cookies_data = json.load(file)
            headers["Cookie"]  = f"EGG_SESS={cookies_data['EGG_SESS']}"

    if request.method == "GET":
        resp = requests.get(url, headers=headers)
    elif request.method == "POST":  
        try:
            data = request.get_json()
            if data is None:
                data = {} 
        except Exception:
            data = {}

        if data.get("stream") == True:
            resp = requests.post(
                url,
                json=request.get_json(),
                headers=headers,
                stream=True,
            )
        else:
            resp = requests.post(
                url,
                json=data,
                headers=headers
            )
    elif request.method == "PUT":
        resp = requests.put(
            url,
            json=request.get_json(),
            headers=headers,
        )
    elif request.method == "DELETE":
        resp = requests.delete(url, headers=headers)
    elif request.method == "OPTIONS":
        resp = requests.options(url, headers=headers)
    if request.method in ["POST"]: 
        if data.get("stream") == True:
            def generate():
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk

            return Response(
                stream_with_context(generate()),
                content_type=resp.headers["content-type"],
            )
        else:
            return Response(
                resp.content, status=resp.status_code, headers=dict(resp.headers)
            )
    else:
        if(resp.status_code != 200): 
            return jsonify({"status": resp.status_code, "message": '出错了'})
        return Response(
            resp.content, status=resp.status_code, headers=dict(resp.headers)
        )
