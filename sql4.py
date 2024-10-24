import sqlite3

def add_is_booked_column():
    conn = sqlite3.connect('rental_management.db') 
    cursor = conn.cursor()
    alter_table_query = '''
    ALTER TABLE properties ADD COLUMN is_booked BOOLEAN DEFAULT 0;
    '''
    try:
        cursor.execute(alter_table_query)  
        conn.commit()  
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()  
add_is_booked_column()
