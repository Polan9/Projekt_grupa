import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from main import DB_Pracownikow


class TestDBPracownikow(unittest.TestCase):

    def setUp(self):
        self.db = DB_Pracownikow()
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    @patch("sqlite3.connect")
    def test_create_DB_pracownicy(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_pracownicy()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pracownicy';")
        self.assertIsNotNone(self.cursor.fetchone(), "Tabela 'pracownicy' nie została utworzona.")

    @patch("sqlite3.connect")
    def test_dodaj_pracownik(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_pracownicy()
        self.db.dodaj_pracownik("Jan", "Kowalski", 1, 0, "jan_kowalski", "haslo123")
        self.cursor.execute("SELECT * FROM pracownicy WHERE id=1;")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Pracownik nie został dodany.")
        self.assertEqual(result[1], "Jan", "Imię pracownika nie zgadza się.")

    @patch("sqlite3.connect")
    def test_usun_pracownik(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_pracownicy()
        self.db.dodaj_pracownik("Jan", "Kowalski", 1, 0, "jan_kowalski", "haslo123")
        self.db.usun_pracownik(1)
        self.cursor.execute("SELECT * FROM pracownicy WHERE id=1;")
        result = self.cursor.fetchone()
        self.assertIsNone(result, "Pracownik nie został usunięty.")

    @patch("sqlite3.connect")
    def test_create_DB_dostepne_auta(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_dostepne_auta()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dostepne_auta';")
        self.assertIsNotNone(self.cursor.fetchone(), "Tabela 'dostepne_auta' nie została utworzona.")

    @patch("sqlite3.connect")
    def test_dodaj_auto(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_dostepne_auta()
        self.db.dodaj_auto(1, "Toyota", "2020", "2023-01-01", 50, 300, "Warszawa")
        self.cursor.execute("SELECT * FROM dostepne_auta WHERE id=1;")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Auto nie zostało dodane.")
        self.assertEqual(result[1], "Toyota", "Marka auta nie zgadza się.")

    @patch("sqlite3.connect")
    def test_usun_auto(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_dostepne_auta()
        self.db.dodaj_auto(1, "Toyota", "2020", "2023-01-01", 50, 300, "Warszawa")
        self.db.usun_auto(1)
        self.cursor.execute("SELECT * FROM dostepne_auta WHERE id=1;")
        result = self.cursor.fetchone()
        self.assertIsNone(result, "Auto nie zostało usunięte.")

    @patch("sqlite3.connect")
    def test_wyswietl_auta(self, mock_connect):
        mock_connect.return_value = self.conn
        self.db.create_DB_dostepne_auta()
        self.db.dodaj_auto(1, "Toyota", "2020", "2023-01-01", 50, 300, "Warszawa")
        with patch("builtins.print") as mock_print:
            self.db.wyswietl_auta()
            mock_print.assert_called_with('(1, "Toyota", "2020", "2023-01-01", 50, 300, "Warszawa", None)\n')

if __name__ == "__main__":
    unittest.main()
