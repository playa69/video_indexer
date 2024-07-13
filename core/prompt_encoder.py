import torch
import logging
import logging

from transformers import AutoTokenizer, AutoModel
from numpy import dot
from numpy.linalg import norm

embedding_model = "sergeyzh/rubert-mini-sts"

tokenizer = AutoTokenizer.from_pretrained(embedding_model)
model = AutoModel.from_pretrained(embedding_model)

# Функция для получения векторного представления текста
def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()

## Лучше не менять!
def cosine_similarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))


def encode(prompt):
    try:
        vector = embed_bert_cls(prompt, model, tokenizer)
        return vector  # получаем numpy.ndarray
    except Exception as e:
        logging.exception(f"prompt_encoder.py: Error processing prompt '{prompt}': {e}")
        raise


if __name__ == "__main__":
    prompt = input()
    result = _encode(prompt)
    print(f"Vector: {result}")
