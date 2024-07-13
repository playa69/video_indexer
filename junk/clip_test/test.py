import glob
from clip_video_encode import clip_video_encode



url = "https://cdn-st.rutubelist.ru/media/dd/6a/ac2964a94bb4aaba578d61b8fc1d/fhd.mp4"

import urllib.request
import uuid

def download_video(src_url):
    download_path = "tmp/" + str(uuid.uuid4()) + ".mp4"
    urllib.request.urlretrieve(src_url, download_path)
    return download_path


VIDS = [download_video(url)]
EMBEDDING_DIR = "embeds"
take_every_5 = 5


clip_video_encode(
    VIDS,
    EMBEDDING_DIR,
    output_format="files",
    take_every_nth=take_every_5,
    captioning_strategy="center", # generate caption for middle frame
    caption_similarity=True,
)

"""
    Encode frames using CLIP image encoder

    Input:
      src:
        str: path to mp4 file
        str: youtube link
        str: path to txt file with multiple mp4's or youtube links
        list: list with multiple mp4's or youtube links
      dest:
        str: directory where to save embeddings to
        None: dest = src + .npy
      output_format:
        str: "files" or "webdataset"
      take_every_nth:
        int: only take every nth frame
      target_fps:
        int: target fps to downsample videos to (-1 means original fps or take_every_nth)
      frame_workers:
        int: number of Processes to distribute video reading to.
      frame_memory_size:
        int: GB of memory for FrameReader.
      metadata_columns:
        str: a comma separated list of metadata column names to look for in src
      use_dst_name:
        bool: use the save name suggested by video2numpy
      distribute:
        str: distribution strategy, currently either slurm or none
      model_name:
        str:
          - open_clip model name, used for selecting CLIP architecture
          - vqgan config path
      pretrained:
        str:
          - open_clip pretrained weights name
          - vqgan weights checkpoint path
      captioning_strategy:
        str: which frames of a video to generate captions for. Possible values are:
          - none: don't generate any captions
          - center: generate a caption for the middle frame
        int: (NOT IMPLEMENTED) step size for which frames to generate captions for
      pass_through_keys:
        str: comma separated list of extension to pass through from input dataset (if webdataset format)
      caption_similarity:
        bool: whether to put the similarity between the average frame embedding and text embedding into metadata
      img_size:
        int: pixel height and width of target output shape
    """