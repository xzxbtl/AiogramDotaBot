from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, BigInteger

metadata_obj = MetaData()


users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("user_id", BigInteger),
    Column("age", String),
    Column("Confirmed", Boolean, default=False),
    Column("Status", String, default="Herald"),
    Column("Balance", Integer, default=0)
)

daily_table = Table(
    "daily",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("time_reward", String),
    Column("user_id", BigInteger)
)

shop_status = Table(
    "StatuShop",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("status_name", String, default=["Herald"]),
    Column("user_id", BigInteger)
)

settings_status = Table(
    "Settings",
    metadata_obj,
    Column("user_id", BigInteger, primary_key=True),
    Column("hidden_id", Boolean, default=False),
    Column("emoji_swap", String, default="💎")
)

works_stable = Table(
    "Works",
    metadata_obj,
    Column("user_id", BigInteger, primary_key=True),
    Column("Job", String, default=None),
    Column("Status", String, default="finished"),
    Column("TakeAward", Boolean, default=False)
)
