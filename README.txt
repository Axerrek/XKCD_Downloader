# xkcd_downloader

## Wymagania

- Python 3.x
- Biblioteka `requests`
- Biblioteka `BeautifulSoup` (bs4)
- Biblioteka `webbrowser`

Możesz zainstalować biblioteki `requests` poleceniem:

pip install requests beautifulsoup4

webbrowser chyba jest wbudowaną biblioteką, ale nie zaszkodzi spróbować

pip install webbrowser


## Uruchomienie

1. Sprawdź, czy masz plik "nr.txt" i wpisz do niego numery interesujących ciebie komiksów
2. Uruchom skrypt `xkcd_downloader.py` poleceniem:

python xkcd_downloader.py

3. Wynikowy plik HTML zostanie zapisany w `output/index.html`. Program automatycznie otworzy plik w domyślnej przeglądarce.