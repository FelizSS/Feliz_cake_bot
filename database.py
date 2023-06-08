import sqlite3

connection = sqlite3.connect('portfolio.db')

sql = connection.cursor()

# sql.execute('create table users (id integer, name integer, phone_number text, gender text);')
# sql.execute('create table products (name integer, id integer, price integer, description text, picture text, notes text);')

def add_user(user_id, name, phone_number, gender):

    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    sql.execute('INSERT INTO users VALUES (?,?,?,?);',
                (user_id, name, phone_number, gender))
    connection.commit()

    return add_user


def get_users():
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    users = sql.execute('select name, id, gender from users;')
    return users.fetchall()

def add_products(id, name, price, description, picture, notes):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()

    sql.execute('insert into products value(?,?,?,?);',
                (id, name, price, description, picture, notes))
    connection.commit()

def get_all_info_product(current_product):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()

    all_products = sql.execute('select * from products where name=?;', (current_product, ))

    return all_products.fetchone()

def get_name_product(category_id):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    product_id = sql.execute('SELECT * FROM products WHERE id=?;', (category_id,))
    return product_id.fetchall()

def cake_product():
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    product_id = sql.execute('SELECT * FROM products WHERE id=11;')
    return product_id.fetchall()

def mini_cake_product():
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    product_id = sql.execute('SELECT * FROM products WHERE id=22;')
    return product_id.fetchall()

def check_user(user_id):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    checker = sql.execute('SELECT id FROM users WHERE id=?;',
                          (user_id,))

    if checker.fetchone():
        return True
    else:
        return False

def add_pr_to_cart(user_id, product_name, price_pr, product_count):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()

    phone_number = sql.execute('select phone_number from users where id=?;', (user_id,))
    user_number = phone_number.fetchone()[0]

    sql.execute('INSERT INTO cart VALUES (?,?,?,?,?);',
                (user_id, product_name, user_number, price_pr * product_count, product_count))

    connection.commit()


def add_pr_to_cart2(user_id, product_name, price_pr, product_count):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()

    phone_number = sql.execute('select phone_number from users where id=?;', (user_id,))
    user_number = phone_number.fetchone()[0]

    sql.execute('INSERT INTO cart2 VALUES (?,?,?,?,?);',
                (user_id, product_name, user_number, price_pr * product_count, product_count))

    connection.commit()


def get_user_cart(user_id):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    all_products_from_cart = sql.execute('SELECT * FROM cart WHERE user_id=?;',
                                         (user_id,))

    return all_products_from_cart.fetchall()

def delete_from_cart(user_id):
    connection = sqlite3.connect('portfolio.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))

    connection.commit()

# sql.execute('CREATE TABLE cart2 (user_id INTEGER, product_name TEXT, user_number TEXT, product_price INTEGER, product_count INTEGER);')

# sql.execute('CREATE TABLE cart (user_id INTEGER, product_name TEXT, user_number TEXT, product_price INTEGER, product_count INTEGER);')

