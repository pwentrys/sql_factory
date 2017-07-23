from utilities.dictionary import Dictionary as d
from utilities.pathings import Pathings as p
from utilities.typesext import Types as t

import pathlib
import re
from .models.replace_flag import Replace_Flag as rf


class ExtractorObject:
    def __init__(self, title: str, columns: list):
        self.title = title
        self.columns = columns


class Extractor:
    Replace_Flags = [
        rf(
            'UNSIGNED', flag={
                'unsigned': True}), rf(
            'AUTO_INCREMENT', flag={
                'nullable': False, 'autoincrement': True, 'primary_key': True}), rf(
            'NOT NULL DEFAULT', flag={
                'nullable': False, 'server_default': "text('CURRENT_TIMESTAMP')"}), rf(
            'NOT NULL', flag={
                'nullable': False}), rf(
            'DEFAULT NULL', flag={
                'nullable': True, 'default': "text('NULL')"}), rf(
            'ON UPDATE', flag={
                'server_onupdate': "text('CURRENT_TIMESTAMP')"}), ]

    @staticmethod
    def _extract_table_name(line: str) -> str:
        """
        Get table name.
        :param line:
        :return:
        """
        _re = re.compile("CREATE TABLE `(.*?)` \(")
        return _re.match(line).groups()[0]

    @staticmethod
    def _extract_engine(line: str) -> str:
        """
        Get engine name.
        :param line:
        :return:
        """
        _re = re.compile("ENGINE=(.*?) ")
        return _re.match(line).groups()[0]

    @staticmethod
    def _extract_charset(line: str) -> str:
        """
        Get charset type.
        :param line:
        :return:
        """
        _re = re.compile("DEFAULT CHARSET=(.*?) ")
        return _re.match(line).groups()[0]

    @staticmethod
    def _extract_column_name(line: str) -> str:
        """
        Get column name.
        :param line:
        :return:
        """
        _re = re.compile("`(.*?)` ")
        return _re.match(line).groups()[0]

    @staticmethod
    def _extract_column_type(line: str) -> dict:
        """
        Extract column by typed regex.
        :param line:
        :return:
        """
        _re = re.compile("(.*?) ")
        res = _re.match(line).groups()[0].strip()
        if res.__contains__('('):
            res_split = res.split('(')
            _type = res_split[0].strip()
            _length = res_split[1][:-1]
            return {'type': _type, 'length': _length}
        else:
            return {'type': res.strip()}

    @staticmethod
    def _extract_replace(line: str, target: str, destination=d.empty) -> str:
        """
        Extract and clean replace.
        :param line:
        :param target:
        :param destination:
        :return:
        """
        return line.replace(target, destination).strip()

    @staticmethod
    def _extract_flags(line: str, replace_flags: list) -> dict:
        """
        Extract flags from line and return as dict obj.
        :param line:
        :param replace_flags:
        :return:
        """
        flags = {}
        for replace_flag in replace_flags:
            target = replace_flag.target
            destination = replace_flag.destination
            if line.__contains__(target):
                line = Extractor._extract_replace(line, target, destination)
                flags.update(replace_flag.flag)
        return flags

    @staticmethod
    def _extract_column(line: str) -> dict:
        """
        Extract column name from string line.
        :param line:
        :return:
        """
        name = Extractor._extract_column_name(line).strip()
        line = line[len(name) + 3:]
        datatype = Extractor._extract_column_type(line)
        line = line[len(datatype) + 3:]
        flags = Extractor._extract_flags(line, Extractor.Replace_Flags)
        return {'name': name, 'type': datatype, 'flags': flags}

    @staticmethod
    def _extract_columns(lines: list) -> list:
        """
        Extract each line from lines
        :param lines:
        :return:
        """
        return [Extractor._extract_column(line) for line in lines]

    @staticmethod
    def _extract_sections(text: str) -> ExtractorObject:
        """
        Extract specific section.
        :param text:
        :return:
        """
        lines = text.splitlines()
        title = Extractor._extract_table_name(lines[0].strip())
        lines = lines[1:-1]
        columns = []
        keys = []

        for line in lines:
            line = str(line).strip()
            if line.startswith('`'):
                columns.append(line)
            else:
                keys.append(line)

        columns = Extractor._extract_columns(columns)
        return ExtractorObject(title, columns)

    @staticmethod
    def sql2file(text: str, path) -> ExtractorObject:
        """
        Write sql text to file.
        :param text:
        :param path:
        :return:
        """
        if isinstance(path, t.StringType):
            path = pathlib.Path(path)

        p.ensure(path.parent)
        return Extractor._extract_sections(text)
