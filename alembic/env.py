import os
from dotenv import load_dotenv
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
# from NutriDash.app.db.database import Base
from app.db.database import Base
target_metadata = Base.metadata
import app.models.waterGoal
import app.models.habits
import app.models.todo



load_dotenv()  

config = context.config

fileConfig(config.config_file_name)


config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
