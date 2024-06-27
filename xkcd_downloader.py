import os
import requests
from bs4 import BeautifulSoup
import webbrowser
# Funkcja do pobierania danych komiksu z API XKCD
def fetch_API(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Utwórzenie struktury katalogów, jeśli nie istnieje
os.makedirs('output/images', exist_ok=True)

# Wczytaj obrazów, wraz z logo XKCD
with open('nr.txt', 'r') as file:
    comic_numbers = [line.strip() for line in file]

xkcd_img_url = 'https://imgs.xkcd.com/static/terrible_small_logo.png'
xkcd_response = requests.get(xkcd_img_url)
with open('output/xkcd.png', 'wb') as img_file:
    img_file.write(xkcd_response.content)

# Utworzenie za każdym uruchomieniem nowego HTML
html_content = '''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My XKCD Gallery</title>
    <link href="../styles.css" rel="stylesheet">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="text-center mt-4 mb-4">Galeria wygenerowanych komiksów XKCD</h1>
            <div class="text-center mb-4">
                <img src="xkcd.png" alt="XKCD Logo">
            </div>
            <div id="comic-numbers" class="mb-3">
            </div>
        </div>
        <div class="row" id="content">
        </div>
    </div>
</body>
</html>'''

#soup znajduje elementy HTML i wstrzykuje informacje do środka
soup = BeautifulSoup(html_content, 'html.parser')

comic_numbers_div = soup.find('div', id='comic-numbers')
content_div = soup.find('div', id='content')

comic_numbers_str = ", ".join(comic_numbers)
comic_numbers_div.string = f"Numery wygenerowanych komiksów: {comic_numbers_str}"

# Dodaj obrazki do <div id="content">
for number in comic_numbers:
    comic_data = fetch_API(number)
    if comic_data:    
        new_div = soup.new_tag('div', **{'class': 'col-12 col-md-6 col-lg-4 mb-4'})
        card_div = soup.new_tag('div', **{'class': 'card'})
        
        # Dodanie tytułu
        card_title = soup.new_tag('h5', **{'class': 'card-title'})
        card_title.string = f'Komiks #{number}: {comic_data["safe_title"]}'
        card_body_div = soup.new_tag('div', **{'class': 'card-body'})
        card_body_div.append(card_title)
        
        # Dodanie obrazka
        img_tag = soup.new_tag('img', src=f'images/{number}.png', **{'class': 'card-img-top', 'alt': f'XKCD Comic {number}'})
        card_div.append(card_body_div)
        card_div.append(img_tag)
        new_div.append(card_div)
        content_div.append(new_div)
        
        # Zapis obrazka do pliku
        img_response = requests.get(comic_data['img'])
        img_filename = f"output/images/{number}.png"
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_response.content)

# Zapisz nowy plik HTML
with open('output/index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"Wygenerowano numery komiksów: {', '.join(comic_numbers)} do pliku HTML")
html_file = 'output/index.html'

#Otworzenie pliku w przeglądarce
if os.path.exists(html_file):
    webbrowser.open(f'file://{os.path.realpath(html_file)}')
else:
    print(f"Plik {html_file} nie istnieje.")