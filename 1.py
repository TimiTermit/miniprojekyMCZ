import słowniki
import random
import uuid

def listak():
    print("WITAJ")
    for el in słowniki.książki:
        print(el["nazwa"])

def listau():
    for el in słowniki.users:
        print("---"*5)
        print(el["imie"])
        print(el["nazwisko"])

def legendak():
    print("j - Wyświetl listę pracowników")
    print("k - Zmień stanowisko pracownika")
    print("a - Wyświetl listę książek dostępnych w bibliotece")
    print("b - Sprawdź szczegółowe dane konkretnej książki")
    print("c - Wyświetl listę użytkowników biblioteki")
    print("d - Wypożycz książkę")
    print("e - Zwróć książkę")
    print("f - Dodaj nowego użytkownika do systemu")
    print("g - Usuń książkę z biblioteki")
    print("h - Przywróć usuniętą książkę")
    print("i - Napraw uszkodzoną książkę")
    print("l - Filtruj książki według liczby stron")

def wypozyczksiazke(users, ksiazki, imie, nazwisko, nazwaksiazki, pracownik):
    for user in users:
        if user["imie"] == imie and user["nazwisko"] == nazwisko:
            break
    else:
        print(f"Użytkownik {imie} {nazwisko} nie istnieje.")
        return
    if len(user["eku"]) >= user["maxlk"]:
        print(f'Użytkownik {imie} {nazwisko} osiągnął limit wypożyczonych książek ({user["maxlk"]}).')
        return
    for ksiazka in ksiazki:
        if ksiazka["nazwa"] == nazwaksiazki:
            break
    else:
        print(f'Książka "{nazwaksiazki}" nie istnieje.')
        return
    if ksiazka["status"] == "wypożyczona":
        print(f'Książka "{nazwaksiazki}" jest już wypożyczona.')
        return
    if ksiazka["status"] == "uszkodzona":
        print(f'Książka "{nazwaksiazki}" jest uszkodzona i nie może być wypożyczona.')
        return
    ksiazka["status"] = "wypożyczona"
    user["ilosczksiazek"] += 1
    pracownik["wypozyczoneksiazki"] += 1
    user["eku"].append(nazwaksiazki)
    print(f'Użytkownik {imie} {nazwisko} wypożyczył książkę "{nazwaksiazki}".')

def zwrocksiazke(users, ksiazki, imie, nazwisko, nazwaksiazki):
    for user in users:
        if user["imie"] == imie and user["nazwisko"] == nazwisko:
            break
    else:
        print(f"Użytkownik {imie} {nazwisko} nie istnieje.")
        return
    
    if nazwaksiazki not in user["eku"]:
        print(f'Użytkownik {imie} {nazwisko} nie ma książki "{nazwaksiazki}".')
        return
    
    for ksiazka in ksiazki:
        if ksiazka["nazwa"] == nazwaksiazki:
            break
    else:
        print(f'Książka "{nazwaksiazki}" nie istnieje w systemie.')
        return
    
    user["eku"].remove(nazwaksiazki)
    user["ilosczksiazek"] -= 1
    ksiazka["zuzycie"] -= 1
    
    if ksiazka["zuzycie"] <= 0:
        ksiazka["status"] = "uszkodzona"
        print(f'Książka "{nazwaksiazki}" została zwrócona, ale jest uszkodzona.')
    else:
        ksiazka["status"] = "dostępna"
        print(f'Użytkownik {imie} {nazwisko} zwrócił książkę "{nazwaksiazki}".')
        
def hasło():
    r = random.randint(0,22)
    l = random.randint(0,76)
    o = random.randint(0,47)
    i = random.randint(55,66)
    haslo = f"{r}{l}{o}{i}"
    print("-"*10)
    print(f"hasło = {haslo}")
    print("-"*10)
    t = input('wprowadź hasło')
    if t == haslo:  
        print("Prawda")
        return True
    else:
        print("Fałsz")
        return False

def daneksiążki():
    u = input("Jakie książki chcesz sprawdzić: ")
    for el in słowniki.książki:
        if el["nazwa"] == u:
            print(f"\nDane książki {u}:")
            for k, v in el.items():
                print(f"{k}: {v}")
            print("-" * 20)  

def dodajksiazke(ksiazki, nazwa, strony,zuzycie):
    nowaksiazka = {
        "nazwa": nazwa,
        "id": uuid.uuid4(),
        "status": "dostępna",
        "strony": strony,
        "zuzycie": zuzycie
    }
    ksiazki.append(nowaksiazka)
    print(f'Książka "{nazwa}" została dodana do biblioteki.')

def usunksiazke(ksiazki, nazwaksiazki,usunieteksiazki):
    for ksiazka in ksiazki:
        if ksiazka["nazwa"] == nazwaksiazki:
            usunieteksiazki.append(ksiazka) 
            ksiazki.remove(ksiazka)
            print(f'Książka "{nazwaksiazki}" została usunięta.')
            return
    print(f'Książka "{nazwaksiazki}" nie została znaleziona.')

def usunksiazkepoid(ksiazki, idksiazki,usunieteksiazki):
    for ksiazka in ksiazki:
        if ksiazka["id"] == idksiazki:
            usunieteksiazki.append(ksiazka)  
            ksiazki.remove(ksiazka)
            print(f'Książka o ID {idksiazki} została usunięta.')
            return
    print(f'Nie znaleziono książki o ID {idksiazki}.')

def rodzajeusuniecia():
    print("Dostępne sposoby usunięcia książki:")
    print("1. Usunięcie książki po nazwie")
    print("2. Usunięcie książki po ID")

def przywroksiazke(ksiazki, usunieteksiazki, idksiazki):
    for ksiazka in usunieteksiazki:
        if ksiazka["id"] == idksiazki:
            ksiazki.append(ksiazka)  
            usunieteksiazki.remove(ksiazka)  
            print(f'Książka "{ksiazka["nazwa"]}" została przywrócona.')
            return
    print(f'Nie znaleziono książki o ID {idksiazki} w usuniętych książkach.')
# uwaga na len
def rodzajedodania():
    print("\nMożesz dodać książkę na dwa sposoby:")
    print("1. Dodaj nową książkę do listy.")
    print("2. Przywróć książkę z listy usuniętych.")

def rodzajeprzywrocenia():
    print("\nMożesz przywrócić książkę na dwa sposoby:")
    print("1. Przywróć książkę z listy usuniętych na podstawie ID.")
    print("2. Przywróć książkę z listy usuniętych na podstawie nazwy.")

def przywroksiazke2(ksiazki, usunieteksiazki, nazwaksiazki):
    for ksiazka in usunieteksiazki:
        if ksiazka["nazwa"] == nazwaksiazki:
            ksiazki.append(ksiazka)
            usunieteksiazki.remove(ksiazka)
            print(f'Książka "{nazwaksiazki}" została przywrócona.')
            return
    print(f'Nie znaleziono książki o nazwie "{nazwaksiazki}" w usuniętych książkach.')

def kpostronach(ksiazki, lstron):
    krotsze = []
    dluzsze = []
    for k in ksiazki:
        if k["strony"] < lstron:
            krotsze.append(k)
        else:
            dluzsze.append(k)
    print(f'\nKsiążki krótsze niż {lstron} stron:')
    for ksiazka in krotsze:
        print(f'- {ksiazka["nazwa"]} ({ksiazka["strony"]} stron)')
    print(f'\nKsiążki dłuższe lub równe {lstron} stron:')
    for ksiazka in dluzsze:
        print(f'- {ksiazka["nazwa"]} ({ksiazka["strony"]} stron)')

def naprawksiazke(ksiazki, nazwaksiazki):
    for ksiazka in ksiazki:
        if ksiazka["nazwa"] == nazwaksiazki:
            if ksiazka["status"] == "uszkodzona":
                ksiazka["zuzycie"] = 10
                ksiazka["status"] = "dostępna"
                print(f'Książka "{nazwaksiazki}" została naprawiona i jest teraz dostępna.')
            else:
                print(f'Książka "{nazwaksiazki}" nie jest uszkodzona, więc nie wymaga naprawy.')
            return
    print(f'Książka "{nazwaksiazki}" nie istnieje w systemie.')

def listapracownikow():
    for el in słowniki.pracownicy:
        print("---"*5)
        print(el["imie"])
        print(el["nazwisko"])
        print(el["stanowisko"])

def awans(pracownicy, imie, nazwisko, nstanowisko):
    for pracownik in pracownicy:
        if pracownik["imie"] == imie and pracownik["nazwisko"] == nazwisko:
            pracownik["stanowisko"] = nstanowisko
            print(f'Stanowisko pracownika {imie} {nazwisko} zostało zmienione na "{nstanowisko}".')
            return
    print(f'Nie znaleziono pracownika {imie} {nazwisko}.')

def dodajużytkownika(users, imie, nazwisko, maxlk):
    for user in users:
        if user["imie"] == imie and user["nazwisko"] == nazwisko:
            print(f'Użytkownik {imie} {nazwisko} już istnieje w systemie.')
            return
    nowyużytkownik = {
        "imie": imie,
        "nazwisko": nazwisko,
        "maxlk": maxlk,  
        "ilosczksiazek": 0,
        "eku": []  
    }
    users.append(nowyużytkownik)
    print(f'Dodano nowego użytkownika: {imie} {nazwisko}.')

if hasło():
    while True:
        print("\nWybierz pracownika:")
        for i in range(len(słowniki.pracownicy)):
            print(f"{i}. {słowniki.pracownicy[i]['imie']} {słowniki.pracownicy[i]['nazwisko']}")

        wybor = input("Numer pracownika (q = wyjście): ")

        if wybor == 'q':  
            break 

        if wybor.isdigit():  
            nr = int(wybor)
            if 0 <= nr < len(słowniki.pracownicy):  
                pracownik = słowniki.pracownicy[nr]  
                print(f"\nWybrano pracownika: {pracownik['imie']} {pracownik['nazwisko']}")
                
                while True:
                    legendak()
                    opcja = input("\nWybierz opcję: ")
                    
                    if opcja == 'a':
                        listak()
                    elif opcja == 'b':
                        daneksiążki()
                    elif opcja == 'c':
                        listau()
                    elif opcja == 'd':
                        imie = input("Imię użytkownika: ")
                        nazwisko = input("Nazwisko użytkownika: ")
                        nazwaksiazki = input("Nazwa książki: ")
                        wypozyczksiazke(słowniki.users, słowniki.książki, imie, nazwisko, nazwaksiazki, pracownik)
                    elif opcja == 'e':
                        imie = input("Imię użytkownika: ")
                        nazwisko = input("Nazwisko użytkownika: ")
                        nazwaksiazki = input("Nazwa książki: ")
                        zwrocksiazke(słowniki.users, słowniki.książki, imie, nazwisko, nazwaksiazki)
                    elif opcja == 'f':
                        imie = input("Imię nowego użytkownika: ")
                        nazwisko = input("Nazwisko nowego użytkownika: ")
                        maxlk = int(input("Maksymalna liczba książek: "))
                        dodajużytkownika(słowniki.users, imie, nazwisko, maxlk)
                    elif opcja == 'g':
                        nazwaksiazki = input("Nazwa książki do usunięcia: ")
                        usunksiazke(słowniki.ksiazki, nazwaksiazki, słowniki.usunieteksiazki)
                    elif opcja == 'h':
                        idksiazki = input("ID książki do przywrócenia: ")
                        przywroksiazke(słowniki.ksiazki, słowniki.usunieteksiazki, idksiazki)
                    elif opcja == 'i':
                        nazwaksiazki = input("Nazwa książki do naprawy: ")
                        naprawksiazke(słowniki.książki, nazwaksiazki)
                    elif opcja == 'l':
                        lstron = int(input("Podaj liczbę stron: "))
                        kpostronach(słowniki.książki, lstron)
                    elif opcja == 'j': 
                        listapracownikow()
                    elif opcja == 'k': 
                        imie = input("Imię pracownika: ")
                        nazwisko = input("Nazwisko pracownika: ")
                        nowe_stanowisko = input("Nowe stanowisko: ")
                        awans(słowniki.pracownicy, imie, nazwisko, nowe_stanowisko)
                    elif opcja == 'q':
                        print("Wylogowano pracownika.")
                        break
                    else:
                        print("Niepoprawna opcja, spróbuj ponownie.")
            else:
                print("Niepoprawny numer pracownika, spróbuj ponownie.")
        else:
            print("Niepoprawny wybór. Wpisz numer pracownika.")
else:
    print("Niepoprawne hasło. Program zakończony.")
