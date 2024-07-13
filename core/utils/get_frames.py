from moviepy.editor import *
from PIL import Image

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
