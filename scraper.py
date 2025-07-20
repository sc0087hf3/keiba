from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=Falseでブラウザ画面表示
    page = browser.new_page()
    page.goto("https://db.netkeiba.com/horse/2022109143")
    print(page.title())
    browser.close()