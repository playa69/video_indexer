FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -U openai-whisper
RUN pip install eventlet
RUN pip install cython
RUN pip install ruclip==0.0.2
RUN pip install moviepy
RUN pip install huggingface-hub==0.2.1
RUN pip install transformers==4.41.2
RUN pip install python-redis-lock==4.0.0
RUN pip install tantivy==0.20.1
RUN pip install sentencepiece==0.2.0

RUN mkdir tmp

COPY app.py .
COPY backend.py .
COPY test ./test
COPY setup.py .
COPY models_loader.py .
COPY tasks ./tasks
COPY conf ./conf
COPY core ./core
COPY storage ./storage

RUN python3 setup.py
RUN python3 models_loader.py

RUN pip install protobuf==5.27.1

COPY search_template.html .
