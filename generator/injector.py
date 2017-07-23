from utilities.dictionary import Dictionary as d
from .io.writer import Writer as writer


class Injector:
    TYPE_DICT = {
        'string': 'STRING',
        'datetime': 'TIMESTAMP',
        'timestamp': 'TIMESTAMP',
        'int': 'Integer',
        'varchar': 'VARCHAR',
        'longtext': 'Text',
        'float': 'Float',
        'date': 'Date',
    }

    @staticmethod
    def _format_class_name(title: str) -> str:
        """
        Cleans up class name.
        :param title:
        :return:
        """
        if title.endswith('es'):
            title = title[:-2]
        elif title.endswith('s'):
            title = title[:-1]
        return f'{title[0].upper()}{title[1:].lower()}'

    @staticmethod
    def _get_class_name(title: str) -> str:
        """
        Return tabbed class name.
        :param title:
        :return:
        """
        return f'{d.space_tab}class {Injector._format_class_name(title)}(Base):\n'

    @staticmethod
    def _get_table_name(title: str) -> str:
        """
        Return tabbed table name.
        :param title:
        :return:
        """
        return f"{d.space_tab}{d.space_tab}__tablename__ = '{title.lower().strip()}'\n\n"

    @staticmethod
    def _determine_type(string: str) -> str:
        """
        Get type from dict.
        :param string:
        :return:
        """
        string = string.lower().strip()
        return Injector.TYPE_DICT.get(string, string)

    @staticmethod
    def _get_column(column: dict)-> str:
        """
        Returns column name.
        :param column:
        :return:
        """
        text = [f'{d.space_tab}{d.space_tab}{column["name"]} = Column(\n']
        datatype = column["type"]
        if datatype.__contains__('length') and Injector._determine_type(
                datatype["type"]) != 'Integer':
            text.append(
                f'{d.space_tab}{d.space_tab}{d.space_tab}{Injector._determine_type(datatype["type"])}({datatype["length"]}),\n')
        else:
            text.append(
                f'{d.space_tab}{d.space_tab}{d.space_tab}{Injector._determine_type(datatype["type"])},\n')

        flags = column["flags"]
        if len(flags) > 0:
            for key in flags:
                v = flags.get(key)
                text.append(
                    f'{d.space_tab}{d.space_tab}{d.space_tab}{key}={v},\n')
            text[len(text) - 1] = text[len(text) - 1][:-2]

        return f"{''.join(text)}\n{d.space_tab}{d.space_tab})\n"

    @staticmethod
    def _get_columns(columns: list) -> str:
        """
        Returns column header.
        :param columns:
        :return:
        """
        out = []
        for column in columns:
            out.append(Injector._get_column(column))
        return ''.join(out)

    @staticmethod
    def _get_repr(name: str) -> str:
        """
        Return repr.
        :param name:
        :return:
        """
        return f'f"{name}=' + "{" + f'self.{name}' + "}" + f'," \\\n'

    @staticmethod
    def _get_reprs(columns: list) -> str:
        """
        Return reprs.
        :param columns:
        :return:
        """
        out = []
        for column in columns:
            out.append(
                f'{d.space_tab}{d.space_tab}{d.space_tab}{d.space_tab}   {Injector._get_repr(column["name"])}')

        return ''.join(out)[:-5] + '" \\'

    @staticmethod
    def extractor2file(extraction, path):
        """
        Extract out to file.
        :param extraction:
        :param path:
        :return:
        """
        writer.write(''.join([
            f'from sqlalchemy import MetaData, Float, Date, Table, Column, Integer, String, DateTime, ForeignKey, TIMESTAMP, text, VARCHAR, Text\n',
            # f'from sqlalchemy.ext.declarative import declarative_base\n\n\n',
            # f'Base = declarative_base()\n\n\n',
            f'\n',
            f'\n',
            f'def {extraction.title.lower()}(Base):\n',
            Injector._get_class_name(extraction.title),
            Injector._get_table_name(extraction.title),
            Injector._get_columns(extraction.columns),
            f'\n{d.space_tab}{d.space_tab}def __repr__(self):\n'
            f'{d.space_tab}{d.space_tab}{d.space_tab}return f"<{Injector._format_class_name(extraction.title)}(" \\\n'
            f'{Injector._get_reprs(extraction.columns)}\n'
            f'{d.space_tab}{d.space_tab}{d.space_tab}{d.space_tab}   f")>"\n'
            f'\n'
            f'{d.space_tab}return {Injector._format_class_name(extraction.title)}\n'
        ]), path)
