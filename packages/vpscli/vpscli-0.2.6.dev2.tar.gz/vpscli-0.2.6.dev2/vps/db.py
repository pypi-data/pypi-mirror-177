#!/usr/bin/env python
import ssl

import aiomysql

from vps.auth import Accounts

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile=Accounts.ssl_cert)
dbname = "vpsstatus"

async def create_pool():
    return await aiomysql.create_pool(
        host=Accounts.host,
        port=3306,
        user=Accounts.username,
        password=Accounts.password,
        db=Accounts.database,
        ssl=ctx,
    )

async def load_data(loop, key:str, limits:int=1000):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            resp = await cur.execute(
                "SELECT * FROM {} WHERE `key` = '{}' LIMIT {}".format(dbname, key, limits))
            return resp


async def insert_once(loop, key: str, value: str):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            cmd = 'INSERT INTO {} (`key`, `value`) VALUES ("{}", "{}") ON DUPLICATE KEY UPDATE `value` = "{}"'.format(dbname, key, value, value)
            resp = await cur.execute(cmd)
            await conn.commit()
            return resp
