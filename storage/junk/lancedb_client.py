from contextlib import contextmanager

import lancedb
import redis_lock
import logging
import uuid
import math
import random
import os
import asyncio

from redis import Redis
from lancedb.index import IvfPq
from lancedb.pydantic import LanceModel, Vector

'''
S3_ADDRESS = "s3://video-search-testing/lancedb"
S3_KEY_ID = "YCAJEQbKfzZlWcfjQg9gK19MN"
S3_KEY = os.getenv("S3_KEY")
S3_REGION = "ru-central1"
S3_ENDPOINT = "https://storage.yandexcloud.net"
'''

VECTOR_SIZE = 512
#TABLE_NAME = "video_indexer_v2"
TABLE_NAME = "testing_table_16_06"

class Model(LanceModel):
    id: str
    description: str
    hashtags: str
    vector: Vector(VECTOR_SIZE)


conn = Redis(host='redis', port=6379)
_COMMIT_LOCK = redis_lock.Lock(conn, "lancedb_lock")


@contextmanager
def commit_lock():
    # Acquire the lock
    #_COMMIT_LOCK.acquire()
    try:
      yield
    except:
      logging.exception(f"LanceDB write operation failed: ")
      raise
    finally:
      pass
      #_COMMIT_LOCK.release()


async def connect():
    '''
    db = await lancedb.connect_async(
        S3_ADDRESS,
        storage_options={
            "aws_access_key_id": S3_KEY_ID,
            "aws_secret_access_key": S3_KEY,
            "region": S3_REGION,
            "endpoint": S3_ENDPOINT,
        },
    )
    '''
    db = await lancedb.connect_async(
        "testing_connect_16_06",
    )
    return db

async def create_table(db):
    with commit_lock():
        return await db.create_table(
            TABLE_NAME,
            schema=Model.to_arrow_schema(),
            exist_ok=True,
        )


async def open_table(db):
    return await db.open_table(
        TABLE_NAME,
    )

async def drop_table(db):
    with commit_lock():
        await db.drop_table(TABLE_NAME)


async def insert_row(table, test_model_row: Model):
    with commit_lock():
        # if isinstance(test_model_row, Model):
        if test_model_row is Model:
            test_model_row = [test_model_row]
        await table.add(test_model_row)


async def drop_row(table, id: str):
    with commit_lock():
        await table.delete(f'id = "{id}"')


async def create_index(table, max_iterations=50):
    def find_closest_divisor(n):
            target_divisor = n // 16
            closest_divisor = None
            closest_distance = float('inf')

            for i in range(1, int(n**0.5) + 1):
                if n % i == 0:
                    for divisor in [i, n // i]:
                        distance = abs(divisor - target_divisor)
                        if distance < closest_distance:
                            closest_divisor = divisor
                            closest_distance = distance

            return closest_divisor

    with commit_lock():
        row_count = await table.count_rows()
        partitions = math.ceil(math.sqrt(row_count)) ## The number of IVF partitions to create.
        num_sub_vect = find_closest_divisor(VECTOR_SIZE) ## Number of sub-vectors of PQ.

        index_conf = IvfPq(
            distance_type='cosine',
            num_partitions=partitions,
            num_sub_vectors=num_sub_vect,
            max_iterations=max_iterations,
        )

        await table.create_index(
            "vector",
            config=index_conf,
        )


async def search(table, vector, limit, refine = 10, fine_probe = 50):

    # https://lancedb.github.io/lancedb/migration/#closeable-table
    df_search = await table.vector_search(vector) \
        .distance_type("cosine") \
        .limit(limit) \
        .nprobes(fine_probe) \
        .refine_factor(refine) \
        .to_pandas()

    return df_search


async def insert_random(table, n):
    data = [Model(id="rand_" + uuid.uuid4().hex, vector=[random.random() for _ in range(VECTOR_SIZE)]) for i in range(n)]
    await insert_row(table, data)


def insert_row_sync(url, tensor, description):
    hashtags = " ".join([d for d in description.split() if d.startswith("#") and len(d) > 4])
    async def _insert(url, tensor):
        db = await connect()
        table = await create_table(db)
        await insert_row(table, [Model(id=url, description=description[:512], hashtags=hashtags, vector=tensor)])
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_insert(url, tensor))
    except:
        asyncio.run(_insert(url, tensor))


async def test():
    db = await connect()
    table = await create_table(db)
    await insert_random(table, 1000)
    # await create_index(table)

    import time
    t1 = time.time()
    df = await search(table, [random.random() for _ in range(VECTOR_SIZE)], 10)
    t2 = time.time()
    print(t2 - t1)
    print(df)
    await drop_table(db)


if __name__ == "__main__":
    asyncio.run(test())
