#!/usr/bin/env python3
"""
Aevatar 测试基类
提供浏览器初始化、截图等公共方法
"""

import asyncio
import os
import logging
import inspect
from datetime import datetime
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class AevatarPytestTest:
    """Aevatar pytest测试基类"""
    
    def __init__(self):
        self.BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
        self.LOGIN_URL = "https://aevatar-station-ui-staging.aevatar.ai"
        self.EMAIL = "aevatarwh1@teml.net"
        self.PASSWORD = "Wh520520!"
        self.SCREENSHOT_DIR = "test-screenshots"
        
        # 创建截图目录
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)
    
    async def setup_browser(self):
        """初始化浏览器"""
        logger.info("🌌 初始化浏览器 (有头模式)...")
        self.playwright = await async_playwright().start()
        
        # 启动浏览器
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # 有头模式
            slow_mo=2000,    # 操作间隔2秒，便于观察
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-gpu',
                '--window-size=1280,720',
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
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 创建页面
        self.page = await self.context.new_page()
        
        # 监听控制台消息
        self.page.on("console", lambda msg: logger.info(f"控制台: {msg.text}"))
        
        logger.info("✅ 浏览器初始化完成")
    
    async def teardown_browser(self):
        """清理浏览器资源"""
        try:
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
            logger.info("🧹 浏览器资源清理完成")
        except Exception as e:
            logger.error(f"❌ 清理资源时出错: {e}")
    
    async def take_screenshot(self, filename: str):
        """截图，自动添加测试名称和时间戳前缀，并保存到测试名称对应的子目录
        
        Args:
            filename: 截图文件名描述（如：01_login_page.png）
            
        Returns:
            str: 截图路径，失败返回None
            
        说明:
            最终文件路径: test-screenshots/{测试名称}/{测试名称}_{时间戳}_{原文件名}
            例如: test-screenshots/test_aevatar_login/test_aevatar_login_20251023_150525_01_login_page.png
        """
        try:
            # 获取调用者的函数名（测试用例名）
            frame = inspect.currentframe()
            caller_frame = frame.f_back
            test_name = caller_frame.f_code.co_name if caller_frame else "unknown_test"
            
            # 生成时间戳
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 创建以测试名称命名的子目录
            test_dir = os.path.join(self.SCREENSHOT_DIR, test_name)
            os.makedirs(test_dir, exist_ok=True)
            
            # 组合新文件名：test_name_timestamp_original_filename
            new_filename = f"{test_name}_{timestamp}_{filename}"
            
            # 保存到测试名称对应的子目录
            screenshot_path = os.path.join(test_dir, new_filename)
            await self.page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"📸 截图已保存: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"❌ 截图失败: {e}")
            return None

