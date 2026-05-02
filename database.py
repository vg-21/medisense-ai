import sqlite3

DB_PATH = "medisense.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT,
            user_input TEXT,
            key_findings TEXT,
            summary TEXT,
            next_steps TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_analysis(input_type, user_input, key_findings, summary, next_steps):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (input_type, user_input, key_findings, summary, next_steps)
        VALUES (?, ?, ?, ?, ?)
    ''', (input_type, user_input, key_findings, summary, next_steps))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Returns last 10 analyses as a list
    cursor.execute('''
        SELECT DATE(created_at), input_type, summary 
        FROM chat_history 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        result.append([row[0], row[1], row[2]])
    return result

# Auto-create on first run
init_db()
