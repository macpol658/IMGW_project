Sprawozdanie z projektu 

Do fetchera użyto scrappingu strony przy pomocy pakietu BeatifulSoup. Istnieje opcja unzip,
jeżeli jest wybrana to fetcher po pobraniu pliku rozpakowuje go, a następnie usuwa.

Handler ma domyślnie ustawioną opcję delete, która usuwa analizowany plik po rozdzieleniu danych.

Visualizer, na podstawie podanego typu danych oraz stacji, dokonuje file mappingu oraz wybiera
z plików konkretne kolumny (tak samo działają statystyki oraz prognozowanie) potrzebne do
wykonania wykresu. Wybrano 13 przykładowych typów danych.

Przykładowe użycie programu (CLI):

python meteopy/workflows/entrypoint.py download klimat 2000 2000

python meteopy/workflows/entrypoint.py download opad 2000 2000

python meteopy/workflows/entrypoint.py download synop 2001 2001

python meteopy/workflows/entrypoint.py basic_summary TAVG 249180010 249180160 249200240  

python meteopy/workflows/entrypoint.py full_analysis DESZ USL 354220195 354210185 353170235
-s 2001-01-03 -e 2001-12-20 -c -fd 30 

Sposób użycia każdej z powyższych komend  oraz dodatkowe opcjemożna również zobaczyć dzięki
użyciu --help.

Te same funkcjonalności można osiągnąć zakomentowanymi komendami w main.

