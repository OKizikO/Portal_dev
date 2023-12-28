import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_metrics (
    date TEXT PRIMARY KEY,
    alerts REAL,
    district_rank TEXT,
    market_rank TEXT,
    company_rank TEXT,
    ucr REAL
)
''')

conn.commit()
conn.close()
