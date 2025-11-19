#!/usr/bin/env python3
"""
Aevatar 测试配置文件
包含共享的 pytest fixtures
"""

import os
import sys
import logging
import pytest
from playwright.async_api import async_playwright

# 添加当前目录到路径，支持绝对导入
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from aevatar_utils import TestDataLoader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_data():
    """
    会话级别的测试数据fixture
    一次加载，整个测试会话复用
    """
    return TestDataLoader.load_yaml_data()


@pytest.fixture(scope="session")
def environment_config(test_data):
    """获取环境配置"""
    return test_data.get('environment', {})


@pytest.fixture(scope="session")
def browser_config(test_data):
    """获取浏览器配置"""
    return test_data.get('browser', {})


@pytest.fixture
async def browser_context(browser_config, environment_config):
    """
    浏览器上下文fixture
    每个测试函数独立的浏览器实例
    """
    logger.info("🌌 初始化浏览器上下文...")
    playwright = await async_playwright().start()
    
    try:
        # 启动浏览器
        browser = await playwright.chromium.launch(
            headless=browser_config.get('headless', False),
            slow_mo=environment_config.get('slow_mo', 2000),
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-gpu',
                f'--window-size={browser_config["viewport"]["width"]},{browser_config["viewport"]["height"]}',
                '--start-maximized',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-hang-monitor',
                '--disable-prompt-on-repost',
                '--disable-popup-blocking',
                '--password-store=basic',
                '--use-mock-keychain',
                '--no-service-autorun',
                '--disable-search-engine-choice-screen',
                '--enable-use-zoom-for-dsf=false',
                '--force-color-profile=srgb',
                '--enable-automation',
                '--export-tagged-pdf'
            ]
        )
        
        # 创建浏览器上下文
        context = await browser.new_context(
            viewport=browser_config.get('viewport'),
            user_agent=browser_config.get('user_agent')
        )
        
        # 创建页面
        page = await context.new_page()
        
        # 监听控制台消息
        page.on("console", lambda msg: logger.info(f"控制台: {msg.text}"))
        
        logger.info("✅ 浏览器初始化完成")
        
        # 返回页面对象供测试使用
        yield page
        
    finally:
        # 清理资源
        logger.info("🧹 清理浏览器资源...")
        try:
            await browser.close()
            await playwright.stop()
            logger.info("✅ 浏览器资源清理完成")
        except Exception as e:
            logger.error(f"❌ 清理资源时出错: {e}")


@pytest.fixture
async def screenshot_helper(browser_context, environment_config):
    """
    截图辅助fixture
    提供截图功能（返回async函数）
    """
    screenshot_dir = environment_config.get('screenshot_dir', 'test-screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    
    async def take_screenshot(filename: str):
        """截图函数"""
        try:
            screenshot_path = os.path.join(screenshot_dir, filename)
            await browser_context.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"📸 截图已保存: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"❌ 截图失败: {e}")
            return None
    
    return take_screenshot


@pytest.fixture
async def login_helper(browser_context, environment_config, screenshot_helper):
    """
    登录辅助fixture
    提供通用登录功能（返回async函数）
    """
    from aevatar_utils import SelectorHelper, TestDataLoader
    
    async def perform_login(email: str, password: str):
        """
        执行登录操作
        
        Args:
            email: 邮箱
            password: 密码
            
        Returns:
            登录是否成功
        """
        page = browser_context
        
        # 导航到登录页面
        await page.goto(environment_config.get('login_url'))
        await screenshot_helper("login_page.png")
        logger.info("✅ 导航到登录页面")
        
        # 等待页面加载
        await page.wait_for_timeout(3000)
        
        # 获取选择器配置
        selectors = TestDataLoader.get_selectors('login')
        
        # 填写邮箱
        if email:
            email_input = await SelectorHelper.find_element_with_selectors(
                page, 
                selectors.get('email_input', [])
            )
            if email_input:
                await email_input.fill(email)
                logger.info(f"✅ 邮箱输入完成: {email}")
            else:
                logger.error("❌ 未找到邮箱输入框")
                return False
        
        # 填写密码
        if password:
            password_input = await SelectorHelper.find_element_with_selectors(
                page,
                selectors.get('password_input', [])
            )
            if password_input:
                await password_input.fill(password)
                logger.info("✅ 密码输入完成")
            else:
                logger.error("❌ 未找到密码输入框")
                return False
        
        await screenshot_helper("form_filled.png")
        
        # 点击登录按钮
        login_button = await SelectorHelper.find_element_with_selectors(
            page,
            selectors.get('submit_button', [])
        )
        if login_button:
            await login_button.click()
            logger.info("✅ 登录按钮已点击")
        else:
            logger.error("❌ 未找到登录按钮")
            return False
        
        # 等待登录完成
        await page.wait_for_timeout(5000)
        await screenshot_helper("login_result.png")
        
        return True
    
    return perform_login


def pytest_configure(config):
    """pytest配置钩子"""
    # 添加自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "positive: 正向测试用例")
    config.addinivalue_line("markers", "negative: 负向测试用例")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "workflow: workflow相关测试")
    config.addinivalue_line("markers", "integration: 集成测试")

