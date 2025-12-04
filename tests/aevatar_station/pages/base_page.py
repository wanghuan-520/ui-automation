"""
BasePage - 所有页面对象的基类
提供通用的页面操作方法和SSL证书处理
"""
from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """页面对象基类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://localhost:3000"
        self.auth_url = "https://localhost:44320"
    
    def navigate_to(self, path=""):
        """导航到指定路径"""
        url = f"{self.base_url}{path}"
        logger.info(f"导航到: {url}")
        self.page.goto(url)
    
    def wait_for_load(self, timeout=30000):
        """等待页面加载完成"""
        logger.info("等待页面加载完成")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def handle_ssl_warning(self):
        """处理SSL证书警告"""
        try:
            logger.info("检查SSL证书警告")
            # 等待一下确保警告页面加载
            self.page.wait_for_timeout(1000)
            
            # 检查是否有证书错误页面
            page_content = self.page.content()
            if "ERR_CERT_AUTHORITY_INVALID" in page_content or "您的连接不是私密连接" in page_content:
                logger.info("检测到SSL证书警告，开始处理")
                
                # 点击"高级"按钮
                advanced_button = self.page.locator("button:has-text('高级'), button:has-text('Advanced')")
                if advanced_button.is_visible(timeout=2000):
                    advanced_button.click()
                    logger.info("已点击'高级'按钮")
                
                # 等待一下让链接出现
                self.page.wait_for_timeout(500)
                
                # 点击"继续前往localhost"链接
                continue_link = self.page.locator("a:has-text('继续前往localhost'), a:has-text('Proceed to localhost')")
                if continue_link.is_visible(timeout=2000):
                    continue_link.click()
                    logger.info("已点击'继续前往localhost'链接")
                    
                # 等待页面跳转
                self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.debug(f"SSL警告处理异常（可能不需要处理）: {e}")
            pass
    
    def click_element(self, selector, timeout=10000):
        """点击元素"""
        logger.info(f"点击元素: {selector}")
        self.page.click(selector, timeout=timeout)
    
    def fill_input(self, selector, value, timeout=10000):
        """填写输入框"""
        logger.info(f"填写输入框 {selector}: {value}")
        self.page.fill(selector, value, timeout=timeout)
    
    def get_text(self, selector, timeout=10000):
        """获取元素文本"""
        return self.page.text_content(selector, timeout=timeout)
    
    def is_visible(self, selector, timeout=5000):
        """检查元素是否可见"""
        try:
            return self.page.is_visible(selector, timeout=timeout)
        except:
            return False
    
    def wait_for_element(self, selector, timeout=10000):
        """等待元素出现"""
        logger.info(f"等待元素出现: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, filename):
        """截图"""
        path = f"screenshots/{filename}"
        logger.info(f"截图保存到: {path}")
        self.page.screenshot(path=path)
    
    def get_current_url(self):
        """获取当前URL"""
        return self.page.url
    
    def wait_for_url(self, url_pattern, timeout=10000):
        """等待URL匹配"""
        logger.info(f"等待URL匹配: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def logout(self):
        """退出登录"""
        try:
            logger.info("开始退出登录")
            
            # 点击用户菜单按钮（通常在右上角）
            user_menu_selectors = [
                "button:has-text('Toggle user menu')",
                "button[aria-label*='user menu' i]",
                "button[aria-label*='Toggle user menu' i]",
                ".user-menu-button",
                "[data-testid='user-menu-button']"
            ]
            
            for selector in user_menu_selectors:
                if self.is_visible(selector, timeout=2000):
                    logger.info(f"找到用户菜单按钮: {selector}")
                    self.click_element(selector)
                    self.page.wait_for_timeout(1000)
                    break
            
            # 点击Logout/Sign Out按钮
            logout_selectors = [
                "button:has-text('Logout')",
                "button:has-text('Sign out')",
                "a:has-text('Logout')",
                "a:has-text('Sign out')",
                "[role='menuitem']:has-text('Logout')",
                "[role='menuitem']:has-text('Sign out')"
            ]
            
            for selector in logout_selectors:
                if self.is_visible(selector, timeout=2000):
                    logger.info(f"找到退出按钮: {selector}")
                    self.click_element(selector)
                    break
            
            # 等待跳转到首页或登录页
            self.page.wait_for_timeout(2000)
            logger.info(f"退出登录完成，当前URL: {self.page.url}")
            
        except Exception as e:
            logger.warning(f"退出登录过程中出现异常: {e}")
            # 尝试直接导航到首页
            self.navigate_to("/")
            self.page.wait_for_timeout(1000)

