"""
Settings (Emailing) 页面对象
定义Settings页面Emailing Tab的元素和操作方法
"""
from playwright.sync_api import Page
import logging
from tests.aevatar_station.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SettingsEmailingPage(BasePage):
    """Settings Emailing页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin/settings"
        
        # Tab导航元素
        self.EMAILING_TAB = "button[role='tab']:has-text('Emailing'), [role='tab']:has-text('Emailing')"
        self.FEATURE_MANAGEMENT_TAB = "button[role='tab']:has-text('Feature'), [role='tab']:has-text('Feature')"
        
        # 表单字段元素
        self.DISPLAY_NAME_INPUT = "input[name='defaultFromDisplayName'], input[placeholder*='display name' i]"
        self.FROM_ADDRESS_INPUT = "input[name='defaultFromAddress'], input[placeholder*='from address' i]"
        self.HOST_INPUT = "input[name='host'], input[placeholder*='host' i]"
        self.PORT_INPUT = "input[name='port'], input[type='number']"
        
        # Checkbox元素
        self.ENABLE_SSL_CHECKBOX = "input[type='checkbox'][name*='ssl' i], input[type='checkbox'] >> nth=0"
        self.USE_DEFAULT_CREDENTIALS_CHECKBOX = "input[type='checkbox'][name*='credential' i], input[type='checkbox'] >> nth=1"
        
        # 认证字段元素
        self.DOMAIN_INPUT = "input[name='domain'], input[placeholder*='domain' i]"
        self.USERNAME_INPUT = "input[name='userName'], input[placeholder*='user name' i]:not([type='checkbox'])"
        self.PASSWORD_INPUT = "input[name='password'], input[type='password']"
        
        # 保存按钮（可能没有，自动保存）
        self.SAVE_BUTTON = "button:has-text('Save'), button[type='submit']"
        
        # 成功/错误消息
        self.SUCCESS_MESSAGE = "[role='alert']:has-text('success'), .toast-success, text=successfully"
        self.ERROR_MESSAGE = "[role='alert']:has-text('error'), .toast-error, .text-danger"
    
    def navigate(self):
        """导航到Settings页面"""
        logger.info("导航到Settings页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
        # 等待Tab加载
        self.page.wait_for_selector(self.EMAILING_TAB, timeout=10000)
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            self.page.wait_for_selector(self.EMAILING_TAB, timeout=10000)
            self.page.wait_for_selector(self.HOST_INPUT, timeout=10000)
            logger.info("Settings Emailing页面加载完成")
            return True
        except Exception as e:
            logger.error(f"Settings页面加载失败: {e}")
            return False
    
    def click_emailing_tab(self):
        """点击Emailing Tab"""
        logger.info("点击Emailing Tab")
        self.page.locator(self.EMAILING_TAB).first.click()
        self.page.wait_for_timeout(1000)
    
    def click_feature_management_tab(self):
        """点击Feature Management Tab"""
        logger.info("点击Feature Management Tab")
        self.page.locator(self.FEATURE_MANAGEMENT_TAB).first.click()
        self.page.wait_for_timeout(1000)
    
    def fill_display_name(self, value: str):
        """填写Display Name"""
        logger.info(f"填写Display Name: {value}")
        self.page.locator(self.DISPLAY_NAME_INPUT).first.fill(value)
    
    def fill_from_address(self, value: str):
        """填写From Address"""
        logger.info(f"填写From Address: {value}")
        self.page.locator(self.FROM_ADDRESS_INPUT).first.fill(value)
    
    def fill_host(self, value: str):
        """填写Host"""
        logger.info(f"填写Host: {value}")
        self.page.locator(self.HOST_INPUT).first.fill(value)
    
    def fill_port(self, value: int):
        """填写Port"""
        logger.info(f"填写Port: {value}")
        self.page.locator(self.PORT_INPUT).first.fill(str(value))
    
    def set_enable_ssl(self, enable: bool):
        """设置Enable SSL"""
        logger.info(f"设置Enable SSL: {enable}")
        checkbox = self.page.locator(self.ENABLE_SSL_CHECKBOX).first
        if enable:
            checkbox.check()
        else:
            checkbox.uncheck()
    
    def set_use_default_credentials(self, enable: bool):
        """设置Use Default Credentials"""
        logger.info(f"设置Use Default Credentials: {enable}")
        checkbox = self.page.locator(self.USE_DEFAULT_CREDENTIALS_CHECKBOX).first
        if enable:
            checkbox.check()
        else:
            checkbox.uncheck()
    
    def fill_domain(self, value: str):
        """填写Domain"""
        logger.info(f"填写Domain: {value}")
        self.page.locator(self.DOMAIN_INPUT).first.fill(value)
    
    def fill_username(self, value: str):
        """填写Username"""
        logger.info(f"填写Username: {value}")
        self.page.locator(self.USERNAME_INPUT).first.fill(value)
    
    def fill_password(self, value: str):
        """填写Password"""
        logger.info(f"填写Password: {value}")
        self.page.locator(self.PASSWORD_INPUT).first.fill(value)
    
    def click_save(self):
        """点击保存按钮"""
        try:
            logger.info("点击保存按钮")
            save_btn = self.page.locator(self.SAVE_BUTTON).first
            if save_btn.is_visible(timeout=2000):
                save_btn.click()
                # 优化：不使用networkidle
                self.page.wait_for_timeout(2000)
                logger.info("保存按钮已点击")
            else:
                logger.warning("未找到保存按钮，可能是自动保存")
        except Exception as e:
            logger.warning(f"点击保存按钮失败（可能是自动保存）: {e}")
    
    def configure_smtp(self, display_name: str = None, from_address: str = None,
                      host: str = None, port: int = None, enable_ssl: bool = None,
                      use_default_credentials: bool = None, domain: str = None,
                      username: str = None, password: str = None):
        """
        配置SMTP设置
        
        Args:
            display_name: 显示名称
            from_address: 发件人地址
            host: SMTP服务器地址
            port: 端口号
            enable_ssl: 启用SSL
            use_default_credentials: 使用默认凭据
            domain: 域名
            username: 用户名
            password: 密码
        """
        logger.info("配置SMTP设置")
        
        if display_name is not None:
            self.fill_display_name(display_name)
        
        if from_address is not None:
            self.fill_from_address(from_address)
        
        if host is not None:
            self.fill_host(host)
        
        if port is not None:
            self.fill_port(port)
        
        if enable_ssl is not None:
            self.set_enable_ssl(enable_ssl)
        
        if use_default_credentials is not None:
            self.set_use_default_credentials(use_default_credentials)
        
        if domain is not None:
            self.fill_domain(domain)
        
        if username is not None:
            self.fill_username(username)
        
        if password is not None:
            self.fill_password(password)
        
        # 点击保存（如果有保存按钮）
        self.click_save()
        
        logger.info("SMTP配置已填写完成")
    
    def get_display_name_value(self) -> str:
        """获取Display Name值"""
        try:
            value = self.page.locator(self.DISPLAY_NAME_INPUT).first.input_value()
            return value
        except Exception as e:
            logger.error(f"获取Display Name失败: {e}")
            return ""
    
    def get_from_address_value(self) -> str:
        """获取From Address值"""
        try:
            value = self.page.locator(self.FROM_ADDRESS_INPUT).first.input_value()
            return value
        except Exception as e:
            logger.error(f"获取From Address失败: {e}")
            return ""
    
    def get_host_value(self) -> str:
        """获取Host值"""
        try:
            value = self.page.locator(self.HOST_INPUT).first.input_value()
            return value
        except Exception as e:
            logger.error(f"获取Host失败: {e}")
            return ""
    
    def get_port_value(self) -> int:
        """获取Port值"""
        try:
            value = self.page.locator(self.PORT_INPUT).first.input_value()
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"获取Port失败: {e}")
            return 0
    
    def is_ssl_enabled(self) -> bool:
        """检查SSL是否启用"""
        try:
            is_checked = self.page.locator(self.ENABLE_SSL_CHECKBOX).first.is_checked()
            return is_checked
        except Exception as e:
            logger.error(f"检查SSL状态失败: {e}")
            return False
    
    def is_default_credentials_enabled(self) -> bool:
        """检查默认凭据是否启用"""
        try:
            is_checked = self.page.locator(self.USE_DEFAULT_CREDENTIALS_CHECKBOX).first.is_checked()
            return is_checked
        except Exception as e:
            logger.error(f"检查默认凭据状态失败: {e}")
            return False
    
    def get_username_value(self) -> str:
        """获取Username值"""
        try:
            value = self.page.locator(self.USERNAME_INPUT).first.input_value()
            return value
        except Exception as e:
            logger.error(f"获取Username失败: {e}")
            return ""
    
    def is_success_message_visible(self) -> bool:
        """检查成功消息是否显示"""
        try:
            is_visible = self.page.locator(self.SUCCESS_MESSAGE).is_visible(timeout=5000)
            if is_visible:
                message = self.page.locator(self.SUCCESS_MESSAGE).first.text_content()
                logger.info(f"成功消息: {message}")
            return is_visible
        except Exception as e:
            return False
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否显示"""
        try:
            is_visible = self.page.locator(self.ERROR_MESSAGE).is_visible(timeout=3000)
            if is_visible:
                message = self.page.locator(self.ERROR_MESSAGE).first.text_content()
                logger.info(f"错误消息: {message}")
            return is_visible
        except Exception as e:
            return False
    
    def is_field_valid(self, selector: str) -> bool:
        """检查字段的HTML5验证状态"""
        try:
            is_valid = self.page.evaluate(f"""
                document.querySelector("{selector}").validity.valid
            """)
            return is_valid
        except Exception as e:
            logger.error(f"检查字段验证状态失败: {e}")
            return True
    
    def take_screenshot(self, filename: str):
        """截图并保存"""
        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图保存到: {screenshot_path}")
        return screenshot_path

