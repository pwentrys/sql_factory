from utilities.typesext import Types as t


class Replace_Flag:
    def __init__(self, target: str, destination='', flag=None):
        assert isinstance(destination, t.StringType), f'Type is not string: {destination}'
        if isinstance(flag, t.NoneType):
            flag = {self.target: True}
        assert isinstance(flag, t.DictType), f'Flag type is not dict: {flag}'

        self.target = target
        self.destination = destination
        self.flag = flag
