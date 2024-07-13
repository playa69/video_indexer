import ruclip
from torch.nn import functional as F
from core.utils.get_frames import get_frames

clip = None
processor = None
predictor = None


def load_clip():
    global clip, processor, predictor
    if not clip:
        device = 'cpu'
        ruclip.MODELS['ai-forever/ruclip-vit-base-patch16-384'] = dict(
            repo_id='ai-forever/ruclip-vit-base-patch16-384',
            filenames=[
                'bpe.model', 'config.json', 'pytorch_model.bin'
            ]
        ) # hack to get newest weights
        clip, processor = ruclip.load('ai-forever/ruclip-vit-base-patch16-384', device=device)
        predictor = ruclip.Predictor(clip, processor, device, bs=8)


def encode_video(path, description):
    availiable_symbols = "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю "
    description = ''.join([c for c in description.lower() if c in availiable_symbols])
    description = description.strip()

    global predictor, processor
    load_clip()

    frames = get_frames(path)
    text_features = predictor.get_text_latents([description])
    image_features = predictor.get_image_latents(frames)

    result_vector = None
    cum_similarity = -10**6
    for tensor in image_features:
        _cum_similarity = sum([F.cosine_similarity(tensor, _t, dim=0) for _t in image_features])
        if _cum_similarity > cum_similarity:
            result_vector = tensor
            _cum_similarity = _cum_similarity
    return result_vector, text_features[0]


def embed_text(text):
  return predictor.get_text_latents([text])[0].tolist()
