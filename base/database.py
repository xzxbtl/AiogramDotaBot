import asyncio
import os
import sys
from models import metadata_obj
from main.core import async_engine

sys.path.insert(1, os.path.join(sys.path[0], '..'))


async def create_tables():
    try:
        async_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.create_all)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        async_engine.echo = False


async def insert_data():
    ...


asyncio.run(create_tables())
