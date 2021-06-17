import asyncpg
from pprint import pprint


async def connect_to_db():
    conn = await asyncpg.connect(
        user="Tim", password="000168154", database="stage", host="postgres", port="5432"
    )
    async with conn.transaction():
        await conn.execute(
            """CREATE TABLE if not exists users(
                           email TEXT NOT NULL,
                           password TEXT NOT NULL,
                           username TEXT NOT NULL,
                           vk_id INT NULL, 
                           vk_token TEXT NULL);"""
        )
    return conn


async def write_to_db(table: str, conn, values: list):
    try:
        await conn.execute(f"""INSERT INTO {table} VALUES {tuple(values)};""")
    except Exception as error:
        print(f"ERROR: {error}")


async def read_table_from_db(table: str, conn):
    try:
        rows = await conn.fetch(f"SELECT * FROM {table}")
        values = [row.values() for row in rows]
        pprint(values)
    except Exception as error:
        print(f"ERROR: {error}")


async def disconnect_to_db(conn):
    await conn.close()
