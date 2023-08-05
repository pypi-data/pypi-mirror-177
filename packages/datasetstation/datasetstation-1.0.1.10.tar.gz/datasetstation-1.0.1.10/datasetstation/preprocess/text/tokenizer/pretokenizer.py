from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import jieba
from pyhanlp import HanLP, JClass
from tokenizers import (AddedToken, NormalizedString, PreTokenizedString,
                        Tokenizer)
from tokenizers.pre_tokenizers import PreTokenizer, Whitespace


class CharacterPreTokenizer:
    def unicode_split(
        self, i: int, normalized_string: NormalizedString
    ) -> List[NormalizedString]:
        return [normalized_string[idx : idx + 1] for idx, _ in enumerate(str(normalized_string))]  # type: ignore

    def pre_tokenize(self, pretok: PreTokenizedString):
        pretok.split(self.unicode_split)

    def decode(self, tokens):
        return "".join(tokens)


class JiebaPreTokenizer:
    def jieba_split(self, i: int, normalized_string: NormalizedString) -> List[NormalizedString]:
        splits = []
        # we need to call `str(normalized_string)` because jieba expects a str,
        # not a NormalizedString
        for token, start, stop in jieba.tokenize(str(normalized_string)):
            splits.append(normalized_string[start:stop]) # type: ignore

        return splits
        # We can also easily do it in one line:
        # return [normalized_string[w[1] : w[2]] for w in jieba.tokenize(str(normalized_string))]

    def odd_number_split(
        self, i: int, normalized_string: NormalizedString
    ) -> List[NormalizedString]:
        # Just an odd example...
        splits = []
        last = 0
        for (i, char) in enumerate(str(normalized_string)):
            if char.isnumeric() and int(char) % 2 == 1:
                splits.append(normalized_string[last:i]) # type: ignore
                last = i
        # Don't forget the last one
        splits.append(normalized_string[last:]) # type: ignore
        return splits

    def pre_tokenize(self, pretok: PreTokenizedString):
        # Let's call split on the PreTokenizedString to split using `self.jieba_split`
        pretok.split(self.jieba_split)
        # Here we can call `pretok.split` multiple times if we want to apply
        # different algorithm, but we generally just need to call it once.
        pretok.split(self.odd_number_split)


class HanLPreTokenizer:
    Term =JClass("com.hankcs.hanlp.seg.common.Term")
    IndexTokenizer = JClass("com.hankcs.hanlp.tokenizer.IndexTokenizer")
    # IndexTokenizer.SEGMENT.enableIndexMode(JInt(1))  # type: ignore

    def hanlp_split(self, i: int, normalized_string: NormalizedString):
        splits = []
        for term in HanLPreTokenizer.IndexTokenizer.segment(str(normalized_string)):  # type: ignore
            splits.append(normalized_string[term.offset, len(term.word)+term.offset]) # type: ignore
        return splits

    def pre_tokenize(self, pretok: PreTokenizedString):
        pretok.split(self.hanlp_split)




