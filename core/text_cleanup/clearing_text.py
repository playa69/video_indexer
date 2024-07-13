import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
import numpy as np
import os
from collections import Counter
import json

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Текстовые функции предобработки
def convert_lowercase(text):
    return text.lower()

def remove_url(text):
    re_url = re.compile(r'https?://\S+|www\.\S+')
    return re_url.sub('', text)

exclude = string.punctuation
def remove_punc(text):
    return text.translate(str.maketrans('', '', exclude))

def remove_stopwords(text):
    stopwrds = stopwords.words('russian')
    words = word_tokenize(text,language = "russian")
    filtered_words = [word for word in words if word not in stopwrds]
    return ' '.join(filtered_words)

def perform_lemmatize(text):
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lem.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

def preprocess_text(text):
    text = convert_lowercase(text)
    text = remove_url(text)
    text = remove_punc(text)
    text = remove_stopwords(text)
    text = perform_lemmatize(text)
    return text

def extract_important_words_using_embeddings(texts, model_name='paraphrase-multilingual-MiniLM-L12-v2', top_n=10):
    model = SentenceTransformer(model_name)
    important_words = []
    
    for text in texts:
        preprocessed_text = preprocess_text(text)
        words = word_tokenize(preprocessed_text)
        
        if len(words) == 0:
            important_words.append([])  
            continue
        
        word_embeddings = model.encode(words, convert_to_tensor=True)
        text_embedding = model.encode([preprocessed_text], convert_to_tensor=True)
        
        similarities = util.pytorch_cos_sim(text_embedding, word_embeddings)[0]
        
        sorted_indices = np.argsort(-similarities.cpu().numpy())
        
        top_words = [words[idx] for idx in sorted_indices[:top_n]]
        important_words.append(top_words)
    
    return important_words

def process_text_files_in_directory(directory, top_n=20):
    texts = []
    filenames = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
                filenames.append(filename)
    
    all_texts_combined = ' '.join(texts)
    preprocessed_combined_text = preprocess_text(all_texts_combined)
    all_words = word_tokenize(preprocessed_combined_text)
    
    word_counts = Counter(all_words)
    max_freq = max(word_counts.values(), default=1)
    normalized_frequencies = {word: freq / max_freq for word, freq in word_counts.items()}
    
    important_words = extract_important_words_using_embeddings(texts, top_n=top_n)
    
    important_words_data = {}
    
    for idx, words in enumerate(important_words):
        file_key = f"{filenames[idx]}"
        important_words_data[file_key] = []
        for word in set(words):
            important_words_data[file_key].append({
                "word": word,
                "count": word_counts[word],
                "normalized_frequency": normalized_frequencies[word]
            })
    
    # Запись данных в JSON файл
    with open('important_words.json', 'w', encoding='utf-8') as json_file:
        json.dump(important_words_data, json_file, ensure_ascii=False, indent=4)

# Пример использования
directory = 'C:/users/bodya/Desktop/rag_/RAG_LLAMMA/txt_data'
process_text_files_in_directory(directory, top_n=20)
