from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import time
import json
from redis import Redis

import random
from storage import sync_lancedb_client
import app as celery_tasks
from core import prompt_encoder
from tasks import video_2_text

from pydantic import BaseModel
from redis_lru import RedisLRU

app = FastAPI()

redis_conn = Redis(host='redis', port=6379)
redis_lru_cache = RedisLRU(redis_conn, max_size=2 ** 10)

video_2_text.load_clip()

lance_table = None
sync_lance_table = None

table_update_time = time.time()

class VideoModel(BaseModel):
    link: str
    description: str

def query_to_embedding(query):
    return video_2_text.embed_text(query)

"""
синхронный инсерт рандом
"""
# sync_lancedb_client
@app.get("/api/sync_insert_random")
async def sync_insert_rand():
    db = sync_lancedb_client.connect()
    sync_lancedb_client.create_table(db)
    table = sync_lancedb_client.open_table(db)
    sync_lancedb_client.insert_random(table, 10000)
"""
синхронный поиск 
"""
# sync_lancedb_client
@app.get("/api/search_html")
async def sync_search(query: str = "новости", response_class=HTMLResponse):
    global sync_lance_table, table_update_time

    t1_vector = time.time()

    embedding = query_to_embedding(query)

    t2 = time.time()

    if not sync_lance_table or time.time() > table_update_time + 120:
        db = sync_lancedb_client.connect()
        sync_lancedb_client.create_table(db)
        sync_lance_table = sync_lancedb_client.open_table(db)
        table_update_time = time.time()
    
    t3 = time.time()

    vector_results = sync_lancedb_client.search(sync_lance_table, embedding, limit=4000)

    t4 = time.time()

    text_result = []
    visual_result = []
    used = []

    for row in vector_results.to_dict(orient='records'):
        if "[visual]" in row["id"]:
            if len(visual_result) == 10:
                continue
            id = row["id"].replace("[visual]", "")
            if id in used:
                continue
            used.append(id)
            visual_result.append(row)
        if "[audio+text]" in row["id"]:
            if len(text_result) == 10:
                continue
            id = row["id"].replace("[audio+text]", "")
            if id in used:
                continue
            used.append(id)
            text_result.append(row)
    t2_vector = time.time()

    tech_info = f'{t2_vector - t1_vector}s. {t4 - t3}s. on vector search. {t2 - t1_vector}s. on embedding.'
    
    def _get_html(row):
        url = row["id"].replace("[audio+text]", "").replace("[visual]", "")
        desc = row["description"]
        return f"""
        <div class="result-item">
                <video src="{url}" controls></video>
                <div class="info">
                    <h3>Distance: {row["_distance"]}</h3>
                    <p>{desc}</p>
                </div>
        </div>
        """
    
    VISUAL_HTML = []
    TEXT_HTML = []
    for row in visual_result[:10]:
        VISUAL_HTML.append(_get_html(row))
    for row in text_result[:10]:
        TEXT_HTML.append(_get_html(row))
    
    with open("search_template.html", "r") as f:
        template = f.read()
    
    html = template.replace("<!-- VISUAL_RESULT -->", "\n".join(VISUAL_HTML)).replace("<!-- TEXT_RESULT -->", "\n".join(TEXT_HTML)).replace("<!-- TECHINCAL -->", tech_info)

    # TODO: Add correct description
    return HTMLResponse(content=html, status_code=200)

"""
ручка по спецификации
"""
@app.get("/api/search")
async def sync_search_specification(query: str):

    global sync_lance_table, table_update_time
    
    embedding = query_to_embedding(query)
    if not sync_lance_table or time.time() > table_update_time + 120:
        db = sync_lancedb_client.connect()
        sync_lancedb_client.create_table(db)
        sync_lance_table = sync_lancedb_client.open_table(db)
        table_update_time = time.time()

    vector_results = sync_lancedb_client.search(sync_lance_table, embedding, limit=1500)

    text_result = []
    visual_result = []
    used = []

    for row in vector_results.to_dict(orient='records'):
        if "[visual]" in row["id"]:
            if len(visual_result) == 10:
                continue
            id = row["id"].replace("[visual]", "")
            if id in used:
                continue
            used.append(id)
            visual_result.append(row)
        if "[audio+text]" in row["id"]:
            if len(text_result) == 10:
                continue
            id = row["id"].replace("[audio+text]", "")
            if id in used:
                continue
            used.append(id)
            text_result.append(row)

    query = ' '.join(["#" + i for i in query.split(' ') if i])
    hashtag_results = sync_lancedb_client.search_fts(sync_lance_table, query, 20)
    if len(hashtag_results) > 1: 
        top_hashtags = hashtag_results[['id', 'description']].to_dict(orient='records')
    else:
        top_hashtags = None

    result = {
        "visual_results": [dict(id=r["id"], description=r["description"]) for r in visual_result],
        "text_summary_results": [dict(id=r["id"], description=r["description"]) for r in text_result],
        "hashtag_results": top_hashtags,
    }


    ## TO DO 
    ##перетянуть весь discription
    return JSONResponse(content=result, status_code=200)
    ##return HTMLResponse(content=html, status_code=200)

"""
синхронный индекс 
"""
@app.post("/api/index")
async def add_video_to_index(video: VideoModel):
    # Добавление видео в индекс
    task = celery_tasks.video_2_text.delay(video.link, video.description)

    return { "video": video.link, "description" : video.description }
    ## "link", "description"

@app.get("/api/create_indexes")
async def create_indexes():
    db = sync_lancedb_client.connect()
    table = sync_lancedb_client.create_table(db)
    sync_lancedb_client.create_index_fts(table)
    return "success"

@app.get("/api/test")
async def root():
    task = celery_tasks.sleep.delay()
    return {"message": task.id}

@app.get("/api/add")
async def add(url: str, description: str):
    task = celery_tasks.video_2_text.delay(url, description)
    return {"task_id": task.id}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="backend", port=5556, log_level="debug", forwarded_allow_ips="*", proxy_headers=True)
