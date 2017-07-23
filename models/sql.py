class SQL:
    def __init__(self, args: dict):
        self.base = args.get('base')
        self.engine = args.get('engine')
        self.session = args.get('session')
        self.tables = args.get('tables')

        self._create_all()

    def _create_all(self):
        """
        Create all tables by way of metadata.
        :return:
        """
        self.base.metadata.create_all(self.engine)
