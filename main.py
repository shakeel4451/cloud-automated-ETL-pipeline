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
  except:
    print