import codecs

from subword_nmt.apply_bpe import BPE
from janome.tokenizer import Tokenizer as JanomeTokenizer
from nltk.tokenize import wordpunct_tokenize

from ..utils.data import load_json


class BaseTokenizer(object):
    def __init__(self, codes_path, vocab_path):
        codes = codecs.open(codes_path, encoding="utf-8")
        self.bpe = BPE(codes)

        self.vocab = load_json(vocab_path)

        self.cls_token = "<s>"
        self.pad_token = "<pad>"
        self.sep_token = "</s>"
        self.unk_token = "<unk>"

    @property
    def cls_token_id(self):
        return self.vocab[self.cls_token]

    @property
    def pad_token_id(self):
        return self.vocab[self.pad_token]

    @property
    def sep_token_id(self):
        return self.vocab[self.sep_token]

    @property
    def unk_token_id(self):
        return self.vocab[self.unk_token]

    def tokenize(self, text):
        raise NotImplementedError()

    def convert_token_to_id(self, token):
        return self.vocab.get(token, self.unk_token_id)

    def convert_tokens_to_ids(self, tokens):
        token_ids = [self.convert_token_to_id(token) for token in tokens]
        return token_ids


class MeCabBPE(BaseTokenizer):
    def __init__(self, codes_path, vocab_path):
        super().__init__(codes_path, vocab_path)
        self.janome = JanomeTokenizer(wakati=True)

    def tokenize(self, text):
        tokens = list(self.janome.tokenize(text))
        tokens = self.bpe.process_line(" ".join(tokens))
        return tokens.split()


class NLTKBPE(BaseTokenizer):
    def tokenize(self, text):
        tokens = wordpunct_tokenize(text)
        tokens = self.bpe.process_line(" ".join(tokens))
        return tokens.split()
