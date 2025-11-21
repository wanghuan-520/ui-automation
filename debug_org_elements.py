from playwright.sync_api import sync_playwright
import time
import os

def dump_org_page_elements():
    with sync_playwright() as p:
        # 使用有头模式以便观察
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            print("1. 登录...")
            page.goto("http://localhost:5173", timeout=60000)
            
            print("   页面源码预览:")
            print(page.content()[:500])
            
            print("   等待输入框...")
            page.wait_for_selector("input[type='email']", timeout=30000)
            
            # 登录
            print("   输入凭据...")
            page.fill("input[type='email']", "haylee@test.com")
            page.fill("input[type='password']", "Wh520520!")
            page.click("button[type='submit']")
            print("   点击登录，等待跳转...")
            
            # 放宽等待条件，只要 URL 变了或者出现 dashboard 元素即可
            try:
                page.wait_for_url("**/dashboard/**", timeout=60000)
                print("✅ 登录跳转成功")
            except:
                print(f"⚠️ 跳转超时，当前URL: {page.url}")
                page.screenshot(path="debug_screenshots/login_timeout.png")
            
            print("2. 导航到 Organisation 页面...")
            # 尝试通过点击顶部导航栏的 O1 (Organization Switcher) 或者 Settings
            # 先打印一下当前页面的所有按钮，找找线索
            print("   查找导航按钮...")
            buttons = page.locator("button").all()
            for btn in buttons:
                if btn.is_visible():
                     txt = btn.text_content().strip()
                     # 查找 Settings 或 Organisation 相关的按钮
                     if txt in ["Settings", "O1", "Organization", "My Organization"]:
                         print(f"   Found Nav Button: {txt}")
                         # 如果是 Settings，点进去看看
                         if txt == "Settings":
                             btn.click()
                             print("   Clicked Settings")
                             time.sleep(2)
                             break

            # 再次尝试直接 URL (更正可能的 URL 结构)
            # 常见的结构: /dashboard/organization/profile, /dashboard/settings/members
            potential_urls = [
                "http://localhost:5173/dashboard/organization",
                "http://localhost:5173/dashboard/settings/organization",
                "http://localhost:5173/dashboard/settings"
            ]
            
            for url in potential_urls:
                print(f"   尝试访问: {url}")
                page.goto(url)
                time.sleep(3)
                if "404" not in page.title():
                    print(f"   访问成功: {page.url}")
                    break
            
            print(f"当前URL: {page.url}")
            
            # 截图确认位置
            if not os.path.exists("debug_screenshots"):
                os.makedirs("debug_screenshots")
            page.screenshot(path="debug_screenshots/org_page_probe.png")
            
            # 3. 获取关键元素 HTML
            print("3. 抓取页面元素...")
            
            # 尝试定位 "Create Project" 按钮
            buttons = page.locator("button").all()
            print("\n--- Buttons ---")
            for btn in buttons:
                if await_visibility(btn):
                    txt = btn.text_content().strip()
                    if txt:
                        print(f"Button: '{txt}' | HTML: {btn.evaluate('el => el.outerHTML')}")
            
            # 尝试定位表格 (Projects/Members/Roles)
            tables = page.locator("table, [role='table']").all()
            print(f"\n--- Tables found: {len(tables)} ---")
            for i, tbl in enumerate(tables):
                if await_visibility(tbl):
                    print(f"Table {i} HTML (first 500 chars): {tbl.evaluate('el => el.outerHTML')[:500]}...")

        except Exception as e:
            print(f"❌ 发生错误: {e}")
            page.screenshot(path="debug_screenshots/error_probe.png")
        finally:
            browser.close()

def await_visibility(locator):
    try:
        return locator.is_visible(timeout=1000)
    except:
        return False

if __name__ == "__main__":
    dump_org_page_elements()

