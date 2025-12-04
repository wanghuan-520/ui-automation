import asyncio
from playwright.async_api import async_playwright
import json

async def inspect_page():
    async with async_playwright() as p:
        # 尝试使用 Firefox
        print("启动 Firefox 浏览器...")
        try:
            browser = await p.firefox.launch(headless=True)
        except Exception:
             print("Firefox 未找到，回退到 Chromium (Headful)...")
             browser = await p.chromium.launch(headless=False, args=["--ignore-certificate-errors", "--no-sandbox", "--disable-gpu"])
        
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        print("1. 导航到登录页...")
        await page.goto("https://localhost:3000/")
        
        # 登录流程
        print("2. 执行登录...")
        # 点击 Sign In (根据现有 POM)
        await page.click("button:has-text('Sign In')")
        await page.wait_for_load_state("networkidle")
        
        # 填写登录信息
        await page.fill("#LoginInput_UserNameOrEmailAddress", "haylee@test.com")
        await page.fill("#LoginInput_Password", "Wh520520!")
        await page.click("button[type='submit']:has-text('Login')")
        
        # 等待登录完成
        await page.wait_for_load_state("networkidle")
        
        print("3. 导航到 Profile 页面...")
        await page.goto("https://localhost:3000/admin/profile")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000) # 额外等待页面渲染
        
        print("4. 扫描页面元素...")
        
        elements_info = []
        
        # 定义感兴趣的元素选择器
        selectors = [
            "input", 
            "button", 
            "a[role='tab']", 
            "select",
            "textarea",
            ".alert",
            "[role='alert']"
        ]
        
        for selector in selectors:
            elements = await page.locator(selector).all()
            for i, el in enumerate(elements):
                if await el.is_visible():
                    info = {
                        "tag": selector,
                        "id": await el.get_attribute("id") or "",
                        "name": await el.get_attribute("name") or "",
                        "type": await el.get_attribute("type") or "",
                        "class": await el.get_attribute("class") or "",
                        "placeholder": await el.get_attribute("placeholder") or "",
                        "text": (await el.inner_text()).strip() if selector != "input" else "",
                        "value": await el.input_value() if selector == "input" else "",
                        "role": await el.get_attribute("role") or "",
                        "outerHTML": await el.evaluate("el => el.outerHTML")
                    }
                    elements_info.append(info)
        
        # 打印结果
        print("\n=== 页面元素扫描结果 ===")
        print(json.dumps(elements_info, indent=2, ensure_ascii=False))
        
        # 截图以供参考
        await page.screenshot(path="profile_page_inspection.png")
        print("\n页面截图已保存为 profile_page_inspection.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_page())
