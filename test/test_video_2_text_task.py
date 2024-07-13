from core import prompt_encoder
from tasks import video_2_text

import tasks
from tasks import sleep
from tasks import video_2_text
import core
import storage


print(prompt_encoder.encode("test"))
print(video_2_text.video_2_text_impl("https://cdn-st.rutubelist.ru/media/dd/6a/ac2964a94bb4aaba578d61b8fc1d/fhd.mp4"))
