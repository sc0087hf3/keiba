import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# User-Agentのリスト
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    # 他にも追加してOK
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...",
]

random_user_agent = random.choice(user_agents)

base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202507030406&rf=race_list'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(user_agent=random_user_agent)
    page = context.new_page()

    # 最初のページを開く
    page.goto(base_url)
    page.wait_for_selector('#act-manual_update', state='visible')

    # 有効化を待つ
    button = page.locator('#act-manual_update')
    button.wait_for(state='enabled', timeout=10000)
    button.click()

    # HTMLを取得してパース
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
        # tbody内の<tr>をすべて取得
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr', class_='HorseList') if tbody else []

    for row in rows:
        # 馬名
        horse_name_tag = row.find('span', class_='HorseName')
        horse_name = horse_name_tag.text.strip() if horse_name_tag else ''

        # 馬番
        umaban_tag = row.find('td', class_='Umaban1')
        umaban = umaban_tag.text.strip() if umaban_tag else ''

        # オッズ
        odds_tag = row.find('span', class_='Odds_Ninki')
        odds = odds_tag.text.strip() if odds_tag else ''

        print(f'馬番: {umaban}, 馬名: {horse_name}, オッズ: {odds}')
        print('----------------')
    browser.close()


import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    # 他にも追加してOK
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...",
]
random_user_agent = random.choice(user_agents)

base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202507030406&rf=race_list'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent=random_user_agent)
    page = context.new_page()

    page.goto(base_url)
    page.wait_for_selector('#act-manual_update', state='visible')

    # 有効化を待つ
    button = page.locator('#act-manual_update')
    button.wait_for(state='enabled', timeout=150000)
    button.click()
    
    # HTML取得
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', class_='Shutuba_Table')
    tbody = table.find('tbody') if table else None
    rows = tbody.find_all('tr', class_='HorseList') if tbody else []

    for row in rows:
        horse_name = row.find('span', class_='HorseName').text.strip() if row.find('span', class_='HorseName') else ''
        umaban = row.find('td', class_='Umaban1').text.strip() if row.find('td', class_='Umaban1') else ''
        odds = row.find('span', class_='Odds_Ninki').text.strip() if row.find('span', class_='Odds_Ninki') else ''
        print(f'馬番: {umaban}, 馬名: {horse_name}, オッズ: {odds}')
        print('----------------')

    browser.close()
