import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.collection import Collector
from cellcommdb.config import TestConfig
from cellcommdb.extensions import db
from cellcommdb.models import Complex, Protein, Multidata, Interaction, ComplexComposition, Gene


class DatabaseNumberOfEntries(TestCase):
    def test_protein(self):
        query = db.session.query(Protein.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        assert len(dataframe) == 4150

    def test_gene(self):
        query = db.session.query(Gene.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        assert len(dataframe) == 5511

    def test_complex(self):
        query = db.session.query(Complex.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        assert len(dataframe) == 236

    def test_multidata(self):
        query = db.session.query(Multidata.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        assert len(dataframe) == 4386

    def test_interaction(self):
        query = db.session.query(Interaction.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe[dataframe['source'] == 'curated']), 82,
                         'Number of curated interactions not equal')
        self.assertEqual(len(dataframe), 42257, 'Number of interactions not equal')

    def test_complex_composition(self):
        query = db.session.query(ComplexComposition.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        assert len(dataframe) == 497

    def create_app(self):
        return create_app(TestConfig)

    def _populate_db(self):
        with self.app.app_context():
            collector = Collector(self.app)
            collector.all()

    def setUp(self):
        # self._clear_db()
        # db.create_all()
        # self._populate_db()

        self.client = self.app.test_client()

    @staticmethod
    def _clear_db():
        db.session.remove()
        db.reflect()
        db.drop_all()
