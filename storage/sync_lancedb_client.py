from contextlib import contextmanager

import lancedb

import logging
import uuid
import math
import random
import os
import asyncio
import re

from lancedb.index import IvfPq
from lancedb.pydantic import LanceModel, Vector

VECTOR_SIZE = 512
TABLE_NAME = "test_v7"
HEAP = 1024 * 1024 * 1024 * 2  # 2GB heap size

class Model(LanceModel):
    id: str
    description: str
    hashtags: str
    vector: Vector(VECTOR_SIZE)

def insert_fts_data(table, data):
    preprocessed_data = [
      {"id": item["id"], "description": item["description"], "hashtags": " ".join(item["hashtags"]), "vector": item["vector"]}
      for item in data
    ]
    table.add(preprocessed_data)

def insert_fts_row(id, description, hashtags, vector):
    db = connect()
    table = create_table(db)
    insert_fts_data(table, [
        dict(
            id=id,
            description=description,
            hashtags=hashtags,
            vector=vector,
        )
    ])


def remove_hashtags(text):
    return re.sub(r'#', '', text.lower())

def search_fts(table, query, limit):
    preprocessed_query = remove_hashtags(query)
    df_searh_fts = table.search(preprocessed_query) \
        .limit(limit)  \
        .select(["id", "hashtags", "description"])   \
        .to_pandas()
    return df_searh_fts

def create_index_fts(table):
    table.create_fts_index(["description", "hashtags"], replace=True)

def connect():
    db = lancedb.connect(
        "/shared/prod_v0",
    )
    return db

def create_table(db):
    return db.create_table(
        TABLE_NAME,
        schema=Model.to_arrow_schema(),
        exist_ok=True,
    )

def open_table(db):
    return db.open_table(
        TABLE_NAME,
    )

def drop_table(db):
    db.drop_table(TABLE_NAME)

def insert_row(table, test_model_row: Model):
    # if isinstance(test_model_row, Model):
    if test_model_row is Model:
        test_model_row = [test_model_row]
    table.add(test_model_row)

def drop_row(table, id: str):
    table.delete(f'id = "{id}"')

def create_index(table, max_iterations=50):
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

    row_count = table.count_rows()
    partitions = math.ceil(math.sqrt(row_count))  # The number of IVF partitions to create.
    num_sub_vect = find_closest_divisor(VECTOR_SIZE)  # Number of sub-vectors of PQ.

    try:
      # python3.10 lancedb==0.8.2 tantivy==0.20.1 
      # for prom env
      table.create_index(
          vector_column_name="vector",
          distance_type='cosine',
          num_sub_vectors=num_sub_vect,
          num_partitions=partitions,
      )
    except TypeError:
      # python3.12 lancedb==0.8.2 tantivy==0.22.0 
      # for local env
      table.create_index(
          vector_column_name="vector",
          metric='cosine', 
          num_sub_vectors=num_sub_vect,
          num_partitions=partitions,
      )


def search(table, vector, limit, refine=100, fine_probe=1000):
    # https://lancedb.github.io/lancedb/migration/#closeable-table
    # python3.12 lancedb==0.8.2 tantivy==0.22.0 
    # for local env
    df_search = table.search(vector) \
        .metric("cosine") \
        .limit(limit) \
        .refine_factor(refine) \
        .to_pandas()
    return df_search


def insert_random(table, n):
    def generate_random_hashtags():
        words = ["кот",  "машина", "деньги", "весна", "лето", "осень", "зима", "новости", "работа"]
        words += [
				  "любовь", "жизнь", "мода", "еда", "друзья", "музыка", "спорт", "лето", 
					"путешествия", "счастье", "фото", "красота", "природа", "вечер", "работа", 
					"машина", "кот", "собака", "море", "осень", "зима", "весна", "семья", "праздник", 
					"город", "дом", "солнце", "творчество", "день", "ночь", "забота", "учеба", "улыбка", 
					"здоровье", "любимый", "уют", "дети", "позитив", "дождь", "развлечение", 
					"пейзаж", "закат", "мечта", "успех", "работа", "вдохновение", "достижение", "приключение", 
					"стиль", "культура"
				]
        return ' '.join([f"#{random.choice(words)}" for _ in range(random.randint(2, 5))])
    data = [
        Model(
            id="rand_" + uuid.uuid4().hex,
            description="Random description",
            hashtags=generate_random_hashtags(),
            vector=[random.random() for _ in range(VECTOR_SIZE)]
        ) for i in range(n)
    ]
    insert_row(table, data)


def test():
    db = connect()
    table = create_table(db)
    create_index(table)
    create_index_fts(table)
    query = "#пейзаж"
    results = search_fts(table, query, 10)
    print(results)

    import time
    t1 = time.time()
    df = search(table, [random.random() for _ in range(VECTOR_SIZE)], 10)
    t2 = time.time()
    print(t2 - t1)
    print(df)

if __name__ == "__main__":
    test()

