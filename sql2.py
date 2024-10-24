import sqlite3

def create_database():
    conn = sqlite3.connect('rental_management.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            address TEXT NOT NULL,
            price REAL NOT NULL,
            type TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
