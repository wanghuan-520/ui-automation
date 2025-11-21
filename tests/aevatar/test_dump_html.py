import pytest
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage

def test_dump_editor_html(page: Page):
    login_page = LocalhostEmailLoginPage(page)
    login_page.navigate()
    login_page.login_with_email("haylee@test.com", "Wh520520!")
    
    page.wait_for_url("**/dashboard/workflows")
    page.click("button:has-text('New Workflow')")
    page.wait_for_timeout(5000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)
    
    with open("editor_dump.html", "w", encoding="utf-8") as f:
        f.write(page.content())

