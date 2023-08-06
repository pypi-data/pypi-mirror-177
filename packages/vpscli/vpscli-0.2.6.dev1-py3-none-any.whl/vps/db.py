#!/usr/bin/env python
import ssl

import aiomysql

from vps.auth import Accounts

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile=Accounts.ssl_cert)


async def insert_once(loop, key: str, values: list):
    pool = await aiomysql.create_pool(
        host=Accounts.host,
        port=3306,
        user=Accounts.username,
        password=Accounts.password,
        db=Accounts.database,
        loop=loop,
        ssl=ctx,
    )
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            resp = await cur.execute(
                "INSERT INTO db (`key`, `value`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value=%s",
                (key, values, values))
            await conn.commit()
            return resp
