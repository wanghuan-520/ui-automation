from playwright.sync_api import sync_playwright
import sys

print("Starting Playwright check...")
try:
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        print("Browser launched. New context...")
        page = browser.new_page()
        print("Context created. Navigating to example.com...")
        page.goto("https://example.com", timeout=10000)
        print(f"Page title: {page.title()}")
        browser.close()
        print("Browser closed. Success.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

