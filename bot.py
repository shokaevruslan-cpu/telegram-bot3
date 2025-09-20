import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text, select, insert, update
from sqlalchemy.orm import sessionmaker

# DATABASE_URL должен быть вида:
# postgresql+psycopg://username:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаём подключение к базе
engine = create_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"),
    connect_args={"sslmode": "require"},
    future=True
)

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

# Сессии для работы с БД
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# 📌 Функции работы с БД
def log_mood(timestamp, mood_value):
    with SessionLocal() as session:
        session.execute(insert(mood_log).values(timestamp=timestamp, mood=mood_value))
        session.commit()

def get_mood_history():
    with SessionLocal() as session:
        result = session.execute(select(mood_log)).fetchall()
        return result

def save_journal_entry(timestamp, entry_text):
    with SessionLocal() as session:
        session.execute(insert(journal).values(timestamp=timestamp, entry=entry_text))
        session.commit()

def get_user_settings():
    with SessionLocal() as session:
        result = session.execute(select(user_settings)).fetchone()
        return result

def set_user_notify(value: str):
    with SessionLocal() as session:
        result = session.execute(select(user_settings)).fetchone()
        if result:
            session.execute(
                update(user_settings)
                .where(user_settings.c.id == result.id)
                .values(notify=value)
            )
        else:
            session.execute(insert(user_settings).values(notify=value))
        session.commit()


