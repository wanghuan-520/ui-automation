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
    
    # 页面主要按钮（页面顶部的Create按钮，包含图标）
    CREATE_KEY_BUTTON = "button:has-text('Create'):has(img)"  # 页面顶部的Create按钮包含图标，对话框中的不包含
    
    # API Keys表格
    APIKEYS_TABLE = "role=table"
    KEY_NAME_CELL = "cell[cursor=pointer]"
    KEY_STATUS = "text=Active"
    KEY_ACTION_MENU = "button:has(img)"  # 修正：操作菜单是button，包含img图标
    
    # Create/Edit API Key弹窗
    DIALOG_TITLE = "role=dialog >> role=heading[name='Create new API key']"  # 使用role定位
    DIALOG_NAME_INPUT = "role=dialog >> role=textbox[name='Name of the key']"  # 使用role定位，更准确
    DIALOG_CREATE_BUTTON = "role=dialog >> role=button[name='Create']"  # 使用role定位Create按钮
    DIALOG_CANCEL_BUTTON = "role=dialog >> role=button[name='Cancel']"  # 使用role定位Cancel按钮
    DIALOG_CLOSE_BUTTON = "role=dialog >> role=button[name='Close']"  # 使用role定位Close按钮
    
    # 操作菜单项（点击操作按钮后弹出的菜单）
    EDIT_MENU_ITEM = "div[cursor='pointer']:has-text('Edit')"  # 修正：使用cursor属性，避免ambiguity
    DELETE_MENU_ITEM = "div[cursor='pointer']:has-text('Delete')"  # 修正：使用cursor属性，避免匹配到Key名称中的Delete
    
    # 删除确认弹窗
    DELETE_DIALOG = "role=dialog"  # 修正：使用role定位
    DELETE_CONFIRM_BUTTON = "button:has-text('Yes')"  # 修正：确认按钮文本是'Yes'
    DELETE_CANCEL_BUTTON = "button:has-text('Cancel')"  # 修正：取消按钮
    
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
        # 使用first()来确保点击页面顶部的Create按钮（而不是对话框中的）
        create_button = self.page.locator("button:has-text('Create')").first
        create_button.click()
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
            # 点击Create按钮
            self.click_create_key()
            
            # 等待弹窗出现 - 使用role=dialog更准确
            self.page.wait_for_selector("role=dialog", timeout=5000)
            self.page.wait_for_timeout(500)
            
            # 输入Key名称 - 使用更新后的定位器
            self.page.fill(self.DIALOG_NAME_INPUT, key_name)
            self.page.wait_for_timeout(500)
            
            # 点击对话框内的Create按钮
            self.click_element(self.DIALOG_CREATE_BUTTON)
            
            # 等待对话框完全消失
            try:
                self.page.wait_for_selector("role=dialog", state="detached", timeout=3000)
                logger.info("✅ 对话框已关闭")
            except:
                logger.warning("⚠️  对话框未关闭，可能有验证错误")
            
            # 等待API Key创建完成
            self.page.wait_for_timeout(2000)
            
            # 刷新页面确保列表更新
            self.page.reload()
            self.page.wait_for_timeout(2000)
            self.wait_for_page_load()
            
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
            List[Dict[str, str]]: API Keys列表，每个Key包含name和status
        """
        logger.info("获取API Keys列表")
        api_keys = []
        
        try:
            # 等待表格加载
            self.page.wait_for_selector(self.APIKEYS_TABLE, timeout=5000)
            self.page.wait_for_timeout(1000)  # 等待数据加载
            
            # 检查是否有"No API keys created yet"的消息
            no_data_message = self.page.locator("text=No API keys created yet")
            if no_data_message.is_visible(timeout=1000):
                logger.info("当前没有API Keys")
                return []
            
            # 获取所有行 - 使用正确的定位器
            table = self.page.locator(self.APIKEYS_TABLE)
            tbody = table.locator("tbody")
            rows = tbody.locator("tr").all()
            
            logger.info(f"找到 {len(rows)} 行数据")
            
            for row in rows:
                try:
                    cells = row.locator("td").all()
                    if len(cells) >= 5:  # Name, Client ID, API Key, Created, Created By, (Actions)
                        name_text = cells[0].text_content().strip()
                        
                        # 跳过"No API keys created yet"行
                        if "No API keys" in name_text:
                            continue
                        
                        api_key = {
                            "name": name_text,
                            "client_id": cells[1].text_content().strip() if len(cells) > 1 else "",
                            "api_key": cells[2].text_content().strip() if len(cells) > 2 else "",
                            "created": cells[3].text_content().strip() if len(cells) > 3 else "",
                            "created_by": cells[4].text_content().strip() if len(cells) > 4 else "",
                            "status": "Active"  # 默认状态
                        }
                        api_keys.append(api_key)
                        logger.debug(f"API Key信息: {api_key}")
                except Exception as row_error:
                    logger.warning(f"解析行数据失败: {str(row_error)}")
                    continue
            
            logger.info(f"成功获取 {len(api_keys)} 个API Keys")
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
        # 找到包含该Key名称的行，然后点击最后一列的操作按钮
        row = self.page.locator(f"tr:has-text('{key_name}')")
        # 获取该行最后一个cell中的button（操作菜单按钮）
        action_button = row.locator("td").last.locator("button")
        action_button.click()
        self.page.wait_for_timeout(500)
    
    @allure.step("编辑API Key: {old_name} -> {new_name}")
    def edit_api_key_name(self, old_name: str, new_name: str) -> bool:
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
            
            # 等待菜单出现（菜单是dialog类型）
            self.page.wait_for_timeout(1000)
            
            # 从所有dialog中查找Edit选项
            dialogs = self.page.locator("role=dialog").all()
            edit_clicked = False
            for dialog in dialogs:
                try:
                    if not dialog.is_visible():
                        continue
                    edit_option = dialog.get_by_text("Edit", exact=True)
                    if edit_option.count() > 0 and edit_option.is_visible():
                        edit_option.click()
                        edit_clicked = True
                        logger.info("✅ 成功点击Edit菜单项")
                        break
                except Exception as e:
                    logger.debug(f"在dialog中查找Edit失败: {e}")
                    continue
            
            if not edit_clicked:
                raise Exception("未找到Edit菜单项")
            
            self.page.wait_for_timeout(1000)
            
            # 等待编辑对话框出现 (Edit API Key dialog)
            edit_dialog_input = 'role=dialog[name="Edit API Key"] >> role=textbox[name="Name of the Key"]'
            self.page.wait_for_selector(edit_dialog_input, timeout=5000)
            self.page.wait_for_timeout(500)
            
            # 清空并输入新名称
            self.page.fill(edit_dialog_input, "")
            self.page.fill(edit_dialog_input, new_name)
            self.page.wait_for_timeout(500)
            
            # 点击保存按钮（Save按钮）
            save_button = 'role=dialog[name="Edit API Key"] >> role=button[name="Save"]'
            self.click_element(save_button)
            
            # 等待弹窗关闭
            try:
                self.page.wait_for_selector("role=dialog", state="detached", timeout=3000)
                logger.info("✅ 编辑对话框已关闭")
            except:
                logger.warning("⚠️  编辑对话框未关闭")
            
            # 刷新页面确保列表更新
            self.page.reload()
            self.page.wait_for_timeout(2000)
            self.wait_for_page_load()
            
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
            
            # 等待菜单出现（菜单是dialog类型）
            self.page.wait_for_timeout(1000)
            
            # 从所有dialog中查找Delete选项（使用getByText避免匹配到Key名称中的Delete）
            # 遍历所有可见的dialog，找到包含Delete的操作菜单
            dialogs = self.page.locator("role=dialog").all()
            delete_clicked = False
            for dialog in dialogs:
                try:
                    # 检查dialog是否可见
                    if not dialog.is_visible():
                        continue
                    # 在每个dialog中查找Delete文本
                    delete_option = dialog.get_by_text("Delete", exact=True)
                    if delete_option.count() > 0 and delete_option.is_visible():
                        delete_option.click()
                        delete_clicked = True
                        logger.info("✅ 成功点击Delete菜单项")
                        break
                except Exception as e:
                    logger.debug(f"在dialog中查找Delete失败: {e}")
                    continue
            
            if not delete_clicked:
                raise Exception("未找到Delete菜单项")
            
            self.page.wait_for_timeout(1000)
            
            # 等待删除确认对话框出现（包含"Yes"按钮的对话框）
            self.page.wait_for_selector(self.DELETE_CONFIRM_BUTTON, timeout=5000)
            self.page.wait_for_timeout(500)
            
            # 点击确认删除（Yes按钮）
            self.click_element(self.DELETE_CONFIRM_BUTTON)
            
            # 等待对话框关闭和删除完成
            try:
                self.page.wait_for_selector("button:has-text('Yes')", state="detached", timeout=5000)
                logger.info("✅ 删除确认对话框已关闭")
            except:
                logger.warning("⚠️  删除确认对话框未关闭，但继续执行")
            
            # 刷新页面确保列表更新
            self.page.reload()
            self.page.wait_for_timeout(2000)
            self.wait_for_page_load()
            
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
        # 使用dialog role更准确
        return self.is_element_visible("role=dialog", timeout=2000)
    
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
    
    # ========== 以下是测试脚本中使用的方法别名和补充方法 ==========
    
    def is_create_dialog_visible(self) -> bool:
        """
        验证创建对话框是否可见（is_create_dialog_open的别名）
        
        Returns:
            bool: 对话框是否可见
        """
        return self.is_create_dialog_open()
    
    
    @allure.step("点击对话框Cancel按钮")
    def click_cancel_create(self) -> None:
        """点击对话框的Cancel按钮"""
        logger.info("点击Cancel按钮")
        self.click_element(self.DIALOG_CANCEL_BUTTON)
        self.page.wait_for_timeout(500)
    
    @allure.step("点击对话框Create按钮")
    def click_dialog_create(self) -> None:
        """点击对话框的Create按钮"""
        logger.info("点击对话框Create按钮")
        self.click_element(self.DIALOG_CREATE_BUTTON)
        self.page.wait_for_timeout(1000)
    
    @allure.step("点击Workflows菜单")
    def click_workflows_menu(self) -> None:
        """点击侧边栏Workflows菜单"""
        logger.info("点击Workflows菜单")
        self.click_element(self.WORKFLOWS_MENU)
        self.page.wait_for_timeout(2000)
    
    @allure.step("点击API Keys菜单")
    def click_apikeys_menu(self) -> None:
        """点击侧边栏API Keys菜单"""
        logger.info("点击API Keys菜单")
        self.click_element(self.APIKEYS_MENU)
        self.page.wait_for_timeout(2000)

