from abc import ABC, abstractmethod
import sqlite3
from distutils.command.config import config
from pickletools import pybytes_or_str
from posixpath import curdir
from unittest import case


class Menu(ABC):
    @abstractmethod
    def show_menu(self):
        pass


class Pracownik_ABC(ABC):
    @abstractmethod
    def __init__(self, imie, nazwisko, id, is_menager, login):
        pass


class DB_ABC(ABC):
    # DB pracownicy
    @abstractmethod
    def create_DB_pracownicy(self):
        pass

    @abstractmethod
    def dodaj_pracownik(self):
        pass

    @abstractmethod
    def usun_pracownik(self):
        pass

    # DB Dostepne Auta
    @abstractmethod
    def create_DB_dostepne_auta(self):
        pass

    @abstractmethod
    def dodaj_auto(self):
        pass

    @abstractmethod
    def usun_auto(self):
        pass

    @abstractmethod
    def wynajmij(self):
        pass

    @abstractmethod
    def wyswietl_auta(self):
        pass

    # Wynajete

    @abstractmethod
    def wyswietl_wynajete_auta(self):
        pass

    @abstractmethod
    def zwolnij_auto_2_0(self):
        pass

    # Klienci
    @abstractmethod
    def create_DB_klienci(self):
        pass

    @abstractmethod
    def dodaj_klienta(self):
        pass

    @abstractmethod
    def usun_klienta(self):
        pass

    @abstractmethod
    def historia_klienta_db(self):
        pass

    @abstractmethod
    def add_to_history_klienta(self):
        pass

    @abstractmethod
    def create_DB_raports(self):
        pass

    @abstractmethod
    def add_raport(self):
        pass



class DB_Pracownikow(DB_ABC):


    # Pracownicy
    def create_DB_pracownicy(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        create_table = """
        CREATE TABLE IF NOT EXISTS pracownicy (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
        Imie TEXT NOT NULL,
        Nazwisko TEXT NOT NULL,
        is_menager INTEGER,
        Login TEXT NOT NULL,
        Haslo TEXT NOT NULL
        );
        """
        try:
            cursor.execute(create_table)
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()

    def dodaj_pracownik(self, imie_, nazwisko_, id_, is_menager, login, haslo):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        sql = f"""
        INSERT INTO pracownicy (imie,nazwisko,id,is_menager,Login,Haslo) VALUES ("{imie_}","{nazwisko_}","{id_}","{is_menager}","{login}","{haslo}");
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def usun_pracownik(self, id_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        id_sql = f""" DELETE FROM pracownicy WHERE id = "{id_t}" """
        cursor.execute(id_sql)
        print("Pracownik pomyslnie usuniety :)")
        conn.commit()
        conn.close()

    # Dostepne Auta
    def create_DB_dostepne_auta(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS dostepne_auta (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        Marka TEXT NOT NULL,
        Rocznik TEXT NOT NULL,
        Ostatni_Przeglad TEXT NOT NULL,
        Stawka_godzinowa INTEGER NOT NULL,
        Stawka_dniowa INTEGER NOT NULL,
        Lokalizacja TEXT NOT NULL,
        Czy_wynajety INTEGER
        )
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def dodaj_auto(self, id_t, Marka_t, Rocznik_t, Ostani_Przeglad_t, Stawka_godzinowa_t, Stawka_dniowa_t,
                   Lokalizacja_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        sql = f"""
        INSERT 
        INTO dostepne_auta (id, Marka, Rocznik, Ostatni_Przeglad, Stawka_godzinowa, Stawka_dniowa, Lokalizacja) 
        VALUES ("{id_t}", "{Marka_t}", "{Rocznik_t}", "{Ostani_Przeglad_t}", "{Stawka_dniowa_t}", "{Stawka_godzinowa_t}", "{Lokalizacja_t}")
        """
        cursor.execute(sql)
        print("Auto Dodane Pomsylnie!")
        conn.commit()
        conn.close()

    def usun_auto(self, id_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        sql = f"""DELETE FROM dostepne_auta WHERE id = "{id_t}" """
        cursor.execute(sql)
        print("Auto usuniete :)")
        conn.commit()
        conn.close()

    def add_to_history_klienta(self,customer_id,car_id,date_start,date_end,was_report,report_id):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        query = f"""INSERT 
                    INTO historia_klientow (client_id,car_id,date_start,date_end,was_report,report_id) 
                    VALUES ("{customer_id}", "{car_id}", "{date_start}","{date_end}","{was_report}","{report_id}") 
                    """

        cursor.execute(query)


        conn.commit()
        conn.close()

    def wynajmij(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        id_t = 0
        sql = f"""SELECT * FROM dostepne_auta WHERE id = "{id_t}" """

        sql4 = """SELECT * FROM klienci"""
        cursor.execute(sql4)
        dane_klientow = cursor.fetchall()
        print("Klienci")
        for dane in dane_klientow:
            print(f"{dane} \n")
        wybrany_klient_id = input("Wybierz klienta ktory wynajmuje (id)")

        sql5 = f"""SELECT Pesel FROM klienci WHERE id = "{wybrany_klient_id}" """
        cursor.execute(sql5)
        wybrany_klient = cursor.fetchall()
        wybrany_klient = wybrany_klient[0]

        sql6 = f"""SELECT * FROM dostepne_auta 
        WHERE Czy_wynajety < 1 OR Czy_wynajety IS NULL 
        """

        cursor.execute(sql6)
        dostepne_auta = cursor.fetchall()

        print("Dostepne Samochody   \n")
        for row in dostepne_auta:
            print(f"{row}  \n")

        id_t = input("wybierz auto (id)")

        cursor.execute(sql)
        dane = cursor.fetchall()
        dane1 = dane[0]


        print(dane_klientow)
        date_start = input("Podaj date wynajecia")
        date_end = input("Podaj date konca wynajecia")
        was_raport = input("czy byl raport o uszkodzeniu TAK lub NIE")

        if was_raport == "TAK":
            data_raportu = input("podaj date raportu")
            opis = input("Opis raportu: ")
            raport_id = DB_Pracownikow().add_raport(id_t,data_raportu,opis )
            was_report = 1
        elif was_raport == "NIE":
            was_report = 0
            raport_id = None

        query_czy_wynajety = f"""
        UPDATE dostepne_auta
        SET Czy_wynajety = 1
        WHERE id = "{id_t}";
        """
        cursor.execute(query_czy_wynajety)

        conn.commit()
        conn.close()




        self.add_to_history_klienta(wybrany_klient_id, id_t, date_start, date_end, was_report,raport_id)

    def wyswietl_auta(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()
        sql = f"""SELECT * FROM dostepne_auta 
        WHERE Czy_wynajety < 1 OR Czy_wynajety IS NULL 
        """
        cursor.execute(sql)

        res = cursor.fetchall()
        print("Dostepne Auta:  \n")
        for _ in res:
            print(f"{_}\n")


    def zwolnij_auto_2_0(self,id_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        query_czy_wynajety = f"""
               UPDATE dostepne_auta
               SET Czy_wynajety = 0
               WHERE id = "{id_t}";
               """

        sql4 = """SELECT * FROM klienci"""
        cursor.execute(sql4)
        dane_klientow = cursor.fetchall()
        print("Klienci")
        for dane in dane_klientow:
            print(f"{dane} \n")
        wybrany_klient_id = input("Wybierz klienta ktory wynajmuje (id)")



        date_start = input("Podaj date wynajecia")
        date_end = input("Podaj date konca wynajecia")
        was_raport = input("czy byl raport o uszkodzeniu TAK lub NIE")

        if was_raport == "TAK":
            data_raportu = input("podaj date raportu")
            opis = input("Opis raportu: ")
            raport_id = DB_Pracownikow().add_raport(id_t,data_raportu,opis )
            was_report = 1
        elif was_raport == "NIE":
            was_report = 0
            raport_id = None



        self.add_to_history_klienta(wybrany_klient_id, id_t, date_start, date_end, was_report,raport_id)



        cursor.execute(query_czy_wynajety)
        conn.commit()
        conn.close()


    # Wynajete Auta


    def create_DB_raports(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()


        query = """ CREATE TABLE IF NOT EXISTS raports (
        RaportID INTEGER PRIMARY KEY,
        Car_id INTEGER NOT NULL,
        Date TEXT NOT NULL,
        Discription TEXT NOT NULL
        )
                     
         """

        cursor.execute(query)
        conn.commit()
        conn.close()

    def add_raport(self, car_id, date, discription):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        query = f"""INSERT INTO raports (Car_id, Date, Discription)
                    VALUES ("{car_id}","{date}","{discription}")
                    """
        cursor.execute(query)
        conn.commit()
        conn.close()

        return cursor.lastrowid

    def wyswietl_wynajete_auta(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        sql6 = f"""SELECT * FROM dostepne_auta 
            WHERE Czy_wynajety = 1 OR Czy_wynajety IS NOT NULL 
            """
        cursor.execute(sql6)
        res = cursor.fetchall()
        print("Wynajete Auta:  \n")
        for _ in res:
            print(f"{_}\n")


    # Klienci
    def create_DB_klienci(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS klienci (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL, 
        Imie TEXT NOT NULL,
        Nazwisko TEXT NOT NULL,
        Telefon TEXT NOT NULL,
        Email TEXT NOT NULL,
        Data_Urodzenia TEXT NOT NULL,
        Pesel INTEGER NOT NULL,
        Adres TEXT NOT NULL
        );
        """
        try:
            cursor.execute(sql)
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()

## CLIENT HISTORY
    def historia_klienta_db(self):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        query = """ CREATE TABLE IF NOT EXISTS historia_klientow (
        history_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        client_id INTEGER NOT NULL,
        car_id INTEGER NOT NULL,
        date_start TEXT NOT NULL,
        date_end TEXT NOT NULL,
        was_report INTEGER NOT NULL,
        report_id INTEGER        
        
        
        ) """

        cursor.execute(query)
        conn.commit()
        conn.close()


## CLIENT HISTORY


    def dodaj_klienta(self, id_t, Imie_t, Nazwisko_t, Telefon_t, Email_t, Data_Urodzenia_t, Pesel_t, Adres_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        sql = f"""
                INSERT INTO klienci (id, Imie, Nazwisko, Telefon, Email, Data_Urodzenia, Pesel, Adres) VALUES 
                ("{id_t}","{Imie_t}","{Nazwisko_t}","{Telefon_t}","{Email_t}","{Data_Urodzenia_t}","{Pesel_t}", "{Adres_t}");       """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def usun_klienta(self, id_t):
        conn = sqlite3.connect("Pracownicy.db", timeout=5)
        cursor = conn.cursor()

        id_sql = f""" DELETE FROM klienci WHERE id = "{id_t}" """
        cursor.execute(id_sql)
        print("Klient pomyslnie usuniety :)")
        conn.commit()
        conn.close()


class Pracownik(Pracownik_ABC):
    def __init__(self, imie, nazwisko, id, is_menager):
        self.imie = imie
        self.nazwisko = nazwisko
        self.id = id
        self.is_menager = is_menager


class ShowMenu(Menu):
    def show_menu(self):
        print('1. Logowanie')
        wybor = input(" ")
        match wybor:
            case '1':
                print("Login:")
                login = input()
                print("Haslo:")
                haslo = input()
                conn = sqlite3.connect("Pracownicy.db", timeout=5)
                cursor = conn.cursor()
                get_data_ = f"""SELECT * FROM pracownicy WHERE Login="{login}" AND Haslo="{haslo}" """
                cursor.execute(get_data_)
                Dane_uzytkownika = cursor.fetchall()
                conn.commit()
                conn.close()
                if len(Dane_uzytkownika) == 1:
                    print("zalogowano")
                    while True:
                        print("1. Samochody")
                        print("2. Klienci")
                        # If is a Menager
                        try:
                            if Dane_uzytkownika[0][3] > 0:
                                print("3. Dodaj Pracownika")
                                print("4. Usun Pracownika")
                        except IndexError:
                            pass

                        wybor = input(" ")

                        # Dodaj Pracownika
                        if wybor == "3" and Dane_uzytkownika[0][3] == 1:
                            id_sql = """SELECT id FROM pracownicy"""
                            conn = sqlite3.connect("Pracownicy.db", timeout=5)
                            cursor = conn.cursor()
                            cursor.execute(id_sql)
                            res = cursor.fetchall()
                            conn.commit()
                            conn.close()

                            for id in res:
                                max_id = id
                                if id > max_id:
                                    max_id = id

                            imie_t = input("Imie: ")
                            Nazwisko_t = input("Nazwisko: ")
                            is_menager_t = input("Is menager:  0 if no, 1 if yes")
                            login_t = input("Login: ")
                            haslo_t = input("Haslo: ")

                            DB_Pracownikow().dodaj_pracownik(imie_t, Nazwisko_t, max_id[0] + 1, is_menager_t, login_t,
                                                             haslo_t)

                        # Usun Pracownika
                        elif wybor == "4" and Dane_uzytkownika[0][3] == 1:
                            conn = sqlite3.connect("Pracownicy.db", timeout=5)
                            cursor = conn.cursor()
                            get_data_ = f"""SELECT * FROM pracownicy"""
                            cursor.execute(get_data_)
                            res = cursor.fetchall()

                            print(f"Lista Pracownikow:\n")
                            for _ in res:
                                print(f"{_}\n")

                            id_t = input("Id pracownika:  ")
                            DB_Pracownikow().usun_pracownik(id_t)



                        #                       #Samochody
                        elif wybor == "1":
                            print("1. Dostepne ")
                            print("2. Wynajete ")
                            wybor2 = input(" ")

                            match wybor2:

                                case "1":
                                    print("1. Dodaj Samochod")
                                    print("2. Wynajmij Samochod")
                                    print("3. Dostepne Samochody Lista")

                                    wybor3 = input(" ")
                                    match wybor3:

                                        case "1":
                                            # Dodaj Auto
                                            Marka_t = input("Marka:  ")
                                            Rocznik_t = input("Rocznik:  ")
                                            Ostani_Przeglad_t = input("Ostani Przeglad:  ")
                                            Stawka_godzinowa_t = input("Stawka Godzinowa:  ")
                                            Stawka_dniowa_t = input("Stawka Dniowa:  ")
                                            Lokalizacja_t = input("Lokalizacja:  ")

                                            conn = sqlite3.connect("Pracownicy.db", timeout=5)
                                            cursor = conn.cursor()

                                            sql = """ SELECT id FROM dostepne_auta"""

                                            cursor.execute(sql)

                                            res = cursor.fetchall()
                                            if len(res) != 0:
                                                for id in res:
                                                    id_max = id
                                                    if id > id_max:
                                                        id_max = id
                                            else:
                                                id_max = 0

                                            if id_max == 0:
                                                DB_Pracownikow().dodaj_auto(id_max, Marka_t, Rocznik_t,
                                                                            Ostani_Przeglad_t, Stawka_godzinowa_t,
                                                                            Stawka_dniowa_t, Lokalizacja_t)
                                            else:
                                                DB_Pracownikow().dodaj_auto(id_max[0] + 1, Marka_t, Rocznik_t,
                                                                            Ostani_Przeglad_t, Stawka_godzinowa_t,
                                                                            Stawka_dniowa_t, Lokalizacja_t)

                                        # Wynajmij
                                        case "2":
                                            DB_Pracownikow().wynajmij()

                                        # Lista
                                        case "3":
                                            DB_Pracownikow().wyswietl_auta()

                                # Wynajete
                                case "2":
                                    print("1. Wynajete auta")
                                    print("2. Zwolnij auto")
                                    wybor5 = input(" ")

                                    if wybor5 == "1":
                                        DB_Pracownikow().wyswietl_wynajete_auta()
                                    elif wybor5 == "2":
                                        DB_Pracownikow().wyswietl_wynajete_auta()
                                        id_auta = input("Id auta:  ")
                                        DB_Pracownikow().zwolnij_auto_2_0(id_auta)


                        # Klienci
                        elif wybor == "2":
                            print("1. Dodaj Klienta")
                            print("2. Usun Klienta")
                            print("3  Wyswietl Liste Klientow")
                            wybor4 = input(" ")

                            match wybor4:
                                # Dodaj Klienta
                                case "1":
                                    conn = sqlite3.connect("Pracownicy.db", timeout=5)
                                    cursor = conn.cursor()

                                    sql = """SELECT id FROM klienci"""

                                    cursor.execute(sql)
                                    res = cursor.fetchall()
                                    if len(res) != 0:
                                        for id in res:
                                            id_max = id
                                            if id > id_max:
                                                id_max = id
                                    else:
                                        id_max = 0

                                    imie_t = input("Imie: ")
                                    Nazwisko_t = input("Nazwisko: ")
                                    Telefon_t = input("Telefone: ")
                                    Email_t = input("Email: ")
                                    Data_Urodzenia_t = input("Data Urodzenia: ")
                                    Pesel_t = input("Pesel: ")
                                    Adres_t = input("Adres: ")

                                    if id_max == 0:
                                        DB_Pracownikow().dodaj_klienta(id_max, imie_t, Nazwisko_t, Telefon_t, Email_t,
                                                                       Data_Urodzenia_t, Pesel_t, Adres_t)
                                    else:
                                        DB_Pracownikow().dodaj_klienta(id_max[0] + 1, imie_t, Nazwisko_t, Telefon_t,
                                                                       Email_t, Data_Urodzenia_t, Pesel_t, Adres_t)

                                # Usun Klienta
                                case "2":
                                    conn = sqlite3.connect("Pracownicy.db", timeout=5)
                                    cursor = conn.cursor()
                                    sql = """SELECT * FROM klienci"""
                                    cursor.execute(sql)
                                    res = cursor.fetchall()
                                    print(f"Lista Klientow:\n")
                                    for _ in res:
                                        print(f"{_}\n")
                                    id_t = input("Id pracownika: ")
                                    DB_Pracownikow().usun_klienta(id_t)

                                case "3":
                                    conn = sqlite3.connect("Pracownicy.db", timeout=5)
                                    cursor = conn.cursor()
                                    sql = """SELECT * FROM klienci"""
                                    cursor.execute(sql)
                                    res = cursor.fetchall()
                                    print(f"Lista Klientow:\n")
                                    for _ in res:
                                        print(f"{_}\n")

                else:
                    print("zle haslo lub login")


while __name__ == '__main__':
    DB_Pracownikow().create_DB_pracownicy()
    DB_Pracownikow().create_DB_klienci()
    DB_Pracownikow().create_DB_dostepne_auta()
    DB_Pracownikow().historia_klienta_db() #CREATE DB
    DB_Pracownikow().create_DB_raports()
    try:
        DB_Pracownikow().dodaj_pracownik("admin", "admin", -1, 1, "admin", "admin")
    except:
        pass

    ShowMenu().show_menu()