Welcome to Text Adventure Game's documentation!
===============================================
Zadanie
=======
Jako zadanie dostałem do zrealizowania program, który pozwala:


Zrealizować program pozwalający graczowi na poruszanie się po opisanej tekstem mapie, walkę z przeciwnikami, podnoszenie przedmiotów etc. ("text adventure game").

Gracz powinien wydawać polecenia tekstowo (np. "idę na północ", albo "go west", czy "attack goblin", ale też "look around"). Na mapie powinny być przedmioty niezbędne do dostania się do innych obszarów świata ("klucze"), które gracz może jakoś zdobywać ("pickup key", "buy gem").

Mapa powinna być wczytywalna z pliku, gdzie możliwa byłaby pełna konfiguracja świata: * rodzaje lokalizacji z ich opisem tekstowym, * sąsiedztwo (graf) lokalizacji (co jest "na północ", czy "za mostem"), * przedmioty - ich położenie i wpływ na odblokowywanie lokalizacji, * przeciwnicy i ich siła itp.

Rodzaje poleceń obsługiwanych przez grę powinny umożliwiać w miarę "naturalną" interakcję ze światem, ale mogą (a nawet muszą - ze względu na złożoność języka naturalnego) być ograniczone do określonego zestawu komend.

Gracz powinien móc zapisać i odtworzyć stan gry.


Konfiguracja
============

Aby dodać nową grę należy:

1) Stworzyć folder w folderze configuration - nazwa tego folderu będzie wykorzystana jako nazwa gry, wszystkie pliki konfiguracyjne należy umieścić w tym folderze

2) Należy stworzyć plik player.json który będzie zawierał informację o graczu

Przykładowe gracz:

    {
        "base_health": 100,

        "health": 100,

        "strength": 10,

        "weapon":{

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
        }]
    }

3) Należy stworzyć plik fields.json który będzie zawierał listę pól na planszy, pola mają być opisane jsonem, tutaj też do pól należy przydzielić wrogów i przedmioty które można podnosić

    [
        {
            "name": "Dangerous Paved Road",

            "description": "A road paved with stones.\nAnd what's behind this cart?\nIt's a Mighty White Dragon",

            "danger": -10,

            "enemy":{
                "name": "Mighty White Dragon",

                "base_health": 200,

                "health": 200,

                "regeneration": 50,

                "strength": 20,

                "random_strength": 20,

                "shouts": ["What a small little human!", "I eat people like you for breakfast!"],

                "description": "Mighty White Dragon is a guardian of the Castle"
            },

            "item":{

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

4) Należy stworzyć plik lvl1.txt w którym będą umieszczone indeksy pól z pliku fields.json, sąsiadujące pola mają być oddzielone tabami, całość ma mieć kształt prostokąta

5) Aby wprowadzić gracza w historię należy stworzyć dodatkowo plik introduction.txt, zawartość tego pliku będzie wyświetlona graczowi od razu po rozpoczęciu nowej gry


Graj
====

1) Aby zagrać należy odpalić plik main.py
2) Dalej zostanie się poprowadzonym przez program -> cały czas będą wyświetlane dostępne dla gracza komendy


