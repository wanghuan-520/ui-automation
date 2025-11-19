"""
Profile/Settings页面对象
负责用户个人设置、组织管理、项目管理功能
"""
from playwright.sync_api import Page, Locator
from typing import Optional, Dict
import allure
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ProfileSettingsPage(BasePage):
    """Profile/Settings页面对象"""
    
    # 页面URL
    PROFILE_URL = "/profile"
    
    # 侧边栏导航 - Profile
    PROFILE_SECTION = "text=Profile"
    PROFILE_GENERAL_MENU = "generic:has-text('General')"
    PROFILE_NOTIFICATIONS_MENU = "generic:has-text('Notifications')"
    
    # 侧边栏导航 - Organisations
    ORGANISATIONS_SECTION = "text=Organisations"
    ORG_GENERAL_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='General']"
    ORG_PROJECT_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Project']"
    ORG_MEMBER_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Member']"
    ORG_ROLE_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Role']"
    
    # 侧边栏导航 - Projects
    PROJECTS_SECTION = "text=Projects"
    PROJECT_GENERAL_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='General']"
    PROJECT_MEMBER_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='Member']"
    PROJECT_ROLE_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='Role']"
    
    # Profile General页面元素
    NAME_INPUT = "textbox >> nth=0"  # 第一个textbox
    EMAIL_INPUT = "textbox[disabled]"
    SAVE_BUTTON = "button:has-text('Save')"
    RESET_PASSWORD_BUTTON = "button:has-text('Reset Password')"
    RESET_PASSWORD_DESCRIPTION = "text=A password reset link will be sent"
    
    # 页面加载指示器
    page_loaded_indicator = "text=Profile"
    
    def __init__(self, page: Page):
        """
        初始化Profile/Settings页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.PROFILE_URL}"
        logger.info(f"初始化Profile/Settings页面: {self.page_url}")
    
    @allure.step("导航到Profile页面")
    def navigate(self) -> None:
        """导航到Profile页面"""
        logger.info(f"导航到Profile页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查Profile页面是否已加载
        
        Returns:
            bool: 页面是否已加载
        """
        try:
            self.page.wait_for_selector(self.PROFILE_SECTION, timeout=5000)
            logger.info("Profile页面已加载")
            return True
        except Exception as e:
            logger.error(f"Profile页面加载失败: {str(e)}")
            return False
    
    @allure.step("修改用户名称为: {new_name}")
    def update_name(self, new_name: str) -> None:
        """
        更新用户名称
        
        Args:
            new_name: 新的用户名称
        """
        logger.info(f"修改用户名称为: {new_name}")
        
        # 清空输入框
        self.page.fill(self.NAME_INPUT, "")
        # 输入新名称
        self.page.fill(self.NAME_INPUT, new_name)
        # 点击保存
        self.click_element(self.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)
        
        logger.info("用户名称修改完成")
    
    @allure.step("获取当前用户名称")
    def get_current_name(self) -> str:
        """
        获取当前用户名称
        
        Returns:
            str: 当前用户名称
        """
        logger.info("获取当前用户名称")
        name = self.page.input_value(self.NAME_INPUT)
        logger.info(f"当前用户名称: {name}")
        return name
    
    @allure.step("获取当前邮箱地址")
    def get_current_email(self) -> str:
        """
        获取当前邮箱地址
        
        Returns:
            str: 当前邮箱地址
        """
        logger.info("获取当前邮箱地址")
        email = self.page.input_value(self.EMAIL_INPUT)
        logger.info(f"当前邮箱: {email}")
        return email
    
    @allure.step("点击Reset Password按钮")
    def click_reset_password(self) -> None:
        """点击重置密码按钮"""
        logger.info("点击Reset Password按钮")
        self.click_element(self.RESET_PASSWORD_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("导航到 {section} > {menu}")
    def navigate_to_menu(self, section: str, menu: str) -> None:
        """
        导航到指定菜单
        
        Args:
            section: 部分名称 (Profile, Organisations, Projects)
            menu: 菜单名称 (General, Notifications, Project, Member, Role)
        """
        logger.info(f"导航到 {section} > {menu}")
        
        section_map = {
            "Profile": {
                "General": self.PROFILE_GENERAL_MENU,
                "Notifications": self.PROFILE_NOTIFICATIONS_MENU
            },
            "Organisations": {
                "General": self.ORG_GENERAL_MENU,
                "Project": self.ORG_PROJECT_MENU,
                "Member": self.ORG_MEMBER_MENU,
                "Role": self.ORG_ROLE_MENU
            },
            "Projects": {
                "General": self.PROJECT_GENERAL_MENU,
                "Member": self.PROJECT_MEMBER_MENU,
                "Role": self.PROJECT_ROLE_MENU
            }
        }
        
        menu_selector = section_map.get(section, {}).get(menu)
        if menu_selector:
            self.click_element(menu_selector)
            self.page.wait_for_timeout(1000)
            logger.info(f"已导航到 {section} > {menu}")
        else:
            logger.error(f"未找到菜单: {section} > {menu}")
    
    @allure.step("验证名称是否更新为: {expected_name}")
    def verify_name_updated(self, expected_name: str) -> bool:
        """
        验证名称是否更新成功
        
        Args:
            expected_name: 期望的名称
            
        Returns:
            bool: 名称是否匹配
        """
        logger.info(f"验证名称是否为: {expected_name}")
        current_name = self.get_current_name()
        
        matches = current_name == expected_name
        if matches:
            logger.info(f"名称验证成功: {current_name}")
        else:
            logger.error(f"名称验证失败 - 期望: {expected_name}, 实际: {current_name}")
        
        return matches
    
    @allure.step("验证邮箱是否为disabled状态")
    def verify_email_disabled(self) -> bool:
        """
        验证Email输入框是否为disabled状态
        
        Returns:
            bool: 是否为disabled状态
        """
        logger.info("验证Email输入框disabled状态")
        
        try:
            email_element = self.page.locator(self.EMAIL_INPUT)
            is_disabled = email_element.is_disabled()
            
            if is_disabled:
                logger.info("Email输入框为disabled状态")
            else:
                logger.warning("Email输入框不是disabled状态")
            
            return is_disabled
        except Exception as e:
            logger.error(f"检查Email disabled状态失败: {str(e)}")
            return False
    
    @allure.step("验证Reset Password说明文字是否显示")
    def verify_reset_password_description(self) -> bool:
        """
        验证Reset Password说明文字是否显示
        
        Returns:
            bool: 说明文字是否可见
        """
        logger.info("验证Reset Password说明文字")
        return self.is_element_visible(self.RESET_PASSWORD_DESCRIPTION)
    
    @allure.step("点击Dashboard按钮")
    def click_dashboard_button(self) -> None:
        """点击顶部导航的Dashboard按钮"""
        logger.info("点击Dashboard按钮")
        dashboard_button = "button:has-text('Dashboard')"
        self.click_element(dashboard_button)
        self.page.wait_for_timeout(2000)

