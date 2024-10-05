import sqlite3

connection = sqlite3.connect('data_base.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    photo TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')


initiate_db()

# cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
#                ('Анальгин', 'Это эффективное обезболивающее лекарственное средство', '100',
#                 'F:\\Documents\\Proekty\\План_написания_админ_панели\\Анальгин.png'))
#
# cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
#                ('Витамин В12', 'Участвует в развитии клеток крови', '200',
#                 'F:\\Documents\\Proekty\\План_написания_админ_панели\\Витамин В12.png'))
#
# cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
#                ('Ибупрофен', 'Это препарат, предназначенный для снижения боли', '300',
#                 'F:\\Documents\\Proekty\\План_написания_админ_панели\\Ибупрофен.png'))
#
# cursor.execute('INSERT INTO Products (title, description, price, photo) VALUES (?, ?, ?, ?)',
#                ('Фестал', 'От дискомфорта и болей в животе', '400',
#                 'F:\\Documents\\Proekty\\План_написания_админ_панели\\Фестал.png'))


def is_included(username):
    check_user = cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    if check_user.fetchone():
        return True
    else:
        return False


def add_user(username, email, age, balance):
    cursor.execute('''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
    ''', (username, email, age, balance))
    connection.commit()


def get_all_products1():
    cursor.execute(' SELECT title, description, price, photo FROM Products WHERE title=? ', ('Анальгин',))
    check_product1 = cursor.fetchall()
    return check_product1


def get_all_products2():
    cursor.execute(' SELECT title, description, price, photo FROM Products WHERE title=? ', ('Витамин В12',))
    check_product2 = cursor.fetchall()
    return check_product2


def get_all_products3():
    cursor.execute(' SELECT title, description, price, photo FROM Products WHERE title=? ', ('Ибупрофен',))
    check_product3 = cursor.fetchall()
    return check_product3


def get_all_products4():
    cursor.execute(' SELECT title, description, price, photo FROM Products WHERE title=? ', ('Фестал',))
    check_product4 = cursor.fetchall()
    return check_product4


connection.commit()
# connection.close()
