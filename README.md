# Klient bazy danych

### Opis zadania

- Program udający klienta bazy danych, pozwalający na utworzenie/usunięcie tabeli, dodawanie/usuwanie wpisów w niej, oraz wyszukanie danych.
- Możliwe utworzenie tabeli o dowolnej liczbie kolumn, każda kolumna zawierająca
- dane typu _liczba całkowita_ albo _liczba rzeczywista_ albo _tekst._
- Typ _liczba_ _całkowita_ pozwala na przechowywanie liczb całkowitych (pythonowy _int)._
- Typ _liczba rzeczywista_ pozwala na przechowywanie liczb rzeczywistych (pythonowy _float)._
- Typ _tekst_ pozwala na przechowywanie dowolnego tekstu (domyślny typ tekstowy
- pythona).
- Nazwy tabel i kolumn nie mogą być puste (muszą zawierać przynajmniej jeden znak drukowalny).
- Główne okno powinno powinno posiadać listę tabel znajdujących się w bazie danych, listę wpisów w zaznaczonej tabeli (lista lub dowolny czytelny sposób prezentacji danych), oraz przyciski &quot;Dodaj tabelę&quot;, &quot;Usuń tabelę&quot;, &quot;Dodaj wiersz&quot;, &quot;Usuń wiersz&quot; i &quot;Wyszukaj w tabeli&quot;.
- Okno dodawania tabeli powinno pozwalać na wpisanie nazwy tabeli oraz dodanie kolumn (nazwa i typ).
- Okno dodawania wiersza powinno wyświetlać nazwy kolumn i pola tekstowe służące wpisaniu danych. Walidacja typów wpisanych danych powinna odbywać się przy próbie dodania wiersza (np. Jeśli pole tekstowe kolumny typu _liczba całkowita_ zawiera tekst nie rzutujący się na liczbę całkowitą, to powinien zostać wyświetlony błąd - okienko, znacznik na polu tekstowym lub inne).
- Przed usunięciem tabeli/wiersza użytkownik powinien być proszony o potwierdzenie.
- Okno wyszukiwania powinno zawierać pole tekstowe, do którego wpisywany jest kod lambda-wyrażenia zwracającego prawdę lub fałsz i przyjmującego jeden argument - słownik _kolumna:wartość._ Lambda ta jest wywoływana dla każdego wiersza wybranej tabeli, wyświetlane są wiersze dla których lambda zwróci prawdę. Przykładowo: wpisanie &quot;lambda row: row[&quot;ID&quot;]\>5 or row[&quot;ocena&quot;]\<3&quot; zwróci wszystkie wiersze których kolumna &quot;ID&quot; ma wartość większą od 5 lub kolumna &quot;ocena&quot; ma wartość mniejszą od 3.
- Wynik wyszukiwania powinien być wyświetlony w oknie wyszukiwania (np. po utracie
focusa w polu tekstowym, po wciśnięciu przycisku wyszukiwania, po każdej edycji).
- **Na wyższą ocenę:** Po zamknięciu programu dane (tabele i ich zawartość)
powinny być zapisywane na dysk, a po jego uruchomieniu wczytywane.

### Testy

1. Utworzenie tabeli &quot;testi&quot; z kolumnami liczbową &quot;ID&quot; (typ _int),_ dwoma tekstowymi &quot;imię&quot; oraz &quot;nazwisko&quot; oraz liczbową &quot;wzrost&quot; (typ _float_).
2. Dodanie wiersza do tabeli &quot;testi&quot; z danymi &quot;1&quot;, &quot;Roch&quot;, &quot;Przyłbipięt&quot;, &quot;1.50&quot; -oczekiwane powodzenie.
3. Dodanie wiersza do tabeli &quot;testi&quot; z danymi &quot;2&quot;, &quot;Ziemniaczysław&quot;, &quot;Bulwiasty&quot;, &quot;1.91&quot; - oczekiwane powodzenie.
4. Dodanie wiersza do tabeli &quot;testi&quot; z danymi &quot;cztery&quot;, &quot;bla&quot;, &quot;bla&quot;, &quot;-90&quot; - oczekiwane niepowodzenie (dane tekstowe w polu liczbowym).
2. Dodanie wiersza do tabeli &quot;testi&quot; z danymi &quot;3.14&quot;, &quot;pi&quot;: ludolfina&quot;, &quot;314e-2&quot; -oczekiwane niepowodzenie (liczba rzeczywista w kolumnie z liczbę całkowitą).
3. Wyświetlenie zawartości tabeli dtest1&quot;.
4. Dodanie trzech kolejnych wierszy do tabeli &quot;testi&quot; i usunięcie dwóch wierszy z niej (pierwszego i środkowego), w obu przypadkach najpierw anulowanie operacji, a potem jej akceptacja.
5. Utworzenie tabeli &quot;test2&quot; z kolumnami &quot;reserved&quot; typu _stringoraz_ &quot;kolor typu _liczba_ _całkowita._
6. Dodanie wiersza do tabeli &quot;test2&quot; z danymi (puste pole), &quot;1337&quot; - oczekiwane powodzenie.
7. Dodanie wiersza do tabeli &quot;test2&quot; z danymi &quot;bla&quot;, &quot;1939b&quot; - oczekiwane niepowodzenie (tekst w polu typu _liczba całkowita)._
8. Usunięcie tabeli &quot;test2&quot;, najpierw anulowanie operacji, a potem jej akceptacja.
9. Próba utworzenia tabeli bez nazwy - oczekiwane niepowodzenie.
10. Próba utworzenia tabeli o nazwie &quot; &quot; (spacja) - oczekiwane niepowodzenie.
11. Próba utworzenia tabeli z kolumną bez nazwy - oczekiwane niepowodzenie.
12. Próba utworzenia tabeli z kolumną o nazwie &quot; &quot; (cztery spacje) - oczekiwane niepowodzenie,
13. Wypełnij tabelę &quot;testi&quot; danymi testowymi (kolejne wartości &quot;ID, &quot;wzrost&quot; między 1.0 i 2.0) , wyszukaj wiersze dla których &quot;wzrost&quot; ma wartość podaną przez prowadzącego oraz &quot;ID&quot; jest liczbą parzystą lub nieparzystą (zależnie od woli prowadzącego).


## Przykłady

Tworzenie tabel

![image](https://user-images.githubusercontent.com/17951356/173257792-3f4d3bd1-704e-493e-9ffb-775d98201234.png)

Walidacja

![image](https://user-images.githubusercontent.com/17951356/173257796-9ffa2e11-a8d8-49ac-8e0b-a3e8fc752633.png)

Filtrowanie

![image](https://user-images.githubusercontent.com/17951356/173257797-f414b767-b8db-41b2-bf14-9c0f73b3ec29.png)
