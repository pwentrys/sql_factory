class Types:
    BoolType = type(True)
    DictType = type({})
    IntType = type(0)
    ListType = type([])
    NoneType = type(None)
    StringType = type('')

    def add_type(self, key: str, c: type):
        if not Types.__dict__.__contains__(key):
            Types.__setattr__(key, c)

    @staticmethod
    def from_key(key: str) -> type:
        assert key.endswith('Type'), f'{key} doesn\'t end with Type.'
        return Types._from_key(key)

    @staticmethod
    def _from_key(key: str) -> type:
        return Types.__getattribute__(key)

    def __dolog__(self) -> str:
        out = self.__dict__.copy()
        out.update(Types.__dict__)
        return ''.join(
            [f'{key}: {out.get(key)}\n' for key in out
             if key.endswith('Type')])


Types = Types()
