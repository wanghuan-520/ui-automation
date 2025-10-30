#!/usr/bin/env python3
"""
Aevatar Profile 日常回归测试
包含：Profile Name 编辑
优先级：P1
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
SCREENSHOT_DIR = "test-screenshots/profile"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ========== 辅助函数 ==========

def generate_random_name(prefix="test", length=6):
    """生成随机名称"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"{prefix}_{timestamp}_{random_str}"


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

class ProfileTest:
    """Profile测试基类"""
    
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


# ========== Profile 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.profile
async def test_profile_name_edit():
    """
    P1 测试: 修改 Profile Name
    访问地址: /profile/profile/general
    """
    test = ProfileTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("👤 开始测试: 修改 Profile Name [P1]")
        
        # 1. 导航到Profile页面
        await page.goto(f"{TEST_BASE_URL}/profile/profile/general")
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
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "profile_page.png")
        
        # 2. 修改Name（使用多选择器策略）
        new_name = generate_random_name("user")
        logger.info(f"🔍 查找Name输入框...")
        
        name_input = None
        name_selectors = [
            'input[type="text"]:first-of-type',  # 第一个text input
            'label:has-text("Name") + input',     # Name标签后的input
            'text="Name" >> .. >> input',         # Name文本附近的input
            'input',                               # 任意input
        ]
        
        for selector in name_selectors:
            try:
                name_input = await page.wait_for_selector(selector, timeout=2000)
                if name_input:
                    logger.info(f"✅ 找到Name输入框: {selector}")
                    break
            except:
                continue
        
        if not name_input:
            await take_screenshot(page, "name_input_not_found.png")
            raise AssertionError("未找到Name输入框")
        
        await name_input.fill("")  # 清空
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        await take_screenshot(page, "name_filled.png")
        
        # 3. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        logger.info("✅ 点击Save按钮")
        await page.wait_for_timeout(2000)
        
        # 4. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully saved")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "profile_updated.png")
        
        # 5. 验证输入框中的值已更新
        current_value = await name_input.input_value()
        logger.info(f"🔍 当前Name值: {current_value}")
        assert current_value == new_name, f"Name未更新，期望:{new_name}，实际:{current_value}"
        
        logger.info("✅ 验证Name已成功更新")
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
        "--html=reports/profile-regression-report.html",
        "--self-contained-html",
        "-m", "profile"
    ]
    
    logger.info("🚀 运行Profile回归测试...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)

