import ruclip
import torch
import base64
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from moviepy.editor import *
import urllib.request
import uuid

device = 'cpu'
clip, processor = ruclip.load('ai-forever/ruclip-vit-base-patch16-384', device=device)


predictor = ruclip.Predictor(clip, processor, device, bs=8)



url = "https://cdn-st.rutubelist.ru/media/dd/6a/ac2964a94bb4aaba578d61b8fc1d/fhd.mp4"

def download_video(src_url):
    download_path = str(uuid.uuid4()) + ".mp4"
    urllib.request.urlretrieve(src_url, download_path)
    return download_path

def get_frames(video, frames=10):
    clip = VideoFileClip(video)
    n_frames = clip.fps * clip.duration // 1
    frame_step = max(1, n_frames // frames)
    frame_step += 1
    frame_n = 0
    result = []
    for frame in clip.iter_frames():
        if frame_n % frame_step == 0:
            result.append(Image.fromarray(frame, 'RGB').resize((256, 256)))
        frame_n += 1
    print(result[0])
    return result


def encode_video(url, description, description_weight=0.0):
    path = download_video(url)
    frames = get_frames(path)
    text_features = predictor.get_text_latents([description]) * description_weight
    image_features = predictor.get_image_latents(frames)

    result_vector = image_features[0]
    for vec in image_features[1:]:
        result_vector = result_vector + vec
    result_vector = result_vector / len(image_features)

    result_vector += text_features[0]
    result_vector /= 1 + description_weight
    return result_vector

video_encoding = encode_video(url, "лепка глина")

queries = [
    "девушка",
    "заяц",
    "заяц лепит из глины",
    "мастер лепки из глины",
    "скульптор",
    "лепка чашки",
    "крутые тачки",
    "порно"
]

from tqdm import tqdm

queries_mapping = {q: predictor.get_text_latents([q])[0] for q in tqdm(queries)}

from torch import nn

for q in queries_mapping:
    print(q, nn.functional.cosine_similarity(video_encoding, queries_mapping[q], dim=0))
