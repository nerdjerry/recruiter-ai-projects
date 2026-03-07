import os

import pytest

from app.services.csv_importer import CsvImporter


VALID_CSV = "date,description,amount\n2024-01-15,Grocery Store,45.50\n2024-01-16,Gas Station,30.00\n"
CSV_WITH_CATEGORY = "date,description,amount,category\n2024-01-15,Grocery Store,45.50,food\n"
BAD_CSV = "name,value\nfoo,bar\n"


class TestCsvImporter:
    def test_parse_valid_csv(self, tmp_path):
        db = str(tmp_path / "test.db")
        importer = CsvImporter(db_path=db)
        transactions = importer.import_csv(VALID_CSV)
        assert len(transactions) == 2
        assert transactions[0].description == "Grocery Store"
        assert transactions[0].amount == 45.50

    def test_parse_with_category(self, tmp_path):
        db = str(tmp_path / "test.db")
        importer = CsvImporter(db_path=db)
        transactions = importer.import_csv(CSV_WITH_CATEGORY)
        assert transactions[0].category == "food"

    def test_missing_columns_raises(self, tmp_path):
        db = str(tmp_path / "test.db")
        importer = CsvImporter(db_path=db)
        with pytest.raises(KeyError):
            importer.import_csv(BAD_CSV)

    def test_save_and_fetch_roundtrip(self, tmp_path):
        db = str(tmp_path / "test.db")
        importer = CsvImporter(db_path=db)
        transactions = importer.import_csv(VALID_CSV)
        importer.save_transactions(transactions)

        # Fetch without day filter to retrieve all stored transactions
        fetched = importer.get_transactions()
        assert len(fetched) == 2
        assert fetched[0].description in ("Grocery Store", "Gas Station")

    def test_get_transactions_with_filters(self, tmp_path):
        db = str(tmp_path / "test.db")
        importer = CsvImporter(db_path=db)
        transactions = importer.import_csv(CSV_WITH_CATEGORY)
        importer.save_transactions(transactions)

        results = importer.get_transactions(category="food")
        assert len(results) == 1

        results = importer.get_transactions(min_amount=100.0)
        assert len(results) == 0
