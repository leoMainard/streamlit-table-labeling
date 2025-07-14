from sqlalchemy import inspect 
from sqlmodel import create_engine, Session, SQLModel, select

from streamlit_table_labeling.utils.config import Environnement
from streamlit_table_labeling.utils.config import logger
from streamlit_table_labeling.db.schemas import TableLabeling

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
            logger.info(f"Check tables in database. Found tables: {tables}")
            logger.info(f"Connection successful to the database: {self.db_url}")

    
    def connect(self):
        return self.engine.connect()

    def close(self):
        self.engine.dispose()

    def get_engine(self):
        return self.engine
    
    def get_random_table_to_labelise(self):
        """Fetch a random table that is not labeled yet."""

        with self.connect() as connection:
            statement = select(TableLabeling).where(TableLabeling.done == False).order_by(TableLabeling.id)
            result = connection.execute(statement)
            row = result.fetchone()
            if row:
                logger.info(f"Selected table for labeling: {row.id}")
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
        # 1 - Véhicules
        vehicles_table = TableLabeling(
            labels=None,
            table=[
                ["Immatriculation", "Marque", "Modèle", "Année"],
                ["AB-123-CD", "Peugeot", "208", "2019"],
                ["XY-456-ZW", "Renault", "Clio", "2020"]
            ]
        )

        # 2 - Véhicules
        vehicles_table_2 = TableLabeling(
            labels=None,
            table=[
                ["Immatriculation", "Marque", "Modèle", "Année"],
                ["JK-789-LM", "Citroën", "C3", "2018"],
                ["GH-321-OP", "Toyota", "Yaris", "2021"]
            ]
        )

        # 3 - Bâtiments
        buildings_table = TableLabeling(
            labels=None,
            table=[
                ["Adresse", "Ville", "Surface m2"],
                ["12 rue de Paris", "Lyon", "120"],
                ["45 avenue Victor Hugo", "Marseille", "300"]
            ]
        )

        # 4 - Bâtiments
        buildings_table_2 = TableLabeling(
            labels=None,
            table=[
                ["Adresse", "Ville", "Surface m2"],
                ["78 boulevard Saint-Michel", "Paris", "200"],
                ["5 chemin des Lilas", "Toulouse", "150"]
            ]
        )

        # 5 - Sinistres
        claims_table = TableLabeling(
            labels=None,
            table=[
                ["Référence", "Date", "Type", "Montant €"],
                ["S001", "2023-01-15", "Incendie", "5000"],
                ["S002", "2023-03-02", "Dégât des eaux", "2000"]
            ]
        )

        # 6 - Sinistres
        claims_table_2 = TableLabeling(
            labels=None,
            table=[
                ["Référence", "Date", "Type", "Montant €"],
                ["S003", "2023-06-20", "Vol", "3500"],
                ["S004", "2023-08-10", "Tempête", "4000"]
            ]
        )

        # 7 - Produits alimentaires
        food_table = TableLabeling(
            labels=None,
            table=[
                ["Produit", "Catégorie", "Prix €"],
                ["Pomme", "Fruits", "1.2"],
                ["Carotte", "Légumes", "0.9"]
            ]
        )

        # 8 - Employés
        employees_table = TableLabeling(
            labels=None,
            table=[
                ["Nom", "Poste", "Salaire €"],
                ["Martin", "Développeur", "3500"],
                ["Durand", "Designer", "3200"]
            ]
        )

        # 9 - Animaux
        animals_table = TableLabeling(
            labels=None,
            table=[
                ["Espèce", "Nom", "Âge"],
                ["Chat", "Mimi", "3"],
                ["Chien", "Rex", "5"]
            ]
        )

        # 10 - Inventaire
        inventory_table = TableLabeling(
            labels=None,
            table=[
                ["Article", "Quantité", "Prix unitaire €"],
                ["Stylo", "100", "0.5"],
                ["Cahier", "200", "1.2"]
            ]
        )

        # Ajout de toutes les entrées
        session.add_all([
            vehicles_table,
            vehicles_table_2,
            buildings_table,
            buildings_table_2,
            claims_table,
            claims_table_2,
            food_table,
            employees_table,
            animals_table,
            inventory_table
        ])

        session.commit()

        entries = session.exec(select(TableLabeling)).all()
        for entry in entries:
            print(entry)