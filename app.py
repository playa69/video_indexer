import os
import uvicorn

from celery import Celery
from tasks.sleep import sleep_impl
from tasks.video_2_text import video_2_text_impl

os.environ.setdefault('CELERY_CONFIG_MODULE', 'conf.celery_config')

app = Celery('app')
app.config_from_envvar('CELERY_CONFIG_MODULE')


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def video_2_text(url, description=""):
    return video_2_text_impl(url, description)

@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def sleep():
    return sleep_impl()
