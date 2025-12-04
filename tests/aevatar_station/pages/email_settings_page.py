"""
EmailSettingsPage - 邮件设置页面对象
路径: /admin/settings
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class EmailSettingsPage(BasePage):
    """邮件设置页面对象"""
    
    # 元素定位器
    EMAILING_TAB = "button:has-text('Emailing')"
    FEATURE_MANAGEMENT_TAB = "button:has-text('Feature management')"
    DISPLAY_NAME_INPUT = "input[name*='displayName']"
    FROM_ADDRESS_INPUT = "input[name*='fromAddress']"
    HOST_INPUT = "input[name*='host']"
    PORT_INPUT = "input[type='number'], input[name*='port']"
    ENABLE_SSL_CHECKBOX = "input[type='checkbox'][name*='ssl']"
    USE_DEFAULT_CREDENTIALS_CHECKBOX = "input[type='checkbox'][name*='credentials']"
    DOMAIN_INPUT = "input[name*='domain']"
    USERNAME_INPUT = "input[name*='userName']:not([name*='display'])"
    PASSWORD_INPUT = "input[name*='password']"
    MANAGE_FEATURES_BUTTON = "button:has-text('Manage Host Features')"
    
    def navigate(self):
        """导航到邮件设置页面"""
        logger.info("导航到邮件设置页面")
        self.navigate_to("/admin/settings")
        # 等待页面加载
        self.page.wait_for_timeout(2000)
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.EMAILING_TAB) or self.is_visible(self.HOST_INPUT)
    
    def configure_email(self, host, port, from_address, enable_ssl=True):
        """配置邮件服务器"""
        logger.info("配置邮件服务器")
        
        # 填写Host
        self.fill_input(self.HOST_INPUT, host)
        
        # 填写Port
        self.fill_input(self.PORT_INPUT, str(port))
        
        # 填写From Address
        self.fill_input(self.FROM_ADDRESS_INPUT, from_address)
        
        # 勾选Enable SSL
        if enable_ssl:
            self.page.check(self.ENABLE_SSL_CHECKBOX)
    
    def click_feature_management_tab(self):
        """点击Feature Management标签页"""
        logger.info("切换到Feature Management标签页")
        self.click_element(self.FEATURE_MANAGEMENT_TAB)
        self.page.wait_for_timeout(2000)
    
    def is_manage_features_button_visible(self):
        """检查Manage Features按钮是否可见"""
        return self.is_visible(self.MANAGE_FEATURES_BUTTON)

