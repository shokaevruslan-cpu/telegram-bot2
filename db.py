import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text
from sqlalchemy.sql import select, insert, update

DATABASE_URL = os.getenv("DATABASE_URL")

# Создаём подключение к базе
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
metadata = MetaData()

# Таблица настроения
mood_log = Table(
    "mood_log",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", String),
    Column("mood", Integer),
)

# Таблица дневника
journal = Table(
    "journal",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", String),
    Column("entry", Text),
)

# Таблица настроек пользователя
user_settings = Table(
    "user_settings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("notify", String),
)

# Создаём таблицы (если их ещё нет)
metadata.create_all(engine)


# 📌 Функции работы с БД
def log_mood(timestamp, mood_value):
    with engine.begin() as conn:
        conn.execute(insert(mood_log).values(timestamp=timestamp, mood=mood_value))


def get_mood_history():
    with engine.begin() as conn:
        result = conn.execute(select(mood_log)).fetchall()
        return result


def save_journal_entry(timestamp, entry_text):
    with engine.begin() as conn:
        conn.execute(insert(journal).values(timestamp=timestamp, entry=entry_text))


def get_user_settings():
    with engine.begin() as conn:
        result = conn.execute(select(user_settings)).fetchone()
        return result


def set_user_notify(value: str):
    with engine.begin() as conn:
        result = conn.execute(select(user_settings)).fetchone()
        if result:
            conn.execute(update(user_settings).values(notify=value))
        else:
            conn.execute(insert(user_settings).values(notify=value))
