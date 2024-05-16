import asyncpg

DATABASE_URL = "postgresql://test_2:test_2@localhost/connection"

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS message_mappings (
                original_message_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL
            )
        """)
    finally:
        await conn.close()

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)
