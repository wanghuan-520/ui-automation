"""
注册页面对象模块
提供注册页面的元素定位和操作方法
"""
import logging
from tests.aevatar_station.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class RegisterPage(BasePage):
    """注册页面对象类"""
    
    # 页面URL
    REGISTER_URL = "/Account/Register"
    
    # 页面元素定位器（支持中英文）
    # 修正：移除宽泛的h1-h5匹配，只匹配包含特定文本的h4，避免匹配到隐藏元素
    PAGE_TITLE = 'h4:has-text("Register"), h4:has-text("注册"), strong:has-text("Register")'
    USERNAME_INPUT = 'input[name="Input.UserName"], input#Input_UserName, input[type="text"][placeholder*="name"]'
    EMAIL_INPUT = 'input[name="Input.EmailAddress"], input[type="email"], input#Input_EmailAddress'
    PASSWORD_INPUT = 'input[name="Input.Password"], input[type="password"], input#Input_Password'
    REGISTER_BUTTON = 'button:has-text("注册"), button:has-text("Register"), button:has-text("Sign Up"), button[type="submit"]'
    LOGIN_LINK = 'a:has-text("登录"), a:has-text("Login"), a:has-text("Sign In")'
    ALREADY_REGISTERED_TEXT = 'text="已经注册", text="Already registered", text="Already have an account"'
    LANGUAGE_SWITCHER = 'button:has-text("简体中文")'
    
    # 错误消息定位器
    ERROR_MESSAGE = '.text-danger, .invalid-feedback, [role="alert"]'
    SUCCESS_MESSAGE = '.alert-success, .text-success'
    
    def __init__(self, page):
        """初始化注册页面对象
        
        Args:
            page: Playwright Page对象
        """
        super().__init__(page)
        # 注册页面使用ABP后端URL
        self.page_url = self.auth_url + self.REGISTER_URL
    
    def navigate(self, return_url=None):
        """导航到注册页面
        
        Args:
            return_url: 注册成功后的返回URL（可选）
        """
        url = self.page_url
        if return_url:
            url = f"{self.page_url}?returnUrl={return_url}"
            logger.info(f"导航到注册页面（带returnUrl）: {url}")
        else:
            logger.info(f"导航到注册页面: {url}")
        
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)
        logger.info("注册页面加载完成")
    
    def is_loaded(self) -> bool:
        """检查注册页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 只检查核心表单元素
            username_visible = self.is_visible(self.USERNAME_INPUT, timeout=5000)
            email_visible = self.is_visible(self.EMAIL_INPUT, timeout=5000)
            password_visible = self.is_visible(self.PASSWORD_INPUT, timeout=5000)
            register_button_visible = self.is_visible(self.REGISTER_BUTTON, timeout=5000)
            
            is_loaded = all([
                username_visible,
                email_visible,
                password_visible,
                register_button_visible
            ])
            
            logger.info(f"注册页面加载检查: {is_loaded}")
            logger.info(f"  用户名: {username_visible}, 邮箱: {email_visible}, 密码: {password_visible}, 按钮: {register_button_visible}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def fill_username(self, username: str):
        """填写用户名
        
        Args:
            username: 用户名
        """
        logger.info(f"填写用户名: {username}")
        self.fill_input(self.USERNAME_INPUT, username)
    
    def fill_email(self, email: str):
        """填写邮箱地址
        
        Args:
            email: 邮箱地址
        """
        logger.info(f"填写邮箱: {email}")
        self.fill_input(self.EMAIL_INPUT, email)
    
    def fill_password(self, password: str):
        """填写密码
        
        Args:
            password: 密码
        """
        logger.info(f"填写密码: {'*' * len(password)}")
        self.fill_input(self.PASSWORD_INPUT, password)
    
    def click_register_button(self):
        """点击注册按钮"""
        logger.info("点击注册按钮")
        # 尝试多个选择器
        selectors = [
            'button:has-text("注册")',
            'button:has-text("Register")',
            'button[type="submit"]',
            'input[type="submit"][value*="注册"]',
            'input[type="submit"][value*="Register"]'
        ]
        clicked = False
        for selector in selectors:
            try:
                if self.is_visible(selector, timeout=2000):
                    self.click_element(selector)
                    clicked = True
                    break
            except:
                continue
        if not clicked:
            raise Exception("无法找到注册按钮")
        self.page.wait_for_timeout(1000)
    
    def click_login_link(self):
        """点击登录链接"""
        logger.info("点击登录链接")
        self.click_element(self.LOGIN_LINK)
        self.page.wait_for_timeout(1000)
    
    def register(self, username: str, email: str, password: str):
        """完整的注册流程
        
        Args:
            username: 用户名
            email: 邮箱地址
            password: 密码
        """
        logger.info(f"开始注册流程 - 用户名: {username}, 邮箱: {email}")
        
        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)
        self.click_register_button()
        
        # ⚡ 优化：使用selector等待替代networkidle（更快）
        try:
            self.page.wait_for_selector(self.REGISTER_BUTTON, state="visible", timeout=5000)
        except:
            pass
        self.page.wait_for_timeout(2000)  # 等待注册响应
        
        logger.info("注册请求已提交")
    
    def get_username_value(self) -> str:
        """获取用户名输入框的值
        
        Returns:
            str: 用户名值
        """
        return self.get_input_value(self.USERNAME_INPUT)
    
    def get_email_value(self) -> str:
        """获取邮箱输入框的值
        
        Returns:
            str: 邮箱值
        """
        return self.get_input_value(self.EMAIL_INPUT)
    
    def get_password_value(self) -> str:
        """获取密码输入框的值
        
        Returns:
            str: 密码值
        """
        return self.get_input_value(self.PASSWORD_INPUT)
    
    def is_error_message_visible(self) -> bool:
        """检查是否显示错误消息
        
        Returns:
            bool: 是否显示错误消息
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def get_error_message(self) -> str:
        """获取错误消息文本
        
        Returns:
            str: 错误消息文本
        """
        if self.is_error_message_visible():
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_success_message_visible(self) -> bool:
        """检查是否显示成功消息
        
        Returns:
            bool: 是否显示成功消息
        """
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=3000)
    
    def get_success_message(self) -> str:
        """获取成功消息文本
        
        Returns:
            str: 成功消息文本
        """
        if self.is_success_message_visible():
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def is_field_valid(self, field_selector: str) -> bool:
        """检查字段的HTML5验证状态
        
        Args:
            field_selector: 字段选择器
            
        Returns:
            bool: 字段是否有效
        """
        try:
            is_valid = self.page.evaluate(f"""
                (selector) => {{
                    const element = document.querySelector(selector);
                    return element ? element.validity.valid : false;
                }}
            """, field_selector)
            return is_valid
        except Exception as e:
            logger.error(f"检查字段验证状态失败: {e}")
            return False
    
    def is_username_valid(self) -> bool:
        """检查用户名字段是否有效
        
        Returns:
            bool: 用户名是否有效
        """
        return self.is_field_valid(self.USERNAME_INPUT)
    
    def is_email_valid(self) -> bool:
        """检查邮箱字段是否有效
        
        Returns:
            bool: 邮箱是否有效
        """
        return self.is_field_valid(self.EMAIL_INPUT)
    
    def is_password_valid(self) -> bool:
        """检查密码字段是否有效
        
        Returns:
            bool: 密码是否有效
        """
        return self.is_field_valid(self.PASSWORD_INPUT)
    
    def get_username_validation_message(self) -> str:
        """获取用户名字段的验证消息
        
        Returns:
            str: 验证消息
        """
        try:
            message = self.page.evaluate(f"""
                document.querySelector("{self.USERNAME_INPUT}").validationMessage
            """)
            return message
        except Exception as e:
            logger.error(f"获取用户名验证消息失败: {e}")
            return ""
    
    def get_email_validation_message(self) -> str:
        """获取邮箱字段的验证消息
        
        Returns:
            str: 验证消息
        """
        try:
            message = self.page.evaluate(f"""
                document.querySelector("{self.EMAIL_INPUT}").validationMessage
            """)
            return message
        except Exception as e:
            logger.error(f"获取邮箱验证消息失败: {e}")
            return ""
    
    def get_password_validation_message(self) -> str:
        """获取密码字段的验证消息
        
        Returns:
            str: 验证消息
        """
        try:
            message = self.page.evaluate(f"""
                document.querySelector("{self.PASSWORD_INPUT}").validationMessage
            """)
            return message
        except Exception as e:
            logger.error(f"获取密码验证消息失败: {e}")
            return ""
    
    def is_already_registered_text_visible(self) -> bool:
        """检查"已经注册？"文本是否可见
        
        Returns:
            bool: 文本是否可见
        """
        return self.is_visible(self.ALREADY_REGISTERED_TEXT, timeout=3000)
    
    def is_login_link_visible(self) -> bool:
        """检查登录链接是否可见
        
        Returns:
            bool: 链接是否可见
        """
        return self.is_visible(self.LOGIN_LINK, timeout=3000)
    
    def wait_for_navigation(self, timeout: int = 10000):
        """等待页面导航完成
        
        Args:
            timeout: 超时时间（毫秒）
        """
        try:
            self.page.wait_for_url("**/*", timeout=timeout)
            logger.info(f"导航完成，当前URL: {self.page.url}")
        except Exception as e:
            logger.error(f"等待导航失败: {e}")
    
    def clear_all_fields(self):
        """清空所有输入字段"""
        logger.info("清空所有输入字段")
        self.fill_input(self.USERNAME_INPUT, "")
        self.fill_input(self.EMAIL_INPUT, "")
        self.fill_input(self.PASSWORD_INPUT, "")
