import sqlite3

con = sqlite3.connect('users.db')
cursor = con.cursor()

# User Table
cursor.execute("""CREATE TABLE IF NOT EXISTS 
        users(
        user_ID INT PRIMARY KEY,
        choosing_lang INT DEFAULT 0,
        translate_from TEXT DEFAULT 'Kurdish',
        translate_to TEXT DEFAULT 'English'
        )""")


def insert_user(user_id: int, choosing_lang:int, translate_from: str, translate_to: str):
    cursor.execute('SELECT user_ID FROM users WHERE user_ID=?', (user_id,))
    res = cursor.fetchone()

    if res:
        return
    else:
        cursor.execute("""
                INSERT INTO users VALUES
                (?,?,?,?)
                """, (user_id, choosing_lang, translate_from, translate_to))
        con.commit()


def update_language_from(user_id: int, choosing_lang: int, translate_from: str):
    cursor.execute("""
    UPDATE users
    SET choosing_lang=?, translate_from=?
    WHERE user_ID=?""", (choosing_lang, translate_from, user_id))

    con.commit()


def update_language_to(user_id: int, choosing_lang: int, translate_to: str):
    cursor.execute("""
    UPDATE users
    SET choosing_lang=?, translate_to=?
    WHERE user_ID=?""", (choosing_lang, translate_to, user_id))

    con.commit()


def update_choosing(user_id:int, choosing_lang:int):
    cursor.execute('UPDATE users SET choosing_lang=? WHERE user_ID=?', (choosing_lang, user_id))
    con.commit()


def is_choosing(user_id:int) -> int:
    value = cursor.execute('SELECT choosing_lang FROM users WHERE user_ID=?', (user_id,)).fetchone()

    return value[0]


# CLOSE IT MANE
def get_translate_from(user_id: int) -> str:
    lang = cursor.execute('SELECT translate_from FROM users WHERE user_ID=?', (user_id,)).fetchone()
    return lang[0]

def get_translate_to(user_id: int) -> str:
    lang = cursor.execute('SELECT translate_to FROM users WHERE user_ID=?', (user_id,)).fetchone()
    return lang[0]



