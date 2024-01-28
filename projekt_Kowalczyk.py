import psycopg2 as ps
import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView

db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='psip2023',
    host='localhost',
    port=5432
)
cursor=db_params.cursor()

create_lista_koncertow='''
    CREATE TABLE IF NOT EXISTS lista_koncertow(
    id INT PRIMARY KEY,
    nazwa TEXT(30),
    miasto TEXT(30)
    );
'''
cursor.execute(create_lista_koncertow)
db_params.commit()

create_lista_klientow='''
    CREATE TABLE IF NOT EXISTS lista_klientow(
    id INT PRIMARY KEY,
    imie TEXT(30),
    miejscowosc TEXT(30),
    koncert TEXT(30),
    bilet TEXT(30)
    );
'''
cursor.execute(create_lista_klientow)
db_params.commit()

create_lista_zespolow='''
    CREATE TABLE IF NOT EXISTS lista_zespolow(
    id INT PRIMARY KEY,
    nazwa TEXT(30),
    koncert TEXT(30),
    siedziba TEXT(30)
    );
'''
cursor.execute(create_lista_zespolow)
db_params.commit()

def id_koncerty():
    sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;" #id rosnaco
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    id = [] #pusta lista
    if not wynik_zapytania:
        id.append('1')
    else:
        for row in wynik_zapytania:
            id.append(row[0])
    return int(max(id))+1

def id_klienci():
    sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    id = []
    if not wynik_zapytania:
        id.append('1')
    else:
        for row in wynik_zapytania:
            id.append(row[0])
    return int(max(id))+1

def id_zespoly():
    sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    id = []
    if not wynik_zapytania:
        id.append('1')
    else:
        for row in wynik_zapytania:
            id.append(row[0])
    return int(max(id))+1

def id_koncerty_update():
    sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    lista_id = []
    for row in wynik_zapytania:
        lista_id.append(row[0])
    for idx, id in enumerate(lista_id):
        sql_query_2 = f"UPDATE public.lista_koncertow SET id='{idx+1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()

def id_klienci_update():
    sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    lista_id = []
    for row in wynik_zapytania:
        lista_id.append(row[0])
    for idx, id in enumerate(lista_id):
        sql_query_2 = f"UPDATE public.lista_klientow SET id='{idx+1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()

def id_zespoly_update():
    sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
    cursor.execute(sql_query_1)
    wynik_zapytania = cursor.fetchall()
    lista_id = []
    for row in wynik_zapytania:
        lista_id.append(row[0])
    for idx, id in enumerate(lista_id):
        sql_query_2 = f"UPDATE public.lista_zespolow SET id='{idx+1}' WHERE id='{id}';"
        cursor.execute(sql_query_2)
        db_params.commit()

def get_coordinates(city:str)->list[float,float]:
    adres_url = "https://nominatim.openstreetmap.org/search"
    parameters = {"q": city, "format": "json"}
    response = rq.get(adres_url, parameters)
    data = response.json()
    lat = data[0]["lat"]
    long = data[0]["lon"]
    return [float(lat), float(long)]

def logowanko(event=None):
    password=logowanko_entry.get()
    if password=='psip12345':

        def koncerty():

            def koncerty_wszystko():
                listbox_koncerty.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()
                for idx, row in enumerate(wynik_zapytania):
                    listbox_koncerty.insert(idx, f'Koncert {row[1]}')

                id_koncerty_update()

            def koncerty_dodaj():
                nazwa=entry_koncerty_nazwa.get()
                miasto=entry_koncerty_miasto.get()

                sql_query_1 = f"INSERT INTO public.lista_koncertow(id, nazwa, miasto) VALUES ('{id_koncerty()}', '{nazwa}', '{miasto}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_koncerty_nazwa.delete(0, END)
                entry_koncerty_miasto.delete(0, END)

                koncerty_wszystko()

            def koncerty_edytuj():
                sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i=listbox_koncerty.index(ACTIVE)

                entry_koncerty_nazwa.delete(0, END)
                entry_koncerty_miasto.delete(0, END)

                entry_koncerty_nazwa.insert(0, wynik_zapytania[i][1])
                entry_koncerty_miasto.insert(0, wynik_zapytania[i][2])

                button_koncerty_dodaj.config(text='Dodaj koncert', command=lambda: koncerty_aktualizuj(i))

            def koncerty_aktualizuj(i):
                sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                nazwa=entry_koncerty_nazwa.get()
                miasto=entry_koncerty_miasto.get()

                sql_query_2 = f"UPDATE public.lista_koncertow SET nazwa='{nazwa}',miasto='{miasto}' WHERE nazwa='{wynik_zapytania[i][1]}' and miasto='{wynik_zapytania[i][2]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_koncerty_dodaj.config(text='Dodaj koncert', command=koncerty_dodaj)

                entry_koncerty_nazwa.delete(0, END)
                entry_koncerty_miasto.delete(0, END)

                koncerty_wszystko()

            def koncerty_usun():
                i = listbox_koncerty.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.lista_koncertow WHERE id='{i+1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                koncerty_wszystko()

            def koncerty_szczegoly():
                sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i = listbox_koncerty.index(ACTIVE)

                nazwa=wynik_zapytania[i][1]
                miasto=wynik_zapytania[i][2]
                lokalizacja_koncertu=f'{round(float(get_coordinates(miasto)[0]),4)}\n {round(float(get_coordinates(miasto)[1]),4)}'

                label_koncerty_nazwa_wartosc.config(text=nazwa)
                label_koncerty_miejscowosc_wartosc.config(text=miasto)
                label_koncerty_lokalizacja_wartosc.config(text=lokalizacja_koncertu)

            root_listy = Toplevel(root_wybieranie)
            root_listy.title('Wydarzenia muzyczne')
            root_listy.state('zoomed')

            root_koncerty=Frame(root_listy)
            root_koncerty.grid(row=0, column=0)

            ramka_koncerty_poczatek = Frame(root_koncerty)
            ramka_koncerty_lista = Frame(root_koncerty)
            ramka_koncerty_wprowadzanie = Frame(root_koncerty)
            ramka_koncerty_szczegoly = Frame(root_koncerty)

            ramka_koncerty_poczatek.grid(row=0, column=0, columnspan=2)
            ramka_koncerty_lista.grid(row=1, column=0)
            ramka_koncerty_wprowadzanie.grid(row=1, column=1)
            ramka_koncerty_szczegoly.grid(row=0, column=2, columnspan=2, rowspan=2)

            label_koncerty_napis = Label(ramka_koncerty_poczatek, text='Lista koncertów', font=('Calibri', 20,'bold', 'italic'))
            button_pokaz_liste = Button(ramka_koncerty_poczatek, text='Wszystkie koncerty', command=koncerty_wszystko)

            label_koncerty_napis.grid(row=0, column=0, padx=(335 - label_koncerty_napis.winfo_reqwidth() / 2), pady=(10, 0))
            button_pokaz_liste.grid(row=1, column=0)

            listbox_koncerty = Listbox(ramka_koncerty_lista, width=50, height=5)
            button_koncerty_szczegoly = Button(ramka_koncerty_lista, text='Szczegóły', command=koncerty_szczegoly)
            button_koncerty_usuwanie = Button(ramka_koncerty_lista, text='Usuń', command=koncerty_usun)
            button_koncerty_edytuj = Button(ramka_koncerty_lista, text='Edytuj', command=koncerty_edytuj)

            listbox_koncerty.grid(row=1, column=0, columnspan=3, pady=(10, 0))
            button_koncerty_szczegoly.grid(row=2, column=0)
            button_koncerty_usuwanie.grid(row=2, column=1)
            button_koncerty_edytuj.grid(row=2, column=2)

            label_koncerty_nowe = Label(ramka_koncerty_wprowadzanie, text='Dodaj koncert:',
                                        font=('Calibri', 14, 'italic'))
            label_koncerty_nazwa = Label(ramka_koncerty_wprowadzanie, text='Nazwa koncertu')
            label_koncerty_miasto = Label(ramka_koncerty_wprowadzanie, text='Miejsce koncertu')

            entry_koncerty_nazwa = Entry(ramka_koncerty_wprowadzanie)
            entry_koncerty_miasto = Entry(ramka_koncerty_wprowadzanie)

            label_koncerty_nowe.grid(row=0, column=0, columnspan=2)
            label_koncerty_nazwa.grid(row=1, column=0, sticky=W)
            label_koncerty_miasto.grid(row=2, column=0, sticky=W)

            entry_koncerty_nazwa.grid(row=1, column=1, sticky=W)
            entry_koncerty_miasto.grid(row=2, column=1, sticky=W)

            button_koncerty_dodaj = Button(ramka_koncerty_wprowadzanie, text='Dodaj wydarzenie', command=koncerty_dodaj)
            button_koncerty_dodaj.grid(row=3, column=0, columnspan=2)

            label_koncerty_opis = Label(ramka_koncerty_szczegoly, text='Szczegóły:', font=('Calibri', 14, 'italic'))
            label_koncerty_nazwa = Label(ramka_koncerty_szczegoly, text='Nazwa koncertu')
            label_koncerty_nazwa_wartosc = Label(ramka_koncerty_szczegoly, text='?', width=20)

            label_koncerty_miejscowosc = Label(ramka_koncerty_szczegoly, text='Miasto')
            label_koncerty_miejscowosc_wartosc = Label(ramka_koncerty_szczegoly, text='?', width=20)

            label_koncerty_lokalizacja = Label(ramka_koncerty_szczegoly, text='Współrzędne koncertu')
            label_koncerty_lokalizacja_wartosc = Label(ramka_koncerty_szczegoly, text='?', width=20)


            label_koncerty_opis.grid(row=0, column=0, columnspan=8, pady=10)

            label_koncerty_nazwa.grid(row=1, column=0)
            label_koncerty_nazwa_wartosc.grid(row=2, column=0)

            label_koncerty_miejscowosc.grid(row=3, column=0)
            label_koncerty_miejscowosc_wartosc.grid(row=4, column=0)

            label_koncerty_lokalizacja.grid(row=5, column=0)
            label_koncerty_lokalizacja_wartosc.grid(row=6, column=0)


            def zespoly_wszystko():
                listbox_zespoly.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()
                for idx, row in enumerate(wynik_zapytania):
                    listbox_zespoly.insert(idx, f'Zespół {row[1]}')

                id_zespoly_update()

            def zespoly_dodaj():
                nazwa = entry_zespoly_nazwa.get()
                koncert=entry_zespoly_koncert.get()
                siedziba = entry_zespoly_siedziba.get()

                sql_query_1 = f"INSERT INTO public.lista_zespolow(id, nazwa, koncert, siedziba) VALUES ('{id_zespoly()}', '{nazwa}', '{koncert}', '{siedziba}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_zespoly_nazwa.delete(0, END)
                entry_zespoly_koncert.delete(0, END)
                entry_zespoly_siedziba.delete(0, END)

                zespoly_wszystko()

            def zespoly_edytuj():
                sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i = listbox_koncerty.index(ACTIVE)

                entry_zespoly_nazwa.delete(0, END)
                entry_zespoly_koncert.delete(0, END)
                entry_zespoly_siedziba.delete(0, END)

                entry_zespoly_nazwa.insert(0, wynik_zapytania[i][1])
                entry_zespoly_koncert.insert(0, wynik_zapytania[i][2])
                entry_zespoly_siedziba.insert(0, wynik_zapytania[i][3])

                button_zespoly_dodaj.config(text='Dodaj zespół', command=lambda: zespoly_aktualizuj(i))

            def zespoly_aktualizuj(i):
                sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                nazwa = entry_zespoly_nazwa.get()
                koncert = entry_zespoly_koncert.get()
                siedziba = entry_zespoly_siedziba.get()

                sql_query_2 = f"UPDATE public.lista_zespolow SET nazwa='{nazwa}',koncert='{koncert}', siedziba='{siedziba}' WHERE nazwa='{wynik_zapytania[i][1]}' and koncert='{wynik_zapytania[i][2]}' and siedziba='{wynik_zapytania[i][3]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_koncerty_dodaj.config(text='Dodaj zespół', command=zespoly_dodaj)

                entry_zespoly_nazwa.delete(0, END)
                entry_zespoly_koncert.delete(0, END)
                entry_zespoly_siedziba.delete(0, END)

                zespoly_wszystko()

            def zespoly_usun():
                i = listbox_zespoly.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.lista_zespolow WHERE id='{i + 1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                zespoly_wszystko()

            def zespoly_szczegoly():
                sql_query_1 = f"SELECT * FROM public.lista_zespolow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i = listbox_zespoly.index(ACTIVE)

                nazwa = wynik_zapytania[i][1]
                koncert = wynik_zapytania[i][2]
                siedziba=wynik_zapytania[i][3]
                siedziba_wsp = f'{round((float(get_coordinates(siedziba)[0])), 4)}\n {round((float(get_coordinates(siedziba)[1])), 4)}'

                label_zespoly_nazwa_wartosc.config(text=nazwa)
                label_zespoly_koncert_wartosc.config(text=koncert)
                label_zespoly_lokalizacja_wartosc.config(text=siedziba_wsp)

            root_zespoly = Frame(root_listy)
            root_zespoly.grid(row=1, column=0)

            ramka_zespoly_poczatek = Frame(root_zespoly)
            ramka_zespoly_lista = Frame(root_zespoly)
            ramka_zespoly_wprowadzanie = Frame(root_zespoly)
            ramka_zespoly_szczegoly = Frame(root_zespoly)

            ramka_zespoly_poczatek.grid(row=0, column=0, columnspan=2)
            ramka_zespoly_lista.grid(row=1, column=0)
            ramka_zespoly_wprowadzanie.grid(row=1, column=1)
            ramka_zespoly_szczegoly.grid(row=1, column=2, columnspan=2)

            label_zespoly_napis = Label(ramka_zespoly_poczatek, text='Lista zespołów',
                                         font=('Calibri', 20,'bold', 'italic'))
            button_pokaz_liste = Button(ramka_zespoly_poczatek, text='Wszystkie zespoły', command=zespoly_wszystko)

            label_zespoly_napis.grid(row=0, column=0, padx=(335 - label_zespoly_napis.winfo_reqwidth() / 2),
                                      pady=(10, 0))
            button_pokaz_liste.grid(row=1, column=0)

            listbox_zespoly = Listbox(ramka_zespoly_lista, width=50, height=5)
            button_zespoly_szczegoly = Button(ramka_zespoly_lista, text='Szczegóły', command=zespoly_szczegoly)
            button_zespoly_usuwanie = Button(ramka_zespoly_lista, text='Usuń', command=zespoly_usun)
            button_zespoly_edytuj = Button(ramka_zespoly_lista, text='Edytuj', command=zespoly_edytuj)

            listbox_zespoly.grid(row=1, column=0, columnspan=3, pady=(5, 0))
            button_zespoly_szczegoly.grid(row=2, column=0)
            button_zespoly_usuwanie.grid(row=2, column=1)
            button_zespoly_edytuj.grid(row=2, column=2)

            label_zespoly_nowe = Label(ramka_zespoly_wprowadzanie, text='Dodaj zespół:',
                                        font=('Calibri', 14, 'italic'))
            label_zespoly_nazwa = Label(ramka_zespoly_wprowadzanie, text='Nazwa zespołu')
            label_zespoly_koncert = Label(ramka_zespoly_wprowadzanie, text='Koncert zespołu')
            label_zespoly_siedziba = Label(ramka_zespoly_wprowadzanie, text='Siedziba zespołu')

            entry_zespoly_nazwa = Entry(ramka_zespoly_wprowadzanie)
            entry_zespoly_koncert = Entry(ramka_zespoly_wprowadzanie)
            entry_zespoly_siedziba = Entry(ramka_zespoly_wprowadzanie)

            label_zespoly_nowe.grid(row=0, column=0, columnspan=2)
            label_zespoly_nazwa.grid(row=1, column=0, sticky=W)
            label_zespoly_koncert.grid(row=2, column=0, sticky=W)
            label_zespoly_siedziba.grid(row=3, column=0, sticky=W)

            entry_zespoly_nazwa.grid(row=1, column=1, sticky=W)
            entry_zespoly_koncert.grid(row=2, column=1, sticky=W)
            entry_zespoly_siedziba.grid(row=3, column=1, sticky=W)

            button_zespoly_dodaj = Button(ramka_zespoly_wprowadzanie, text='Dodaj zespół', command=zespoly_dodaj)
            button_zespoly_dodaj.grid(row=4, column=0, columnspan=2)

            label_zespoly_opis = Label(ramka_zespoly_szczegoly, text='Szczegóły:', font=('Calibri', 14, 'italic'))
            label_zespoly_nazwa = Label(ramka_zespoly_szczegoly, text='Nazwa zespołu')
            label_zespoly_nazwa_wartosc = Label(ramka_zespoly_szczegoly, text='?', width=20)

            label_zespoly_koncert = Label(ramka_zespoly_szczegoly, text='Koncert zespołu')
            label_zespoly_koncert_wartosc = Label(ramka_zespoly_szczegoly, text='?', width=20)

            label_zespoly_srodek_szczegoly = Label(ramka_zespoly_szczegoly, text='Współrzędne siedziby')
            label_zespoly_lokalizacja_wartosc = Label(ramka_zespoly_szczegoly, text='?', width=20)

            label_zespoly_opis.grid(row=0, column=0, columnspan=8, pady=10)

            label_zespoly_nazwa.grid(row=1, column=0)
            label_zespoly_nazwa_wartosc.grid(row=2, column=0)

            label_zespoly_koncert.grid(row=3, column=0)
            label_zespoly_koncert_wartosc.grid(row=4, column=0)

            label_zespoly_srodek_szczegoly.grid(row=5, column=0)
            label_zespoly_lokalizacja_wartosc.grid(row=6, column=0)


            def klienci_wszystko():
                listbox_klienci.delete(0, END)
                sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()
                for idx, row in enumerate(wynik_zapytania):
                    listbox_klienci.insert(idx, f'Klient {row[1]}')

                id_klienci_update()

            def klienci_dodaj():
                imie = entry_klienci_imie.get()
                miasto = entry_klienci_miasto.get()
                koncert = entry_klienci_koncert.get()
                bilet = entry_klienci_bilet.get()

                sql_query_1 = f"INSERT INTO public.lista_klientow(id, imie, miejscowosc, koncert, bilet) VALUES ('{id_klienci()}', '{imie}', '{miasto}', '{koncert}', '{bilet}');"
                cursor.execute(sql_query_1)
                db_params.commit()

                entry_klienci_imie.delete(0, END)
                entry_klienci_miasto.delete(0, END)
                entry_klienci_koncert.delete(0, END)
                entry_klienci_bilet.delete(0, END)

                klienci_wszystko()

            def klienci_edytuj():
                sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i=listbox_klienci.index(ACTIVE)

                entry_klienci_imie.delete(0, END)
                entry_klienci_miasto.delete(0, END)
                entry_klienci_koncert.delete(0, END)
                entry_klienci_bilet.delete(0, END)

                entry_klienci_imie.insert(0, wynik_zapytania[i][1])
                entry_klienci_miasto.insert(0, wynik_zapytania[i][2])
                entry_klienci_koncert.insert(0, wynik_zapytania[i][3])
                entry_klienci_bilet.insert(0, wynik_zapytania[i][4])

                button_klienci_dodaj.config(text='Dodaj klienta', command=lambda: klienci_aktualizuj(i))

            def klienci_aktualizuj(i):
                sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                imie = entry_klienci_imie.get()
                miasto = entry_klienci_miasto.get()
                koncert = entry_klienci_koncert.get()
                bilet = entry_klienci_bilet.get()

                sql_query_2 = f"UPDATE public.lista_klientow SET imie='{imie}',miejscowosc='{miasto}', koncert='{koncert}', bilet='{bilet}' WHERE imie='{wynik_zapytania[i][1]}' and miejscowosc='{wynik_zapytania[i][2]}' and koncert='{wynik_zapytania[i][3]}' and bilet='{wynik_zapytania[i][4]}';"
                cursor.execute(sql_query_2)
                db_params.commit()

                button_klienci_dodaj.config(text='Dodaj klienta', command=koncerty_dodaj)

                entry_klienci_imie.delete(0, END)
                entry_klienci_miasto.delete(0, END)
                entry_klienci_koncert.delete(0, END)
                entry_klienci_bilet.delete(0, END)

                klienci_wszystko()

            def klienci_usuwanie():
                i = listbox_klienci.index(ACTIVE)

                sql_query_1 = f"DELETE FROM public.lista_klientow WHERE id='{i+1}';"
                cursor.execute(sql_query_1)
                db_params.commit()

                klienci_wszystko()

            def klienci_szczegoly():
                sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                i = listbox_klienci.index(ACTIVE)

                imie=wynik_zapytania[i][1]
                miasto=wynik_zapytania[i][2]
                koncert=wynik_zapytania[i][3]
                bilet=wynik_zapytania[i][4]

                label_klienci_imie_wartosc.config(text=imie)
                label_klienci_miejscowosc_wartosc.config(text=miasto)
                label_klienci_koncert_wartosc.config(text=koncert)
                label_klienci_bilet_szczegoly_wartosc.config(text=bilet)

            root_klienci=Frame(root_listy)
            root_klienci.grid(row=2, column=0)

            ramka_klienci_poczatek = Frame(root_klienci)
            ramka_klienci_lista = Frame(root_klienci)
            ramka_klienci_wprowadzanie = Frame(root_klienci)
            ramka_klienci_szczegoly = Frame(root_klienci)

            ramka_klienci_poczatek.grid(row=0, column=0, columnspan=2)
            ramka_klienci_lista.grid(row=1, column=0)
            ramka_klienci_wprowadzanie.grid(row=1, column=1)
            ramka_klienci_szczegoly.grid(row=1, column=2, columnspan=2)

            label_klienci_napis = Label(ramka_klienci_poczatek, text='Lista klientów', font=('Calibri', 20,'bold', 'italic'))
            button_pokaz_liste = Button(ramka_klienci_poczatek, text='Wszyscy klienci', command=klienci_wszystko)

            label_klienci_napis.grid(row=0, column=0, padx=(335 - label_koncerty_napis.winfo_reqwidth() / 2), pady=(10, 0))
            button_pokaz_liste.grid(row=1, column=0)

            listbox_klienci = Listbox(ramka_klienci_lista, width=50, height=5)
            button_klienci_szczegoly = Button(ramka_klienci_lista, text='Szczegóły', command=klienci_szczegoly)
            button_klienci_usuwanie = Button(ramka_klienci_lista, text='Usuń', command=klienci_usuwanie)
            button_klienci_edytuj = Button(ramka_klienci_lista, text='Edytuj', command=klienci_edytuj)

            listbox_klienci.grid(row=1, column=0, columnspan=3, pady=(10, 0))
            button_klienci_szczegoly.grid(row=2, column=0)
            button_klienci_usuwanie.grid(row=2, column=1)
            button_klienci_edytuj.grid(row=2, column=2)

            label_klienci_nowe = Label(ramka_klienci_wprowadzanie, text='Dodaj klienta:',
                                        font=('Calibri', 14, 'italic'))
            label_klienci_imie = Label(ramka_klienci_wprowadzanie, text='Imię klienta')
            label_klienci_miasto = Label(ramka_klienci_wprowadzanie, text='Miejscowość klienta')
            label_klienci_koncert = Label(ramka_klienci_wprowadzanie, text='Koncert z klientem')
            label_klienci_bilet = Label(ramka_klienci_wprowadzanie, text='Czy ma bilet (TAK/NIE)')

            entry_klienci_imie = Entry(ramka_klienci_wprowadzanie)
            entry_klienci_miasto = Entry(ramka_klienci_wprowadzanie)
            entry_klienci_koncert = Entry(ramka_klienci_wprowadzanie)
            entry_klienci_bilet = Entry(ramka_klienci_wprowadzanie)

            label_klienci_nowe.grid(row=0, column=0, columnspan=2)
            label_klienci_imie.grid(row=1, column=0, sticky=W)
            label_klienci_miasto.grid(row=2, column=0, sticky=W)
            label_klienci_koncert.grid(row=3, column=0, sticky=W)
            label_klienci_bilet.grid(row=4, column=0, sticky=W)

            entry_klienci_imie.grid(row=1, column=1, sticky=W)
            entry_klienci_miasto.grid(row=2, column=1, sticky=W)
            entry_klienci_koncert.grid(row=3, column=1, sticky=W)
            entry_klienci_bilet.grid(row=4, column=1, sticky=W)

            button_klienci_dodaj = Button(ramka_klienci_wprowadzanie, text='Dodaj klienta', command=klienci_dodaj)
            button_klienci_dodaj.grid(row=5, column=0, columnspan=2)

            label_klienci_opis = Label(ramka_klienci_szczegoly, text='Szczegóły:', font=('Calibri', 14, 'italic'))
            label_klienci_imie = Label(ramka_klienci_szczegoly, text='Imię klienta')
            label_klienci_imie_wartosc = Label(ramka_klienci_szczegoly, text='?', width=20)

            label_klienci_miejscowosc = Label(ramka_klienci_szczegoly, text='Miejscowość')
            label_klienci_miejscowosc_wartosc = Label(ramka_klienci_szczegoly, text='?', width=20)

            label_klienci_koncert = Label(ramka_klienci_szczegoly, text='Koncert')
            label_klienci_koncert_wartosc = Label(ramka_klienci_szczegoly, text='?', width=20)

            label_klienci_bilet_szczegoly = Label(ramka_klienci_szczegoly, text='Bilet')
            label_klienci_bilet_szczegoly_wartosc = Label(ramka_klienci_szczegoly, text='?', width=20)

            label_klienci_opis.grid(row=0, column=0, columnspan=8, pady=10)

            label_klienci_imie.grid(row=1, column=0)
            label_klienci_imie_wartosc.grid(row=2, column=0)

            label_klienci_miejscowosc.grid(row=3, column=0)
            label_klienci_miejscowosc_wartosc.grid(row=4, column=0)

            label_klienci_koncert.grid(row=5, column=0)
            label_klienci_koncert_wartosc.grid(row=6, column=0)

            label_klienci_bilet_szczegoly.grid(row=7, column=0)
            label_klienci_bilet_szczegoly_wartosc.grid(row=8, column=0)

            root_koncerty.mainloop()


        def mapa():

            def mapa_koncerty():
                sql_query_1 = f"SELECT * FROM public.lista_koncertow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                mapka = TkinterMapView(ramka_mapa, width=700, height=400, corner_radius=0)
                mapka.set_position(52.2, 21.0)
                mapka.set_zoom(6)
                mapka.grid(row=7, column=0, columnspan=3, padx=10, pady=(10, 0))

                for row in wynik_zapytania:
                    wsp=get_coordinates(row[2])
                    mapka.set_marker(wsp[0], wsp[1], text=f'{row[1]}', font=('Calibri', 10, 'italic'), text_color='red')

            def mapa_klienci():
                sql_query_1 = f"SELECT * FROM public.lista_klientow ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                mapka = TkinterMapView(ramka_mapa, width=700, height=400, corner_radius=0)
                mapka.set_position(52.2, 21.0)
                mapka.set_zoom(6)
                mapka.grid(row=7, column=0, columnspan=3, padx=10, pady=(10, 0))

                for row in wynik_zapytania:
                    miasto=get_coordinates(row[2])
                    mapka.set_marker(miasto[0], miasto[1], text=f'{row[1]}', font=('Calibri', 10, 'italic'), text_color='red')

            def mapa_klienci_koncertu():
                koncert=entry_mapka_koncert.get()

                sql_query_1 = f"SELECT * FROM public.lista_klientow WHERE koncert='{koncert}' ORDER BY id ASC;"
                cursor.execute(sql_query_1)
                wynik_zapytania = cursor.fetchall()

                mapka = TkinterMapView(ramka_mapa, width=700, height=400, corner_radius=0)
                mapka.set_position(52.2, 21.0)
                mapka.set_zoom(6)
                mapka.grid(row=7, column=0, columnspan=3, padx=10, pady=(10, 0))

                for row in wynik_zapytania:
                    miasto=get_coordinates(row[2])
                    mapka.set_marker(miasto[0], miasto[1], text=f'{row[1]}\nKoncert {row[3]}', font=('Calibri', 10, 'italic'), text_color='red')

            root_mapy = Toplevel(root_wybieranie)
            root_mapy.title('Mapy wydarzeń muzycznych')
            root_mapy.geometry(f'800x600')

            ramka_mapa=Frame(root_mapy)
            ramka_mapa.grid(row=0, column=0)

            label_mapka_wejscie = Label(ramka_mapa, text='Mapy koncertów', font=('Calibri', 12, 'italic'))
            label_mapka_wybierz = Label(ramka_mapa, text='Wybierz mapę:')
            label_mapka_koncerty_wsz = Label(ramka_mapa, text='Mapa wszystkich koncertów')
            button_mapka_koncerty_wsz = Button(ramka_mapa, text='Pokaż', command=mapa_koncerty)
            label_mapka_klienci = Label(ramka_mapa, text='Mapa wszystkich klientów')
            button_mapka_klienci = Button(ramka_mapa, text='Pokaż', command=mapa_klienci)
            label_mapka_klienci_koncert = Label(ramka_mapa, text='Mapa klientów danego koncertu')
            label_mapka_koncert = Label(ramka_mapa, text='Koncert')
            entry_mapka_koncert = Entry(ramka_mapa)
            button_mapka_klienci_koncert = Button(ramka_mapa, text='Pokaż', command=mapa_klienci_koncertu)

            label_mapka_wejscie.grid(row=0, column=0, columnspan=3, pady=(10, 0))
            label_mapka_wybierz.grid(row=1, column=0, columnspan=3)
            label_mapka_koncerty_wsz.grid(row=2, column=0, sticky=W)
            button_mapka_koncerty_wsz.grid(row=2, column=1, sticky=E)
            label_mapka_klienci.grid(row=3, column=0, sticky=W)
            button_mapka_klienci.grid(row=3, column=1, sticky=E)
            label_mapka_klienci_koncert.grid(row=4, column=0, sticky=W)
            label_mapka_koncert.grid(row=5, column=0, sticky=W)
            entry_mapka_koncert.grid(row=5, column=0, padx=50, sticky=W)
            button_mapka_klienci_koncert.grid(row=5, column=1, sticky=E)

            root_mapy.mainloop()

        root_wybieranie=Toplevel(root_pass)
        root_wybieranie.title('Wydarzenia muzyczne - funkcje')
        root_wybieranie.geometry('315x95')

        ramka_wybieranie=Frame(root_wybieranie)
        ramka_wybieranie.grid(row=0, column=0, padx=55)

        label_wybor_opcje=Label(ramka_wybieranie, text='Wybierz funkcję:')
        label_wybor_remonty=Label(ramka_wybieranie, text='Listy wydarzeń muzycznych')
        label_wybor_mapa=Label(ramka_wybieranie, text='Mapy wydarzeń muzycznych')
        button_wybor_remonty=Button(ramka_wybieranie, text='Kliknij', command=koncerty)
        button_wybor_mapa=Button(ramka_wybieranie, text='Kliknij', command=mapa)

        label_wybor_opcje.grid(row=0, column=0, columnspan=2)
        label_wybor_remonty.grid(row=1, column=0, sticky=W)
        label_wybor_mapa.grid(row=3, column=0, sticky=W)
        button_wybor_remonty.grid(row=1, column=1, sticky=E)
        button_wybor_mapa.grid(row=3, column=1, sticky=E)

        root_wybieranie.mainloop()

    else:
        logowanko_entry.delete(0, END)
        logowanko_entry.focus()

root_pass=Tk()
root_pass.title('Wydarzenia muzyczne - logowanie')
root_pass.geometry('400x95')

ramka_logowanko=Frame(root_pass)
ramka_logowanko.grid(row=0, column=0, padx=125)

logowanko_napis=Label(ramka_logowanko, text='Wpisz hasło')
logowanko_entry=Entry(ramka_logowanko, width=20, show='*')
logowanko_entry.bind('<Return>', logowanko)
logowanko_button=Button(ramka_logowanko, text='OK', command=logowanko)

logowanko_napis.grid(row=0, column=0, columnspan=2)
logowanko_entry.grid(row=1, column=0, padx=(3,0))
logowanko_button.grid(row=1, column=1, columnspan=2)

root_pass.mainloop()


