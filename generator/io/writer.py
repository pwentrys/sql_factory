import os
from pathlib import Path

from utilities.typesext import Types as t
from utilities.dictionary import Dictionary as d
from utilities.pathings import Pathings as pathings
from utilities.transformers import Transformers as xform
from utilities.timeformats import TimeFormats as tform


class Writer:
    @staticmethod
    def _write(text: str, path):
        """
        For debug.
        :param text:
        :param path:
        :return:
        """
        print(f'Writing to {path}.')
        path.write_text(text, encoding='utf-8')

    @staticmethod
    def write(text, dst):
        """
        Write text to destination.
        :param text:
        :param dst:
        :return:
        """
        if isinstance(text, t.ListType):
            text = xform.list2string(text, d.empty)

        assert isinstance(
            text, t.StringType), f'Text type is not string: {text}'

        while text.__contains__('\n\n\n\n'):
            text = text.replace('\n\n\n\n', '\n\n\n')

        path = Path(dst)
        pathings.ensure(path.parent)
        if not str(path).endswith(
                d.cmd) and not str(path).endswith('.sql'):
            text = f'{Writer.get_generated_text(path)}{text}'
        try:
            if path.is_file():
                cur_formatted = Writer.format_text(
                    path.read_text(encoding=d.utf_8))
                new_formatted = Writer.format_text(text)
                if cur_formatted == new_formatted:
                    # print(f'No need to update {path}.')
                    return False
                else:
                    Writer._write(text, path)
                    return True
            else:
                Writer._write(text, path)
                return True
        except Exception as error:
            print(error)

    @staticmethod
    def format_text(text: str) -> str:
        """
        Auto gen text.
        :param text:
        :return:
        """
        if text.__contains__('  {:-^30}\n'.format(' Auto - End ')):
            text_split = text.split('  {:-^30}\n'.format(' Auto - End '))
            text = text_split[len(text_split) - 1]

        return text

    @staticmethod
    def get_generated_text(path) -> str:
        """
        Returns text from path.
        :param path:
        :return:
        """
        assert not isinstance(path, t.StringType), f'Path was string: {path}'
        count = 1
        if path.is_file():
            text = path.read_text(encoding=d.utf_8)
            if text.__contains__('  COUNT: '):
                idx = text.find('  COUNT: ') + len('  COUNT: ')
                count = int(text[idx:idx + 20].replace('-',
                                                       '').replace('#', '').strip()) + 1

        out = [
            '  {:-^30}'.format(' Auto - Begin '),
            '    PC:{:^25}'.format(
                str(os.environ.get("COMPUTERNAME", "ANONYMOUS"))),
            '    BY:{:^25}'.format(
                str(os.environ.get("USERNAME", "ANONYMOUS"))),
            '    ON:{:^25}'.format(str(tform.now2f())),
            '    COUNT:{:^20}'.format(str(count)),
            '  {:-^30}'.format(' Auto - End ')]

        outs = []
        if str(path).endswith(f'.{d.md}'):
            for line in out:
                outs.append(f'{line.rstrip()}\n')
        else:
            for line in out:
                outs.append(f'#{line.rstrip()}\n')

        return f"{''.join(outs)}\n\n"
