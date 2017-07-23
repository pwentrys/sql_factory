from pathlib import Path

from utilities.dictionary import Dictionary as d
from utilities.typesext import Types as t


class Reader:
    @staticmethod
    def read(path):
        text = d.empty
        if isinstance(path, t.StringType):
            path = Path(path)

        if not path.is_file():
            return text

        try:
            text = path.read_text(encoding=d.utf_8)
        except Exception as error:
            print(error)
            text = d.empty
        finally:
            return text
