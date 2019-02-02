import sqlite3

DB_NAME = 'userimage.db'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def main():
    sql_create_image_table = """CREATE TABLE IF NOT EXISTS images (
                                        sender integer PRIMARY KEY,
                                        image_url text NOT NULL
                                    );"""

    # create a database connection
    conn = create_connection(DB_NAME)
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_image_table)
    else:
        print("Error! cannot create the database connection.")


def create_entry(sender_id, image_url):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            sql = ''' INSERT INTO images(sender,image_url)
                      VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, (sender_id, image_url))
    except sqlite3.Error as e:
        print ('e')


def delete_entry(sender_id):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            sql = 'DELETE FROM images WHERE sender=?'
            cur = conn.cursor()
            cur.execute(sql, (sender_id,))
    except sqlite3.Error as e:
        print ('e')


def get_entry(sender_id):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM images WHERE sender=?", (sender_id,))
            rows = cur.fetchall()
            if rows:
                return rows[0][1]
            return
    except sqlite3.Error as e:
        print ('e')


if __name__ == '__main__':
    main()