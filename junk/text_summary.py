import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Загрузка токенизатора и модели
sumamarizer_tokenizer = None
sumamarizer_model = None
def load_summarizer_model():
    '''
    transformers==4.41.2
    sentencepiece==0.2.0
    '''
    global sumamarizer_tokenizer, sumamarizer_model
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    if sumamarizer_tokenizer is None:
      sumamarizer_tokenizer = AutoTokenizer.from_pretrained(model_name)
    if sumamarizer_model is None:
      sumamarizer_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text):
    global sumamarizer_tokenizer, sumamarizer_model
    """
    Суммаризирует входной текст и обрабатывает слова.

    Параметры:
    text (str): Входной текст .

    Возвращает:
    tuple: Пара, содержащая самари (str) и список обработанных слов (list).
    """
    load_summarizer_model() 
    # Функция для обработки пробелов
    WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
    input_ids = sumamarizer_tokenizer(
        [WHITESPACE_HANDLER(text)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )["input_ids"]
    output_ids = sumamarizer_model.generate(
        input_ids=input_ids,
        max_length=100,
        no_repeat_ngram_size=3,
        num_beams=3
    )[0]
    summary = sumamarizer_tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    words = re.findall(r'\b\w+\b', summary)
    # Фильтруем слова длиной меньше 3 и добавляем # в начало каждого слова
    processed_words = ['#' + word for word in words if len(word) >= 3]
    return summary, processed_words

def test():
  text = """
  Маркетинг и менеджмент имеют похожую терминологию, но смысл терминов часто различается. Причиной такого положения дел является то, что маркетинг взаимодействует с внешней средой бизнес-организаций, участники которой независимы и действуют в соответствие со своими интересами и целями. В противоположность этому менеджмент взаимодействует с внутренней средой, все элементы которой являются объектами управления.
  """
  result = summarize_text(text)
  print(result)

if __name__ == '__main__':
  test()

