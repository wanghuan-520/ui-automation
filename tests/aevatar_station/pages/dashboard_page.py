"""
Dashboard页面对象
定义Dashboard页面的元素和操作方法
"""
from playwright.sync_api import Page
import logging
from tests.aevatar_station.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    """Dashboard页面对象类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = "/admin"
        
        # 欢迎区域元素
        self.WELCOME_TITLE = "text=Welcome back"
        self.SYSTEM_MESSAGE = "text=Here's what's happening"
        self.HOST_BADGE = "text=Host"
        
        # 用户信息卡片元素
        self.USER_PROFILE_CARD = "section:has-text('User Profile')"
        self.USER_PROFILE_TITLE = "heading:has-text('User Profile')"
        self.USER_AVATAR = self.USER_PROFILE_CARD + " >> [role='generic']:has-text('李W'), [role='generic']:has-text('W')"
        self.USER_NAME = self.USER_PROFILE_CARD + " >> text=/.*Wang/"
        self.USER_EMAIL = self.USER_PROFILE_CARD + " >> text=/@/"
        self.USER_USERNAME = self.USER_PROFILE_CARD + " >> text=/Username:/"
        self.AUTHENTICATED_BADGE = "text=Authenticated"
        
        # 验证状态元素
        self.EMAIL_VERIFICATION = "text=Email Verification"
        self.EMAIL_NOT_VERIFIED = self.USER_PROFILE_CARD + " >> text=Not Verified >> nth=0"
        self.PHONE_VERIFICATION = "text=Phone Verification"
        self.PHONE_NOT_VERIFIED = self.USER_PROFILE_CARD + " >> text=Not Verified >> nth=1"
        
        # 系统状态卡片元素
        self.MULTI_TENANCY_CARD = "section:has-text('Multi-tenancy'):has-text('Disabled'), section:has-text('Multi-tenancy'):has-text('Enabled')"
        self.MULTI_TENANCY_TITLE = "heading:has-text('Multi-tenancy')"
        self.MULTI_TENANCY_STATUS = self.MULTI_TENANCY_CARD + " >> text=/Disabled|Enabled/"
        
        self.CURRENT_TENANT_CARD = "section:has-text('Current Tenant')"
        self.CURRENT_TENANT_TITLE = "heading:has-text('Current Tenant')"
        self.CURRENT_TENANT_VALUE = self.CURRENT_TENANT_CARD + " >> text=/Host|Tenant/"
        
        self.SESSION_CARD = "section:has-text('Session')"
        self.SESSION_TITLE = "heading:has-text('Session')"
        self.SESSION_STATUS = self.SESSION_CARD + " >> text=/No Session|Active/"
        
        # 系统配置卡片元素
        self.SYSTEM_CONFIG_CARD = "section:has-text('System Configuration')"
        self.SYSTEM_CONFIG_TITLE = "heading:has-text('System Configuration')"
        
        # Localization
        self.LOCALIZATION_SECTION = self.SYSTEM_CONFIG_CARD + " >> text=Localization"
        self.CURRENT_CULTURE = self.SYSTEM_CONFIG_CARD + " >> text=/Current Culture:/"
        self.DEFAULT_RESOURCE = self.SYSTEM_CONFIG_CARD + " >> text=/Default Resource:/"
        
        # Timing
        self.TIMING_SECTION = self.SYSTEM_CONFIG_CARD + " >> text=Timing"
        self.TIME_ZONE = self.SYSTEM_CONFIG_CARD + " >> text=/Time Zone:/"
        self.CLOCK_KIND = self.SYSTEM_CONFIG_CARD + " >> text=/Clock Kind:/"
        
        # Features
        self.FEATURES_SECTION = self.SYSTEM_CONFIG_CARD + " >> text=Features"
        self.ENABLED_FEATURES = self.SYSTEM_CONFIG_CARD + " >> text=/Enabled Features:/"
    
    def navigate(self):
        """导航到Dashboard页面"""
        logger.info("导航到Dashboard页面")
        self.navigate_to(self.page_url)
        self.wait_for_load()
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        try:
            # 等待关键元素出现
            self.page.wait_for_selector(self.WELCOME_TITLE, timeout=10000)
            self.page.wait_for_selector(self.USER_PROFILE_CARD, timeout=10000)
            logger.info("Dashboard页面加载完成")
            return True
        except Exception as e:
            logger.error(f"Dashboard页面加载失败: {e}")
            return False
    
    def get_welcome_message(self) -> str:
        """获取欢迎消息"""
        try:
            element = self.page.locator(self.WELCOME_TITLE).first
            text = element.text_content()
            logger.info(f"欢迎消息: {text}")
            return text
        except Exception as e:
            logger.error(f"获取欢迎消息失败: {e}")
            return ""
    
    def is_host_user(self) -> bool:
        """检查是否为Host用户"""
        try:
            is_visible = self.page.locator(self.HOST_BADGE).is_visible(timeout=5000)
            logger.info(f"Host用户标识可见: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"检查Host用户失败: {e}")
            return False
    
    def get_user_name(self) -> str:
        """获取用户姓名"""
        try:
            # 查找包含姓名的元素
            name_locator = self.page.locator(self.USER_PROFILE_CARD).locator("text=/李明|Wang/").first
            name = name_locator.text_content()
            logger.info(f"用户姓名: {name}")
            return name.strip() if name else ""
        except Exception as e:
            logger.error(f"获取用户姓名失败: {e}")
            return ""
    
    def get_user_email(self) -> str:
        """获取用户邮箱"""
        try:
            email_locator = self.page.locator(self.USER_EMAIL).first
            email = email_locator.text_content()
            logger.info(f"用户邮箱: {email}")
            return email.strip() if email else ""
        except Exception as e:
            logger.error(f"获取用户邮箱失败: {e}")
            return ""
    
    def is_authenticated(self) -> bool:
        """检查认证状态"""
        try:
            is_visible = self.page.locator(self.AUTHENTICATED_BADGE).is_visible(timeout=5000)
            logger.info(f"认证状态可见: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"检查认证状态失败: {e}")
            return False
    
    def is_email_verified(self) -> bool:
        """检查邮箱是否已验证"""
        try:
            # 如果显示"Not Verified"，则未验证
            not_verified = self.page.locator(self.EMAIL_NOT_VERIFIED).is_visible(timeout=5000)
            is_verified = not not_verified
            logger.info(f"邮箱验证状态: {is_verified}")
            return is_verified
        except Exception as e:
            logger.error(f"检查邮箱验证状态失败: {e}")
            return False
    
    def is_phone_verified(self) -> bool:
        """检查手机是否已验证"""
        try:
            # 如果显示"Not Verified"，则未验证
            not_verified = self.page.locator(self.PHONE_NOT_VERIFIED).is_visible(timeout=5000)
            is_verified = not not_verified
            logger.info(f"手机验证状态: {is_verified}")
            return is_verified
        except Exception as e:
            logger.error(f"检查手机验证状态失败: {e}")
            return False
    
    def get_multi_tenancy_status(self) -> str:
        """获取多租户状态"""
        try:
            status_locator = self.page.locator(self.MULTI_TENANCY_STATUS).first
            status = status_locator.text_content()
            logger.info(f"多租户状态: {status}")
            return status.strip() if status else ""
        except Exception as e:
            logger.error(f"获取多租户状态失败: {e}")
            return ""
    
    def get_current_tenant(self) -> str:
        """获取当前租户"""
        try:
            tenant_locator = self.page.locator(self.CURRENT_TENANT_VALUE).first
            tenant = tenant_locator.text_content()
            logger.info(f"当前租户: {tenant}")
            return tenant.strip() if tenant else ""
        except Exception as e:
            logger.error(f"获取当前租户失败: {e}")
            return ""
    
    def get_session_status(self) -> str:
        """获取会话状态"""
        try:
            status_locator = self.page.locator(self.SESSION_STATUS).first
            status = status_locator.text_content()
            logger.info(f"会话状态: {status}")
            return status.strip() if status else ""
        except Exception as e:
            logger.error(f"获取会话状态失败: {e}")
            return ""
    
    def get_current_culture(self) -> str:
        """获取当前文化设置"""
        try:
            culture_text = self.page.locator(self.CURRENT_CULTURE).text_content()
            # 提取 "Current Culture: English" 中的 "English"
            culture = culture_text.split(":")[-1].strip() if culture_text else ""
            logger.info(f"当前文化: {culture}")
            return culture
        except Exception as e:
            logger.error(f"获取当前文化失败: {e}")
            return ""
    
    def get_time_zone(self) -> str:
        """获取时区设置"""
        try:
            tz_text = self.page.locator(self.TIME_ZONE).text_content()
            # 提取 "Time Zone: N/A" 中的 "N/A"
            tz = tz_text.split(":")[-1].strip() if tz_text else ""
            logger.info(f"时区: {tz}")
            return tz
        except Exception as e:
            logger.error(f"获取时区失败: {e}")
            return ""
    
    def get_enabled_features_count(self) -> int:
        """获取启用的功能数量"""
        try:
            features_text = self.page.locator(self.ENABLED_FEATURES).text_content()
            # 提取 "Enabled Features: 0" 中的 "0"
            count_str = features_text.split(":")[-1].strip() if features_text else "0"
            count = int(count_str)
            logger.info(f"启用的功能数量: {count}")
            return count
        except Exception as e:
            logger.error(f"获取启用功能数量失败: {e}")
            return 0
    
    def is_user_profile_card_visible(self) -> bool:
        """检查用户信息卡片是否可见"""
        try:
            is_visible = self.page.locator(self.USER_PROFILE_CARD).is_visible(timeout=5000)
            logger.info(f"用户信息卡片可见: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"检查用户信息卡片失败: {e}")
            return False
    
    def is_system_config_card_visible(self) -> bool:
        """检查系统配置卡片是否可见"""
        try:
            is_visible = self.page.locator(self.SYSTEM_CONFIG_CARD).is_visible(timeout=5000)
            logger.info(f"系统配置卡片可见: {is_visible}")
            return is_visible
        except Exception as e:
            logger.error(f"检查系统配置卡片失败: {e}")
            return False
    
    def take_screenshot(self, filename: str):
        """截图并保存"""
        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"截图保存到: {screenshot_path}")
        return screenshot_path

