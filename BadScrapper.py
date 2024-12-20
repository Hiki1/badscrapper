from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Usage - modify the user in the format below
user = '<surname>, <name>'
base_url = 'https://pzbad.tournamentsoftware.com/find?DateFilterType=0&StartDate=2024-01-01&EndDate=2025-01-01&Distance=100&page=99&PostalCode=01-001'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'ASP.NET_SessionId=n2wa3x5cn3yyrfenztrffx1g; st=l=1045&exp=46010.9120430556&c=1&cp=23; _ga=GA1.1.2018179285.1734641600; _ga_FNL59NFQ13=GS1.1.1734641600.1.1.1734641899.0.0.0'
}

# Initialize WebDriver with Selenium Wire
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--log-level=1")
driver = webdriver.Chrome(options=options)

# Set custom headers
driver.header_overrides = headers

def fetch_data(url, class_name):
    driver.get(url)
    try:
        # Wait for the element to be present
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        )
    except TimeoutException:
        pass  # Do nothing if TimeoutException occurs (could mean that element was not found)

    page_html = driver.page_source
    parsed_html = BeautifulSoup(page_html, 'html.parser')
    return parsed_html

def extract_tournaments(parsed_html):
    data = []
    for item in parsed_html.find_all('div', class_='media__content'):
        title = item.find('h4').text
        link = item.find('a')['href']
        data.append({'title': title, 'link': link})
    return data

def extract_players(parsed_html):
    players = []
    for item in parsed_html.find_all('li', class_='list__item js-alphabet-list-item'):
        player_name = item.find('span', class_='nav-link__value').text
        link = item.find('a')['href']
        players.append({'player_name': player_name, 'link': link})
    return players

if __name__ == '__main__':
    print(f"--------------")
    print(f"PZBAD scrapper")
    print(f"--------------")
    print(f"User extracted: {user}")
    print(f"URL: {base_url}")
    
    parsed_html = fetch_data(base_url, '-smst-hidden')
    data = extract_tournaments(parsed_html)
    i = 1
    tournament_count = len(data)
    print(f"Tournaments to be searched: {tournament_count}\n")
    progress_bar = tqdm(total=tournament_count, position=0, leave=True)

    for entry in data:
        progress_bar.update(1)
        id = entry['link'].split('=')[1]
        tournament_players_url = f"https://pzbad.tournamentsoftware.com/tournament/{id}/players"
        parsed_html = fetch_data(tournament_players_url, 'player-list__cat')
        players = extract_players(parsed_html)
        for player in players:
            if user in player['player_name']:
                player_id = player['link'].split('=')[2]
                tournament_player_link = f"https://pzbad.tournamentsoftware.com/tournament/{id}/player/{player_id}"
                tqdm.write(f"{i}: {entry['title'].replace('\n', '')}; {tournament_player_link} ; {player['player_name']}")
                i += 1        
    driver.quit()