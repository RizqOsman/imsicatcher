import sqlite3
from datetime import datetime
from collections import Counter

DB_FILE = 'imsicatcher.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS imsi_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imsi TEXT,
        timestamp TEXT,
        signal_strength REAL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist (
        imsi TEXT PRIMARY KEY,
        label TEXT
    )''')
    conn.commit()
    conn.close()

def save_imsi(imsi: str, signal_strength: float | None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO imsi_logs (imsi, timestamp, signal_strength) VALUES (?, ?, ?)',
                   (imsi, datetime.now().isoformat(), signal_strength))
    conn.commit()
    conn.close()

def get_all_imsis():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT imsi, timestamp, signal_strength FROM imsi_logs ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_to_blacklist(imsi: str, label: str | None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO blacklist (imsi, label) VALUES (?, ?)', (imsi, label))
    conn.commit()
    conn.close()

def get_blacklisted_imsis():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT imsi, label FROM blacklist')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_statistics():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT imsi, signal_strength FROM imsi_logs')
    rows = cursor.fetchall()
    conn.close()
    imsis = [r[0] for r in rows]
    signals = [r[1] for r in rows if r[1] is not None]
    most_common = [i[0] for i in Counter(imsis).most_common(5)]
    avg_signal = round(sum(signals) / len(signals), 2) if signals else None
    return len(imsis), avg_signal, most_common