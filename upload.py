import datetime
import hashlib
import os
import re
import sqlite3
from pathlib import Path

import requests
from flask import jsonify

from config import Config
from upload_oss import OSSClient


class Uploader:
    def __init__(self):
        config = Config()
        self.ossClient = OSSClient()
        self.folder_name = "upload"
        self.folder = os.path.join("assets", self.folder_name)
        self.domain = config.get("static_domain")
        self.static_type = config.get("static_type")
        self.max_file_size = config.get("static_max_file_size")
        self.dbpath = os.path.join("files", "db", "upload.db")
        self.init_db()

    def init_db(self):
        os.makedirs(os.path.dirname(self.dbpath), exist_ok=True)
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                upload_time TEXT NOT NULL, 
                user_agent TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_extension TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                storage_directory TEXT NOT NULL,
                file_hash TEXT NOT NULL
            )
        """
        )

        # print("Database check done.")
        conn.close()

    def query_by_filename(self, original_filename):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT filepath FROM uploads WHERE original_filename=?",
            (original_filename,),
        )
        result = cursor.fetchone()

        filepath = result[0] if result else None

        conn.close()
        return filepath

    def query_by_hash(self, file_hash):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()

        cursor.execute("SELECT filepath FROM uploads WHERE file_hash=?", (file_hash,))
        result = cursor.fetchone()

        filepath = result[0] if result else None

        conn.close()
        return filepath

    def fetch(self, request):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"})

        originalURL = data.get("url")
        newURL = self.query_by_filename(originalURL)
        if newURL:
            return jsonify(
                {
                    "code": 0,
                    "msg": "done",
                    "data": {"originalURL": originalURL, "url": newURL},
                }
            )

        newURL = self.fetch_file(originalURL, request)
        return jsonify(
            {
                "code": 0,
                "msg": "done",
                "data": {"originalURL": originalURL, "url": newURL},
            }
        )

    def fetch_file(self, url, request):
        ip = request.remote_addr
        user_agent = request.user_agent.string
        final_path = ""

        try:
            # 发送GET请求获取图片数据
            response = requests.get(url)
            response.raise_for_status()
            content = response.content

            # 从URL中提取图片文件名
            filename = self.get_filename(Path(url).name)
            year = datetime.datetime.now().strftime("%Y")
            month = datetime.datetime.now().strftime("%m")
            filepath = os.path.join(self.folder, year, month)
            # 构造图片的本地保存路径
            saveto = os.path.join(filepath, filename)
            # 将图片数据写入本地文件
            with open(saveto, "wb") as f:
                f.write(content)

            size = len(content)
            ext = os.path.splitext(filename)[1]
            orig_name = url
            hash_value = self.get_hash(saveto)
            final_path = f"{self.domain}/{self.folder_name}/{year}/{month}/{filename}"

            if self.static_type == "oss":
                final_path = self.ossClient.upload_file(saveto)

            conn = sqlite3.connect(self.dbpath)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO uploads (ip, upload_time, user_agent, file_size, "
                "file_extension, original_filename, filepath, storage_directory, file_hash) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    ip,
                    datetime.datetime.now(),
                    user_agent,
                    size,
                    ext,
                    orig_name,
                    final_path,
                    filepath,
                    hash_value,
                ),
            )
            conn.commit()
            conn.close()

        except Exception as ex:
            print(ex)

        return final_path

    def upload(self, request):
        files = request.files
        ip = request.remote_addr
        user_agent = request.user_agent.string

        succMap = {}
        errFiles = []

        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()

        for name, f in files.items():
            try:
                # 1. 检查文件名是否为空
                if not name:
                    continue

                # 2. 检查上传内容是否为空
                # if not f.stream.read(1):
                #     errFiles.append(name)
                #     continue

                # 新增:校验文件大小
                if f.content_length > int(self.max_file_size):
                    errFiles.append(name)
                    continue

                filename = self.get_filename(f.filename)
                filepath = self.save_file(f, filename)

                with open(filepath, "wb") as file:
                    file.write(f.read())

                succMap[f.filename] = self.save_one_file(
                    f, ip, user_agent, cursor, filename, filepath
                )

            except Exception as e:
                errFiles.append(f.filename)

        conn.commit()
        conn.close()
        return {
            "msg": "done",
            "code": 0,
            "data": {"errFiles": errFiles, "succMap": succMap},
        }

    def delete_file(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
        else:
            print(f"Path {path} does not exist")

    def save_one_file(self, f, ip, user_agent, cursor, filename, filepath):
        size = f.content_length
        ext = os.path.splitext(f.filename)[1]
        orig_name = f.filename
        hash_value = self.get_hash(filepath)

        final_path = self.query_by_hash(hash_value)
        if final_path:
            self.delete_file(filepath)
            return final_path

        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        final_path = f"{self.domain}/{self.folder_name}/{year}/{month}/{filename}"

        if self.static_type == "oss":
            final_path = self.ossClient.upload_file(filepath)

        cursor.execute(
            "INSERT INTO uploads (ip, upload_time, user_agent, file_size, "
            "file_extension, original_filename, filepath, storage_directory, file_hash) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (
                ip,
                datetime.datetime.now(),
                user_agent,
                size,
                ext,
                orig_name,
                final_path,
                filepath,
                hash_value,
            ),
        )

        return final_path

    def get_filename(self, filename):
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        name, ext = os.path.splitext(filename)
        return f"{dt}{ext}"

    def save_file(self, fileobj, filename):
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        path = f"{self.folder}/{year}/{month}"
        if not os.path.exists(path):
            os.makedirs(path)

        filepath = os.path.join(path, filename)
        filepath = re.sub(r"\\", "/", filepath)

        # with codecs.open(filepath, "wb", encoding="utf-8") as file:
        #     file.write(fileobj.read())

        # fileobj.save(filepath)
        return filepath

    def get_hash(self, filepath):
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
