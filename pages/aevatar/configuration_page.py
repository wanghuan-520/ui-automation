"""
Configuration页面对象
负责Webhook、CROS等配置管理功能
"""
from playwright.sync_api import Page, Locator
from typing import List, Dict, Optional
import allure
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ConfigurationPage(BasePage):
    """Configuration页面对象"""
    
    # 页面URL
    CONFIGURATION_URL = "/dashboard/configuration"
    
    # 侧边栏导航
    APIKEYS_MENU = "text=API Keys"
    WORKFLOWS_MENU = "text=Workflows"
    CONFIGURATION_MENU = "text=Configuration"
    
    # Tab导航
    WEBHOOK_TAB = "text=Webhook"
    CROS_TAB = "text=Cros"
    
    # Webhook配置元素
    WEBHOOK_TABLE = "role=table >> nth=0"  # 第一个表格
    WEBHOOK_CREATE_BUTTON = "button:has-text('Create')"
    WEBHOOK_NAME_INPUT = "input[placeholder='Enter name']"
    WEBHOOK_URL_INPUT = "input[placeholder='Enter URL']"
    WEBHOOK_SAVE_BUTTON = "button:has-text('Save')"
    WEBHOOK_ACTION_MENU = "combobox[cursor=pointer]"
    
    # CROS配置元素
    CROS_TABLE = "role=table >> nth=0"  # 第一个表格
    CROS_CREATE_BUTTON = "button:has-text('Create')"
    CROS_ORIGIN_INPUT = "input[placeholder='Enter origin']"
    CROS_SAVE_BUTTON = "button:has-text('Save')"
    CROS_ACTION_MENU = "combobox[cursor=pointer]"
    
    # 通用操作菜单
    EDIT_MENU_ITEM = "text=Edit"
    DELETE_MENU_ITEM = "text=Delete"
    
    # 删除确认弹窗
    DELETE_DIALOG = "text=Delete >> ancestor::div[role='dialog']"
    DELETE_CONFIRM_BUTTON = "button:has-text('Delete')"
    DELETE_CANCEL_BUTTON = "button:has-text('Cancel')"
    
    # 页面加载指示器
    page_loaded_indicator = "text=Webhook"
    
    def __init__(self, page: Page):
        """
        初始化Configuration页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.CONFIGURATION_URL}"
        logger.info(f"初始化Configuration页面: {self.page_url}")
    
    @allure.step("导航到Configuration页面")
    def navigate(self) -> None:
        """导航到Configuration页面"""
        logger.info(f"导航到Configuration页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查Configuration页面是否已加载
        
        Returns:
            bool: 页面是否已加载
        """
        try:
            self.page.wait_for_selector(self.WEBHOOK_TAB, timeout=5000)
            logger.info("Configuration页面已加载")
            return True
        except Exception as e:
            logger.error(f"Configuration页面加载失败: {str(e)}")
            return False
    
    @allure.step("切换到 {tab_name} 标签页")
    def switch_to_tab(self, tab_name: str) -> None:
        """
        切换到指定标签页
        
        Args:
            tab_name: 标签名称 (Webhook, Cros)
        """
        logger.info(f"切换到 {tab_name} 标签页")
        tab_selector = f"text={tab_name}"
        self.click_element(tab_selector)
        self.page.wait_for_timeout(1000)
    
    # ========== Webhook相关方法 ==========
    
    @allure.step("获取Webhook列表")
    def get_webhook_list(self) -> List[Dict[str, str]]:
        """
        获取Webhook列表
        
        Returns:
            List[Dict[str, str]]: Webhook列表
        """
        logger.info("获取Webhook列表")
        webhooks = []
        
        try:
            # 确保在Webhook标签页
            self.switch_to_tab("Webhook")
            
            # 等待表格加载
            self.page.wait_for_selector(self.WEBHOOK_TABLE, timeout=5000)
            
            # 获取所有行
            rows = self.page.query_selector_all(f"{self.WEBHOOK_TABLE} >> tbody >> tr")
            logger.info(f"找到 {len(rows)} 个Webhook")
            
            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) >= 3:
                    webhook = {
                        "name": cells[0].text_content().strip(),
                        "url": cells[1].text_content().strip(),
                        "created_at": cells[2].text_content().strip()
                    }
                    webhooks.append(webhook)
                    logger.debug(f"Webhook信息: {webhook}")
            
            return webhooks
        except Exception as e:
            logger.error(f"获取Webhook列表失败: {str(e)}")
            return []
    
    @allure.step("创建Webhook: {name}, {url}")
    def create_webhook(self, name: str, url: str) -> bool:
        """
        创建Webhook
        
        Args:
            name: Webhook名称
            url: Webhook URL
            
        Returns:
            bool: 是否创建成功
        """
        logger.info(f"创建Webhook: {name}, {url}")
        
        try:
            # 确保在Webhook标签页
            self.switch_to_tab("Webhook")
            
            # 点击Create按钮
            self.click_element(self.WEBHOOK_CREATE_BUTTON)
            self.page.wait_for_timeout(1000)
            
            # 输入名称和URL
            self.page.fill(self.WEBHOOK_NAME_INPUT, name)
            self.page.fill(self.WEBHOOK_URL_INPUT, url)
            
            # 点击Save
            self.click_element(self.WEBHOOK_SAVE_BUTTON)
            self.page.wait_for_timeout(2000)
            
            logger.info(f"Webhook '{name}' 创建成功")
            return True
        except Exception as e:
            logger.error(f"创建Webhook失败: {str(e)}")
            return False
    
    @allure.step("验证Webhook是否存在: {webhook_name}")
    def verify_webhook_exists(self, webhook_name: str) -> bool:
        """
        验证Webhook是否存在于列表中
        
        Args:
            webhook_name: Webhook名称
            
        Returns:
            bool: Webhook是否存在
        """
        logger.info(f"验证Webhook是否存在: {webhook_name}")
        webhooks = self.get_webhook_list()
        webhook_names = [wh["name"] for wh in webhooks]
        
        exists = webhook_name in webhook_names
        if exists:
            logger.info(f"Webhook '{webhook_name}' 存在于列表中")
        else:
            logger.warning(f"Webhook '{webhook_name}' 不在列表中")
        
        return exists
    
    @allure.step("删除Webhook: {webhook_name}")
    def delete_webhook(self, webhook_name: str) -> bool:
        """
        删除Webhook
        
        Args:
            webhook_name: Webhook名称
            
        Returns:
            bool: 是否删除成功
        """
        logger.info(f"删除Webhook: {webhook_name}")
        
        try:
            # 确保在Webhook标签页
            self.switch_to_tab("Webhook")
            
            # 找到包含该Webhook名称的行，然后点击操作菜单
            row = self.page.locator(f"tr:has-text('{webhook_name}')")
            action_menu = row.locator(self.WEBHOOK_ACTION_MENU)
            action_menu.click()
            self.page.wait_for_timeout(500)
            
            # 点击Delete菜单项
            self.click_element(self.DELETE_MENU_ITEM)
            self.page.wait_for_timeout(1000)
            
            # 确认删除
            self.click_element(self.DELETE_CONFIRM_BUTTON)
            self.page.wait_for_timeout(2000)
            
            logger.info(f"Webhook '{webhook_name}' 已删除")
            return True
        except Exception as e:
            logger.error(f"删除Webhook失败: {str(e)}")
            return False
    
    # ========== CROS相关方法 ==========
    
    @allure.step("获取CROS列表")
    def get_cros_list(self) -> List[Dict[str, str]]:
        """
        获取CROS列表
        
        Returns:
            List[Dict[str, str]]: CROS列表
        """
        logger.info("获取CROS列表")
        cros_list = []
        
        try:
            # 切换到CROS标签页
            self.switch_to_tab("Cros")
            
            # 等待表格加载
            self.page.wait_for_selector(self.CROS_TABLE, timeout=5000)
            
            # 获取所有行
            rows = self.page.query_selector_all(f"{self.CROS_TABLE} >> tbody >> tr")
            logger.info(f"找到 {len(rows)} 个CROS配置")
            
            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) >= 2:
                    cros = {
                        "origin": cells[0].text_content().strip(),
                        "created_at": cells[1].text_content().strip()
                    }
                    cros_list.append(cros)
                    logger.debug(f"CROS信息: {cros}")
            
            return cros_list
        except Exception as e:
            logger.error(f"获取CROS列表失败: {str(e)}")
            return []
    
    @allure.step("创建CROS: {origin}")
    def create_cros(self, origin: str) -> bool:
        """
        创建CROS配置
        
        Args:
            origin: 源地址
            
        Returns:
            bool: 是否创建成功
        """
        logger.info(f"创建CROS: {origin}")
        
        try:
            # 切换到CROS标签页
            self.switch_to_tab("Cros")
            
            # 点击Create按钮
            self.click_element(self.CROS_CREATE_BUTTON)
            self.page.wait_for_timeout(1000)
            
            # 输入origin
            self.page.fill(self.CROS_ORIGIN_INPUT, origin)
            
            # 点击Save
            self.click_element(self.CROS_SAVE_BUTTON)
            self.page.wait_for_timeout(2000)
            
            logger.info(f"CROS '{origin}' 创建成功")
            return True
        except Exception as e:
            logger.error(f"创建CROS失败: {str(e)}")
            return False
    
    @allure.step("验证CROS是否存在: {origin}")
    def verify_cros_exists(self, origin: str) -> bool:
        """
        验证CROS是否存在于列表中
        
        Args:
            origin: 源地址
            
        Returns:
            bool: CROS是否存在
        """
        logger.info(f"验证CROS是否存在: {origin}")
        cros_list = self.get_cros_list()
        origins = [cros["origin"] for cros in cros_list]
        
        exists = origin in origins
        if exists:
            logger.info(f"CROS '{origin}' 存在于列表中")
        else:
            logger.warning(f"CROS '{origin}' 不在列表中")
        
        return exists
    
    @allure.step("删除CROS: {origin}")
    def delete_cros(self, origin: str) -> bool:
        """
        删除CROS配置
        
        Args:
            origin: 源地址
            
        Returns:
            bool: 是否删除成功
        """
        logger.info(f"删除CROS: {origin}")
        
        try:
            # 切换到CROS标签页
            self.switch_to_tab("Cros")
            
            # 找到包含该origin的行，然后点击操作菜单
            row = self.page.locator(f"tr:has-text('{origin}')")
            action_menu = row.locator(self.CROS_ACTION_MENU)
            action_menu.click()
            self.page.wait_for_timeout(500)
            
            # 点击Delete菜单项
            self.click_element(self.DELETE_MENU_ITEM)
            self.page.wait_for_timeout(1000)
            
            # 确认删除
            self.click_element(self.DELETE_CONFIRM_BUTTON)
            self.page.wait_for_timeout(2000)
            
            logger.info(f"CROS '{origin}' 已删除")
            return True
        except Exception as e:
            logger.error(f"删除CROS失败: {str(e)}")
            return False
    
    # ========== 通用方法 ==========
    
    @allure.step("点击侧边栏菜单: {menu_name}")
    def click_sidebar_menu(self, menu_name: str) -> None:
        """
        点击侧边栏菜单
        
        Args:
            menu_name: 菜单名称 (API Keys, Workflows, Configuration)
        """
        logger.info(f"点击侧边栏菜单: {menu_name}")
        menu_selector = f"text={menu_name}"
        self.click_element(menu_selector)
        self.page.wait_for_timeout(2000)
    
    @allure.step("验证页面URL包含: {expected_path}")
    def verify_url_contains(self, expected_path: str) -> bool:
        """
        验证当前URL是否包含指定路径
        
        Args:
            expected_path: 期望的路径
            
        Returns:
            bool: URL是否包含指定路径
        """
        current_url = self.get_current_url()
        contains = expected_path in current_url
        
        if contains:
            logger.info(f"URL包含预期路径: {expected_path}")
        else:
            logger.warning(f"URL不包含预期路径: {expected_path}, 当前URL: {current_url}")
        
        return contains

