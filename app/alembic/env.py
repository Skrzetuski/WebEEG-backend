from sqlalchemy import URL
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
from logging.config import fileConfig

from models.base import Base

url_db = URL.create(
    "postgresql",
    username=os.getenv("DATABASE_USER", "postgres"),
    password=os.getenv("DATABASE_PASSWORD", "password"),  
    host=os.getenv("DATABASE_URL", "localhost"),
    database=os.getenv("DATABASE_NAME", "noesisdb"),
    port=os.getenv("DATABASE_PORT", "5432")
)

config = context.config
config.set_main_option("sqlalchemy.url", url_db.render_as_string(hide_password=False))

target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
