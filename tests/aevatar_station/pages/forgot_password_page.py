"""
忘记密码页面对象模块
提供忘记密码页面的元素定位和操作方法
"""
import logging
from tests.aevatar_station.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ForgotPasswordPage(BasePage):
    """忘记密码页面对象类"""
    
    # 页面URL
    FORGOT_PASSWORD_URL = "/Account/ForgotPassword"
    
    # 页面元素定位器
    PAGE_TITLE = "text=忘记密码？"
    HINT_TEXT = "text=您的电子邮件中将收到重置密码的链接"
    EMAIL_INPUT = 'input[name="Input.EmailAddress"]'
    SUBMIT_BUTTON = 'button:has-text("提交")'
    LOGIN_LINK = 'a:has-text("登录")'
    LANGUAGE_SWITCHER = 'button:has-text("简体中文")'
    
    # 消息定位器
    SUCCESS_MESSAGE = '.alert-success, .text-success, [role="alert"].alert-success'
    ERROR_MESSAGE = '.alert-danger, .text-danger, .invalid-feedback, [role="alert"].alert-danger'
    INFO_MESSAGE = '.alert-info, .text-info'
    
    def __init__(self, page):
        """初始化忘记密码页面对象
        
        Args:
            page: Playwright Page对象
        """
        super().__init__(page)
        # 忘记密码页面使用ABP后端URL
        self.page_url = self.auth_url + self.FORGOT_PASSWORD_URL
    
    def navigate(self):
        """导航到忘记密码页面"""
        logger.info(f"导航到忘记密码页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)
        logger.info("忘记密码页面加载完成")
    
    def is_loaded(self) -> bool:
        """检查忘记密码页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 检查页面标题和关键元素
            title_visible = self.is_visible(self.PAGE_TITLE, timeout=5000)
            email_visible = self.is_visible(self.EMAIL_INPUT, timeout=5000)
            submit_button_visible = self.is_visible(self.SUBMIT_BUTTON, timeout=5000)
            
            is_loaded = all([
                title_visible,
                email_visible,
                submit_button_visible
            ])
            
            logger.info(f"忘记密码页面加载检查: {is_loaded}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    def fill_email(self, email: str):
        """填写邮箱地址
        
        Args:
            email: 邮箱地址
        """
        logger.info(f"填写邮箱: {email}")
        self.fill_input(self.EMAIL_INPUT, email)
    
    def click_submit_button(self):
        """点击提交按钮"""
        logger.info("点击提交按钮")
        self.click_element(self.SUBMIT_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def click_login_link(self):
        """点击登录链接"""
        logger.info("点击登录链接")
        self.click_element(self.LOGIN_LINK)
        self.page.wait_for_timeout(1000)
    
    def submit_forgot_password(self, email: str):
        """完整的忘记密码提交流程
        
        Args:
            email: 邮箱地址
        """
        logger.info(f"开始提交忘记密码请求 - 邮箱: {email}")
        
        self.fill_email(email)
        self.click_submit_button()
        
        # 等待页面响应
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)
        
        logger.info("忘记密码请求已提交")
    
    def get_email_value(self) -> str:
        """获取邮箱输入框的值
        
        Returns:
            str: 邮箱值
        """
        return self.get_input_value(self.EMAIL_INPUT)
    
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
    
    def is_info_message_visible(self) -> bool:
        """检查是否显示信息消息
        
        Returns:
            bool: 是否显示信息消息
        """
        return self.is_visible(self.INFO_MESSAGE, timeout=3000)
    
    def get_info_message(self) -> str:
        """获取信息消息文本
        
        Returns:
            str: 信息消息文本
        """
        if self.is_info_message_visible():
            return self.get_text(self.INFO_MESSAGE)
        return ""
    
    def is_hint_text_visible(self) -> bool:
        """检查提示文本是否可见
        
        Returns:
            bool: 提示文本是否可见
        """
        return self.is_visible(self.HINT_TEXT, timeout=3000)
    
    def get_hint_text(self) -> str:
        """获取提示文本
        
        Returns:
            str: 提示文本
        """
        if self.is_hint_text_visible():
            return self.get_text(self.HINT_TEXT)
        return ""
    
    def is_email_valid(self) -> bool:
        """检查邮箱字段的HTML5验证状态
        
        Returns:
            bool: 邮箱是否有效
        """
        try:
            is_valid = self.page.evaluate(f"""
                (selector) => {{
                    const element = document.querySelector(selector);
                    return element ? element.validity.valid : false;
                }}
            """, self.EMAIL_INPUT)
            return is_valid
        except Exception as e:
            logger.error(f"检查邮箱验证状态失败: {e}")
            return False
    
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
    
    def is_email_field_required(self) -> bool:
        """检查邮箱字段是否为必填
        
        Returns:
            bool: 是否必填
        """
        try:
            is_required = self.page.evaluate(f"""
                document.querySelector("{self.EMAIL_INPUT}").required
            """)
            return is_required
        except Exception as e:
            logger.error(f"检查必填状态失败: {e}")
            return False
    
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
    
    def clear_email_field(self):
        """清空邮箱输入字段"""
        logger.info("清空邮箱输入字段")
        self.fill_input(self.EMAIL_INPUT, "")
    
    def is_submit_button_enabled(self) -> bool:
        """检查提交按钮是否启用
        
        Returns:
            bool: 按钮是否启用
        """
        try:
            is_enabled = not self.page.locator(self.SUBMIT_BUTTON).is_disabled()
            logger.info(f"提交按钮启用状态: {is_enabled}")
            return is_enabled
        except Exception as e:
            logger.error(f"检查按钮状态失败: {e}")
            return False

