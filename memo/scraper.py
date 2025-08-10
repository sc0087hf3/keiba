import random
import time
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
]

def get_inner_text_or_none(element):
    if element is None:
        return ""
    try:
        return element.inner_text().strip()
    except Exception:
        return ""

def main():
    start_time = time.time()  # 開始時刻を記録
    
    url_login = "https://regist.netkeiba.com/account/?pid=login"  # ログインページURLを正確にセットしてください
    race_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202504020609&rf=race_listcd "
    username = "gangshishidao@gmail.com"  # ここにログインID
    password = "yajima244"           # ここにパスワード
    
    user_agent = random.choice(USER_AGENTS)
    print(f"使用User-Agent: {user_agent}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # ログイン処理
        page.goto(url_login)
        page.wait_for_selector('input[name="pswd"]', timeout=30000)
        page.fill('input[name="login_id"]', username)
        page.fill('input[name="pswd"]', password)
        page.click('input[type="image"]')  # ログインボタンが画像タイプの場合の例
        page.wait_for_load_state('networkidle')  # ログイン後の読み込み完了を待つ

        print("ログインしてページ取得完了")

        # レースページに移動
        page.goto(race_url)
        page.wait_for_selector("table.Shutuba_Table tbody tr.HorseList")
        page.wait_for_timeout(3000)

        # 初回オッズ更新時刻取得
        official_time_elem = page.query_selector("#official_time")
        official_time = official_time_elem.inner_text().strip() if official_time_elem else ""
        print(f"初回オッズ更新時刻: {official_time}")

        # 「更新」ボタンを待ってからdisabledを外してクリック
        button = page.query_selector("#act-manual_update")
        if button:
            style = button.get_attribute("style") or ""
            if "display:none" in style:
                print("更新ボタンはあるけど非表示（レース後かも）")
            else:
                print("強制的にボタンのdisabledを外してクリックします...")
                page.evaluate("""
                    const btn = document.querySelector('#act-manual_update');
                    if (btn) {
                        btn.disabled = false;
                        btn.click();
                    }
                """)
                time.sleep(5)
        else:
            print("更新ボタンがそもそも存在しない（ページ構造の変化など）")

        # 更新が反映されるまで待つ（5秒待機。必要に応じて調整してください）
        time.sleep(5)

        # 更新後のオッズ更新時刻取得
        official_time_elem = page.query_selector("#official_time")
        updated_official_time = official_time_elem.inner_text().strip() if official_time_elem else ""
        print(f"更新後オッズ更新時刻: {updated_official_time}")

        # オッズテーブル取得例（全行をループ）
        rows = page.query_selector_all("table.Shutuba_Table tbody tr.HorseList")
        print(f"取得した行数: {len(rows)}")

        for i, row in enumerate(rows):
            cells = row.query_selector_all("td")
            waku = get_inner_text_or_none(cells[0]) if len(cells) > 0 else ""
            umaban = get_inner_text_or_none(cells[1]) if len(cells) > 1 else ""
            
            # 馬名とhorse_id
            horse_link_elem = row.query_selector("td.HorseInfo span.HorseName a")
            horse_name = get_inner_text_or_none(horse_link_elem)
            horse_href = horse_link_elem.get_attribute("href") if horse_link_elem else ""
            horse_id = horse_href.rstrip('/').split('/')[-1] if horse_href else ""
            
            seirei = get_inner_text_or_none(cells[3]) if len(cells) > 3 else ""  # 性齢
            kinryo = get_inner_text_or_none(cells[4]) if len(cells) > 4 else ""  # 斤量
            kisyu = get_inner_text_or_none(cells[5]) if len(cells) > 5 else ""   # 騎手
            odds = get_inner_text_or_none(row.query_selector("td.Txt_R.Popular span"))
            ninki = get_inner_text_or_none(row.query_selector("td.Popular"))  # 人気
            
            print(f"枠:{waku}, 馬番:{umaban}, 馬名:{horse_name}, horse_id:{horse_id}, 性齢:{seirei}, 斤量:{kinryo}, 騎手:{kisyu}, オッズ:{odds}, 人気:{ninki}")

        browser.close()

        end_time = time.time()  # 終了時刻を記録
        duration = end_time - start_time
        print(f"処理時間: {duration:.2f} 秒")
        
if __name__ == "__main__":
    main()
