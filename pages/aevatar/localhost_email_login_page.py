from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger
from typing import Optional
import re

logger = get_logger(__name__)

class LocalhostEmailLoginPage(BasePage):
    """localhost:5173 邮箱登录页 Page Object"""
    
    # 页面元素定位器
    EMAIL_INPUT = "input[type='email'], input[placeholder*='email' i]"
    PASSWORD_INPUT = "input[type='password'], input[placeholder*='password' i]"
    # 尝试多种按钮选择器，按优先级排序
    LOGIN_BUTTON = "button[type='submit'], button:has-text('Continue'), button:has-text('Login'), button:has-text('Log in'), button:has-text('Sign in'), button:has-text('Submit'), form button"
    FORGET_PASSWORD_LINK = "text=Forget Password?, text=Forgot Password?"
    SIGNUP_LINK = "text=Sign up, text=Register"
    SHOW_PASSWORD_BUTTON = "[aria-label*='show'], [aria-label*='password']"
    ERROR_MESSAGE = "text=/error|invalid|incorrect|wrong|错误|失败/i"
    PAGE_TITLE = "text=/login|sign in|email/i"
    BACK_BUTTON = "button:has-text('Back'), [aria-label*='back']"
    EDIT_EMAIL_BUTTON = "text=Edit, button:has-text('Edit')"
    
    # 页面加载指示器
    page_loaded_indicator = "input[type='email'], input[type='password']"
    
    def __init__(self, page: Page):
        """
        初始化邮箱登录页
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = "http://localhost:5173"
    
    def navigate(self) -> None:
        """导航到登录页面"""
        logger.info(f"导航到登录页: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 检查关键元素是否可见
            email_visible = self.is_element_visible(self.EMAIL_INPUT, timeout=5000)
            password_visible = self.is_element_visible(self.PASSWORD_INPUT, timeout=5000)
            
            # 至少邮箱或密码框之一可见
            is_loaded = email_visible or password_visible
            
            logger.info(f"登录页加载状态: 邮箱框={email_visible}, 密码框={password_visible}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载失败: {str(e)}")
            return False
    
    def enter_email(self, email: str) -> bool:
        """
        输入邮箱
        
        Args:
            email: 邮箱地址
            
        Returns:
            bool: 是否输入成功
        """
        try:
            logger.info(f"输入邮箱: {email}")
            email_locator = self.page.locator(self.EMAIL_INPUT).first
            email_locator.click()
            email_locator.fill(email)
            
            # 检查输入值（不使用断言）
            input_value = email_locator.input_value()
            if input_value != email:
                logger.warning(f"邮箱输入值不匹配: 期望={email}, 实际={input_value}")
                return False
            
            logger.info("邮箱输入成功")
            return True
        except Exception as e:
            logger.error(f"输入邮箱失败: {str(e)}")
            return False
    
    def enter_password(self, password: str) -> bool:
        """
        输入密码
        
        Args:
            password: 密码
            
        Returns:
            bool: 是否输入成功
        """
        try:
            logger.info(f"输入密码: {'*' * len(password)}")
            password_locator = self.page.locator(self.PASSWORD_INPUT).first
            password_locator.click()
            password_locator.fill(password)
            
            logger.info("密码输入成功")
            return True
        except Exception as e:
            logger.error(f"输入密码失败: {str(e)}")
            return False
    
    def click_login(self) -> bool:
        """
        点击登录/继续按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击登录按钮")
            self.page.click(self.LOGIN_BUTTON)
            self.page.wait_for_timeout(2000)
            logger.info("登录按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击登录按钮失败: {str(e)}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """
        完整登录流程
        
        Args:
            email: 邮箱地址
            password: 密码
            
        Returns:
            bool: 是否登录成功
        """
        try:
            logger.info(f"执行完整登录流程: {email}")
            
            # 输入邮箱
            if not self.enter_email(email):
                return False
            
            # 输入密码
            if not self.enter_password(password):
                return False
            
            # 点击登录
            if not self.click_login():
                return False
            
            # 等待登录响应
            self.page.wait_for_timeout(3000)
            
            logger.info("完整登录流程执行完成")
            return True
        except Exception as e:
            logger.error(f"登录流程失败: {str(e)}")
            return False
    
    def toggle_password_visibility(self) -> bool:
        """
        切换密码可见性
        
        Returns:
            bool: 是否切换成功
        """
        try:
            logger.info("切换密码可见性")
            if self.is_element_visible(self.SHOW_PASSWORD_BUTTON, timeout=2000):
                self.page.click(self.SHOW_PASSWORD_BUTTON)
                self.page.wait_for_timeout(500)
                logger.info("密码可见性切换成功")
                return True
            else:
                logger.warning("未找到密码可见性切换按钮")
                return False
        except Exception as e:
            logger.error(f"切换密码可见性失败: {str(e)}")
            return False
    
    def is_password_visible(self) -> bool:
        """
        检查密码是否可见（明文显示）
        
        Returns:
            bool: 密码是否可见
        """
        try:
            password_input = self.page.locator(self.PASSWORD_INPUT).first
            input_type = password_input.get_attribute("type")
            is_visible = input_type == "text"
            logger.info(f"密码可见性: {is_visible} (type={input_type})")
            return is_visible
        except Exception as e:
            logger.error(f"检查密码可见性失败: {str(e)}")
            return False
    
    def click_forget_password(self) -> bool:
        """
        点击忘记密码链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击忘记密码链接")
            self.page.click(self.FORGET_PASSWORD_LINK)
            self.page.wait_for_timeout(1000)
            logger.info("忘记密码链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击忘记密码链接失败: {str(e)}")
            return False
    
    def click_signup(self) -> bool:
        """
        点击注册链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击注册链接")
            self.page.click(self.SIGNUP_LINK)
            self.page.wait_for_timeout(1000)
            logger.info("注册链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击注册链接失败: {str(e)}")
            return False
    
    def get_error_message(self) -> Optional[str]:
        """
        获取错误提示信息
        
        Returns:
            Optional[str]: 错误信息，如果没有错误则返回None
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3000):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.info(f"发现错误提示: {error_text}")
                return error_text
            else:
                logger.info("未发现错误提示")
                return None
        except Exception as e:
            logger.warning(f"获取错误信息失败: {str(e)}")
            return None
    
    def is_login_successful(self, timeout: int = 5000) -> bool:
        """
        判断是否登录成功（通过URL变化）
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否登录成功
        """
        try:
            # 等待URL变化
            self.page.wait_for_timeout(timeout)
            current_url = self.get_current_url()
            
            # 如果URL不再是登录页，认为登录成功
            is_success = current_url != self.page_url and "login" not in current_url.lower()
            
            logger.info(f"登录状态检查: {is_success} (当前URL: {current_url})")
            return is_success
        except Exception as e:
            logger.error(f"检查登录状态失败: {str(e)}")
            return False
    
    def login_with_email(self, email: str, password: str) -> bool:
        """
        使用邮箱和密码登录（别名方法，兼容其他测试代码）
        
        Args:
            email: 邮箱地址
            password: 密码
            
        Returns:
            bool: 是否登录成功
        """
        return self.login(email, password)
    
    def verify_login_success(self, timeout: int = 5000) -> bool:
        """
        验证登录是否成功
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否登录成功
        """
        return self.is_login_successful(timeout)

