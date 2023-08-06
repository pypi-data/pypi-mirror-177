from .tokenizers import select_tokenizer


class RoBERTaTokenizer:
    @staticmethod
    def from_pretrained(version="ja_20190121_m10000_v24000"):
        return select_tokenizer(version)
