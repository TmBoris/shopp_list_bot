import sqlite3 as sq
from os import sep


async def db_connect() -> None:
    global db, cur, cur2, users

    db = sq.connect('copy2.db')
    cur = db.cursor()
    cur2 = db.cursor()
    users = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS product(product_id INTEGER PRIMARY KEY, title TEXT, user_id INTEGER)")
    cur2.execute("CREATE TABLE IF NOT EXISTS velga(velga_id INTEGER PRIMARY KEY, name TEXT, user_id TEXT)")
    users.execute("CREATE TABLE IF NOT EXISTS usersinfo(user_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, username TEXT)")

    db.commit()


async def reg_new_user(user_id: int, first_name: str, last_name: str, username: str):

    users.execute("INSERT or IGNORE INTO usersinfo (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, username, ))

    db.commit()


async def get_all_users():

    usersy = users.execute("SELECT user_id FROM usersinfo").fetchall()

    return usersy  # list


async def get_name_from_id(user):
    adder_you_know = users.execute("SELECT first_name FROM usersinfo WHERE user_id IN (?)", (user, )).fetchall()
    www = adder_you_know[0][0]

    return www


async def get_title_from_id(i):
    deleted_product = cur.execute("SELECT title FROM product WHERE product_id IN (?)", (i, )).fetchall()
    ttt = deleted_product[0][0]

    return ttt


async def get_all_products():

    products = cur.execute("SELECT * FROM product").fetchall()

    return products  # list


async def create_new_product(state):

    async with state.proxy() as data:
        product = cur.execute("INSERT INTO product (title) VALUES (?)", (data['title'], ))
        db.commit()

    return product


async def delete_product(product_id: int) -> None:
    cur.execute("DELETE FROM product WHERE product_id = ?", (product_id,))
    db.commit()


async def edit_product(product_id: int, title: str) -> None:
    cur.execute("UPDATE product SET title = ? WHERE product_id = ?", (title, product_id,))
    db.commit()


async def get_all_velgas():

    velgas = cur2.execute("SELECT * FROM velga").fetchall()

    return velgas  # list


async def create_new_velga(state):

    async with state.proxy() as data:
        velga = cur2.execute("INSERT INTO velga (name) VALUES (?)", (data['name'], ))
        db.commit()

    return velga


async def delete_velga(velga_id: int) -> None:
    cur2.execute("DELETE FROM velga WHERE velga_id = ?", (velga_id,))
    db.commit()


async def edit_velga(velga_id: int, name: str) -> None:
    cur2.execute("UPDATE velga SET title = ? WHERE velga_id = ?", (name, velga_id,))
    db.commit()