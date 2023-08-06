import abc

from collections import namedtuple


class Tokenizer(abc.ABC):
    @abc.abstractmethod
    def wakati(self, sent) -> list[str]:
        pass

    @abc.abstractmethod
    def wakati_baseform(self, sent) -> list[str]:
        pass

    @abc.abstractmethod
    def tokenize(self, text) -> namedtuple:
        pass

    @abc.abstractmethod
    def filter_by_pos(self, sent, pos=('名詞',)) -> list[namedtuple]:
        pass
