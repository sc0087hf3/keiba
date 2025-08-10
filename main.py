# main.py
from db import SessionLocal
from scraper.netkeiba import scrape_race_list, scrape_odds
from weather.weather_api import get_weather
from models import tables

def main():
    session = SessionLocal()

    # 例：指定日のレースを取得
    date = "20250721"
    races = scrape_race_list(date)

    # 例：レース情報をDBに登録（要実装）
    # for race in races:
    #     db_race = tables.Race(...)
    #     session.add(db_race)

    # 例：天気情報を取得
    weather = get_weather("Tokyo")
    print("Weather:", weather)

    # 例：オッズを取得
    # odds = scrape_odds(race_id)

    session.commit()
    session.close()

if __name__ == "__main__":
    main()
