"""
LandingPage - 首页页面对象
路径: /
"""
from tests.aevatar_station.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LandingPage(BasePage):
    """首页页面对象"""
    
    # 元素定位器 - Header
    LOGO = "a:has-text('Aevatar AI')"
    WORKFLOW_NAV = "a:has-text('Workflow')"
    GITHUB_NAV = "a:has-text('GitHub')"
    NAVIGATION_MENU_BUTTON = "button:has-text('Toggle navigation menu')"
    USER_MENU_BUTTON = "button:has-text('Toggle user menu')"
    SIGN_IN_BUTTON = "button:has-text('Sign In'), a:has-text('Sign In')"  # 登录按钮（可能是button或link）
    
    # 元素定位器 - Hero Section
    PAGE_HEADING = "h1:has-text('Aevatar Station')"
    SUBTITLE = "text=Distributed AI Platform"
    DESCRIPTION = "text=Your all-in-one platform for creating, managing, and deploying"
    CREATE_WORKFLOW_BUTTON = 'button:has-text("Create Workflow")'
    VIEW_ON_GITHUB_BUTTON = 'button:has-text("View on GitHub")'
    DASHBOARD_IMAGE = 'img[alt*="Dashboard"]'
    
    # 元素定位器 - Platform Section
    PLATFORM_HEADING = "text=Enterprise-Grade AI Agent Platform"
    PLATFORM_DESCRIPTION = "text=Aevatar Station provides a complete foundation"
    
    # 元素定位器 - CTA Section
    ADMIN_PANEL_BUTTON = 'button:has-text("Admin Panel")'
    
    # 元素定位器 - Footer
    FOOTER = "contentinfo"
    COPYRIGHT = "text=© 2025 Aevatar"
    TERMS_OF_SERVICE_LINK = 'a:has-text("Terms of Service")'
    PRIVACY_LINK = 'a:has-text("Privacy")'
    
    def navigate(self):
        """导航到首页"""
        logger.info("导航到首页")
        self.navigate_to("/")
        self.handle_ssl_warning()
    
    def is_loaded(self):
        """检查页面是否加载完成"""
        return self.is_visible(self.PAGE_HEADING)
    
    def click_sign_in(self):
        """点击Sign In按钮"""
        logger.info("点击Sign In按钮")
        self.click_element(self.SIGN_IN_BUTTON)
        self.handle_ssl_warning()
    
    def click_get_started(self):
        """点击Get Started按钮"""
        logger.info("点击Get Started按钮")
        self.click_element(self.GET_STARTED_BUTTON)
    
    def click_workflow_nav(self):
        """点击Workflow导航"""
        logger.info("点击Workflow导航")
        self.click_element(self.WORKFLOW_NAV)
    
    def is_logged_in(self):
        """检查用户是否已登录"""
        return self.is_visible(self.USER_MENU_BUTTON, timeout=5000)
    
    def is_user_menu_visible(self):
        """检查用户菜单按钮是否可见"""
        return self.is_visible(self.USER_MENU_BUTTON)
    
    def click_create_workflow(self):
        """点击Create Workflow按钮"""
        logger.info("点击Create Workflow按钮")
        self.click_element(self.CREATE_WORKFLOW_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def click_view_on_github(self):
        """点击View on GitHub按钮"""
        logger.info("点击View on GitHub按钮")
        self.click_element(self.VIEW_ON_GITHUB_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def click_admin_panel(self):
        """点击Admin Panel按钮"""
        logger.info("点击Admin Panel按钮")
        self.click_element(self.ADMIN_PANEL_BUTTON)
        self.handle_ssl_warning()
        self.page.wait_for_timeout(2000)
    
    def click_logo(self):
        """点击Logo"""
        logger.info("点击Logo")
        self.click_element(self.LOGO)
        self.page.wait_for_timeout(1000)
    
    def click_github_nav(self):
        """点击GitHub导航链接"""
        logger.info("点击GitHub导航链接")
        self.click_element(self.GITHUB_NAV)
        self.page.wait_for_timeout(1000)
    
    def click_user_menu(self):
        """点击用户菜单按钮"""
        logger.info("点击用户菜单按钮")
        self.click_element(self.USER_MENU_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def click_navigation_menu(self):
        """点击导航菜单按钮（移动端）"""
        logger.info("点击导航菜单按钮")
        self.click_element(self.NAVIGATION_MENU_BUTTON)
        self.page.wait_for_timeout(1000)
    
    def is_heading_visible(self):
        """检查主标题是否可见"""
        return self.is_visible(self.PAGE_HEADING)
    
    def is_subtitle_visible(self):
        """检查副标题是否可见"""
        return self.is_visible(self.SUBTITLE)
    
    def is_description_visible(self):
        """检查描述文本是否可见"""
        return self.is_visible(self.DESCRIPTION)
    
    def is_dashboard_image_visible(self):
        """检查Dashboard图片是否可见"""
        return self.is_visible(self.DASHBOARD_IMAGE, timeout=5000)
    
    def is_platform_heading_visible(self):
        """检查平台介绍标题是否可见"""
        return self.is_visible(self.PLATFORM_HEADING)
    
    def is_create_workflow_button_visible(self):
        """检查Create Workflow按钮是否可见"""
        return self.is_visible(self.CREATE_WORKFLOW_BUTTON)
    
    def is_admin_panel_button_visible(self):
        """检查Admin Panel按钮是否可见"""
        return self.is_visible(self.ADMIN_PANEL_BUTTON)
    
    def is_footer_visible(self):
        """检查Footer是否可见"""
        return self.is_visible(self.FOOTER)
    
    def is_copyright_visible(self):
        """检查版权信息是否可见"""
        return self.is_visible(self.COPYRIGHT)
    
    def click_terms_of_service(self):
        """点击Terms of Service链接"""
        logger.info("点击Terms of Service链接")
        self.click_element(self.TERMS_OF_SERVICE_LINK)
        self.page.wait_for_timeout(1000)
    
    def click_privacy(self):
        """点击Privacy链接"""
        logger.info("点击Privacy链接")
        self.click_element(self.PRIVACY_LINK)
        self.page.wait_for_timeout(1000)
    
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        logger.info("滚动到页面底部")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
    
    def get_page_title(self):
        """获取页面标题"""
        return self.page.title()
    
    def verify_all_hero_elements_visible(self):
        """验证Hero区域所有元素可见"""
        logger.info("验证Hero区域所有元素")
        checks = {
            "主标题": self.is_heading_visible(),
            "副标题": self.is_subtitle_visible(),
            "描述文本": self.is_description_visible(),
            "Create Workflow按钮": self.is_create_workflow_button_visible(),
            "Dashboard图片": self.is_dashboard_image_visible()
        }
        
        all_visible = all(checks.values())
        logger.info(f"Hero元素检查结果: {checks}")
        return all_visible

