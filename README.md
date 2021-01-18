# **Welcome to Text Adventure Game's readme!**

# Informacje o projekcie

**Projekt:** _Text Adventure Game_

**Twórca:** _Bartłomiej Krawczyk_

**Przedmiot:** _Podstawy Informatyki i Programowania_

# Zadanie

Zrealizować program pozwalający graczowi na poruszanie się po opisanej tekstem mapie, walkę z przeciwnikami, podnoszenie przedmiotów etc. ("text adventure game").

Gracz powinien wydawać polecenia tekstowo (np. "idę na północ", albo "go west", czy "attack goblin", ale też "look around"). Na mapie powinny być przedmioty niezbędne do dostania się do innych obszarów świata ("klucze"), które gracz może jakoś zdobywać ("pickup key", "buy gem").

Mapa powinna być wczytywalna z pliku, gdzie możliwa byłaby pełna konfiguracja świata: _ rodzaje lokalizacji z ich opisem tekstowym, _ sąsiedztwo (graf) lokalizacji (co jest "na północ", czy "za mostem"), _ przedmioty - ich położenie i wpływ na odblokowywanie lokalizacji, _ przeciwnicy i ich siła itp.

Rodzaje poleceń obsługiwanych przez grę powinny umożliwiać w miarę "naturalną" interakcję ze światem, ale mogą (a nawet muszą - ze względu na złożoność języka naturalnego) być ograniczone do określonego zestawu komend.

Gracz powinien móc zapisać i odtworzyć stan gry.

# Funkcjonalności Krytyczne

### Gra tekstowa:

- Poruszanie się gracza po mapie opisanej tekstem
- Program ma reagować na polecenia tekstowe - w każdym ruchu gracz ma wyświetlone dostępne aktualnie komendy
- Gracz ma dostęp do mapy - grafu lokalizacji
- Walka z przeciwnikami
- Podnoszenie przedmiotów
- Gracz ma możliwość używania przedmiotów:
  - `kluczy` - na polu z wejściem można użyć odpowiedniego klucza aby otworzyć nową lokalizację
  - `broni` - włożenie broni w slot z bronią - zwiększa bazową siłę
  - `zbroi` - włożenie zbroi w slot ze zbroją - redukuje zadawane obrażenia
  - `eliksirów` - natychmiastowe leczenie

### Konfiguracja:

- Możliwa pełna konfiguracja świata
- Wczytywanie różnych lokalizacji, przedmiotów oraz wrogów
- Wczytywanie gracza
- Możliwość edycji historii gry z poziomu konfiguracji
- Możliwość dodawania własnych gier

### Zapis:

- Możliwość zapisu stanu gry
- Możliwość wczytania zapisanego stanu gry

# Podstawowe działanie programu

### Program podzielony jest na moduły:

#### **Główne:**

- **[Main](./main.py)** - główny moduł - inicjuje klasę [Game](./game.py), a następnie w pętli wywołuje jej metodę round().
- **[Game](./game.py)** - główna klasa - śledzi stan gry - trzyma informacje o graczu oraz odwiedzonych przez niego lokalizacjach.

- **Location:** - moduł odpowiadający za informacje o lokalizacji.

  - **[Location](./location/location.py)** - zawiera macierz pól danej lokalizacji.
  - **[Field](./location/field.py)** - zawiera informacje o danym polu, przedmiot na nim znajdujący się oraz wroga.

- **Entities:** - moduł odpowiadający za postaci oraz przedmioty.
  - **[Player](./entities/player.py)** - klasa odpowiadająca za trzymanie informacji o graczu.
  - **[Enemy](./entities/enemy.py)** - klasa odpowiadająca za trzymanie informacji o wrogu.
  - **[Equipment](./entities/equipment.py)** - klasa odpowiadająca za trzymanie informacji o przedmiotach.

#### **Poboczne:**

- [Setup](./setup.py) - klasa poboczna - umożliwia wstępne zainicjowanie klasy game oraz wprowadzenie w historię gry.
- Utils:
  - [Format](./utils/format.py) - funkcje do formatowania i wyświetlania ładnych ładnych wizualnie ozdób/przerywników.
  - [IO](./utils/io.py) - zawiera metody do zapisu i odczytu plików z konfiguracji oraz zapisów.
  - [Player Input](./utils/player_input.py) - zawiera metody któr będą wymagały inputu od gracza - zapętlają zapytanie dopóki nie dostaną poprawnego inputu od gracza.

# Graj

1. Aby zagrać należy odpalić plik [main.py](./main.py).
2. Dalej zostanie się poprowadzonym przez program -> cały czas będą wyświetlane dostępne dla gracza komendy.
   1. Należy wybrać nową grę / załadować poprzedni zapis.
   2. Korzystając z dostępnych komend postarać się dostać do pola opisanego literą `G` - jest to pole, które jest bramą do kolejnej lokalizacji lub polem na którego wejście kończy grę.
3. Rozgrywkę kończy użycie komendy `Exit` lub dotarcie do pola wygrywającego.

# Konfiguracja

Aby dodać nową grę należy:

1. Stworzyć folder w folderze configuration - nazwa tego folderu będzie wykorzystana jako nazwa gry, wszystkie pliki konfiguracyjne należy umieścić w tym folderze.

2. Należy stworzyć plik player.json który będzie zawierał informację o graczu.

Przykładowy gracz:

```json
{
  "base_health": 100,
  "health": 100,
  "strength": 10,
  "weapon": {
    "class": "Weapon",
    "name": "Wooden Sword",
    "description": "Simple sword",
    "base_strength": 1,
    "random_strength": 5
  },
  "equipment_size": 10,
  "equipment": [
    {
      "class": "Potion",
      "name": "Health Potion",
      "description": "",
      "health": 100
    }
  ]
}
```

3. Należy stworzyć plik fields.json który będzie zawierał listę pól na planszy, pola mają być opisane jsonem, tutaj też do pól należy przydzielić wrogów i przedmioty które można podnosić.

```json
[
  {
    "name": "Dangerous Paved Road",
    "description": "A road paved with stones.\nAnd what's behind this cart?\nIt's a Mighty White Dragon",
    "danger": -10,
    "enemy": {
      "name": "Mighty White Dragon",
      "base_health": 200,
      "health": 200,
      "regeneration": 50,
      "strength": 20,
      "random_strength": 20,
      "shouts": [
        "What a small little human!",
        "I eat people like you for breakfast!"
      ],
      "description": "Mighty White Dragon is a guardian of the Castle"
    },

    "item": {
      "class": "Weapon",
      "name": "King's Sword",
      "description": "It's base strength is equal to 25, but random buff is 100 :o",
      "base_strength": 25,
      "random_strength": 100
    },
    "enterable": true,
    "seen": false,
    "go_to": 0
  }
]
```

4. Należy stworzyć plik lvl1.txt w którym będą umieszczone indeksy pól z pliku fields.json, sąsiadujące pola mają być oddzielone tabami, całość ma mieć kształt prostokąta.

```
15	14	0	0	0	0	0	12	12	11	11
14	14	14	0	0	8	8	8	8	8	11
14	14	14	0	0	8	6	6	6	6	6
0	14	14	14	0	8	6	7	7	7	7
0	0	14	14	0	8	6	7	7	7	5
0	0	0	8	8	1	2	2	2	3	4
0	0	8	8	0	8	6	7	7	7	5
8	8	8	0	0	8	6	7	7	7	7
8	0	0	0	0	8	6	6	6	6	6
8	0	0	0	0	8	8	8	8	9	10
13	0	0	0	0	12	12	12	12	10	10

```

5. Podobnie można tworzyć kolejne lokalizacje należy je będzie nazwać tak jak nazwa podawana w przedmiocie - kluczu, który otwiera daną lokalizację.

6. Aby wprowadzić gracza w historię należy stworzyć dodatkowo plik introduction.txt, zawartość tego pliku będzie wyświetlona graczowi od razu po rozpoczęciu nowej gry.

# Zapis

W trakcie gry gdy gracz znajduje się poza walką ma możliwość zapisania stanu gry.

Należy użyć komendy `Save`, a następnie podać nazwę pliku pod jaką ma zostać zapisany postęp.
Gra zapisywana jest w formanie json.

# Odczyt

Aby odczytać zapis należy uruchomić program na nowo i wybrać opcję `Load from file`.

Następnie wskazać numer wybranego pliku z zapisanym postępem.

# Docstring

Resztę dokumentacji można znaleźć [tutaj](./documentation/index.html) lub pośrednio można otworzyć ją w przeglądarce poprzez plik index.html znajdujący się w folderze documentation.

# Podsumowanie

Wydaje mi się, że wszystkie założenia zadania udało mi się wypełnić.

Jestem zadowolony z efektów jakie osiągnąłem, oraz z ciekawej historii jaką udało mi się przekazać w grze `Dungeons and Dragons`.
