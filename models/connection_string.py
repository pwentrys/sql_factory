from config.configuration import USERNAME, PASSWORD, ADDRESS, PORT, PROTOCOL, SCHEMA, OPTIONS
from base64 import decodebytes


class Connection_String:
    PROTOCOL = PROTOCOL
    USERNAME = USERNAME
    PASSWORD = PASSWORD
    ADDRESS = ADDRESS
    PORT = PORT
    SCHEMA = SCHEMA
    OPTIONS = OPTIONS

    def __init__(self, args=None):
        if args is not None:
            Connection_String._parse(self, args)

    @staticmethod
    def _parse(cs, args: dict):
        """
        Lazy arg to attribute parser.
        :param cs:
        :param args:
        :return:
        """
        for key in args.keys():
            cs.__setattr__(key, args.get(key))

    def update(self, args=None):
        """
        Update obj using args dict.
        :param args:
        :return:
        """
        if args is None:
            args = {}

        self._update(args)

    def _update(self, args: dict):
        """
        Update each attribute using arg || default fallback.
        :param args:
        :return:
        """
        self.PROTOCOL = args.get('PROTOCOL', Connection_String.PROTOCOL)
        self.USERNAME = args.get('USERNAME', Connection_String.USERNAME)
        self.PASSWORD = args.get('PASSWORD', Connection_String.PASSWORD)
        self.ADDRESS = args.get('ADDRESS', Connection_String.ADDRESS)
        self.PORT = args.get('PORT', Connection_String.PORT)
        self.SCHEMA = args.get('SCHEMA', Connection_String.SCHEMA)
        self.OPTIONS = args.get('OPTIONS', Connection_String.OPTIONS)

    def compile(self):
        """
        Returns compiled connection string.
        :return:
        """
        return f'{self.PROTOCOL}://' \
               f'{self.USERNAME}:' \
               f'{decodebytes(self.PASSWORD).decode("utf-8")}@' \
               f'{self.ADDRESS}:' \
               f'{self.PORT}' \
               f'/{self.SCHEMA}' \
               f'?{self.OPTIONS}'
