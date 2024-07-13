from lancedb.pydantic import LanceModel
import asyncio
import lancedb
import re
import os
import random
import string

# LanceDB connection settings
db_path_test = '~/lance_db'
FTS_TABLE_NAME = "FTS_table"
HEAP = 1024 * 1024 * 1024 * 2  # 2GB heap size

class ModelFTS(LanceModel):
    id: str
    hashtags: str

async def connect_to_lancedb():
    db = await lancedb.connect_async(
        db_path_test,
        storage_options={"timeout": "60s"}
    )
    return db

async def create_fts_table(db):
    await drop_fts_table(db)
    schema = ModelFTS.to_arrow_schema()
    table = await db.create_table(FTS_TABLE_NAME, schema=schema, exist_ok=True)
    
    """ # Use synchronous interface to create the FTS index
    sync_db = lancedb.connect(
        db_path_test,
        storage_options={"timeout": "60s"}
    )  """
    sync_table = db.open_table(FTS_TABLE_NAME)
    sync_table.create_fts_index("hashtags", writer_heap_size=HEAP, replace=True)
    
    return table

async def drop_fts_table(db):
    try:
        await db.drop_table(FTS_TABLE_NAME)
    except Exception as e:
        print(f"Error dropping table {FTS_TABLE_NAME}: {e}")

def preprocess_text(text):
    return re.sub(r'#', '', text.lower())

async def insert_fts_data(table, data):
    preprocessed_data = [{"id": item["id"], "hashtags": preprocess_text(item["hashtags"])} for item in data]
    await table.add(preprocessed_data)

async def search_fts_hashtags(table, query):
    preprocessed_query = preprocess_text(query)
    results = await table.search(preprocessed_query).limit(10).select(["hashtags"]).to_list()
    return results

def generate_random_hashtags():
    words = ["кот", "жопа", "машина", "деньги", "весна", "лето", "осень", "зима", "новости", "работа"]
    return ' '.join([f"#{random.choice(words)}" for _ in range(random.randint(2, 5))])

def generate_random_text(length=30):
    letters = string.ascii_letters + string.digits + " "
    return ''.join(random.choice(letters) for _ in range(length))

async def test_fts():
    db = await connect_to_lancedb()
    table = await create_fts_table(db)

    # Sample data to insert
    data = [
        {"id": str(i), "hashtags": generate_random_hashtags()} for i in range(1, 1001)
    ]
    await insert_fts_data(table, data)

    # Perform a search
    query = "#машина"
    results = await search_fts_hashtags(table, query)
    print(results)

    # Drop the table after testing
    await drop_fts_table(db)

if __name__ == "__main__":
    asyncio.run(test_fts())
