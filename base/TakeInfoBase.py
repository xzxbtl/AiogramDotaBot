from aiogramproject.base.main.core import async_engine
from aiogramproject.base.models import users_table, daily_table, shop_status, settings_status, works_stable
from datetime import datetime


# Кеш по балансу
async def update_cache(user_id, new_balance):
    TakeInfo.user_cache[user_id]['balance'] = new_balance


class TakeInfo:
    user_cache = {}

    @staticmethod
    async def take_balance(query):
        async with async_engine.begin() as conn:
            user_id = query.from_user.id
            query_sql = users_table.select().where(users_table.c.user_id == user_id).with_only_columns(
                users_table.c.Balance,
            )
            result = await conn.execute(query_sql)
            row = result.fetchone()

            if row is None:
                return

            balance = row[0]

            TakeInfo.user_cache[user_id] = {
                'balance': balance
            }

            return balance

    @staticmethod
    async def update_balance_and_add_to_daily(user_id, new_balance):
        async with async_engine.begin() as conn:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%d-%m-%Y %H:%M")
            # Баланс обновление
            stmt_update = users_table.update().where(users_table.c.user_id == user_id).values(Balance=new_balance)
            await conn.execute(stmt_update)

            stmt_daily = daily_table.insert().values(
                time_reward=formatted_time,
                user_id=user_id
            )
            await conn.execute(stmt_daily)

    @staticmethod
    async def update_balance(user_id, new_balance):
        async with async_engine.begin() as conn:
            # Баланс обновление
            stmt_update = users_table.update().where(users_table.c.user_id == user_id).values(Balance=new_balance)
            await conn.execute(stmt_update)

    @staticmethod
    async def update_satus(user_id, new_status):
        async with async_engine.begin() as conn:
            stmt_update = users_table.update().where(users_table.c.user_id == user_id).values(Status=new_status)
            await conn.execute(stmt_update)

    @staticmethod
    async def create_status(user_id, new_status_name):
        async with async_engine.begin() as conn:
            await conn.execute(shop_status.insert().values(user_id=user_id, status_name=new_status_name))

    @staticmethod
    async def get_status_list(user_id):
        async with async_engine.begin() as conn:
            query = shop_status.select().where(shop_status.c.user_id == user_id).with_only_columns(
                shop_status.c.status_name,
            )
            result = await conn.execute(query)
            existing_status = result.fetchall()
            return existing_status

    @staticmethod
    async def take_all_info_about_user(user_id):
        async with async_engine.connect() as conn:
            query = users_table.select().where(users_table.c.user_id == user_id).with_only_columns(
                users_table.c.Status,
                users_table.c.Balance,
                users_table.c.username,
                users_table.c.Confirmed,
            )
            result = await conn.execute(query)
            row = result.fetchone()
            if row is not None:
                status = row[0] if row is not None else "Herald"
                balance = row[1] if row is not None else 0
                username = row[2]
                confirmed = row[3]
            else:
                status = "Herald"
                balance = 0
                username = None
                confirmed = False

            return status, balance, username, confirmed

    @staticmethod
    async def user_cache_info_profile(user_id):
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)

        TakeInfo.user_cache[user_id] = {
            'status': status,
            'balance': balance,
            'username': username,
            'confirmed': confirmed
        }

    @staticmethod
    async def take_hidden_id(query):
        async with async_engine.begin() as conn:
            user_id = query.from_user.id
            query_sql = settings_status.select().where(settings_status.c.user_id == user_id).with_only_columns(
                settings_status.c.hidden_id,
            )
            result = await conn.execute(query_sql)
            row = result.fetchone()

            if row is None:
                return

            hidden_id = row[0]

            TakeInfo.user_cache[user_id] = {
                'hidden_id': hidden_id
            }

            return hidden_id

    @staticmethod
    async def hide_user_id(user_id, hide_user_id):
        async with async_engine.begin() as conn:
            stmt_update = settings_status.update().where(settings_status.c.user_id == user_id) \
                .values(hidden_id=hide_user_id)
            result = await conn.execute(stmt_update)

            if result.rowcount == 0:
                stmt_insert = settings_status.insert().values(user_id=user_id, hidden_id=hide_user_id)
                await conn.execute(stmt_insert)

            if hide_user_id:
                return True
            else:
                return False

    @staticmethod
    async def take_hidden_new_value(query):
        async with async_engine.begin() as conn:
            user_id = query.from_user.id
            query_sql = settings_status.select().where(settings_status.c.user_id == user_id).with_only_columns(
                settings_status.c.emoji_swap,
            )
            result = await conn.execute(query_sql)
            row = result.fetchone()

            if row is None:
                return

            emoji_swap = row[0]

            TakeInfo.user_cache[user_id] = {
                'emoji': emoji_swap
            }

            return emoji_swap

    @staticmethod
    async def new_emoji(user_id, new_emoji):
        async with async_engine.begin() as conn:
            stmt_update = settings_status.update().where(settings_status.c.user_id == user_id) \
                .values(emoji_swap=new_emoji)
            result = await conn.execute(stmt_update)

            if result.rowcount == 0:
                stmt_insert = settings_status.insert().values(user_id=user_id, hidden_id=new_emoji)
                await conn.execute(stmt_insert)

    @staticmethod
    async def create_job(user_id, job, status_process, take_award):
        async with async_engine.begin() as conn:
            stmt_update = works_stable.update().where(works_stable.c.user_id == user_id) \
                .values(Job=job, Status=status_process, TakeAward=take_award)
            result = await conn.execute(stmt_update)

            if result.rowcount == 0:
                stmt_insert = works_stable.insert().values(user_id=user_id, Job=job,
                                                           Status=status_process)
                await conn.execute(stmt_insert)

    @staticmethod
    async def take_status_job(user_id):
        async with async_engine.connect() as conn:
            query = works_stable.select().where(works_stable.c.user_id == user_id).with_only_columns(
                works_stable.c.Job,
                works_stable.c.Status,
                works_stable.c.TakeAward,
            )
            result = await conn.execute(query)
            row = result.fetchone()
            job = row[0] if row is not None else None
            status = row[1] if row is not None else "finished"
            take_award = row[2] if row is not None else False

            return job, status, take_award
