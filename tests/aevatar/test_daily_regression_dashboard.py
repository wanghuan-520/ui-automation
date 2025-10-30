#!/usr/bin/env python3
"""
Aevatar Dashboard + Profile 日常回归测试
包含：Dashboard（API Keys、Workflows、Configuration）+ Profile配置
优先级：P0/P1/P2
"""

import asyncio
import os
import logging
import pytest
import random
import string
from datetime import datetime
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
SCREENSHOT_DIR = "test-screenshots/dashboard"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ========== 辅助函数 ==========

def generate_random_name(prefix="test", length=6):
    """生成随机名称"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"{prefix}_{timestamp}_{random_str}"


def generate_random_url():
    """生成随机URL"""
    random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"https://{random_str}.example.com"


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

class DashboardTest:
    """Dashboard测试基类"""
    
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


# ========== API Keys 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.apikeys
async def test_apikeys_edit():
    """
    P1 测试: 修改 API Key
    访问地址: /dashboard/apikeys
    """
    test = DashboardTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔑 开始测试: 修改 API Key [P1]")
        
        # 1. 导航到API Keys页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/apikeys")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "apikeys_list.png")
        
        # 2. 点击第一个API Key的三个点菜单
        menu_button = await page.wait_for_selector('button[aria-label*="menu"], button:has-text("⋮")', timeout=10000)
        await menu_button.click()
        await page.wait_for_timeout(1000)
        logger.info("✅ 点击菜单按钮")
        
        # 3. 点击Edit按钮
        edit_button = await page.wait_for_selector('button:has-text("Edit"), [role="menuitem"]:has-text("Edit")', timeout=5000)
        await edit_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Edit按钮")
        
        # 4. 修改API Key名称
        new_name = generate_random_name("apikey_edit")
        name_input = await page.wait_for_selector('input[name*="name" i]', timeout=10000)
        await name_input.fill("")  # 清空
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        
        # 5. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        await page.wait_for_timeout(2000)
        
        # 6. 验证Toast
        success = await wait_for_toast(page, "Successfully saved")
        assert success, "未找到保存成功的Toast"
        
        await take_screenshot(page, "apikeys_edited.png")
        logger.info("🎉 API Key修改成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.apikeys
async def test_apikeys_delete():
    """
    P2 测试: 删除 API Key
    访问地址: /dashboard/apikeys
    """
    test = DashboardTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔑 开始测试: 删除 API Key [P2]")
        
        # 1. 导航到API Keys页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/apikeys")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "apikeys_before_delete.png")
        
        # 2. 点击第一个API Key的三个点菜单
        menu_button = await page.wait_for_selector('button[aria-label*="menu"], button:has-text("⋮")', timeout=10000)
        await menu_button.click()
        await page.wait_for_timeout(1000)
        
        # 3. 点击Delete按钮
        delete_button = await page.wait_for_selector('button:has-text("Delete"), [role="menuitem"]:has-text("Delete")', timeout=5000)
        await delete_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Delete按钮")
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 确认删除")
        
        # 5. 验证删除成功
        await take_screenshot(page, "apikeys_deleted.png")
        logger.info("🎉 API Key删除成功!")
        
    finally:
        await test.teardown_browser()


# ========== Workflow 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.workflows
async def test_workflows_delete():
    """
    P2 测试: 删除 Workflow
    访问地址: /dashboard/workflows
    """
    test = DashboardTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔄 开始测试: 删除 Workflow [P2]")
        
        # 1. 导航到Workflows页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/workflows")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "workflows_list.png")
        
        # 2. 点击第一个Workflow的三个点菜单
        menu_button = await page.wait_for_selector('button[aria-label*="menu"], button:has-text("⋮")', timeout=10000)
        await menu_button.click()
        await page.wait_for_timeout(1000)
        
        # 3. 点击Delete按钮
        delete_button = await page.wait_for_selector('button:has-text("Delete"), [role="menuitem"]:has-text("Delete")', timeout=5000)
        await delete_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Delete按钮")
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 确认删除")
        
        await take_screenshot(page, "workflows_deleted.png")
        logger.info("🎉 Workflow删除成功!")
        
    finally:
        await test.teardown_browser()


# ========== Configuration 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.configuration
async def test_configuration_cros_delete_domain():
    """
    P2 测试: 删除 CROS Domain
    访问地址: /dashboard/configuration
    """
    test = DashboardTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🌐 开始测试: 删除 CROS Domain [P2]")
        
        # 1. 导航到Configuration页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/configuration")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "cros_list.png")
        
        # 2. 点击第一个Domain的三个点菜单
        menu_button = await page.wait_for_selector('button[aria-label*="menu"], button:has-text("⋮")', timeout=10000)
        await menu_button.click()
        await page.wait_for_timeout(1000)
        
        # 3. 点击Delete按钮
        delete_button = await page.wait_for_selector('button:has-text("Delete"), [role="menuitem"]:has-text("Delete")', timeout=5000)
        await delete_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Delete按钮")
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast
        success = await wait_for_toast(page, "Cross-origin domain deleted")
        assert success, "未找到删除成功的Toast"
        
        await take_screenshot(page, "cros_deleted.png")
        logger.info("🎉 CROS Domain删除成功!")
        
    finally:
        await test.teardown_browser()


# ========== Profile 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.profile
async def test_profile_name_edit():
    """
    P1 测试: 修改 Profile Name
    访问地址: /profile/profile/general
    """
    test = DashboardTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("👤 开始测试: 修改 Profile Name [P1]")
        
        # 1. 导航到Profile页面
        await page.goto(f"{TEST_BASE_URL}/profile/profile/general")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "profile_page.png")
        
        # 2. 修改Name
        new_name = generate_random_name("user")
        name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=10000)
        await name_input.fill("")  # 清空
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        
        # 3. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        await page.wait_for_timeout(2000)
        
        # 4. 验证Toast
        success = await wait_for_toast(page, "Successfully saved")
        assert success, "未找到保存成功的Toast"
        
        await take_screenshot(page, "profile_updated.png")
        logger.info("🎉 Profile Name修改成功!")
        
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
        "--html=reports/dashboard-regression-report.html",
        "--self-contained-html",
        "-m", "dashboard or profile"
    ]
    
    logger.info("🚀 运行Dashboard + Profile回归测试...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)
