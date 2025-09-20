import os
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text

# строка подключения к БД
DATABASE_URL = os.getenv("DATABASE_URL")

# движок SQLAlchemy (sslmode=require для Neon)
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
metadata = MetaData()

# таблицы
mood_log = Table(
    "mood_log", metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", String, nullable=False),
    Column("mood", Integer, nullable=False)
)

journal = Table(
    "journal", metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", String, nullable=False),
    Column("entry", Text),
    Column("image_path", String)
)

user_settings = Table(
    "user_settings", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("notify", Integer, default=1)
)

# создать таблицы, если нет
metadata.create_all(engine)

# --- функции ---
def log_mood(mood_value: int):
    with engine.begin() as conn:
        conn.execute(mood_log.insert().values(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            mood=mood_value
        ))

def get_mood_history():
    with engine.begin() as conn:
        result = conn.execute(mood_log.select().order_by(mood_log.c.timestamp.desc()))
        return result.fetchall()

def save_journal_entry(entry_text: str, image_path=None):
    with engine.begin() as conn:
        conn.execute(journal.insert().values(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            entry=entry_text,
            image_path=image_path
        ))

def get_user_settings(user_id: int):
    with engine.begin() as conn:
        result = conn.execute(user_settings.select().where(user_settings.c.user_id == user_id)).fetchone()
        if result:
            return result.notify
        else:
            conn.execute(user_settings.insert().values(user_id=user_id, notify=1))
            return 1

def set_user_notify(user_id: int, notify: int):
    with engine.begin() as conn:
        conn.execute(user_settings.insert().values(user_id=user_id, notify=notify).prefix_with("ON CONFLICT (user_id) DO UPDATE SET notify=excluded.notify"))
