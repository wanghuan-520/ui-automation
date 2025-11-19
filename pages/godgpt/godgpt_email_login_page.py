from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger
from typing import Optional
import re

logger = get_logger(__name__)

class GodGPTEmailLoginPage(BasePage):
    """GodGPT 密码输入页 Page Object"""
    
    # 页面元素定位器
    PAGE_TITLE = "text=Login with email"
    BACK_BUTTON = "button:has-text('Back'), [aria-label*='back'], img[alt*='back']"
    EMAIL_DISPLAY = "text=/@/"  # 匹配邮箱格式
    EDIT_BUTTON = "text=Edit"
    PASSWORD_INPUT = "input[type='password'], input[placeholder*='password' i]"
    SHOW_PASSWORD_BUTTON = "[aria-label*='show'], [aria-label*='password'], button:near(:text('password'))"
    CONTINUE_BUTTON = "button:has-text('Continue')"
    FORGET_PASSWORD_LINK = "text=Forget Password?"
    LOGIN_SIGNUP_LINK = "text=Log in / Sign up"
    ERROR_MESSAGE = "text=/error|invalid|incorrect|wrong|错误|不正确/i"
    
    # 页面加载指示器
    page_loaded_indicator = "input[type='password'], input[placeholder*='password' i]"
    
    def __init__(self, page: Page):
        """
        初始化密码输入页
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        # URL 是动态的，包含邮箱参数
        self.page_url_pattern = "https://godgpt-ui-testnet.aelf.dev/email-login"
    
    def navigate(self) -> None:
        """
        导航到密码输入页（通常不直接导航，而是通过登录首页跳转）
        """
        logger.warning("密码输入页通常不直接导航，需要通过登录首页输入邮箱后跳转")
    
    def is_loaded(self) -> bool:
        """
        检查页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 检查密码输入框是否可见
            password_input_visible = self.is_element_visible(self.PASSWORD_INPUT, timeout=10000)
            
            # 检查URL是否包含 /email-login
            current_url = self.get_current_url()
            url_match = "/email-login" in current_url
            
            logger.info(f"密码输入页加载状态: 密码输入框={password_input_visible}, URL匹配={url_match}")
            return password_input_visible and url_match
        except Exception as e:
            logger.error(f"检查页面加载失败: {str(e)}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30000):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间(毫秒)
        """
        logger.info("等待密码输入页加载完成")
        try:
            # 等待URL变化
            self.page.wait_for_url(re.compile(r".*/email-login.*"), timeout=timeout)
            # 等待密码输入框出现
            self.page.wait_for_selector(self.PASSWORD_INPUT, timeout=timeout)
            # 等待渲染完成
            self.page.wait_for_timeout(2000)
            logger.info("密码输入页加载完成")
        except Exception as e:
            logger.warning(f"等待页面加载超时: {str(e)}")
    
    def get_displayed_email(self) -> Optional[str]:
        """
        获取显示的邮箱地址
        
        Returns:
            Optional[str]: 邮箱地址，如果未找到则返回None
        """
        try:
            # 从URL参数中获取邮箱
            current_url = self.get_current_url()
            if "email=" in current_url:
                email = current_url.split("email=")[1].split("&")[0]
                # URL解码
                from urllib.parse import unquote
                email = unquote(email)
                logger.info(f"从URL获取邮箱: {email}")
                return email
            
            # 从页面元素中获取邮箱（备选方案）
            email_elements = self.page.locator("text=/@/").all()
            if email_elements:
                email_text = email_elements[0].text_content()
                logger.info(f"从页面元素获取邮箱: {email_text}")
                return email_text
            
            logger.warning("未找到显示的邮箱地址")
            return None
        except Exception as e:
            logger.error(f"获取显示的邮箱失败: {str(e)}")
            return None
    
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
            
            # 验证输入（注意：密码输入框可能隐藏值）
            logger.info("密码输入成功")
            return True
        except Exception as e:
            logger.error(f"输入密码失败: {str(e)}")
            return False
    
    def click_continue(self) -> bool:
        """
        点击继续按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Continue 按钮")
            self.page.click(self.CONTINUE_BUTTON)
            # 等待登录处理
            self.page.wait_for_timeout(3000)
            logger.info("Continue 按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Continue 按钮失败: {str(e)}")
            return False
    
    def click_show_hide_password(self) -> bool:
        """
        点击显示/隐藏密码图标
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("切换密码可见性")
            # 查找密码可见性切换按钮（通常是眼睛图标）
            toggle_buttons = [
                "button:near(input[type='password'])",
                "[aria-label*='show']",
                "[aria-label*='hide']",
                "img[alt*='eye']"
            ]
            
            for selector in toggle_buttons:
                if self.is_element_visible(selector, timeout=2000):
                    self.page.click(selector)
                    logger.info("密码可见性切换成功")
                    return True
            
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
            # 检查密码输入框的type属性
            password_input = self.page.locator(self.PASSWORD_INPUT).first
            input_type = password_input.get_attribute("type")
            
            is_visible = input_type == "text"
            logger.info(f"密码可见性状态: {is_visible} (type={input_type})")
            return is_visible
        except Exception as e:
            logger.error(f"检查密码可见性失败: {str(e)}")
            return False
    
    def click_edit_email(self) -> bool:
        """
        点击编辑邮箱按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Edit 按钮")
            self.page.click(self.EDIT_BUTTON)
            self.page.wait_for_timeout(1000)
            logger.info("Edit 按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Edit 按钮失败: {str(e)}")
            return False
    
    def click_forget_password(self) -> bool:
        """
        点击忘记密码链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Forget Password 链接")
            self.page.click(self.FORGET_PASSWORD_LINK)
            self.page.wait_for_timeout(1000)
            logger.info("Forget Password 链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Forget Password 链接失败: {str(e)}")
            return False
    
    def click_back(self) -> bool:
        """
        点击返回按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击返回按钮")
            self.page.click(self.BACK_BUTTON)
            self.page.wait_for_timeout(1000)
            logger.info("返回按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击返回按钮失败: {str(e)}")
            return False
    
    def get_password_validation_error(self) -> Optional[str]:
        """
        获取密码验证错误信息
        
        Returns:
            Optional[str]: 错误信息，如果没有错误则返回None
        """
        try:
            # 尝试查找错误提示元素
            error_selectors = [
                "text=/error|invalid|incorrect|wrong|错误|不正确|密码/i",
                ".error-message",
                "[role='alert']",
                ".validation-error"
            ]
            
            for selector in error_selectors:
                if self.is_element_visible(selector, timeout=3000):
                    error_text = self.get_element_text(selector)
                    logger.info(f"发现密码验证错误: {error_text}")
                    return error_text
            
            logger.info("未发现密码验证错误")
            return None
        except Exception as e:
            logger.warning(f"获取密码验证错误失败: {str(e)}")
            return None
    
    def is_login_signup_link_visible(self) -> bool:
        """
        检查 Log in / Sign up 链接是否可见
        
        Returns:
            bool: 链接是否可见
        """
        return self.is_element_visible(self.LOGIN_SIGNUP_LINK)
    
    def wait_for_login_success(self, timeout: int = 10000) -> bool:
        """
        等待登录成功（URL跳转）
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否登录成功
        """
        try:
            logger.info("等待登录成功...")
            # 等待URL变化，离开 email-login 页面
            self.page.wait_for_url(re.compile(r"^((?!email-login).)*$"), timeout=timeout)
            
            current_url = self.get_current_url()
            logger.info(f"登录后跳转到: {current_url}")
            return True
        except Exception as e:
            logger.error(f"等待登录成功超时: {str(e)}")
            return False
    
    def get_page_title_text(self) -> Optional[str]:
        """
        获取页面标题文本
        
        Returns:
            Optional[str]: 页面标题文本
        """
        try:
            title_text = self.get_element_text(self.PAGE_TITLE)
            logger.info(f"页面标题: {title_text}")
            return title_text
        except Exception as e:
            logger.warning(f"获取页面标题失败: {str(e)}")
            return None

