import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import config

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect(config.DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY,
    total_messages INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Проверка и создание записи статистики
    cursor.execute("SELECT COUNT(*) FROM stats")
    if cursor.fetchone()[0] == 0:
        # CORREGIDO: Sangría agregada aquí
        cursor.execute("INSERT INTO stats (total_messages) VALUES (0)")
    
    conn.commit()
    conn.close()

def get_user_stats(user_id: int) -> Dict:
    """Получить статистику пользователя"""
    conn = sqlite3.connect(config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM messages WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return {"messages_count": result["count"]}

def update_global_stats():
    """Обновить глобальную статистику"""
    conn = sqlite3.connect(config.DATABASE_URL)
    # CORREGIDO: Agregado row_factory para que funcione cursor.fetchone()["total"]
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM messages")
    total = cursor.fetchone()["total"]
    
    cursor.execute("INSERT OR REPLACE INTO stats (id, total_messages, updated_at) VALUES (1, ?, CURRENT_TIMESTAMP)", (total,))
    conn.commit()
    conn.close()

def save_message(user_id: int, message: str, response: str):
    """Сохранить сообщение и ответ"""
    conn = sqlite3.connect(config.DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO messages (user_id, message, response) VALUES (?, ?, ?)", 
    (user_id, message, response))
    conn.commit()
    conn.close()

def get_user_info(user_id: int) -> Dict:
    """Получить информацию о пользователе"""
    conn = sqlite3.connect(config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        # CORREGIDO: Sangría agregada al bloque del if
        cursor.execute("INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
        (user_id, "Unknown", "Unknown", ""))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    
    conn.close()
    
    return {
    "id": user["id"],
    "username": user["username"],
    "first_name": user["first_name"],
    "last_name": user["last_name"],
    "created_at": user["created_at"]
    }
