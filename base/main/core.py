import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from .config import settings
from ..models import works_stable

if sys.platform.startswith('win') and os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async_engine = create_async_engine(
    settings.DataBase_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

table = works_stable


async def get_async_engine_connect():
    async with async_engine.connect() as conn:
        await conn.execute(table.delete())
        await conn.commit()
        print(f"Table {table} truncated successfully.")
    print("Data Base READY FOR WORKING")

asyncio.run(get_async_engine_connect())

"""
with sync_engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(f"{res.first()[0] = }")
    
sync_engine = create_engine(
    settings.DataBase_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)
"""
