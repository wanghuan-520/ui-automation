"""
API Keys页面对象
负责API密钥管理功能
"""
from playwright.sync_api import Page, Locator
from typing import List, Dict, Optional
import allure
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ApiKeysPage(BasePage):
    """API Keys页面对象"""
    
    # 页面URL
    APIKEYS_URL = "/dashboard/apikeys"
    
    # 侧边栏导航
    APIKEYS_MENU = "text=API Keys"
    WORKFLOWS_MENU = "text=Workflows"
    CONFIGURATION_MENU = "text=Configuration"
    
    # 页面主要按钮
    CREATE_KEY_BUTTON = "button:has-text('Create Key')"
    
    # API Keys表格
    APIKEYS_TABLE = "role=table"
    KEY_NAME_CELL = "cell[cursor=pointer]"
    KEY_STATUS = "text=Active"
    KEY_ACTION_MENU = "combobox[cursor=pointer]"
    
    # Create/Edit API Key弹窗
    DIALOG_TITLE = "text=Create API Key >> ancestor::div[role='dialog']"
    DIALOG_NAME_INPUT = "input[placeholder='Enter key name']"
    DIALOG_CREATE_BUTTON = "button:has-text('Create')"
    DIALOG_CANCEL_BUTTON = "button:has-text('Cancel')"
    DIALOG_CLOSE_BUTTON = "button[aria-label='Close']"
    
    # 操作菜单
    EDIT_MENU_ITEM = "text=Edit"
    DELETE_MENU_ITEM = "text=Delete"
    
    # 删除确认弹窗
    DELETE_DIALOG = "text=Delete API Key >> ancestor::div[role='dialog']"
    DELETE_CONFIRM_BUTTON = "button:has-text('Delete')"
    DELETE_CANCEL_BUTTON = "button:has-text('Cancel')"
    
    # 页面加载指示器
    page_loaded_indicator = "role=table"
    
    def __init__(self, page: Page):
        """
        初始化API Keys页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.APIKEYS_URL}"
        logger.info(f"初始化API Keys页面: {self.page_url}")
    
    @allure.step("导航到API Keys页面")
    def navigate(self) -> None:
        """导航到API Keys页面"""
        logger.info(f"导航到API Keys页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查API Keys页面是否已加载
        
        Returns:
            bool: 页面是否已加载
        """
        try:
            self.page.wait_for_selector(self.APIKEYS_TABLE, timeout=10000)
            logger.info("API Keys页面已加载")
            return True
        except Exception as e:
            logger.error(f"API Keys页面加载失败: {str(e)}")
            return False
    
    @allure.step("点击Create Key按钮")
    def click_create_key(self) -> None:
        """点击Create Key按钮打开创建弹窗"""
        logger.info("点击Create Key按钮")
        self.click_element(self.CREATE_KEY_BUTTON)
        self.page.wait_for_timeout(1000)
    
    @allure.step("创建API Key: {key_name}")
    def create_api_key(self, key_name: str) -> bool:
        """
        创建API Key
        
        Args:
            key_name: API Key名称
            
        Returns:
            bool: 是否创建成功
        """
        logger.info(f"创建API Key: {key_name}")
        
        try:
            # 点击Create Key按钮
            self.click_create_key()
            
            # 等待弹窗出现
            self.page.wait_for_selector(self.DIALOG_NAME_INPUT, timeout=5000)
            
            # 输入Key名称
            self.page.fill(self.DIALOG_NAME_INPUT, key_name)
            
            # 点击Create按钮
            self.click_element(self.DIALOG_CREATE_BUTTON)
            
            # 等待弹窗关闭
            self.page.wait_for_timeout(2000)
            
            logger.info(f"API Key '{key_name}' 创建成功")
            return True
        except Exception as e:
            logger.error(f"创建API Key失败: {str(e)}")
            return False
    
    @allure.step("获取API Keys列表")
    def get_api_keys_list(self) -> List[Dict[str, str]]:
        """
        获取API Keys列表
        
        Returns:
            List[Dict[str, str]]: API Keys列表，每个Key包含name, created_at, last_used, status
        """
        logger.info("获取API Keys列表")
        api_keys = []
        
        try:
            # 等待表格加载
            self.page.wait_for_selector(self.APIKEYS_TABLE, timeout=5000)
            
            # 获取所有行
            rows = self.page.query_selector_all(f"{self.APIKEYS_TABLE} >> tbody >> tr")
            logger.info(f"找到 {len(rows)} 个API Keys")
            
            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) >= 4:
                    api_key = {
                        "name": cells[0].text_content().strip(),
                        "created_at": cells[1].text_content().strip(),
                        "last_used": cells[2].text_content().strip(),
                        "status": cells[3].text_content().strip()
                    }
                    api_keys.append(api_key)
                    logger.debug(f"API Key信息: {api_key}")
            
            return api_keys
        except Exception as e:
            logger.error(f"获取API Keys列表失败: {str(e)}")
            return []
    
    @allure.step("验证API Key是否存在: {key_name}")
    def verify_api_key_exists(self, key_name: str) -> bool:
        """
        验证API Key是否存在于列表中
        
        Args:
            key_name: API Key名称
            
        Returns:
            bool: API Key是否存在
        """
        logger.info(f"验证API Key是否存在: {key_name}")
        api_keys = self.get_api_keys_list()
        key_names = [key["name"] for key in api_keys]
        
        exists = key_name in key_names
        if exists:
            logger.info(f"API Key '{key_name}' 存在于列表中")
        else:
            logger.warning(f"API Key '{key_name}' 不在列表中")
        
        return exists
    
    @allure.step("点击API Key操作菜单: {key_name}")
    def click_key_action_menu(self, key_name: str) -> None:
        """
        点击API Key的操作菜单
        
        Args:
            key_name: API Key名称
        """
        logger.info(f"点击API Key操作菜单: {key_name}")
        # 找到包含该Key名称的行，然后点击操作菜单
        row = self.page.locator(f"tr:has-text('{key_name}')")
        action_menu = row.locator(self.KEY_ACTION_MENU)
        action_menu.click()
        self.page.wait_for_timeout(500)
    
    @allure.step("编辑API Key: {old_name} -> {new_name}")
    def edit_api_key(self, old_name: str, new_name: str) -> bool:
        """
        编辑API Key名称
        
        Args:
            old_name: 原API Key名称
            new_name: 新API Key名称
            
        Returns:
            bool: 是否编辑成功
        """
        logger.info(f"编辑API Key: {old_name} -> {new_name}")
        
        try:
            # 点击操作菜单
            self.click_key_action_menu(old_name)
            
            # 点击Edit菜单项
            self.click_element(self.EDIT_MENU_ITEM)
            self.page.wait_for_timeout(1000)
            
            # 等待编辑弹窗
            self.page.wait_for_selector(self.DIALOG_NAME_INPUT, timeout=5000)
            
            # 清空并输入新名称
            self.page.fill(self.DIALOG_NAME_INPUT, "")
            self.page.fill(self.DIALOG_NAME_INPUT, new_name)
            
            # 点击保存按钮（Create按钮在编辑模式下可能显示为Save）
            save_button = "button:has-text('Save'), button:has-text('Create')"
            self.click_element(save_button)
            
            # 等待弹窗关闭
            self.page.wait_for_timeout(2000)
            
            logger.info(f"API Key '{old_name}' 已编辑为 '{new_name}'")
            return True
        except Exception as e:
            logger.error(f"编辑API Key失败: {str(e)}")
            return False
    
    @allure.step("删除API Key: {key_name}")
    def delete_api_key(self, key_name: str) -> bool:
        """
        删除API Key
        
        Args:
            key_name: API Key名称
            
        Returns:
            bool: 是否删除成功
        """
        logger.info(f"删除API Key: {key_name}")
        
        try:
            # 点击操作菜单
            self.click_key_action_menu(key_name)
            
            # 点击Delete菜单项
            self.click_element(self.DELETE_MENU_ITEM)
            self.page.wait_for_timeout(1000)
            
            # 等待删除确认弹窗
            self.page.wait_for_selector(self.DELETE_CONFIRM_BUTTON, timeout=5000)
            
            # 点击确认删除
            self.click_element(self.DELETE_CONFIRM_BUTTON)
            
            # 等待删除完成
            self.page.wait_for_timeout(2000)
            
            logger.info(f"API Key '{key_name}' 已删除")
            return True
        except Exception as e:
            logger.error(f"删除API Key失败: {str(e)}")
            return False
    
    @allure.step("取消创建API Key")
    def cancel_create_dialog(self) -> None:
        """关闭创建/编辑弹窗"""
        logger.info("取消创建/编辑API Key")
        
        try:
            # 点击Cancel按钮
            if self.is_element_visible(self.DIALOG_CANCEL_BUTTON, timeout=2000):
                self.click_element(self.DIALOG_CANCEL_BUTTON)
            # 或点击关闭按钮
            elif self.is_element_visible(self.DIALOG_CLOSE_BUTTON, timeout=2000):
                self.click_element(self.DIALOG_CLOSE_BUTTON)
            
            self.page.wait_for_timeout(500)
            logger.info("弹窗已关闭")
        except Exception as e:
            logger.error(f"关闭弹窗失败: {str(e)}")
    
    @allure.step("验证创建弹窗是否打开")
    def is_create_dialog_open(self) -> bool:
        """
        验证创建/编辑弹窗是否打开
        
        Returns:
            bool: 弹窗是否打开
        """
        return self.is_element_visible(self.DIALOG_NAME_INPUT, timeout=2000)
    
    @allure.step("获取API Key状态: {key_name}")
    def get_key_status(self, key_name: str) -> Optional[str]:
        """
        获取指定API Key的状态
        
        Args:
            key_name: API Key名称
            
        Returns:
            Optional[str]: API Key状态，如果未找到返回None
        """
        logger.info(f"获取API Key状态: {key_name}")
        api_keys = self.get_api_keys_list()
        
        for key in api_keys:
            if key["name"] == key_name:
                status = key["status"]
                logger.info(f"API Key '{key_name}' 状态: {status}")
                return status
        
        logger.warning(f"未找到API Key: {key_name}")
        return None
    
    @allure.step("检查API Keys列表是否为空")
    def is_api_keys_list_empty(self) -> bool:
        """
        检查API Keys列表是否为空
        
        Returns:
            bool: 列表是否为空
        """
        api_keys = self.get_api_keys_list()
        is_empty = len(api_keys) == 0
        
        if is_empty:
            logger.info("API Keys列表为空")
        else:
            logger.info(f"API Keys列表包含 {len(api_keys)} 个Key")
        
        return is_empty
    
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

