from loguru import logger
from typing import Optional

from sqlalchemy import select, create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url: str):
        self.__db_url: Optional[str] = db_url
        self.engine: Optional[Engine] = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def create_tables(self, base):
        if not self._check_tables_exist(base):
            base.metadata.create_all(self.engine)
        else:
            logger.info("Tables already created")

    def _check_tables_exist(self, base):
        inspector = Inspector.from_engine(self.engine)
        existing_tables = inspector.get_table_names()
        declared_tables = {table.name for table in base.metadata.sorted_tables}

        return declared_tables.issubset(set(existing_tables))
    
    def connect(self):
        self.engine = create_engine(url=self.__db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        try:
            self.sql_query(query=select(1))
            logger.info("Database connected")
        except Exception as e:
            logger.error(f"Database didn't connect, error {e}")

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            logger.info("Database has disconnected")

    def create_object(self, model_class, **attributes):
        obj = model_class(**attributes)
        self.session.add(obj)
        self.session.commit()
        return obj

    def sql_query(self, query, single: bool = True, is_update: bool = False):
        result = self.session.execute(query)
        if not is_update:
            return result.scalars().first() if single else result.scalars().all()
        self.session.commit()
