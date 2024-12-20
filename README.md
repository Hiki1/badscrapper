
# BadScrapper
Scrapper danych ze strony https://pzbad.tournamentsoftware.com/

## Zależności
```
pip install beautifulsoup4 tqdm selenium-wire selenium
```

## Konfiguracja
```
user = '<nazwisko>, <imie>'
base_url = 'https://pzbad.tournamentsoftware.com/find?DateFilterType=0&StartDate=2023-01-01&EndDate=2025-01-01&Distance=100&page=99&PostalCode=01-001'
```
Url zawiera:

* StartDate=2023-01-01 - data startu wyszukiwania
* EndDate=2025-01-01 - Data końca wyszukiwania
* Distance=100 - Dystans w kilometrach od kodu pocztowego
* page=99 - Ilość załadowanych stron, powinna być wysoka żeby wszystko było wczytane
* PostalCode=01-001 - Kod pocztowy miejsce od którego liczony jest dystans

## Uruchomienie
```
python.exe .\BadScrapper.py
```

## Ograniczenia
Wyszukanie nie może zwrócić więcej niż 1000 turniejów