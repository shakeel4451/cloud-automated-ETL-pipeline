import requests
import sqlite3
import pandas as pd
from datetime import datetime

DB_file="tech_news.db"
EXPORT_FILE = "daily_report.csv"

def setup_database():
  """Initializes the SQLite database and schema."""
  conn=sqlite3.connect(DB_file)
  cursor=conn.cursor()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT,
            score INTEGER,
            extraction_date TEXT
        )

 ''')
  conn.commit()
  return conn

def fetch_top_stories():
  """Extracts data from the Hacker News API."""
  url = "https://hacker-news.firebaseio.com/v0/topstories.json"

  try:
    response = requests.get(url, timeout=10).json()
    stories = []

    for story_id in response[:30]:
      item_url=f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

      item_data=requests.get(item_url,timeout=5).json()
      if item_data and "title" in item_data and "url" in item_data:
        stories.append((
          item_data["id"],
          item_data["title"],
          item_data["url"],
          item_data.get("score", 0),
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          ))
    return stories
  except Exception as e:
    print(f"❌ Extraction Failed: {e}")
    return []
  
def save_to_db(conn,stories):
  """Loads extracted data into the SQLite database."""
  cursor=conn.cursor()
  # INSERT OR IGNORE is our UPSERT logic. If the ID exists, it skips it.
  cursor.executemany('''
        INSERT OR IGNORE INTO articles (id, title, url, score, extraction_date)
        VALUES (?, ?, ?, ?, ?)
    ''', stories)
  conn.commit()