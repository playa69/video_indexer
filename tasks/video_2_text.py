from core.ocr import video_to_text as video_to_text_impl
from core.utils.download import download_video
from core.text_summarizer import summarize_text, load_summarizer_model
from core.video_transcribe import load_whisper, transcribe_video
from core.ruclip_encode_video import encode_video, load_clip, embed_text

import torch
import urllib.request
import uuid
import os
import re

from storage import sync_lancedb_client as lancedb_client

def extract_hashtags(text):
  hashtags = re.findall(r'#\w+', text)
  return hashtags

def video_2_text_impl(video_url, description=""):
    video_url = video_url.replace('"', '').replace("'", '')
    video_path = download_video(video_url)
    ocr_text_from_video = video_to_text_impl(video_path)
    whisper_text_from_video = transcribe_video(video_path)

    description_hashtags = extract_hashtags(description)
    description = " ".join([description, whisper_text_from_video, ocr_text_from_video])
    summarized_text, summarized_hashtags = summarize_text(description)
    hashtags = [hashtag.lower() for hashtag in set(description_hashtags + summarized_hashtags)]

    text_2_embed = " ".join([i.replace("#", "") for i in summarized_hashtags])

    video_encoding, text_encoding = encode_video(video_path, text_2_embed)
    video_encoding_list = video_encoding.tolist()
    text_encoding_list = text_encoding.tolist()

    if not (sum(video_encoding_list) < 0.00001 and sum(video_encoding_list) > -0.00001):  # TODO: 0.001% of the videos encoded with all nulls [BUG]
        lancedb_client.insert_fts_row(id=video_url+"[visual]", vector=video_encoding_list, description=summarized_text, hashtags=hashtags)
    if len(description.split()) > 5 and not (sum(text_encoding_list) < 0.00001 and sum(text_encoding_list) > -0.00001):
        lancedb_client.insert_fts_row(id=video_url+"[audio+text]", vector=text_encoding.tolist(), description=summarized_text, hashtags=hashtags)

    os.remove(video_path)
    return video_url, summarized_text, hashtags, video_encoding.tolist()


if __name__ == "__main__":
    print(video_2_text_impl("video url"))
