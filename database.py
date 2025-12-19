import sqlite3
import os

if not os.path.exists('data'):
    os.makedirs('data')

conn = sqlite3.connect('data/quotes.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quote_tags (
    quote_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (quote_id) REFERENCES quotes(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
)
''')

conn.commit()

def init_db():
    try:
        cursor.execute("SELECT COUNT(*) FROM tags")
        if cursor.fetchone()[0] == 0:
            tags = ['Мотивация', 'Юмор', 'Любовь', 'Философия', 'Успех']
            for tag in tags:
                cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
            
            quotes = [
                ("Всё будет хорошо!", "Оптимист"),
                ("Смех продлевает жизнь", "Доктор"),
                ("Любите друг друга", "Мудрец"),
                ("Учитесь, пока другие спят", "Ученый"),
                ("Мечтайте о большем", "Мечтатель")
            ]
            
            for text, author in quotes:
                cursor.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text, author))
                quote_id = cursor.lastrowid
                
                if "хорошо" in text.lower():
                    cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, 1)", (quote_id,))
                elif "смех" in text.lower():
                    cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, 2)", (quote_id,))
                elif "любите" in text.lower():
                    cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, 3)", (quote_id,))
            
            conn.commit()
            print("База данных инициализирована!")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")

def get_random_quote(tag_name=None):
    try:
        if tag_name:
            cursor.execute('''
                SELECT q.text, q.author 
                FROM quotes q
                JOIN quote_tags qt ON q.id = qt.quote_id
                JOIN tags t ON qt.tag_id = t.id
                WHERE t.name = ?
                ORDER BY RANDOM()
                LIMIT 1
            ''', (tag_name,))
        else:
            cursor.execute('''
                SELECT text, author 
                FROM quotes 
                ORDER BY RANDOM() 
                LIMIT 1
            ''')
        
        result = cursor.fetchone()
        if result:
            return f"{result[0]}\n\n— {result[1]}"
        else:
            return "Цитаты не найдены"
    except Exception as e:
        return f"Ошибка: {e}"

def get_all_tags():
    cursor.execute("SELECT name FROM tags ORDER BY name")
    return [row[0] for row in cursor.fetchall()]

def add_quote(text, author, tags):
    try:
        cursor.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text, author))
        quote_id = cursor.lastrowid
        
        for tag_name in tags:
            cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
            
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_id = cursor.fetchone()[0]
            
            cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, ?)", (quote_id, tag_id))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        return False

init_db()
