 # -*- coding: utf-8 -*-
import os
import sqlite3

from http_service import app


def create_database_if_not_exists():
    database_path = app.config["DATABASE_PATH"]
    if not os.path.exists(database_path):
        conn = sqlite3.connect(database_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS histories
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      key TEXT,
                      update_time TEXT,
                      content TEXT,
                      ip TEXT,
                      user_agent TEXT)"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS keys 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      key TEXT)"""
        )
        conn.close()


if __name__ == "__main__":
    create_database_if_not_exists()

    # Ensure the upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.run(host="0.0.0.0")
