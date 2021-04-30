import asyncpg
from pprint import pprint


async def connect_to_db():
    conn = await asyncpg.connect(
        user="Tim", password="000168154", database="stage", host="postgres", port="5432"
    )
    async with conn.transaction():
        exist = await table_is_exist(conn=conn, table="vk_requests")
        if not exist:
            await conn.execute(
                """CREATE TABLE vk_requests(
                               id INT NOT NULL,
                               code TEXT NOT NULL,
                               date DATE NOT NULL);"""
            )
    return conn


async def write_to_db(table: str, conn, values: list):
    try:
        await conn.execute(f"""INSERT INTO {table} VALUES {tuple(values)};""")
    except Exception as error:
        print(f"ERROR: {error}")


async def read_table_from_db(table: str, conn):
    try:
        values = await conn.fetch(f"SELECT * FROM {table}")
        pprint(values)
    except Exception as error:
        print(f"ERROR: {error}")


async def disconnect_to_db(conn):
    await conn.close()


async def table_is_exist(conn, table: str):
    try:
        await conn.fetchrow(f"SELECT * FROM {table}")
        return True
    except Exception:
        return False

