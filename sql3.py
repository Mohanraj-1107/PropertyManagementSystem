import sqlite3
def create_bookings_table():
    conn = sqlite3.connect('rental_management.db') 
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_name TEXT NOT NULL,
        tenant_email TEXT NOT NULL,
        tenant_phone TEXT NOT NULL,
        property_id INTEGER NOT NULL,
        FOREIGN KEY (property_id) REFERENCES properties(id)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

create_bookings_table()
