from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger
from typing import Optional

logger = get_logger(__name__)

class GodGPTLandingPage(BasePage):
    """GodGPT 登录首页 Page Object"""
    
    # 页面元素定位器
    LOGO_TEXT = "text=GodGPT"
    GET_APP_BUTTON = "text=Get App"
    SKIP_BUTTON = "text=Skip"
    APPLE_LOGIN_BUTTON = "text=Continue with Apple"
    GOOGLE_LOGIN_BUTTON = "text=Continue with Google"
    EMAIL_INPUT = "input[type='text'], input[type='email']"
    EMAIL_INPUT_PLACEHOLDER = "text=/Enter your email/i"
    CONTINUE_EMAIL_BUTTON = "text=Continue with Email"
    OR_DIVIDER = "text=OR"
    TERMS_LINK = "text=Terms of Service"
    PRIVACY_LINK = "text=Privacy Policy"
    CONTACT_LINK = "text=Contact Us"
    
    # 页面加载指示器
    page_loaded_indicator = "text=Continue with Email"
    
    def __init__(self, page: Page):
        """
        初始化登录首页
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = "https://godgpt-ui-testnet.aelf.dev/"
    
    def navigate(self) -> None:
        """导航到登录首页"""
        logger.info(f"导航到GodGPT登录首页: {self.page_url}")
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
            email_input_visible = self.is_element_visible(self.EMAIL_INPUT, timeout=10000)
            continue_button_visible = self.is_element_visible(self.CONTINUE_EMAIL_BUTTON, timeout=10000)
            
            logger.info(f"登录首页加载状态: 邮箱输入框={email_input_visible}, 继续按钮={continue_button_visible}")
            return email_input_visible and continue_button_visible
        except Exception as e:
            logger.error(f"检查页面加载失败: {str(e)}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30000):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间(毫秒)
        """
        logger.info("等待登录首页加载完成")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        # 等待 React 渲染
        self.page.wait_for_timeout(2000)
        
        # 等待关键元素出现
        try:
            self.page.wait_for_selector(self.CONTINUE_EMAIL_BUTTON, timeout=timeout)
            logger.info("登录首页加载完成")
        except Exception as e:
            logger.warning(f"等待页面元素超时: {str(e)}")
    
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
            # 先尝试通过 placeholder 查找
            email_locator = self.page.locator(self.EMAIL_INPUT).first
            email_locator.click()
            email_locator.fill(email)
            
            # 验证输入
            input_value = email_locator.input_value()
            if input_value == email:
                logger.info(f"邮箱输入成功: {email}")
                return True
            else:
                logger.warning(f"邮箱输入值不匹配: 期望={email}, 实际={input_value}")
                return False
        except Exception as e:
            logger.error(f"输入邮箱失败: {str(e)}")
            return False
    
    def click_continue_with_email(self) -> bool:
        """
        点击邮箱登录按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Continue with Email 按钮")
            self.page.click(self.CONTINUE_EMAIL_BUTTON)
            # 等待页面跳转
            self.page.wait_for_timeout(2000)
            logger.info("Continue with Email 按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Continue with Email 按钮失败: {str(e)}")
            return False
    
    def click_apple_login(self) -> bool:
        """
        点击 Apple 登录按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Apple 登录按钮")
            self.page.click(self.APPLE_LOGIN_BUTTON)
            logger.info("Apple 登录按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Apple 登录按钮失败: {str(e)}")
            return False
    
    def click_google_login(self) -> bool:
        """
        点击 Google 登录按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Google 登录按钮")
            self.page.click(self.GOOGLE_LOGIN_BUTTON)
            logger.info("Google 登录按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Google 登录按钮失败: {str(e)}")
            return False
    
    def click_skip(self) -> bool:
        """
        点击跳过按钮
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击 Skip 按钮")
            self.page.click(self.SKIP_BUTTON)
            self.page.wait_for_timeout(1000)
            logger.info("Skip 按钮点击成功")
            return True
        except Exception as e:
            logger.error(f"点击 Skip 按钮失败: {str(e)}")
            return False
    
    def get_email_validation_error(self) -> Optional[str]:
        """
        获取邮箱验证错误信息
        
        Returns:
            Optional[str]: 错误信息，如果没有错误则返回None
        """
        try:
            # 尝试查找错误提示元素（根据实际页面调整选择器）
            error_selectors = [
                "text=/error|invalid|错误|格式不正确/i",
                ".error-message",
                "[role='alert']",
                ".validation-error"
            ]
            
            for selector in error_selectors:
                if self.is_element_visible(selector, timeout=2000):
                    error_text = self.get_element_text(selector)
                    logger.info(f"发现邮箱验证错误: {error_text}")
                    return error_text
            
            logger.info("未发现邮箱验证错误")
            return None
        except Exception as e:
            logger.warning(f"获取邮箱验证错误失败: {str(e)}")
            return None
    
    def is_logo_visible(self) -> bool:
        """
        检查Logo是否可见
        
        Returns:
            bool: Logo是否可见
        """
        return self.is_element_visible(self.LOGO_TEXT)
    
    def is_get_app_button_visible(self) -> bool:
        """
        检查 Get App 按钮是否可见
        
        Returns:
            bool: Get App 按钮是否可见
        """
        return self.is_element_visible(self.GET_APP_BUTTON)
    
    def is_skip_button_visible(self) -> bool:
        """
        检查 Skip 按钮是否可见
        
        Returns:
            bool: Skip 按钮是否可见
        """
        return self.is_element_visible(self.SKIP_BUTTON)
    
    def click_terms_of_service(self) -> bool:
        """
        点击服务条款链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击服务条款链接")
            self.page.click(self.TERMS_LINK)
            logger.info("服务条款链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击服务条款链接失败: {str(e)}")
            return False
    
    def click_privacy_policy(self) -> bool:
        """
        点击隐私政策链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击隐私政策链接")
            self.page.click(self.PRIVACY_LINK)
            logger.info("隐私政策链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击隐私政策链接失败: {str(e)}")
            return False
    
    def click_contact_us(self) -> bool:
        """
        点击联系我们链接
        
        Returns:
            bool: 是否点击成功
        """
        try:
            logger.info("点击联系我们链接")
            self.page.click(self.CONTACT_LINK)
            logger.info("联系我们链接点击成功")
            return True
        except Exception as e:
            logger.error(f"点击联系我们链接失败: {str(e)}")
            return False
    
    def get_page_elements_status(self) -> dict:
        """
        获取页面所有关键元素的可见性状态
        
        Returns:
            dict: 元素状态字典
        """
        status = {
            "logo": self.is_logo_visible(),
            "get_app_button": self.is_get_app_button_visible(),
            "skip_button": self.is_skip_button_visible(),
            "apple_login": self.is_element_visible(self.APPLE_LOGIN_BUTTON),
            "google_login": self.is_element_visible(self.GOOGLE_LOGIN_BUTTON),
            "email_input": self.is_element_visible(self.EMAIL_INPUT),
            "continue_email_button": self.is_element_visible(self.CONTINUE_EMAIL_BUTTON),
            "terms_link": self.is_element_visible(self.TERMS_LINK),
            "privacy_link": self.is_element_visible(self.PRIVACY_LINK)
        }
        
        logger.info(f"页面元素状态: {status}")
        return status

