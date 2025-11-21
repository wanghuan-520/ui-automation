"""
测试辅助函数模块
提供跨测试文件共享的工具函数
"""
import random
import string
from datetime import datetime
from typing import Optional
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage
import logging

logger = logging.getLogger(__name__)


# ========== 随机数据生成 ==========

def generate_random_name(prefix: str = "test", length: int = 6) -> str:
    """
    生成随机名称
    
    Args:
        prefix: 名称前缀
        length: 随机字符串长度
        
    Returns:
        str: 格式为 {prefix}_{timestamp}_{random_str}
    """
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"{prefix}-{timestamp}-{random_str}"


def generate_random_email(domain: str = "example.com") -> str:
    """
    生成随机邮箱地址
    
    Args:
        domain: 邮箱域名
        
    Returns:
        str: 随机邮箱地址
    """
    random_str = ''.join(random.choices(string.ascii_lowercase, k=10))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"test_{timestamp}_{random_str}@{domain}"


def generate_random_url(protocol: str = "https", domain_suffix: str = "example.com") -> str:
    """
    生成随机URL
    
    Args:
        protocol: 协议（http/https）
        domain_suffix: 域名后缀
        
    Returns:
        str: 随机URL
    """
    random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{protocol}://{random_str}.{domain_suffix}"


# ========== Async页面操作辅助函数 ==========

async def take_screenshot_async(page: AsyncPage, screenshot_dir: str, filename: str) -> bool:
    """
    异步截图
    
    Args:
        page: Playwright异步页面对象
        screenshot_dir: 截图目录
        filename: 文件名
        
    Returns:
        bool: 是否成功
    """
    import os
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, filename)
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图: {screenshot_path}")
        return True
    except Exception as e:
        logger.error(f"❌ 截图失败: {e}")
        return False


async def wait_for_toast_async(page: AsyncPage, expected_text: str, timeout: int = 5000) -> bool:
    """
    等待并验证Toast消息（异步）
    
    Args:
        page: Playwright异步页面对象
        expected_text: 期望的Toast文本（支持正则）
        timeout: 超时时间（毫秒）
        
    Returns:
        bool: 是否找到Toast
    """
    try:
        toast_selector = f'text=/.*{expected_text}.*/i'
        toast = await page.wait_for_selector(toast_selector, timeout=timeout)
        if toast:
            logger.info(f"✅ Toast验证: {expected_text}")
            return True
    except:
        logger.warning(f"⚠️ 未找到Toast: {expected_text}")
    return False


async def wait_for_page_initialization_async(page: AsyncPage, max_wait_seconds: int = 30) -> bool:
    """
    等待页面初始化完成（等待Scanning/Initialising状态消失）- 异步
    
    Args:
        page: Playwright异步页面对象
        max_wait_seconds: 最大等待时间（秒）
        
    Returns:
        bool: 是否初始化完成
    """
    logger.info(f"等待页面初始化（最多{max_wait_seconds}秒）...")
    
    for i in range(max_wait_seconds):
        await page.wait_for_timeout(1000)
        
        # 检查是否还有loading文本
        scanning = await page.query_selector('text=/Scanning|Initialising/i')
        if scanning:
            is_visible = await scanning.is_visible()
            if not is_visible:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                return True
        else:
            logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
            return True
    
    logger.warning(f"⚠️ 页面初始化超时 (等待了{max_wait_seconds}秒)")
    return False


# ========== Sync页面操作辅助函数 ==========

def take_screenshot_sync(page: SyncPage, screenshot_dir: str, filename: str) -> bool:
    """
    同步截图
    
    Args:
        page: Playwright同步页面对象
        screenshot_dir: 截图目录
        filename: 文件名
        
    Returns:
        bool: 是否成功
    """
    import os
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, filename)
        page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图: {screenshot_path}")
        return True
    except Exception as e:
        logger.error(f"❌ 截图失败: {e}")
        return False


def wait_for_toast_sync(page: SyncPage, expected_text: str, timeout: int = 5000) -> bool:
    """
    等待并验证Toast消息（同步）
    
    Args:
        page: Playwright同步页面对象
        expected_text: 期望的Toast文本（支持正则）
        timeout: 超时时间（毫秒）
        
    Returns:
        bool: 是否找到Toast
    """
    try:
        toast_selector = f'text=/.*{expected_text}.*/i'
        toast = page.wait_for_selector(toast_selector, timeout=timeout)
        if toast:
            logger.info(f"✅ Toast验证: {expected_text}")
            return True
    except:
        logger.warning(f"⚠️ 未找到Toast: {expected_text}")
    return False


# ========== 数据验证 ==========

def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否有效
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    验证URL格式
    
    Args:
        url: URL地址
        
    Returns:
        bool: 是否有效
    """
    import re
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return bool(re.match(pattern, url))


# ========== 测试环境配置 ==========

class TestConfig:
    """测试环境配置"""
    
    # Staging环境
    STAGING_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
    STAGING_EMAIL = "aevatarwh1@teml.net"
    STAGING_PASSWORD = "Wh520520!"
    
    # Local环境
    LOCAL_BASE_URL = "http://localhost:3000"
    LOCAL_EMAIL = "haylee@test.com"
    LOCAL_PASSWORD = "Wh520520!"
    
    # 截图目录
    SCREENSHOT_ROOT = "test-screenshots"
    
    @classmethod
    def get_screenshot_dir(cls, module_name: str) -> str:
        """
        获取模块专用截图目录
        
        Args:
            module_name: 模块名称（如 "workflows", "api_keys"）
            
        Returns:
            str: 截图目录路径
        """
        import os
        return os.path.join(cls.SCREENSHOT_ROOT, module_name)

