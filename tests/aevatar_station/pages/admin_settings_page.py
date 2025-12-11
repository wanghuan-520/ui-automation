"""
AdminSettingsPage - 管理员设置页面对象
路径: /admin/settings
ABP Framework Settings模块 - 系统配置功能
"""
from playwright.sync_api import Page
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class AdminSettingsPage(BasePage):
    """管理员设置页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin/settings"
        
        # 页面标题
        self.PAGE_TITLE = "h1:has-text('Settings'), h2:has-text('Settings'), .page-title:has-text('Settings')"
        self.BREADCRUMB = "nav[aria-label='breadcrumb'], .breadcrumb"
        
        # Tab导航
        self.TABS_CONTAINER = "[role='tablist'], .nav-tabs"
        self.EMAILING_TAB = "button[role='tab']:has-text('Emailing'), [role='tab']:has-text('Emailing'), a:has-text('Emailing')"
        self.FEATURE_MANAGEMENT_TAB = "button[role='tab']:has-text('Feature'), [role='tab']:has-text('Feature'), a:has-text('Feature')"
        self.IDENTITY_TAB = "button[role='tab']:has-text('Identity'), [role='tab']:has-text('Identity'), a:has-text('Identity')"
        self.ACCOUNT_TAB = "button[role='tab']:has-text('Account'), [role='tab']:has-text('Account'), a:has-text('Account')"
        
        # Tab内容区域
        self.TAB_CONTENT = "[role='tabpanel'], .tab-content, .tab-pane.active"
        
        # ================== Emailing设置 ==================
        # SMTP配置
        self.SMTP_HOST = "input[name*='smtpHost'], input#SmtpHost, input[placeholder*='Host']"
        self.SMTP_PORT = "input[name*='smtpPort'], input#SmtpPort, input[type='number'][name*='port']"
        self.SMTP_USERNAME = "input[name*='smtpUserName'], input#SmtpUserName"
        self.SMTP_PASSWORD = "input[name*='smtpPassword'], input#SmtpPassword"
        self.SMTP_DOMAIN = "input[name*='smtpDomain'], input#SmtpDomain"
        self.SMTP_ENABLE_SSL = "input[name*='smtpEnableSsl'], input[type='checkbox'][id*='ssl']"
        self.SMTP_USE_DEFAULT_CREDENTIALS = "input[name*='useDefaultCredentials'], input[type='checkbox'][id*='default']"
        
        # 发件人配置
        self.DEFAULT_FROM_ADDRESS = "input[name*='defaultFromAddress'], input#DefaultFromAddress, input[type='email']"
        self.DEFAULT_FROM_NAME = "input[name*='defaultFromDisplayName'], input#DefaultFromDisplayName"
        
        # ================== Identity设置 ==================
        # 密码策略
        self.PASSWORD_REQUIRED_LENGTH = "input[name*='requiredLength'], input#RequiredLength"
        self.PASSWORD_REQUIRE_DIGIT = "input[name*='requireDigit'], input[type='checkbox'][id*='digit']"
        self.PASSWORD_REQUIRE_LOWERCASE = "input[name*='requireLowercase'], input[type='checkbox'][id*='lowercase']"
        self.PASSWORD_REQUIRE_UPPERCASE = "input[name*='requireUppercase'], input[type='checkbox'][id*='uppercase']"
        self.PASSWORD_REQUIRE_NON_ALPHANUMERIC = "input[name*='requireNonAlphanumeric'], input[type='checkbox'][id*='nonAlphanumeric']"
        self.PASSWORD_REQUIRED_UNIQUE_CHARS = "input[name*='requiredUniqueChars'], input#RequiredUniqueChars"
        
        # 锁定策略
        self.LOCKOUT_ALLOWED_ATTEMPTS = "input[name*='maxFailedAccessAttempts'], input#MaxFailedAccessAttempts"
        self.LOCKOUT_SECONDS = "input[name*='defaultLockoutTimeSpan'], input#DefaultLockoutTimeSpan"
        self.LOCKOUT_ENABLED = "input[name*='allowedForNewUsers'], input[type='checkbox'][id*='lockout']"
        
        # 用户策略
        self.USER_REQUIRE_EMAIL = "input[name*='requireUniqueEmail'], input[type='checkbox'][id*='email']"
        self.USER_ALLOWED_CHARACTERS = "input[name*='allowedUserNameCharacters']"
        
        # 登录策略
        self.SIGNIN_REQUIRE_CONFIRMED_EMAIL = "input[name*='requireConfirmedEmail'], input[type='checkbox'][id*='confirmedEmail']"
        self.SIGNIN_REQUIRE_CONFIRMED_PHONE = "input[name*='requireConfirmedPhoneNumber'], input[type='checkbox'][id*='confirmedPhone']"
        
        # ================== 通用元素 ==================
        # 保存按钮
        self.SAVE_BUTTON = "button:has-text('Save'), button[type='submit']:has-text('Save')"
        self.SAVE_ALL_BUTTON = "button:has-text('Save all'), button:has-text('Save All')"
        
        # 重置按钮
        self.RESET_BUTTON = "button:has-text('Reset'), button:has-text('Cancel')"
        
        # 测试邮件按钮
        self.SEND_TEST_EMAIL_BUTTON = "button:has-text('Send test email'), button:has-text('Test')"
        
        # 对话框
        self.DIALOG = "[role='dialog'], .modal, .dialog"
        self.DIALOG_TITLE = "[role='dialog'] h2, .modal-title"
        self.DIALOG_CLOSE = "[role='dialog'] button[aria-label*='close' i], .modal .close"
        self.DIALOG_CONFIRM = "[role='dialog'] button:has-text('OK'), [role='dialog'] button:has-text('Send')"
        self.DIALOG_CANCEL = "[role='dialog'] button:has-text('Cancel')"
        
        # 测试邮件对话框
        self.TEST_EMAIL_INPUT = "input[type='email'], input[name*='email']"
        self.TEST_EMAIL_SEND = "button:has-text('Send'), button:has-text('OK')"
        
        # 提示消息
        self.SUCCESS_MESSAGE = ".toast-success, .alert-success, [role='alert']:has-text('success')"
        self.ERROR_MESSAGE = ".toast-error, .alert-danger, [role='alert']:has-text('error')"
        self.INFO_MESSAGE = ".toast-info, .alert-info"
        
        # 表单验证错误
        self.VALIDATION_ERROR = ".text-danger, .field-validation-error, .invalid-feedback"
        
        # 加载状态
        self.LOADING_SPINNER = ".spinner, .loading, [role='progressbar']"
        
        # Section标题
        self.SECTION_PASSWORD = "h3:has-text('Password'), .section-title:has-text('Password')"
        self.SECTION_LOCKOUT = "h3:has-text('Lockout'), .section-title:has-text('Lockout')"
        self.SECTION_USER = "h3:has-text('User'), .section-title:has-text('User')"
        self.SECTION_SIGNIN = "h3:has-text('Sign in'), .section-title:has-text('Sign in')"
    
    def navigate(self):
        """导航到设置页面"""
        logger.info("导航到管理员设置页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            has_tabs = self.is_visible(self.TABS_CONTAINER, timeout=10000)
            has_title = self.is_visible(self.PAGE_TITLE, timeout=5000)
            is_loaded = has_tabs or has_title
            logger.info(f"设置页面加载状态: {is_loaded}")
            return is_loaded
        except Exception as e:
            logger.error(f"检查页面加载状态失败: {e}")
            return False
    
    # ================== Tab导航方法 ==================
    def click_emailing_tab(self):
        """点击Emailing Tab"""
        logger.info("点击Emailing Tab")
        self.page.click(self.EMAILING_TAB)
        self.page.wait_for_timeout(1000)
    
    def click_feature_management_tab(self):
        """点击Feature Management Tab"""
        logger.info("点击Feature Management Tab")
        self.page.click(self.FEATURE_MANAGEMENT_TAB)
        self.page.wait_for_timeout(1000)
    
    def click_identity_tab(self):
        """点击Identity Tab"""
        logger.info("点击Identity Tab")
        self.page.click(self.IDENTITY_TAB)
        self.page.wait_for_timeout(1000)
    
    def click_account_tab(self):
        """点击Account Tab"""
        logger.info("点击Account Tab")
        self.page.click(self.ACCOUNT_TAB)
        self.page.wait_for_timeout(1000)
    
    def is_tab_visible(self, tab_name: str) -> bool:
        """检查指定Tab是否可见"""
        tab_map = {
            "emailing": self.EMAILING_TAB,
            "feature": self.FEATURE_MANAGEMENT_TAB,
            "identity": self.IDENTITY_TAB,
            "account": self.ACCOUNT_TAB,
        }
        selector = tab_map.get(tab_name.lower())
        if selector:
            return self.is_visible(selector, timeout=3000)
        return False
    
    def get_active_tab(self) -> str:
        """获取当前激活的Tab"""
        try:
            active_tab = self.page.locator("[role='tab'][aria-selected='true'], .nav-link.active")
            if active_tab.is_visible():
                return active_tab.text_content().strip()
            return ""
        except Exception as e:
            logger.error(f"获取激活Tab失败: {e}")
            return ""
    
    # ================== Emailing设置方法 ==================
    def fill_smtp_settings(self, host: str = None, port: int = None, 
                          username: str = None, password: str = None,
                          enable_ssl: bool = None):
        """填写SMTP设置"""
        logger.info("填写SMTP设置")
        try:
            if host:
                self.page.fill(self.SMTP_HOST, host)
            if port:
                self.page.fill(self.SMTP_PORT, str(port))
            if username:
                self.page.fill(self.SMTP_USERNAME, username)
            if password:
                self.page.fill(self.SMTP_PASSWORD, password)
            if enable_ssl is not None:
                ssl_checkbox = self.page.locator(self.SMTP_ENABLE_SSL)
                if ssl_checkbox.is_visible():
                    if enable_ssl:
                        ssl_checkbox.check()
                    else:
                        ssl_checkbox.uncheck()
            logger.info("SMTP设置填写完成")
        except Exception as e:
            logger.error(f"填写SMTP设置失败: {e}")
            raise
    
    def fill_email_settings(self, from_address: str = None, from_name: str = None):
        """填写发件人设置"""
        logger.info("填写发件人设置")
        try:
            if from_address:
                self.page.fill(self.DEFAULT_FROM_ADDRESS, from_address)
            if from_name:
                self.page.fill(self.DEFAULT_FROM_NAME, from_name)
            logger.info("发件人设置填写完成")
        except Exception as e:
            logger.error(f"填写发件人设置失败: {e}")
            raise
    
    def click_send_test_email(self):
        """点击发送测试邮件按钮"""
        logger.info("点击发送测试邮件按钮")
        self.page.click(self.SEND_TEST_EMAIL_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def send_test_email(self, email: str):
        """发送测试邮件"""
        logger.info(f"发送测试邮件到: {email}")
        self.click_send_test_email()
        self.page.fill(self.TEST_EMAIL_INPUT, email)
        self.page.click(self.TEST_EMAIL_SEND)
        self.page.wait_for_timeout(2000)
    
    # ================== Identity设置方法 ==================
    def fill_password_settings(self, required_length: int = None,
                              require_digit: bool = None,
                              require_lowercase: bool = None,
                              require_uppercase: bool = None,
                              require_non_alphanumeric: bool = None):
        """填写密码策略设置"""
        logger.info("填写密码策略设置")
        try:
            if required_length:
                self.page.fill(self.PASSWORD_REQUIRED_LENGTH, str(required_length))
            
            if require_digit is not None:
                checkbox = self.page.locator(self.PASSWORD_REQUIRE_DIGIT)
                if checkbox.is_visible():
                    if require_digit:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
            
            if require_lowercase is not None:
                checkbox = self.page.locator(self.PASSWORD_REQUIRE_LOWERCASE)
                if checkbox.is_visible():
                    if require_lowercase:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
            
            if require_uppercase is not None:
                checkbox = self.page.locator(self.PASSWORD_REQUIRE_UPPERCASE)
                if checkbox.is_visible():
                    if require_uppercase:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
            
            if require_non_alphanumeric is not None:
                checkbox = self.page.locator(self.PASSWORD_REQUIRE_NON_ALPHANUMERIC)
                if checkbox.is_visible():
                    if require_non_alphanumeric:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
            
            logger.info("密码策略设置填写完成")
        except Exception as e:
            logger.error(f"填写密码策略设置失败: {e}")
            raise
    
    def fill_lockout_settings(self, max_attempts: int = None, 
                             lockout_seconds: int = None,
                             enabled: bool = None):
        """填写锁定策略设置"""
        logger.info("填写锁定策略设置")
        try:
            if max_attempts:
                self.page.fill(self.LOCKOUT_ALLOWED_ATTEMPTS, str(max_attempts))
            if lockout_seconds:
                self.page.fill(self.LOCKOUT_SECONDS, str(lockout_seconds))
            if enabled is not None:
                checkbox = self.page.locator(self.LOCKOUT_ENABLED)
                if checkbox.is_visible():
                    if enabled:
                        checkbox.check()
                    else:
                        checkbox.uncheck()
            logger.info("锁定策略设置填写完成")
        except Exception as e:
            logger.error(f"填写锁定策略设置失败: {e}")
            raise
    
    # ================== 通用方法 ==================
    def click_save(self):
        """点击保存按钮"""
        logger.info("点击保存按钮")
        self.page.click(self.SAVE_BUTTON)
        self.page.wait_for_timeout(1500)
    
    def click_reset(self):
        """点击重置按钮"""
        logger.info("点击重置按钮")
        self.page.click(self.RESET_BUTTON)
        self.page.wait_for_timeout(500)
    
    def is_save_button_visible(self) -> bool:
        """检查保存按钮是否可见"""
        return self.is_visible(self.SAVE_BUTTON, timeout=5000)
    
    def is_dialog_open(self) -> bool:
        """检查对话框是否打开"""
        return self.is_visible(self.DIALOG, timeout=3000)
    
    def close_dialog(self):
        """关闭对话框"""
        logger.info("关闭对话框")
        if self.is_visible(self.DIALOG_CLOSE, timeout=2000):
            self.page.click(self.DIALOG_CLOSE)
        else:
            self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
    
    def is_success_message_visible(self) -> bool:
        """检查成功消息是否可见"""
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5000)
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)
    
    def has_validation_error(self) -> bool:
        """检查是否有验证错误"""
        return self.is_visible(self.VALIDATION_ERROR, timeout=2000)
    
    def get_validation_errors(self) -> list:
        """获取所有验证错误"""
        try:
            errors = self.page.locator(self.VALIDATION_ERROR).all()
            return [e.text_content() for e in errors if e.text_content()]
        except Exception as e:
            logger.error(f"获取验证错误失败: {e}")
            return []
    
    def press_escape(self):
        """按ESC键"""
        logger.info("按下ESC键")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)
    
    def take_screenshot(self, filename: str):
        """截图"""
        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图保存到: {screenshot_path}")
        return screenshot_path
