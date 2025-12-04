"""
AdminPanelPage - 管理面板页面对象
路径: /admin
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class AdminPanelPage(BasePage):
    """管理面板页面对象"""
    
    # 元素定位器
    HOME_NAV = "a[href='/admin']"
    WORKFLOW_NAV = "a[href='/workflow']"
    WELCOME_HEADING = "h1:has-text('Welcome back')"
    USER_EMAIL = "p:has-text('@test.com'), p:has-text('@')"
    USERNAME_TEXT = "p:has-text('Username:')"
    AUTH_STATUS = "text=Authenticated"
    EMAIL_VERIFICATION = "text=Not Verified"
    MULTITENANCY_STATUS = "text=Disabled"
    CURRENT_TENANT = "text=Host"
    USER_MENU_BUTTON = "button:has-text('Toggle user menu')"
    
    def navigate(self):
        """导航到管理面板"""
        logger.info("导航到管理面板")
        self.navigate_to("/admin")
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.WELCOME_HEADING) or self.is_visible(self.USER_MENU_BUTTON)
    
    def get_user_email(self):
        """获取用户邮箱"""
        logger.info("获取用户邮箱")
        return self.get_text(self.USER_EMAIL)
    
    def is_authenticated(self):
        """检查是否显示认证状态"""
        return self.is_visible(self.AUTH_STATUS)
    
    def click_workflow_nav(self):
        """点击Workflow导航"""
        logger.info("点击Workflow导航")
        self.click_element(self.WORKFLOW_NAV)

