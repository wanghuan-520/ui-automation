"""
Configuration页面对象
负责DLL、CORS等配置管理功能
"""
from playwright.sync_api import Page, Locator
from typing import List, Dict, Optional
import allure
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.page_utils import PageUtils

logger = get_logger(__name__)


class ConfigurationPage(BasePage):
    """Configuration页面对象"""
    
    # 页面URL
    CONFIGURATION_URL = "/dashboard/configuration"
    
    # 侧边栏导航
    APIKEYS_MENU = "text=API Keys"
    WORKFLOWS_MENU = "text=Workflows"
    CONFIGURATION_MENU = "text=Configuration"
    
    # 页面标题
    PAGE_TITLE = "text=Configuration"
    
    # Restart services按钮（⚠️ 有bug，会导致环境挂掉）
    RESTART_SERVICES_BUTTON = "button:has-text('Restart services')"
    
    # ========== DLL区域元素 ==========
    DLL_SECTION = "text=DLL"  # 简化定位器，直接使用文本
    DLL_UPLOAD_BUTTON = "button:has-text('Upload')"  # ⚠️ 有bug，会导致环境挂掉
    DLL_TABLE = "table >> nth=0"  # DLL表格（第一个表格）
    DLL_TABLE_HEADERS = ["DLL File", "Created", "Created By", "Updated", "Updated By", "Status"]
    DLL_NO_DATA = "text=No DLLs uploaded yet"
    
    # ========== CORS区域元素 ==========
    CORS_SECTION = "text=CORS"  # 简化定位器，直接使用文本
    # CORS Add按钮 - 使用role定位器（与MCP探查一致）
    CORS_ADD_BUTTON_ROLE = "role=button[name='Add']"  # 使用role定位器
    CORS_TABLE = "table >> nth=1"  # CORS表格（第二个表格）
    CORS_TABLE_HEADERS = ["Domain", "Created", "Created By"]
    CORS_NO_DATA = "text=No Cross URL added yet"
    
    # CORS创建对话框（基于MCP探查结果）
    CORS_DIALOG = "role=dialog[name='Add cross-origin domain']"  # 使用role定位器
    CORS_DIALOG_TITLE = "role=heading[name='Add cross-origin domain']"  # 对话框标题
    CORS_DOMAIN_INPUT = "role=textbox[name='Domain']"  # Domain输入框
    CORS_DIALOG_ADD_BUTTON = "role=dialog >> role=button[name='Add']"  # dialog内的Add按钮
    CORS_DIALOG_CANCEL_BUTTON = "role=dialog >> role=button[name='Cancel']"  # dialog内的Cancel按钮
    CORS_DIALOG_CLOSE_BUTTON = "role=dialog >> role=button[name='Close']"  # dialog内的Close按钮
    
    # CORS操作菜单
    CORS_MORE_OPTIONS_BUTTON = "button:has-text('More options')"
    
    # 删除确认弹窗（基于MCP探查结果）
    DELETE_DIALOG = "dialog"  # 删除确认对话框
    DELETE_DIALOG_MESSAGE = "text=Are you sure you want to delete this URL?"
    DELETE_CONFIRM_BUTTON = "button:has-text('yes')"  # 注意：按钮显示是小写'yes'
    DELETE_CANCEL_BUTTON = "dialog >> button:has-text('Cancel')"
    
    # 页面加载指示器（使用CORS区域作为加载标识，避免与侧边栏冲突）
    page_loaded_indicator = "text=CORS"
    
    def __init__(self, page: Page):
        """
        初始化Configuration页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.CONFIGURATION_URL}"
        self.page_utils = PageUtils(page)
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
            self.page.wait_for_selector(self.PAGE_TITLE, timeout=5000)
            logger.info("Configuration页面已加载")
            return True
        except Exception as e:
            logger.error(f"Configuration页面加载失败: {str(e)}")
            return False
    
    @allure.step("等待页面初始化完成")
    def wait_for_page_initialization(self, max_wait_seconds: int = 30) -> bool:
        """
        等待页面初始化完成（等待Scanning/Initialising状态消失）
        
        Args:
            max_wait_seconds: 最大等待时间（秒）
            
        Returns:
            bool: 是否初始化完成
        """
        logger.info(f"等待页面初始化（最多{max_wait_seconds}秒）...")
        
        for i in range(max_wait_seconds):
            self.page.wait_for_timeout(1000)
            
            # 检查是否还有Scanning/Initialising文本
            scanning_elements = self.page.locator('text=/Scanning|Initialising/i')
            count = scanning_elements.count()
            
            if count == 0:
                logger.info(f"✅ 页面初始化完成（等待了{i+1}秒）")
                return True
            
            # 检查元素是否可见
            all_hidden = True
            for j in range(count):
                if scanning_elements.nth(j).is_visible():
                    all_hidden = False
                    break
            
            if all_hidden:
                logger.info(f"✅ 页面初始化完成（等待了{i+1}秒）")
                return True
        
        logger.warning(f"⚠️ 页面初始化超时（等待了{max_wait_seconds}秒）")
        return False
    
    # ========== DLL相关方法 ==========
    # ⚠️ 注意：DLL Upload和Restart services功能有bug，会导致环境挂掉
    # 相关测试用例应该被skip
    
    @allure.step("检查DLL区域是否可见")
    def is_dll_section_visible(self) -> bool:
        """
        检查DLL区域是否可见
        
        Returns:
            bool: DLL区域是否可见
        """
        try:
            return self.page.locator(self.DLL_SECTION).is_visible(timeout=5000)
        except:
            return False
    
    @allure.step("检查DLL Upload按钮是否可见")
    def is_dll_upload_button_visible(self) -> bool:
        """
        检查DLL Upload按钮是否可见（⚠️ 不要点击，会导致环境挂掉）
        
        Returns:
            bool: Upload按钮是否可见
        """
        return self.is_element_visible(self.DLL_UPLOAD_BUTTON, timeout=2000)
    
    @allure.step("检查Restart services按钮是否可见")
    def is_restart_services_button_visible(self) -> bool:
        """
        检查Restart services按钮是否可见（⚠️ 不要点击，会导致环境挂掉）
        
        Returns:
            bool: Restart services按钮是否可见
        """
        return self.is_element_visible(self.RESTART_SERVICES_BUTTON, timeout=2000)
    
    # ========== CORS相关方法 ==========
    
    @allure.step("检查CORS区域是否可见")
    def is_cors_section_visible(self) -> bool:
        """
        检查CORS区域是否可见
        
        Returns:
            bool: CORS区域是否可见
        """
        try:
            return self.page.locator(self.CORS_SECTION).is_visible(timeout=5000)
        except:
            return False
    
    @allure.step("点击CORS Add按钮")
    def click_cors_add_button(self) -> None:
        """点击CORS Add按钮"""
        logger.info("点击CORS Add按钮")
        # 等待页面稳定
        self.page.wait_for_timeout(1000)
        # 使用role定位器（与MCP探查一致）
        add_button = self.page.get_by_role('button', name='Add')
        add_button.click()
        logger.info("✅ Add按钮已点击")
        self.page.wait_for_timeout(1000)
    
    @allure.step("验证CORS创建对话框是否打开")
    def is_cors_dialog_open(self) -> bool:
        """
        验证CORS创建对话框是否打开
        
        Returns:
            bool: 对话框是否打开
        """
        try:
            # 等待对话框出现
            self.page.wait_for_timeout(500)
            return self.page.locator(self.CORS_DIALOG).is_visible(timeout=3000)
        except:
            return False
    
    # 别名方法，为了测试代码的可读性
    def is_cors_create_dialog_visible(self) -> bool:
        """
        验证CORS创建对话框是否可见（别名方法）
        
        Returns:
            bool: 对话框是否可见
        """
        return self.is_cors_dialog_open()
    
    @allure.step("填写CORS Domain输入框")
    def fill_cors_domain_input(self, domain: str) -> None:
        """
        填写CORS创建对话框中的Domain输入框
        
        Args:
            domain: 要填写的domain
        """
        logger.info(f"填写Domain输入框: {domain}")
        domain_input = self.page.get_by_role('textbox', name='Domain')
        domain_input.fill(domain)
        self.page.wait_for_timeout(500)
        logger.info("✅ Domain已填写")
    
    @allure.step("点击CORS对话框中的Add按钮")
    def click_cors_dialog_add_button(self) -> None:
        """点击CORS创建对话框中的Add按钮"""
        logger.info("点击对话框中的Add按钮")
        dialog_add_button = self.page.locator(self.CORS_DIALOG_ADD_BUTTON)
        dialog_add_button.click()
        logger.info("✅ Add按钮已点击")
    
    @allure.step("点击CORS对话框中的Cancel按钮")
    def click_cors_dialog_cancel_button(self) -> None:
        """点击CORS创建对话框中的Cancel按钮"""
        logger.info("点击对话框中的Cancel按钮")
        cancel_btn = self.page.locator("role=dialog >> button:has-text('Cancel')")
        if cancel_btn.count() > 0 and cancel_btn.is_visible():
            cancel_btn.click()
            logger.info("✅ Cancel按钮已点击")
    
    @allure.step("获取CORS列表")
    def get_cors_list(self) -> List[Dict[str, str]]:
        """
        获取CORS列表
        
        Returns:
            List[Dict[str, str]]: CORS列表，每个元素包含 domain, created, created_by
        """
        logger.info("获取CORS列表")
        cors_list = []
        
        try:
            # 等待表格加载
            self.page.wait_for_timeout(1000)
            
            # 检查是否有"No Cross URL added yet"
            if self.is_element_visible(self.CORS_NO_DATA, timeout=2000):
                logger.info("CORS列表为空")
                return []
            
            # 获取CORS表格（第二个表格）
            table = self.page.locator(self.CORS_TABLE)
            
            # 等待表格出现
            if not table.is_visible(timeout=2000):
                logger.warning("CORS表格不可见")
                return []
            
            # 获取所有行
            rows = table.locator("tbody >> tr").all()
            
            logger.info(f"找到 {len(rows)} 个CORS配置行")
            
            for row in rows:
                cells = row.locator("td").all()
                if len(cells) >= 3:
                    # 跳过"No Cross URL added yet"行
                    first_cell_text = cells[0].text_content().strip()
                    if "No Cross URL" in first_cell_text or first_cell_text == "":
                        continue
                    
                    cors = {
                        "domain": first_cell_text,
                        "created": cells[1].text_content().strip(),
                        "created_by": cells[2].text_content().strip()
                    }
                    cors_list.append(cors)
                    logger.debug(f"CORS信息: {cors}")
            
            return cors_list
        except Exception as e:
            logger.error(f"获取CORS列表失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    @allure.step("创建CORS: {domain}")
    def create_cors(self, domain: str) -> bool:
        """
        创建CORS配置
        
        Args:
            domain: 域名（例如：https://example.com）
            
        Returns:
            bool: 是否创建成功
        """
        logger.info(f"创建CORS: {domain}")
        
        try:
            # 预检查：确保没有打开的对话框
            try:
                dialogs = self.page.locator("dialog").all()
                for dialog in dialogs:
                    if dialog.is_visible(timeout=500):
                        logger.warning("⚠️ 发现打开的对话框，尝试关闭")
                        cancel_btn = dialog.locator("button:has-text('Cancel')")
                        if cancel_btn.count() > 0:
                            cancel_btn.click()
                            self.page.wait_for_timeout(1000)
            except:
                pass
            
            # 等待页面稳定（关键：确保JS已完全加载）
            self.page.wait_for_timeout(1000)
            logger.info("等待页面稳定完成")
            
            # 使用getByRole点击Add按钮（与MCP探查一致）
            logger.info("使用role定位器点击CORS Add按钮")
            add_button = self.page.get_by_role('button', name='Add')
            add_button.click()
            logger.info("✅ Add按钮已点击")
            
            self.page.wait_for_timeout(1000)  # 等待对话框动画
            self.page_utils.screenshot_step(f"01-点击Add按钮后")
            
            # 等待对话框打开（使用role定位器）
            logger.info("等待对话框出现...")
            self.page.wait_for_selector(self.CORS_DIALOG, timeout=10000)
            logger.info("✅ 对话框已打开")
            self.page_utils.screenshot_step(f"02-对话框已打开")
            
            # 输入domain
            logger.info(f"输入域名: {domain}")
            domain_input = self.page.get_by_role('textbox', name='Domain')
            domain_input.fill(domain)
            self.page.wait_for_timeout(500)
            self.page_utils.screenshot_step(f"03-已输入域名_{domain}")
            
            # 点击dialog内的Add按钮
            logger.info("点击对话框中的Add按钮")
            dialog_add_button = self.page.locator(self.CORS_DIALOG_ADD_BUTTON)
            dialog_add_button.click()
            logger.info("✅ 已点击对话框中的Add按钮")
            
            # 等待对话框关闭
            try:
                self.page.wait_for_selector(self.CORS_DIALOG, state='hidden', timeout=5000)
                logger.info("✅ 对话框已关闭")
            except:
                logger.warning("⚠️ 对话框未关闭")
            
            # ⚠️ 重要：不需要手动刷新，列表会自动更新
            self.page.wait_for_timeout(2000)  # 等待列表更新
            self.page_utils.screenshot_step(f"04-CORS创建完成_{domain}")
            
            logger.info(f"✅ CORS '{domain}' 创建成功")
            return True
        except Exception as e:
            logger.error(f"❌ 创建CORS失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            self.page_utils.screenshot_step(f"ERROR-创建CORS失败")
            return False
    
    @allure.step("验证CORS是否存在: {domain}")
    def verify_cors_exists(self, domain: str) -> bool:
        """
        验证CORS是否存在于列表中
        
        Args:
            domain: 域名
            
        Returns:
            bool: CORS是否存在
        """
        logger.info(f"验证CORS是否存在: {domain}")
        
        # ⚠️ 不需要刷新页面，列表自动更新
        self.page.wait_for_timeout(1000)  # 等待列表渲染
        
        cors_list = self.get_cors_list()
        domains = [cors["domain"] for cors in cors_list]
        
        exists = domain in domains
        if exists:
            logger.info(f"✅ CORS '{domain}' 存在于列表中")
        else:
            logger.warning(f"⚠️ CORS '{domain}' 不在列表中")
            logger.debug(f"当前CORS列表: {domains}")
        
        return exists
    
    @allure.step("删除CORS: {domain}")
    def delete_cors(self, domain: str) -> bool:
        """
        删除CORS配置
        
        Args:
            domain: 域名
            
        Returns:
            bool: 是否删除成功
        """
        logger.info(f"删除CORS: {domain}")
        
        try:
            # 预检查：确保没有打开的对话框
            try:
                dialogs = self.page.locator("dialog").all()
                for dialog in dialogs:
                    if dialog.is_visible(timeout=500):
                        logger.warning("⚠️ 发现打开的对话框，尝试关闭")
                        cancel_btn = dialog.locator("button:has-text('Cancel')")
                        if cancel_btn.count() > 0:
                            cancel_btn.click()
                            self.page.wait_for_timeout(500)
            except:
                pass
            
            # 等待页面稳定
            self.page.wait_for_timeout(1000)
            
            # 找到包含该domain的行
            row = self.page.locator(f"tr:has-text('{domain}')").first
            if row.count() == 0:
                logger.warning(f"❌ 未找到CORS: {domain}")
                return False
            
            self.page_utils.screenshot_step(f"01-准备删除CORS_{domain}")
            
            # 找到该行的More options按钮（使用更鲁棒的方式）
            logger.info(f"查找 '{domain}' 行的More options按钮")
            more_options_button = row.get_by_role('button', name='More options')
            
            # 等待按钮可见
            more_options_button.wait_for(state='visible', timeout=5000)
            logger.info("More options按钮已可见")
            
            more_options_button.click()
            self.page.wait_for_timeout(1000)
            logger.info("✅ 已点击More options按钮")
            self.page_utils.screenshot_step(f"02-点击More_options_{domain}")
            
            # 直接使用getByText查找Delete（更简单鲁棒）
            logger.info("查找Delete菜单项...")
            
            # 等待菜单出现
            self.page.wait_for_timeout(500)
            
            # 使用get_by_text直接查找Delete选项（不限定在dialog中）
            delete_option = self.page.get_by_text("Delete", exact=True)
            
            if delete_option.count() > 0:
                delete_option.click()
                logger.info("✅ 成功点击Delete菜单项")
            else:
                # 如果没找到，尝试在dialog中查找
                dialogs = self.page.locator("dialog").all()
                delete_clicked = False
                for dialog in dialogs:
                    try:
                        if not dialog.is_visible():
                            continue
                        delete_btn = dialog.get_by_text("Delete", exact=True)
                        if delete_btn.count() > 0:
                            delete_btn.click()
                            delete_clicked = True
                            logger.info("✅ 在dialog中找到并点击Delete")
                            break
                    except Exception as e:
                        logger.debug(f"在dialog中查找Delete失败: {e}")
                        continue
                
                if not delete_clicked:
                    raise Exception("❌ 未找到Delete菜单项")
            
            self.page.wait_for_timeout(1000)
            self.page_utils.screenshot_step(f"03-点击Delete菜单项_{domain}")
            
            # 等待删除确认弹窗（增加timeout）
            self.page.wait_for_selector(self.DELETE_DIALOG_MESSAGE, timeout=10000)
            logger.info("删除确认对话框已显示")
            self.page_utils.screenshot_step(f"04-删除确认弹窗_{domain}")
            
            # 点击Yes确认删除
            self.click_element(self.DELETE_CONFIRM_BUTTON)
            logger.info("已点击Yes确认删除")
            
            # 等待对话框关闭
            try:
                self.page.wait_for_selector(self.DELETE_DIALOG, state='detached', timeout=5000)
                logger.info("✅ 删除确认对话框已关闭")
            except:
                logger.warning("⚠️ 删除确认对话框未关闭")
            
            # ⚠️ 重要：不需要手动刷新，列表会自动更新
            self.page.wait_for_timeout(1000)  # 等待列表更新
            self.page_utils.screenshot_step(f"05-CORS删除完成_{domain}")
            
            logger.info(f"✅ CORS '{domain}' 已删除")
            return True
        except Exception as e:
            logger.error(f"❌ 删除CORS失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            self.page_utils.screenshot_step(f"ERROR-删除CORS失败")
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
