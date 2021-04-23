import sqlite3
def insert_test_values():
    connection = sqlite3.connect('data1.db')
    cursor = connection.cursor()

    create_user = 'INSERT INTO users VALUES (?, ?, ?)'
    user = ( 'brawlerdima', '123')
    cursor.execute(create_user, user)

    users = [
        (2, 'timurrab', '456'),
        (3, 'david', 'asd')

    ]
    cursor.executemany(create_user, users)

    create_item = 'INSERT INTO items(id, name, price) VALUES (NULL, ?, ?)'
    item = ('csgo', 100)
    cursor.execute(create_item, item)

    items = [
        ('chess', 50),
        ('dota', 200)
    ]
    cursor.executemany(create_item, items)

    connection.commit()
    connection.close()
