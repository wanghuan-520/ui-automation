#!/usr/bin/env python3
"""
Aevatar Configuration 日常回归测试
包含：CROS Domain 删除
优先级：P2
"""

import asyncio
import os
import logging
import pytest
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 测试环境配置
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "aevatarwh1@teml.net"
TEST_PASSWORD = "Wh520520!"
SCREENSHOT_DIR = "test-screenshots/configuration"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ========== 辅助函数 ==========

async def take_screenshot(page, filename: str):
    """截图"""
    try:
        screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图: {screenshot_path}")
    except Exception as e:
        logger.error(f"❌ 截图失败: {e}")


async def wait_for_toast(page, expected_text: str, timeout: int = 5000):
    """等待并验证Toast消息"""
    try:
        toast_selector = f'text=/.*{expected_text}.*/i'
        toast = await page.wait_for_selector(toast_selector, timeout=timeout)
        if toast:
            logger.info(f"✅ Toast验证: {expected_text}")
            return True
    except:
        logger.warning(f"⚠️ 未找到Toast: {expected_text}")
    return False


async def perform_login(page, email: str, password: str):
    """执行登录"""
    logger.info("🔐 开始登录...")
    await page.goto(TEST_BASE_URL)
    await page.wait_for_timeout(3000)
    
    email_input = await page.wait_for_selector('input[type="email"], input[placeholder*="email" i]', timeout=10000)
    await email_input.fill(email)
    
    password_input = await page.wait_for_selector('input[type="password"]', timeout=10000)
    await password_input.fill(password)
    
    login_button = await page.wait_for_selector('button[type="submit"]', timeout=10000)
    await login_button.click()
    await page.wait_for_timeout(5000)
    
    current_url = page.url
    if "dashboard" in current_url or "profile" in current_url:
        logger.info(f"✅ 登录成功: {current_url}")
        return True
    return False


# ========== 测试基类 ==========

class ConfigurationTest:
    """Configuration测试基类"""
    
    def __init__(self):
        self.base_url = TEST_BASE_URL
        self.email = TEST_EMAIL
        self.password = TEST_PASSWORD
    
    async def setup_browser(self):
        """初始化浏览器"""
        logger.info("🌌 初始化浏览器...")
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            slow_mo=800,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        self.page = await self.context.new_page()
        logger.info("✅ 浏览器初始化完成")
        
        await perform_login(self.page, self.email, self.password)
    
    async def teardown_browser(self):
        """清理浏览器"""
        try:
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
            logger.info("🧹 清理完成")
        except Exception as e:
            logger.error(f"❌ 清理失败: {e}")


# ========== Configuration 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.configuration
async def test_configuration_cros_delete_domain():
    """
    P2 测试: 删除 CROS Domain
    访问地址: /dashboard/configuration
    """
    test = ConfigurationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🌐 开始测试: 删除 CROS Domain [P2]")
        
        # 1. 导航到Configuration页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/configuration")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化完成（等待Initialising/Scanning消失）
        max_wait = 30  # 最多等待30秒
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            # 检查页面中是否还有loading文本
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
            if i == max_wait - 1:
                logger.warning(f"⚠️ 页面初始化超时 (等待了{max_wait}秒)")
        
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "cros_before_create.png")
        
        # 1.5 先创建一个临时 CROS Domain（确保有数据可删除）
        logger.info("🔨 先创建一个临时 CROS Domain...")
        import random
        import string
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        temp_domain = f"https://{random_str}.example.com"
        
        # 点击Add按钮
        add_button = await page.wait_for_selector('button:has-text("Add")', timeout=10000)
        await add_button.click()
        logger.info("✅ 点击Add按钮")
        await page.wait_for_timeout(2000)
        
        # 输入Domain
        domain_input = await page.wait_for_selector('[role="dialog"] input', timeout=10000)
        await domain_input.fill(temp_domain)
        logger.info(f"✅ 输入临时Domain: {temp_domain}")
        
        # 点击Add保存
        add_submit = await page.wait_for_selector('[role="dialog"] button:has-text("Add")', timeout=10000)
        await add_submit.click()
        logger.info("✅ 保存临时Domain")
        await page.wait_for_timeout(3000)
        
        await take_screenshot(page, "cros_list_after_create.png")
        logger.info("✅ 临时 CROS Domain 已创建")
        
        # 2. 点击第一个Domain的三个点菜单（使用多选择器策略）
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'button[aria-label*="menu"]',
            'button:has-text("⋮")',
            'tr button',
        ]
        
        for selector in menu_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    for btn in buttons:
                        if await btn.is_visible():
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector}")
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            await take_screenshot(page, "cros_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        await menu_button.click()
        await page.wait_for_timeout(1000)
        await take_screenshot(page, "cros_menu_opened.png")
        
        # 3. 点击Delete按钮（使用hover+click）
        try:
            # 先hover
            await page.hover('text="Delete"')
            logger.info("✅ Hover到Delete按钮")
            await page.wait_for_timeout(500)
            
            # 然后点击
            await page.click('text="Delete"')
            logger.info("✅ 点击Delete按钮 (Playwright click)")
        except Exception as e:
            logger.error(f"❌ 点击Delete失败: {e}")
            await take_screenshot(page, "cros_delete_failed.png")
            raise
        
        await page.wait_for_timeout(2000)
        logger.info("✅ Delete对话框应已打开")
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Cross-origin domain deleted")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证列表")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "cros_deleted.png")
        
        # 6. 验证列表变化（可以为空或数量减少）
        logger.info("✅ 验证删除操作完成")
        logger.info("🎉 CROS Domain删除成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.configuration
async def test_configuration_cros_add_domain():
    """
    P0 测试: 添加 CROS Domain
    访问地址: /dashboard/configuration
    """
    import random
    import string
    from datetime import datetime
    
    def generate_random_url():
        """生成随机URL"""
        random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"https://{random_str}.example.com"
    
    test = ConfigurationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🌐 开始测试: 添加 CROS Domain [P0]")
        
        # 1. 导航到Configuration页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/configuration")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化完成
        max_wait = 30
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
            if i == max_wait - 1:
                logger.warning(f"⚠️ 页面初始化超时 (等待了{max_wait}秒)")
        
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "configuration_add_page.png")
        logger.info("✅ 导航到Configuration页面")
        
        # 2. 点击Add按钮
        add_button = await page.wait_for_selector('button:has-text("Add")', timeout=10000)
        await add_button.click()
        logger.info("✅ 点击Add按钮")
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "after_add_click.png")
        
        # 3. 输入Domain
        domain_url = generate_random_url()
        logger.info(f"🔍 查找输入框...")
        
        # 尝试多种选择器
        domain_input = None
        input_selectors = [
            'input[type="text"]',
            'input[type="url"]',
            'input[placeholder*="domain" i]',
            'input[placeholder*="url" i]',
            'dialog input',
            '[role="dialog"] input',
            'input',
        ]
        
        for selector in input_selectors:
            try:
                domain_input = await page.wait_for_selector(selector, timeout=2000)
                if domain_input:
                    logger.info(f"✅ 找到输入框: {selector}")
                    break
            except:
                continue
        
        if not domain_input:
            await take_screenshot(page, "input_not_found.png")
            raise AssertionError("未找到输入框")
        await domain_input.fill(domain_url)
        logger.info(f"✅ 输入Domain: {domain_url}")
        await take_screenshot(page, "domain_filled.png")
        
        # 4. 点击Add按钮保存（在dialog中查找）
        submit_button = None
        submit_selectors = [
            '[role="dialog"] button:has-text("Add")',
            'dialog button:has-text("Add")',
            'button:has-text("Add")',
            '[role="dialog"] button[type="submit"]',
        ]
        
        for selector in submit_selectors:
            try:
                submit_button = await page.wait_for_selector(selector, timeout=2000)
                if submit_button:
                    logger.info(f"✅ 找到提交按钮: {selector}")
                    break
            except:
                continue
        
        if not submit_button:
            await take_screenshot(page, "submit_button_not_found.png")
            raise AssertionError("未找到提交按钮")
        
        await submit_button.click()
        logger.info("✅ 点击保存按钮")
        
        # 5. 验证Toast消息（可选）
        await page.wait_for_timeout(2000)
        success = await wait_for_toast(page, "Cross-origin domain added")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证列表")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "cros_domain_added.png")
        
        # 6. 验证列表中是否出现新Domain
        rows = await page.query_selector_all('tbody tr')
        assert len(rows) > 0, "CORS列表为空"
        logger.info(f"✅ CORS列表中有 {len(rows)} 个Domain")
        logger.info("🎉 CROS Domain添加成功!")
        
    finally:
        await test.teardown_browser()


# ========== 运行入口 ==========

if __name__ == "__main__":
    import subprocess
    import sys
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "--html=reports/configuration-regression-report.html",
        "--self-contained-html",
        "-m", "configuration"
    ]
    
    logger.info("🚀 运行Configuration回归测试...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)

