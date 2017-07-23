from .models.connection_string import Connection_String
from .models.sql import SQL as sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Factory:
    NAME = __name__
    CONN = Connection_String()

    @staticmethod
    def create(args: dict) -> sql:
        conn = Factory.CONN
        conn.update(args)

        engine = create_engine(conn.compile(), echo=False)

        Session = sessionmaker(bind=engine)
        session = Session()

        obj = args.get('OBJECT')
        return sql({
            'base': obj.base,
            'engine': engine,
            'session': session,
            'tables': obj.tables()
        })
