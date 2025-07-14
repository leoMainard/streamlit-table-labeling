from sqlalchemy import inspect 
from sqlmodel import create_engine, Session, SQLModel, select

from streamlit_table_labeling.utils.config import Environnement
from streamlit_table_labeling.utils.config import logger
from streamlit_table_labeling.db.schemas import Table

class TableLabelingDatabase:
    def __init__(self):
        self.db_url = self._create_url()
        self.engine = create_engine(self.db_url)

    def _create_url(self):
        return f"postgresql+psycopg2://{Environnement.config('DB_USER')}:" \
               f"{Environnement.config('DB_PASSWORD')}@{Environnement.config('DB_HOSTNAME')}:" \
               f"{Environnement.config('DB_PORT')}/{Environnement.config('DB_NAME')}"
        
    def check_tables(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        if not tables:
            raise ValueError(f"No tables found in the database. Please check your connection and database setup. Your database url is: {self.db_url}")
        else:
            logger.info(f"Found tables: {tables}")

    
    def connect(self):
        return self.engine.connect()

    def close(self):
        self.engine.dispose()

    def get_engine(self):
        return self.engine
    
    def get_random_table_to_labelise(self):
        """Fetch a random table that is not labeled yet."""

        with self.connect() as connection:
            statement = select(Table).where(Table.done == False).order_by(Table.id)
            result = connection.execute(statement)
            row = result.fetchone()
            if row:
                logger.info(f"Selected table for labeling: {row}")
                return row
            else:
                logger.warning("No tables available to label.")
                return None

if __name__ == "__main__":
    db = TableLabelingDatabase()
    engine = db.get_engine()
    SQLModel.metadata.create_all(engine)

    db.check_tables()

    with Session(engine) as session:
        # Create a new table labeling entry
        table_1 = Table(labels=None, table=[["Row 1", "Data 1"], ["Row 2", "Data 2"]])
        table_2 = Table(labels=None, table=[["Row 3", "Data 3"], ["Row 4", "Data 4"]])
        table_3 = Table(labels=None, table=[["Row 5", "Data 5"], ["Row 6", "Data 6"]])

        session.add(table_1)
        session.add(table_2)
        session.add(table_3)

        session.commit()

        # Query the table labeling entries
        entries = session.exec(select(Table)).all()
        for entry in entries:
            print(entry)