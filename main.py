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

  