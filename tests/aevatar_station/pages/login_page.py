"""
LoginPage - 登录页面对象
路径: /Account/Login
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """登录页面对象"""
    
    # 元素定位器（使用实际检测到的元素属性）
    USERNAME_INPUT = "#LoginInput_UserNameOrEmailAddress"
    PASSWORD_INPUT = "#LoginInput_Password"
    REMEMBER_ME_CHECKBOX = "#LoginInput_RememberMe"
    LOGIN_BUTTON = "button[type='submit']:has-text('Login')"
    REGISTER_LINK = "a:has-text('注册'), a:has-text('Register')"
    FORGOT_PASSWORD_LINK = "a:has-text('忘记密码'), a:has-text('Forgot password')"
    LANGUAGE_BUTTON = "button.dropdown-toggle:has-text('English'), button:has-text('简体中文')"
    PASSWORD_TOGGLE_BUTTON = "#PasswordVisibilityButton"
    PAGE_HEADING = "h4:has-text('登录'), h4:has-text('Login'), label:has-text('Username or email address')"
    ERROR_MESSAGE = ".text-danger, .alert-danger, [role='alert']"
    
    def navigate(self):
        """导航到登录页"""
        logger.info("导航到登录页")
        url = f"{self.auth_url}/Account/Login"
        self.page.goto(url)
        self.handle_ssl_warning()
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.PAGE_HEADING) or self.is_visible(self.LOGIN_BUTTON)
    
    def login(self, username, password, remember_me=False, expect_success=True):
        """
        执行登录操作
        
        Args:
            username: 用户名或邮箱
            password: 密码
            remember_me: 是否勾选"记住我"
            expect_success: 是否期望登录成功（True=等待跳转，False=仅提交表单）
        """
        logger.info(f"登录用户: {username}")
        
        # 填写用户名
        self.fill_input(self.USERNAME_INPUT, username)
        
        # 填写密码
        self.fill_input(self.PASSWORD_INPUT, password)
        
        # 勾选记住我
        if remember_me:
            self.page.check(self.REMEMBER_ME_CHECKBOX)
        
        # 点击登录按钮
        self.click_element(self.LOGIN_BUTTON)
        
        # 如果不期望成功（测试失败场景），只等待一小段时间让服务器响应
        if not expect_success:
            logger.info("提交登录表单（不期望成功）...")
            self.page.wait_for_timeout(2000)
            logger.info(f"表单已提交，当前URL: {self.page.url}")
            return
        
        # 期望成功的情况：等待登录完成（URL 不再包含 /Account/Login）
        logger.info("等待登录完成...")
        try:
            # 等待URL变化，最多30秒
            self.page.wait_for_function(
                "() => !window.location.href.includes('/Account/Login')",
                timeout=30000
            )
            logger.info(f"登录跳转完成，当前URL: {self.page.url}")
        except Exception as e:
            logger.error(f"登录跳转超时: {e}")
            logger.error(f"当前URL: {self.page.url}")
            # 检查是否有错误消息
            if self.is_error_message_visible():
                error_msg = self.get_error_message()
                logger.error(f"登录错误: {error_msg}")
                raise Exception(f"登录失败: {error_msg}")
            raise
        
        # 处理可能的SSL警告
        self.handle_ssl_warning()
        
        # 等待页面稳定 - 使用domcontentloaded而不是networkidle
        # networkidle可能因为长轮询/WebSocket/后台请求而永远无法完成
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=30000)
            # 额外等待一段时间让JS初始化
            self.page.wait_for_timeout(2000)
            logger.info("页面DOM加载完成")
        except Exception as e:
            logger.warning(f"页面加载状态检查超时（但可能已成功）: {e}")
    
    def fill_username(self, username):
        """填写用户名"""
        self.fill_input(self.USERNAME_INPUT, username)
    
    def fill_password(self, password):
        """填写密码"""
        self.fill_input(self.PASSWORD_INPUT, password)
    
    def get_username_value(self):
        """获取用户名输入框的值"""
        return self.page.input_value(self.USERNAME_INPUT)
    
    def get_password_value(self):
        """获取密码输入框的值"""
        return self.page.input_value(self.PASSWORD_INPUT)
    
    def is_error_message_visible(self):
        """检查错误消息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def get_error_message(self):
        """获取错误消息文本"""
        if self.is_error_message_visible():
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def click_register(self):
        """点击注册链接"""
        logger.info("点击注册链接")
        self.click_element(self.REGISTER_LINK)
    
    def click_forgot_password(self):
        """点击忘记密码链接"""
        logger.info("点击忘记密码链接")
        self.click_element(self.FORGOT_PASSWORD_LINK)
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        logger.info("切换密码可见性")
        self.click_element(self.PASSWORD_TOGGLE_BUTTON)

