from .extractor import Extractor as extractor
from .injector import Injector as injector


class SQL2Alchemy:
    @staticmethod
    def sql2file(text: str, path):
        extraction = extractor.sql2file(text, path)
        injector.extractor2file(extraction, path)
