from sqlalchemy import text
from app.db.session import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM item LIMIT 1"))
    print(f"Result: {result.fetchone()} | keys: {list(result.keys())}")