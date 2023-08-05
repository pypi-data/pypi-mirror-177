from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

from tokenizers import (AddedToken, NormalizedString, PreTokenizedString,
                        Tokenizer)
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import PreTokenizer, Whitespace
from tokenizers.trainers import WordLevelTrainer

from datasetstation.error import DatasetstoreFunctionNotFoundError
from datasetstation.preprocess.text.tokenizer.pretokenizer import (
    CharacterPreTokenizer, HanLPreTokenizer, JiebaPreTokenizer)
from datasetstation.type import FileListType


class CustomTokenizer(object):

    def __init__(
        self,
        vocab: Optional[Union[str, Dict[str, int]]] = None,
        unk_token: Union[str, AddedToken] = "[UNK]",
        pre_tokenizer = None
    ):
        self.special_tokens = []
        self.special_tokens.append(unk_token)
        if vocab is not None:
            self.tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token=str(unk_token)))
        else:
            self.tokenizer = Tokenizer(WordLevel(unk_token=str(unk_token)))  # type: ignore

        if pre_tokenizer is not None:
            self.tokenizer.pre_tokenizer = PreTokenizer.custom(pre_tokenizer)  # type: ignore
        # self.tokenizer.pre_tokenizer = Whitespace()  # type: ignore
        self.trainer = WordLevelTrainer(special_tokens=self.special_tokens)  # type: ignore

    def train(self, texts: Optional[Union[FileListType, Iterable]]):
        """对文件、文本列表进行训练
        文本应该是正常的、连续的中文，无需做任何处理
        """
        if isinstance(texts, FileListType):
            return self.tokenizer.train(texts.files, self.trainer)
        elif isinstance(texts, str):
            return self.tokenizer.train_from_iterator([texts], self.trainer)
        else:
            return self.tokenizer.train_from_iterator(texts, self.trainer)

    def __call__(
        self, texts: Optional[Union[str, List]]
    ) -> Optional[Union[str, List[str]]]:
        """对单文本或文本列表进行分词处理"""
        if isinstance(texts, str):
            return self.encode(texts)
        elif isinstance(texts, list):
            return [x.ids for x in self.tokenizer.encode_batch(texts)]

    def __getattr__(self, name):
        if getattr(self.tokenizer, name):
            return getattr(self.tokenizer, name)
        else:
            raise DatasetstoreFunctionNotFoundError("当前 tokenizer 不支持此方法")


class CharacterTokenizer(CustomTokenizer):
    """中文单字分词器"""

    def __init__(self, vocab: Optional[Union[str, Dict[str, int]]] = None,
        unk_token: Union[str, AddedToken] = "[UNK]"):
        super(CharacterTokenizer, self).__init__(vocab, unk_token, CharacterPreTokenizer())


class JiebaTokenizer(CustomTokenizer):
    """jieba 中文分词器"""

    def __init__(self, vocab: Optional[Union[str, Dict[str, int]]] = None,
        unk_token: Union[str, AddedToken] = "[UNK]"):
        super(JiebaTokenizer, self).__init__(vocab, unk_token, JiebaPreTokenizer())


class HanLPTokenizer(CustomTokenizer):
    """hanlp 中文分词器"""

    def __init__(self, vocab: Optional[Union[str, Dict[str, int]]] = None, 
        unk_token: Union[str, AddedToken] = "[UNK]"):
        super(HanLPTokenizer, self).__init__(vocab, unk_token, HanLPreTokenizer())
