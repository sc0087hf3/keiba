import os
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import random

from playwright.async_api import async_playwright

# 保存ファイル
SUCCESS_LOG = "success_urls.txt"
FAIL_LOG = "fail_dates.txt"
USER_AGENTS_FILE = "user_agents.txt"

# 出走表ページのURLフォーマット
BASE_URL = "https://race.netkeiba.com/top/race_list.html?kaisai_date={date}"

# 土日を返す
def get_weekend_dates(year):
    date = datetime(year, 8, 1)
    end_date = datetime(year, 12, 31)
    weekends = []
    while date <= end_date:
        if date.weekday() in (5, 6):  # 土日
            weekends.append(date)
        date += timedelta(days=1)
    return weekends

# 取得済みと失敗した日付の読み込み
def load_processed_dates():
    if Path(SUCCESS_LOG).exists():
        with open(SUCCESS_LOG) as f:
            success_dates = {line.strip().split('=')[-1] for line in f if line.strip()}
    else:
        success_dates = set()
    
    if Path(FAIL_LOG).exists():
        with open(FAIL_LOG) as f:
            fail_dates = {line.strip() for line in f if line.strip()}
    else:
        fail_dates = set()
    
    return success_dates, fail_dates

# User-Agentの読み込み
def load_user_agents():
    if not Path(USER_AGENTS_FILE).exists():
        print("user_agents.txt が見つかりません。")
        return []
    with open(USER_AGENTS_FILE) as f:
        return [line.strip() for line in f if line.strip()]

# メイン処理
async def fetch_race_urls():
    weekends = get_weekend_dates(2024)
    success_dates, fail_dates = load_processed_dates()
    user_agents = load_user_agents()
    if not user_agents:
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for date in weekends:
            date_str = date.strftime("%Y%m%d")
            if date_str in success_dates or date_str in fail_dates:
                continue  # スキップ
            
            url = BASE_URL.format(date=date_str)
            user_agent = random.choice(user_agents)

            try:
                context = await browser.new_context(user_agent=user_agent)
                page = await context.new_page()
                print(f"アクセス中: {url} (UA: {user_agent})")
                response = await page.goto(url, timeout=30000)

                if response and response.ok:
                    content = await page.content()
                    if "レース一覧" in content or "race_list" in page.url:
                        with open(SUCCESS_LOG, "a") as f:
                            f.write(f"{url}\n")
                        print(f"✅ 成功: {date_str}")
                    else:
                        raise Exception("ページにレース一覧が見つかりません。")
                else:
                    raise Exception("無効なレスポンス")

                await context.close()
            except Exception as e:
                print(f"❌ 失敗: {date_str} - {e}")
                with open(FAIL_LOG, "a") as f:
                    f.write(f"{date_str}\n")
        await browser.close()

# 実行
if __name__ == "__main__":
    asyncio.run(fetch_race_urls())
