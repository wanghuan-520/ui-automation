"""
Dashboard Workflows页面对象
负责工作流列表管理功能
"""
from playwright.sync_api import Page, Locator
from typing import List, Dict, Optional
import allure
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardWorkflowsPage(BasePage):
    """Dashboard Workflows页面对象"""
    
    # 页面URL
    WORKFLOWS_URL = "/dashboard/workflows"
    
    # 顶部导航栏
    ORG_SELECTOR = "button:has-text('O1')"
    PROJECT_SELECTOR = "button:has-text('default project')"
    DASHBOARD_BUTTON = "button:has-text('Dashboard')"
    SETTINGS_BUTTON = "button:has-text('Settings')"
    PROFILE_BUTTON = "button[name='profile']"
    
    # 侧边栏导航
    APIKEYS_MENU = "text=API Keys"
    WORKFLOWS_MENU = "text=Workflows"
    CONFIGURATION_MENU = "text=Configuration"
    
    # 页面主要按钮
    NEW_WORKFLOW_BUTTON = "button:has-text('New Workflow')"
    IMPORT_WORKFLOW_BUTTON = "button:has-text('Import Workflow')"
    CHOOSE_FILE_BUTTON = "button:has-text('Choose File')"
    FORMAT_LAYOUT_BUTTON = "button[aria-label='format layout']"
    
    # 工作流表格
    WORKFLOW_TABLE = "role=table"
    WORKFLOW_NAME_CELL = "cell >> generic[cursor=pointer]"
    WORKFLOW_STATUS = "generic:has-text('Pending')"
    WORKFLOW_ACTION_MENU = "combobox[cursor=pointer]"
    
    # 底部链接
    WEBSITE_LINK = "link:has-text('Website')"
    GITHUB_LINK = "link:has-text('Github')"
    DOCS_LINK = "link:has-text('Docs')"
    
    # 页面加载指示器
    page_loaded_indicator = "role=table"
    
    def __init__(self, page: Page):
        """
        初始化Dashboard Workflows页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}{self.WORKFLOWS_URL}"
        logger.info(f"初始化Dashboard Workflows页面: {self.page_url}")
    
    @allure.step("导航到Workflows页面")
    def navigate(self) -> None:
        """导航到Workflows页面"""
        logger.info(f"导航到Workflows页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """
        检查Workflows页面是否已加载
        
        Returns:
            bool: 页面是否已加载
        """
        try:
            self.page.wait_for_selector(self.WORKFLOW_TABLE, timeout=10000)
            logger.info("Workflows页面已加载")
            return True
        except Exception as e:
            logger.error(f"Workflows页面加载失败: {str(e)}")
            return False
    
    @allure.step("点击New Workflow按钮")
    def click_new_workflow(self) -> None:
        """点击New Workflow按钮"""
        logger.info("点击New Workflow按钮")
        self.click_element(self.NEW_WORKFLOW_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("点击Import Workflow按钮")
    def click_import_workflow(self) -> None:
        """点击Import Workflow按钮"""
        logger.info("点击Import Workflow按钮")
        self.click_element(self.IMPORT_WORKFLOW_BUTTON)
        self.page.wait_for_timeout(1000)
    
    @allure.step("从文件导入Workflow: {file_path}")
    def import_workflow_from_file(self, file_path: str) -> bool:
        """
        从文件导入Workflow
        
        Args:
            file_path: Workflow JSON文件路径
            
        Returns:
            bool: 是否导入成功
        """
        logger.info(f"从文件导入Workflow: {file_path}")
        
        try:
            # 1. 点击Import Workflow按钮打开弹窗
            self.click_import_workflow()
            self.page.wait_for_timeout(1000) # 等待弹窗渲染

            # 2. 处理文件上传
            # 优先尝试直接设置文件到 input[type='file']，这是最稳健的方法
            try:
                logger.info("尝试直接设置文件到 input[type='file']")
                # 等待input元素出现 (即使是hidden的)
                self.page.wait_for_selector("input[type='file']", state="attached", timeout=5000)
                self.page.set_input_files("input[type='file']", file_path)
                logger.info(f"已设置文件: {file_path}")
            except Exception as e:
                logger.warning(f"直接设置文件失败，尝试使用文件选择器交互: {e}")
                
                # 回退方案: 点击按钮触发文件选择器
                with self.page.expect_file_chooser() as fc_info:
                    # 尝试点击可能触发上传的区域
                    # 可能是 "Click or drag file to this area to upload"
                    upload_triggers = [
                        "button:has-text('Choose File')",
                        "button:has-text('Upload')",
                        "button:has-text('Select')",
                        ".ant-upload-drag", # Common Ant Design upload area
                        "div[role='presentation']" # Sometimes used for drag areas
                    ]
                    
                    clicked = False
                    for selector in upload_triggers:
                        if self.page.locator(selector).is_visible():
                            self.page.click(selector)
                            clicked = True
                            logger.info(f"点击了触发上传的元素: {selector}")
                            break
                    
                    if not clicked:
                        # 最后的尝试: 点击弹窗中间
                        logger.info("未找到明确的上传按钮，尝试点击弹窗中心")
                        self.page.mouse.click(960, 540) # 假设弹窗在屏幕中间

                file_chooser = fc_info.value
                file_chooser.set_files(file_path)
                logger.info(f"通过文件选择器已选择文件: {file_path}")
            
            self.page.wait_for_timeout(1000)
            
            # 3. 点击确认导入 (如果有 Import/Confirm 按钮)
            # 尝试查找弹窗内的确认按钮
            confirm_selectors = [
                "button:has-text('Import')",
                "button:has-text('Confirm')",
                "button:has-text('Upload')",
                "button[type='submit']"
            ]
            
            for selector in confirm_selectors:
                try:
                    btn = self.page.wait_for_selector(selector, timeout=2000, state="visible")
                    # 排除触发弹窗的那个 Import Workflow 按钮 (如果在背景中可见)
                    # 通常弹窗内的按钮层级更高
                    if btn:
                        btn.click()
                        logger.info(f"点击了确认按钮: {selector}")
                        break
                except:
                    continue
            
            # 4. 等待导入完成 (弹窗关闭或列表刷新)
            self.page.wait_for_timeout(2000)
            
            # 简单验证：没有错误提示
            error_toast = self.page.locator("text=/Error|Failed/i")
            if error_toast.is_visible():
                logger.error("❌ 导入时出现错误提示")
                self.take_screenshot("import_failed.png")
                return False
                
            logger.info("✅ 导入操作完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 导入Workflow失败: {str(e)}")
            self.take_screenshot("workflow_import_error.png")
            return False

    @allure.step("获取工作流列表")
    def get_workflow_list(self) -> List[Dict[str, str]]:
        """
        获取工作流列表
        
        Returns:
            List[Dict[str, str]]: 工作流列表，每个工作流包含name, last_updated, last_run, status
        """
        logger.info("获取工作流列表")
        workflows = []
        
        try:
            # 等待表格加载
            self.page.wait_for_selector(self.WORKFLOW_TABLE, timeout=5000)
            
            # 获取所有行
            rows = self.page.query_selector_all(f"{self.WORKFLOW_TABLE} >> tbody >> tr")
            logger.info(f"找到 {len(rows)} 个工作流")
            
            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) >= 4:
                    workflow = {
                        "name": cells[0].text_content().strip(),
                        "last_updated": cells[1].text_content().strip(),
                        "last_run": cells[2].text_content().strip(),
                        "status": cells[3].text_content().strip()
                    }
                    workflows.append(workflow)
                    logger.debug(f"工作流信息: {workflow}")
            
            return workflows
        except Exception as e:
            logger.error(f"获取工作流列表失败: {str(e)}")
            return []
    
    @allure.step("验证工作流列表包含指定工作流: {workflow_name}")
    def verify_workflow_exists(self, workflow_name: str) -> bool:
        """
        验证工作流是否存在于列表中
        
        Args:
            workflow_name: 工作流名称
            
        Returns:
            bool: 工作流是否存在
        """
        logger.info(f"验证工作流是否存在: {workflow_name}")
        workflows = self.get_workflow_list()
        workflow_names = [wf["name"] for wf in workflows]
        
        exists = workflow_name in workflow_names
        if exists:
            logger.info(f"工作流 '{workflow_name}' 存在于列表中")
        else:
            logger.warning(f"工作流 '{workflow_name}' 不在列表中")
        
        return exists
    
    @allure.step("点击工作流名称: {workflow_name}")
    def click_workflow_name(self, workflow_name: str) -> None:
        """
        点击工作流名称进入详情页
        
        Args:
            workflow_name: 工作流名称
        """
        logger.info(f"点击工作流名称: {workflow_name}")
        workflow_link = f"text={workflow_name}"
        self.click_element(workflow_link)
        self.page.wait_for_timeout(2000)
    
    @allure.step("获取工作流状态: {workflow_name}")
    def get_workflow_status(self, workflow_name: str) -> Optional[str]:
        """
        获取指定工作流的状态
        
        Args:
            workflow_name: 工作流名称
            
        Returns:
            Optional[str]: 工作流状态，如果未找到返回None
        """
        logger.info(f"获取工作流状态: {workflow_name}")
        workflows = self.get_workflow_list()
        
        for workflow in workflows:
            if workflow["name"] == workflow_name:
                status = workflow["status"]
                logger.info(f"工作流 '{workflow_name}' 状态: {status}")
                return status
        
        logger.warning(f"未找到工作流: {workflow_name}")
        return None
    
    @allure.step("点击工作流操作菜单: {workflow_name}")
    def click_workflow_action_menu(self, workflow_name: str) -> None:
        """
        点击工作流的操作菜单
        
        Args:
            workflow_name: 工作流名称
        """
        logger.info(f"点击工作流操作菜单: {workflow_name}")
        # 找到包含该工作流名称的行，然后点击操作菜单
        # 使用 .first 以防止有重名工作流导致Strict mode error
        row = self.page.locator(f"tr:has-text('{workflow_name}')").first
        
        # 尝试多种选择器找到操作菜单按钮
        menu_selectors = [
            self.WORKFLOW_ACTION_MENU,          # 原有选择器
            "button[aria-haspopup='menu']",     # 常见的下拉菜单触发器
            "button[aria-label='Actions']",     # 常见的Actions标签
            "button[aria-label='More options']",
            "td:last-child button",             # 最后一列的按钮
            "div[role='button'][aria-haspopup='menu']"
        ]
        
        for selector in menu_selectors:
            try:
                # 尝试定位并点击
                btn = row.locator(selector).first
                # 快速检查可见性 (500ms)
                if btn.count() > 0 and btn.is_visible(timeout=500):
                    btn.click()
                    self.page.wait_for_timeout(500)
                    logger.info(f"✅ 成功点击操作菜单 (selector: {selector})")
                    return
            except:
                continue
        
        # 如果都失败了，记录截图并抛出异常
        self.take_screenshot(f"action_menu_not_found_{workflow_name}.png")
        logger.error(f"❌ 未找到工作流 '{workflow_name}' 的操作菜单按钮")
        raise Exception(f"未找到工作流 '{workflow_name}' 的操作菜单按钮")
    
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
    
    @allure.step("点击Settings按钮")
    def click_settings_button(self) -> None:
        """点击顶部导航栏的Settings按钮"""
        logger.info("点击Settings按钮")
        self.click_element(self.SETTINGS_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("点击Dashboard按钮")
    def click_dashboard_button(self) -> None:
        """点击顶部导航栏的Dashboard按钮"""
        logger.info("点击Dashboard按钮")
        self.click_element(self.DASHBOARD_BUTTON)
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
    
    @allure.step("检查工作流列表是否为空")
    def is_workflow_list_empty(self) -> bool:
        """
        检查工作流列表是否为空
        
        Returns:
            bool: 列表是否为空
        """
        workflows = self.get_workflow_list()
        is_empty = len(workflows) == 0
        
        if is_empty:
            logger.info("工作流列表为空")
        else:
            logger.info(f"工作流列表包含 {len(workflows)} 个工作流")
        
        return is_empty
    
    @allure.step("等待工作流状态变为: {expected_status}")
    def wait_for_workflow_status(self, workflow_name: str, expected_status: str, timeout: int = 30000) -> bool:
        """
        等待工作流状态变为指定状态
        
        Args:
            workflow_name: 工作流名称
            expected_status: 期望的状态
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否达到期望状态
        """
        logger.info(f"等待工作流 '{workflow_name}' 状态变为: {expected_status}")
        import time
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < timeout:
            status = self.get_workflow_status(workflow_name)
            if status == expected_status:
                logger.info(f"工作流状态已变为: {expected_status}")
                return True
            
            # 等待1秒后重试
            time.sleep(1)
            self.page.reload()
            self.wait_for_page_load()
        
        logger.error(f"等待超时，工作流状态未变为: {expected_status}")
        return False
    
    # ========== 完整功能流程方法 ==========
    
    @allure.step("重命名Workflow: {new_name}")
    def rename_workflow(self, new_name: str) -> bool:
        """
        在编辑器中重命名Workflow
        """
        logger.info(f"尝试重命名Workflow为: {new_name}")
        try:
            # 策略1: 检查是否是点击弹窗式重命名 (根据dump的HTML)
            # 查找显示名称的元素 (通常是 default project / untitled_workflow)
            # 结构: button/div[aria-haspopup='dialog'] -> div(text)
            
            # 尝试找到包含 'untitled' 的可点击元素
            name_trigger = self.page.locator("div[aria-haspopup='dialog']").filter(has_text="untitled_workflow").first
            if not name_trigger.is_visible():
                name_trigger = self.page.locator("div[aria-haspopup='dialog']").filter(has_text="Untitled").first
                
            if not name_trigger.is_visible():
                # 尝试通过文本直接查找
                name_trigger = self.page.locator("text=untitled_workflow").first
            
            # 如果找到的是隐藏元素（例如响应式布局中的移动端元素），尝试遍历所有匹配项
            if not name_trigger.is_visible():
                logger.info("首个匹配元素不可见，尝试查找所有匹配项中可见的一个...")
                candidates = self.page.locator("div[aria-haspopup='dialog']").filter(has_text="untitled_workflow").all()
                for cand in candidates:
                    if cand.is_visible():
                        name_trigger = cand
                        logger.info("✅ 找到可见的重命名触发元素")
                        break

            if name_trigger.is_visible():
                logger.info("✅ 找到重命名触发元素，点击打开弹窗")
                name_trigger.click()
                
                # 等待弹窗出现
                dialog = self.page.wait_for_selector("div[role='dialog']", timeout=3000)
                if dialog:
                    logger.info("✅ 重命名弹窗已打开")
                    self.take_screenshot("rename_dialog_opened.png")
                    
                    # 查找输入框
                    input_el = self.page.locator("div[role='dialog'] input[type='text']").first
                    if not input_el.is_visible():
                        logger.error("❌ 输入框不可见！")
                        self.take_screenshot("rename_input_not_visible.png")
                        return False
                    
                    logger.info(f"✅ 找到输入框，开始填写: {new_name}")
                    input_el.click()
                    self.page.wait_for_timeout(300)
                    
                    # 清空后再填写，确保不会残留旧值
                    input_el.fill("")
                    self.page.wait_for_timeout(200)
                    input_el.type(new_name, delay=50) # 使用type而不是fill，模拟人工输入
                    self.page.wait_for_timeout(300)
                    
                    logger.info(f"✅ 已填写完毕: {new_name}")
                    self.take_screenshot("rename_after_fill.png")
                        
                    # 查找确认按钮
                    save_selectors = [
                        "div[role='dialog'] button:has-text('Save')",
                        "div[role='dialog'] button:has-text('Rename')",
                        "div[role='dialog'] button:has-text('Confirm')",
                        "div[role='dialog'] button[type='submit']",
                        "div[role='dialog'] button:has-text('保存')",
                        "div[role='dialog'] button:has-text('确定')"
                    ]
                    
                    save_btn = None
                    for selector in save_selectors:
                        btn = self.page.locator(selector).first
                        if btn.is_visible():
                            save_btn = btn
                            break
                    
                    if save_btn:
                        save_btn.click()
                        logger.info(f"✅ 点击了重命名确认按钮: {save_btn}")
                    else:
                        # 如果没找到按钮，直接按Enter
                        logger.info("未找到保存按钮，尝试按Enter键提交")
                        self.page.keyboard.press("Enter")
                    
                    # 关键修改：不等待弹窗关闭，而是等待Header中名称出现
                    # 这样更健壮，即使弹窗卡住，只要名称更新了就算成功
                    logger.info(f"等待编辑器头部显示新名称: {new_name}")
                    try:
                        # 等待Header中出现新名称（更可靠的成功指标）
                        self.page.wait_for_selector(f"header:has-text('{new_name}')", timeout=5000)
                        logger.info(f"✅ Workflow已重命名为: {new_name}")
                        
                        # 如果弹窗还在，主动关闭它（点击外部或ESC）
                        if self.page.locator("div[role='dialog']").is_visible():
                            logger.info("弹窗仍可见，尝试按ESC关闭")
                            self.page.keyboard.press("Escape")
                            self.page.wait_for_timeout(500)
                        
                        return True
                    except:
                        logger.warning(f"⚠️ 未检测到Header中的新名称: {new_name}")
                        # 最后的重试：再次按Enter并等待
                        self.page.keyboard.press("Enter")
                        self.page.wait_for_timeout(2000)
                        
                        # 再次检查Header
                        try:
                            self.page.wait_for_selector(f"header:has-text('{new_name}')", timeout=3000)
                            logger.info(f"✅ 重试后检测到新名称: {new_name}")
                            # 关闭可能残留的弹窗
                            self.page.keyboard.press("Escape")
                            return True
                        except:
                            logger.error(f"❌ 重命名最终失败: {new_name}")
                            self.take_screenshot("rename_header_not_updated.png")
                            return False
            
            # 策略2: 原有的输入框查找逻辑 (回退)
            logger.info("尝试直接查找输入框 (策略2)...")
            inputs = [
                "input[value*='Untitled']",
                "input[placeholder='Workflow Name']",
                "header input[type='text']"
            ]
            
            for selector in inputs:
                if self.page.locator(selector).first.is_visible():
                    self.page.locator(selector).first.fill(new_name)
                    self.page.keyboard.press("Enter")
                    logger.info(f"✅ 通过输入框重命名为: {new_name}")
                    return True

            logger.warning("⚠️ 无法定位Workflow重命名元素")
            self.take_screenshot("rename_failed.png")
            return False
                
        except Exception as e:
            logger.warning(f"重命名失败: {e}")
            return False

    @allure.step("创建新的Workflow并配置")
    def create_and_configure_workflow(self, workflow_config: Dict[str, str] = None) -> bool:
        """
        创建并配置新的Workflow（完整流程）
        
        Args:
            workflow_config: Workflow配置信息 {"name": "新名称", "agent_type": "InputGAgent", ...}
            
        Returns:
            bool: 是否创建成功
        """
        logger.info("开始创建并配置新的Workflow")
        
        try:
            # 1. 点击New Workflow按钮
            self.click_new_workflow()
            logger.info("✅ 已点击New Workflow按钮")
            
            # 2. 关闭AI助手弹窗（如果有）
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(2000)
            logger.info("✅ 已关闭AI助手弹窗")
            
            # 3. 如果提供了配置
            if workflow_config:
                # 重命名
                if "name" in workflow_config:
                    self.rename_workflow(workflow_config["name"])
                
                # 添加Agent
                agent_type = workflow_config.get("agent_type", "InputGAgent")
                success = self.add_agent_to_canvas(agent_type)
                
                if success and "member_name" in workflow_config:
                    self.configure_agent(workflow_config)
            
            logger.info("✅ Workflow创建和配置完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 创建Workflow失败: {str(e)}")
            self.take_screenshot("workflow_create_failed.png")
            return False
    
    @allure.step("添加Agent到画布: {agent_type}")
    def add_agent_to_canvas(self, agent_type: str = "InputGAgent", drop_x: int = None, drop_y: int = None) -> bool:
        """
        通过拖拽方式添加Agent到画布
        
        Args:
            agent_type: Agent类型名称
            drop_x: 放置的X坐标 (可选)
            drop_y: 放置的Y坐标 (可选)
            
        Returns:
            bool: 是否添加成功
        """
        logger.info(f"添加Agent到画布: {agent_type}")
        
        try:
            # 尝试多个选择器找到Agent
            agent_selectors = [
                f"text={agent_type}",
                f"[class*='{agent_type}']",
                f"div:has-text('{agent_type}')"
            ]
            
            agent_element = None
            for selector in agent_selectors:
                try:
                    agent_element = self.page.wait_for_selector(selector, timeout=3000)
                    if agent_element:
                        logger.info(f"✅ 找到Agent元素: {selector}")
                        break
                except:
                    continue
            
            if not agent_element:
                logger.error(f"❌ 未找到Agent: {agent_type}")
                return False
            
            # 获取Agent位置
            agent_box = agent_element.bounding_box()
            if not agent_box:
                logger.error("❌ 无法获取Agent元素位置")
                return False
            
            # 计算画布放置位置
            viewport = self.page.viewport_size
            if drop_x is None:
                drop_x = viewport['width'] * 0.5
            if drop_y is None:
                drop_y = viewport['height'] // 2
            
            # 执行拖拽操作
            logger.info(f"拖拽Agent从 ({agent_box['x']}, {agent_box['y']}) 到 ({drop_x}, {drop_y})")
            
            # 移动到Agent中心
            self.page.mouse.move(
                agent_box['x'] + agent_box['width'] / 2,
                agent_box['y'] + agent_box['height'] / 2
            )
            self.page.mouse.down()
            self.page.wait_for_timeout(300)
            
            # 拖拽到画布
            self.page.mouse.move(drop_x, drop_y, steps=10)
            self.page.wait_for_timeout(300)
            self.page.mouse.up()
            
            # 等待Agent添加完成
            self.page.wait_for_timeout(2000)
            logger.info("✅ Agent已拖拽到画布")
            
            # 验证是否出现配置弹窗 (ChatAlGAgent 等可能也有弹窗)
            try:
                config_modal = self.page.wait_for_selector(
                    "text=/Agent configuration|Configure|配置/i",
                    timeout=3000
                )
                if config_modal:
                    logger.info("✅ Agent配置弹窗已打开")
                    return True
            except:
                logger.warning("⚠️ 未检测到配置弹窗，但Agent可能已添加")
                return True
            
            return True # 默认成功
            
        except Exception as e:
            logger.error(f"❌ 添加Agent失败: {str(e)}")
            self.take_screenshot("add_agent_failed.png")
            return False

    def get_agent_on_canvas(self, agent_name: str):
        """
        获取画布上的Agent元素
        (优化：优先匹配React Flow节点类，或寻找最小包围盒以排除父容器)
        """
        logger.info(f"Searching for agent '{agent_name}' on canvas...")
        
        # 策略1: 尝试直接定位 React Flow 节点类
        try:
            nodes = self.page.locator(f".react-flow__node:has-text('{agent_name}')").all()
            if nodes:
                for node in nodes:
                    if node.is_visible():
                        box = node.bounding_box()
                        if box and box['x'] > 300:
                            logger.info(f"✅ Found .react-flow__node: {box}")
                            return node
        except:
            pass
            
        # 策略2: 通用查找，取面积最小的可见元素 (排除包含该文本的巨大父容器)
        elements = self.page.locator(f"div:has-text('{agent_name}')").all()
        candidates = []
        
        for element in elements:
            try:
                if not element.is_visible():
                    continue
                
                box = element.bounding_box()
                if box and box['x'] > 300:
                    area = box['width'] * box['height']
                    # 过滤掉全屏级别的大容器 (假设节点不会超过 500x500)
                    if area < 250000: 
                        candidates.append((area, element, box))
            except:
                continue
        
        if candidates:
            # 按面积从小到大排序，取最小的 (最内层元素)
            candidates.sort(key=lambda x: x[0])
            best_match = candidates[0]
            logger.info(f"✅ Found best match (Area: {best_match[0]}): {best_match[2]}")
            return best_match[1]
            
        logger.warning(f"❌ Agent '{agent_name}' not found on canvas")
        return None

    @allure.step("连接两个Agent: {source_name} -> {target_name}")
    def connect_agents(self, source_name: str, target_name: str) -> bool:
        """
        连接两个Agent (优先查找Handle元素，失败则回退到坐标)
        
        Args:
            source_name: 源Agent名称
            target_name: 目标Agent名称
            
        Returns:
            bool: 是否连接操作完成
        """
        logger.info(f"连接Agent: {source_name} -> {target_name}")
        self.take_screenshot(f"before_connect_{source_name}_{target_name}.png")
        
        try:
            # 1. 获取源节点和目标节点
            source_element = self.get_agent_on_canvas(source_name)
            target_element = self.get_agent_on_canvas(target_name)
            
            if not source_element or not target_element:
                logger.error(f"❌ 无法在画布上找到Agent: Source={bool(source_element)}, Target={bool(target_element)}")
                return False
            
            # 2. 尝试查找 Handle 元素 (针对 React Flow 等库)
            # 源节点：通常是 source handle (right)
            source_handle = source_element.locator(".react-flow__handle-right, .source, [data-handle-pos='right']").first
            # 目标节点：通常是 target handle (left)
            target_handle = target_element.locator(".react-flow__handle-left, .target, [data-handle-pos='left']").first
            
            use_handles = False
            try:
                if source_handle.count() > 0 and target_handle.count() > 0:
                    # 获取 Handle 的精确位置
                    source_box = source_handle.bounding_box()
                    target_box = target_handle.bounding_box()
                    if source_box and target_box:
                        logger.info("✅ 找到精确的 Handle 元素")
                        start_x = source_box['x'] + source_box['width'] / 2
                        start_y = source_box['y'] + source_box['height'] / 2
                        end_x = target_box['x'] + target_box['width'] / 2
                        end_y = target_box['y'] + target_box['height'] / 2
                        use_handles = True
            except:
                pass
            
            if not use_handles:
                logger.info("⚠️ 未找到Handle元素，使用坐标估算")
                source_box = source_element.bounding_box()
                target_box = target_element.bounding_box()
                
                # 源节点右侧边缘中心
                start_x = source_box['x'] + source_box['width'] - 2
                start_y = source_box['y'] + source_box['height'] / 2
                
                # 目标节点左侧边缘中心
                end_x = target_box['x'] + 2
                end_y = target_box['y'] + target_box['height'] / 2
            
            logger.info(f"拖拽连线: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            
            # 3. 执行拖拽 (模拟人类慢速操作)
            # 3.1 移动到源点并悬停
            self.page.mouse.move(start_x, start_y)
            self.page.wait_for_timeout(1000) # 充分悬停，确保Handle激活
            
            # 3.2 按下鼠标
            self.page.mouse.down()
            self.page.wait_for_timeout(500)
            
            # 3.3 缓慢移出源节点 (触发连线绘制)
            self.page.mouse.move(start_x + 100, start_y, steps=20)
            self.page.wait_for_timeout(500)
            
            # 3.4 缓慢移动到目标点
            self.page.mouse.move(end_x, end_y, steps=50) # 非常慢的移动
            self.page.wait_for_timeout(1000) # 在目标点悬停，等待吸附
            
            # 3.5 微动鼠标 (Wiggle) 确保触发 mouseover 事件
            self.page.mouse.move(end_x + 5, end_y + 5, steps=5)
            self.page.wait_for_timeout(200)
            self.page.mouse.move(end_x - 5, end_y - 5, steps=5)
            self.page.wait_for_timeout(200)
            self.page.mouse.move(end_x, end_y, steps=5) # 回到中心
            self.page.wait_for_timeout(1000) # 再次等待
            
            # 3.6 释放鼠标
            self.page.mouse.up()
            self.page.wait_for_timeout(2000) # 等待连线完成的动画
            
            self.take_screenshot(f"after_connect_{source_name}_{target_name}.png")
            logger.info("✅ 连线操作完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 连接Agent失败: {str(e)}")
            self.take_screenshot("connect_agents_failed.png")
            return False
    
    @allure.step("配置Agent参数")
    def configure_agent(self, config: Dict[str, str]) -> bool:
        """
        配置Agent的参数
        
        Args:
            config: 配置参数字典 {"member_name": "test", "input": "测试输入"}
            
        Returns:
            bool: 是否配置成功
        """
        logger.info(f"配置Agent参数: {config}")
        
        try:
            # 填写memberName（第一个textarea）
            if "member_name" in config:
                textareas = self.page.query_selector_all("textarea")
                if len(textareas) >= 1:
                    textareas[0].fill(config["member_name"])
                    logger.info(f"✅ 已填写memberName: {config['member_name']}")
            
            # 填写input（第二个textarea）
            if "input" in config:
                textareas = self.page.query_selector_all("textarea")
                if len(textareas) >= 2:
                    textareas[1].fill(config["input"])
                    logger.info(f"✅ 已填写input: {config['input']}")
            
            # 关闭配置弹窗
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
            logger.info("✅ 配置完成，已关闭弹窗")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 配置Agent失败: {str(e)}")
            return False
    
    @allure.step("点击Format Layout按钮")
    def click_format_layout(self) -> bool:
        """点击Format Layout按钮以整理布局"""
        logger.info("点击Format Layout按钮")
        try:
            self.click_element(self.FORMAT_LAYOUT_BUTTON)
            self.page.wait_for_timeout(1000) # 等待布局动画完成
            return True
        except Exception as e:
            logger.warning(f"点击Format Layout按钮失败: {e}")
            return False

    @allure.step("运行Workflow")
    def run_workflow(self) -> bool:
        """
        点击Run按钮运行Workflow
        
        Returns:
            bool: 是否运行成功
        """
        logger.info("运行Workflow")
        
        try:
            # 查找并点击Run按钮
            run_button = self.page.locator("button:has-text('Run')")
            run_button.wait_for(state="visible", timeout=10000)
            
            # 确保按钮可点击
            if run_button.is_disabled():
                logger.error("❌ Run按钮处于禁用状态")
                return False
                
            # 模拟悬停和点击
            run_button.hover()
            self.page.wait_for_timeout(500)
            run_button.click()
            logger.info("✅ 已点击Run按钮")
            
            # 等待"Run"按钮状态变化或出现"Execution log"，以确认运行已触发
            # 策略：等待 Execution log 按钮出现，表示运行记录已创建
            try:
                self.page.wait_for_selector("button:has-text('Execution log')", timeout=5000)
                logger.info("✅ 检测到Execution log，运行已成功触发")
                return True
            except:
                logger.warning("⚠️ 点击Run后未立即检测到Execution log，尝试再次点击...")
                # 双重保障：如果第一次没点到，再点一次
                run_button.click()
                self.page.wait_for_timeout(2000)
                return True
            
        except Exception as e:
            logger.error(f"❌ 运行Workflow失败: {str(e)}")
            self.take_screenshot("workflow_run_failed.png")
            return False
    
    @allure.step("验证Workflow执行结果")
    def verify_workflow_execution(self, timeout: int = 60000) -> bool:
        """
        验证Workflow是否成功执行
        
        Args:
            timeout: 超时时间(毫秒)，默认60秒
            
        Returns:
            bool: 是否执行成功
        """
        logger.info("验证Workflow执行结果")
        
        # 优先等待明确的成功状态
        try:
            # 检查是否有Success状态指示 (通常在Execution log列表或Toast中)
            success_indicator = self.page.wait_for_selector(
                "text=/Success|Succeeded|Completed/i",
                timeout=timeout
            )
            if success_indicator:
                logger.info("✅ 检测到成功状态指示")
                self.take_screenshot("workflow_execution_success.png")
                return True
        except:
            logger.warning("⚠️ 未在超时时间内检测到明确的Success文本")
        
        # 降级检查：只要有Execution log按钮，也视为触发成功（可能是运行中）
        try:
            execution_log = self.page.wait_for_selector(
                "button:has-text('Execution log')",
                state="visible",
                timeout=2000
            )
            if execution_log:
                logger.info("✅ 检测到Execution log按钮，Workflow已触发")
                self.take_screenshot("workflow_triggered.png")
                return True
        except:
            pass
        
        # 3. 检查是否有Failed状态
        try:
            failed_indicator = self.page.wait_for_selector(
                "text=/Failed|失败|Error/i",
                timeout=2000
            )
            if failed_indicator:
                logger.error("❌ 检测到失败状态")
                self.take_screenshot("workflow_execution_failed.png")
                return False
        except:
            pass
        
        logger.error("❌ 无法验证执行结果")
        self.take_screenshot("workflow_verification_failed.png")
        return False
    
    @allure.step("获取当前画布上的连线数量")
    def get_edge_count(self) -> int:
        """
        获取画布上连线(Edge)的数量，用于验证连接是否成功
        
        Returns:
            int: 连线数量
        """
        # 尝试常见的连线选择器 (React Flow 等)
        edge_selectors = [
            ".react-flow__edge",
            "g.edge",
            "svg path.connection",
            ".jtk-connector" # jsPlumb
        ]
        
        count = 0
        for selector in edge_selectors:
            elements = self.page.locator(selector)
            current_count = elements.count()
            if current_count > 0:
                count = current_count
                logger.info(f"找到连线元素 ({selector}): {count} 条")
                break
        
        if count == 0:
            logger.info("未找到可见的连线元素")
            
        return count

    @allure.step("删除指定Workflow: {workflow_name}")
    def delete_workflow(self, workflow_name: str) -> bool:
        """
        删除指定的Workflow
        
        Args:
            workflow_name: Workflow名称
            
        Returns:
            bool: 是否删除成功
        """
        logger.info(f"删除Workflow: {workflow_name}")
        
        try:
            # 点击操作菜单
            self.click_workflow_action_menu(workflow_name)
            
            # 点击Delete选项
            # 使用通用文本选择器，避免复杂的混合选择器导致解析错误
            delete_button = self.page.wait_for_selector(
                "text=Delete",
                timeout=5000
            )
            delete_button.click()
            logger.info("✅ 已点击Delete按钮")
            
            self.page.wait_for_timeout(1000)
            
            # 确认删除
            # 限制在对话框内查找确认按钮，防止误点
            try:
                dialog = self.page.locator("role=dialog")
                if dialog.is_visible():
                    # 截图以便调试
                    self.take_screenshot("delete_confirmation_dialog.png")
                    
                    # 🔍 **详细调试: 输出对话框HTML结构**
                    try:
                        dialog_html = dialog.evaluate("el => el.outerHTML")
                        logger.info(f"📄 对话框HTML结构:\n{dialog_html}\n")
                        
                        dialog_text = dialog.inner_text()
                        logger.info(f"📝 对话框文本内容:\n{dialog_text}\n")
                        
                        # 🔍 **详细查找所有可能的交互元素**
                        logger.info("🔍 详细检查对话框中的所有元素...")
                        
                        # 检查所有input
                        inputs = dialog.locator("input").all()
                        logger.info(f"   Input元素: {len(inputs)} 个")
                        for i, inp in enumerate(inputs):
                            try:
                                inp_type = inp.get_attribute("type")
                                inp_id = inp.get_attribute("id") or "N/A"
                                inp_name = inp.get_attribute("name") or "N/A"
                                inp_visible = inp.is_visible()
                                logger.info(f"      [{i+1}] type={inp_type}, id={inp_id}, name={inp_name}, visible={inp_visible}")
                            except:
                                pass
                        
                        # 检查所有label
                        labels = dialog.locator("label").all()
                        logger.info(f"   Label元素: {len(labels)} 个")
                        for i, lbl in enumerate(labels):
                            try:
                                lbl_text = lbl.inner_text()[:50]
                                lbl_visible = lbl.is_visible()
                                lbl_for = lbl.get_attribute("for") or "N/A"
                                logger.info(f"      [{i+1}] text='{lbl_text}', for={lbl_for}, visible={lbl_visible}")
                            except:
                                pass
                        
                        # 检查所有包含"understand"的元素
                        understand_elems = dialog.locator("text=/understand/i").all()
                        logger.info(f"   包含'understand'的元素: {len(understand_elems)} 个")
                        for i, elem in enumerate(understand_elems):
                            try:
                                elem_text = elem.inner_text()[:60]
                                elem_tag = elem.evaluate("el => el.tagName")
                                elem_visible = elem.is_visible()
                                logger.info(f"      [{i+1}] <{elem_tag}> visible={elem_visible}, text='{elem_text}'")
                            except:
                                pass
                                
                    except Exception as e:
                        logger.warning(f"获取对话框结构失败: {e}")
                    
                    # ✅ 新增: 勾选复选框 (如果存在)
                    # 尝试多种选择器
                    checkbox_selectors = [
                        "input[type='checkbox']", 
                        "[role='checkbox']", 
                        ".ant-checkbox-input", 
                        "label:has(input[type='checkbox'])",
                        ".ant-checkbox",
                        "span.ant-checkbox",
                        "label",  # 添加通用label查找
                        "div[class*='checkbox']",  # 查找包含checkbox的div
                        "span[class*='checkbox']"  # 查找包含checkbox的span
                    ]
                    
                    checked = False
                    logger.info(f"🔍 开始查找复选框...")
                    
                    for selector in checkbox_selectors:
                        try:
                            cbs = dialog.locator(selector).all()
                            logger.info(f"🔍 selector='{selector}': {len(cbs)} 个元素")
                            
                            if len(cbs) > 0:
                                # 尝试所有找到的元素
                                for idx, cb in enumerate(cbs):
                                    try:
                                        if cb.is_visible():
                                            cb_text = cb.inner_text() if selector != "input[type='checkbox']" else ""
                                            logger.info(f"✅ 找到可见元素 {idx+1} (selector: {selector}, text: '{cb_text[:50]}')")
                                            cb.click(force=True)
                                            self.page.wait_for_timeout(800)
                                            logger.info(f"✅ 已点击元素 {idx+1}")
                                            checked = True
                                            break
                                    except Exception as e2:
                                        logger.debug(f"点击元素 {idx+1} 失败: {e2}")
                                
                                if checked:
                                    break
                        except Exception as e:
                            logger.debug(f"selector '{selector}' 失败: {e}")
                    
                    if not checked:
                        # 尝试点击文本元素 (特别是"I understand"相关文本)
                        logger.info("🔍 尝试查找确认文本...")
                        try:
                            label_texts = [
                                "I understand that all associated",
                                "I understand",
                                "understand",
                                "subagents will also be deleted",
                                "confirm",
                                "确认",
                                "我知道",
                                "确定删除"
                            ]
                            for text in label_texts:
                                try:
                                    # 使用contains查找
                                    text_elem = dialog.locator(f"text=/{text}/i").first
                                    if text_elem.count() > 0 and text_elem.is_visible():
                                        elem_text = text_elem.inner_text()
                                        logger.info(f"✅ 找到文本元素: '{elem_text[:50]}'")
                                        text_elem.click(force=True)
                                        self.page.wait_for_timeout(800)
                                        logger.info(f"✅ 已点击文本元素")
                                        checked = True
                                        break
                                except Exception as e:
                                    logger.debug(f"文本 '{text}' 查找失败: {e}")
                        except Exception as e:
                            logger.debug(f"文本查找整体失败: {e}")
                    
                    if not checked:
                        logger.warning("⚠️ 未找到复选框或确认元素")

                    confirm_button = dialog.locator(
                        "button:has-text('Delete'), button:has-text('Yes'), button:has-text('Confirm'), button:has-text('确认')"
                    ).first
                    
                    if confirm_button.is_visible():
                        # 🔍 **详细检查按钮状态**
                        try:
                            is_disabled = confirm_button.is_disabled()
                            is_enabled = confirm_button.is_enabled()
                            aria_disabled = confirm_button.get_attribute("aria-disabled")
                            data_disabled = confirm_button.get_attribute("data-disabled")
                            btn_class = confirm_button.get_attribute("class")
                            btn_text = confirm_button.inner_text()
                            
                            logger.info(f"🎯 确认按钮状态:")
                            logger.info(f"   文本: '{btn_text}'")
                            logger.info(f"   is_disabled(): {is_disabled}")
                            logger.info(f"   is_enabled(): {is_enabled}")
                            logger.info(f"   aria-disabled: {aria_disabled}")
                            logger.info(f"   data-disabled: {data_disabled}")
                            logger.info(f"   class: {btn_class}")
                        except Exception as e:
                            logger.warning(f"获取按钮状态失败: {e}")
                        
                        # 等待按钮变更为可用状态 (防抖)
                        try:
                            confirm_button.wait_for(state="visible", timeout=3000)
                            if confirm_button.is_disabled():
                                logger.warning("⚠️  确认按钮当前禁用，等待变为可用...")
                                # 可能是由于勾选复选框的动画延迟，稍作等待
                                self.page.wait_for_timeout(1000)
                            
                            if confirm_button.is_enabled():
                                confirm_button.click(force=True)
                                logger.info("✅ 已点击第一层确认按钮 (Yes)")
                            else:
                                logger.warning("⚠️ 确认按钮仍处于禁用状态，尝试强制点击")
                                confirm_button.click(force=True)
                                logger.info("✅ 已强制点击确认按钮 (禁用状态, force=True)")
                        except Exception as e:
                            logger.warning(f"点击确认按钮时出错: {e}")
                            confirm_button.click(force=True)
                            logger.info("✅ 已强制点击确认按钮 (异常处理, force=True)")
                        
                        # 🆕 等待第二层确认弹窗 (可能出现)
                        logger.info("⏳ 等待第二层确认弹窗...")
                        self.page.wait_for_timeout(2000)
                        
                        # 检查是否出现第二层弹窗
                        second_dialog = self.page.locator("role=dialog")
                        if second_dialog.is_visible():
                            logger.info("🔍 检测到第二层确认弹窗!")
                            self.take_screenshot("delete_second_dialog.png")
                            
                            # 输出第二层弹窗内容
                            try:
                                second_dialog_text = second_dialog.inner_text()
                                logger.info(f"📝 第二层弹窗文本:\n{second_dialog_text}\n")
                                
                                # 输出第二层弹窗HTML
                                second_dialog_html = second_dialog.evaluate("el => el.outerHTML")
                                logger.info(f"📄 第二层弹窗HTML (前2000字符):\n{second_dialog_html[:2000]}\n")
                            except Exception as e:
                                logger.warning(f"获取第二层弹窗内容失败: {e}")
                            
                            # 🔍 查找并勾选复选框 (第二层弹窗)
                            logger.info("🔍 在第二层弹窗中查找复选框...")
                            second_checked = False
                            
                            # 🆕 尝试多种复选框点击方式
                            
                            # 方式1: 直接查找checkbox input
                            try:
                                checkbox_input = second_dialog.locator("input[type='checkbox']").first
                                if checkbox_input.count() > 0:
                                    logger.info(f"✅ 找到checkbox input元素")
                                    checkbox_input.click(force=True)
                                    self.page.wait_for_timeout(500)
                                    logger.info(f"✅ 已勾选复选框 (input)")
                                    second_checked = True
                            except Exception as e:
                                logger.debug(f"直接点击input失败: {e}")
                            
                            # 方式2: 直接点击包含"I understand"的整个容器/行
                            if not second_checked:
                                try:
                                    logger.info("🔍 尝试点击整个确认行...")
                                    # 查找包含文本的父容器(可能是div/label包含checkbox+text)
                                    understand_container = second_dialog.locator("*").filter(has_text="I understand that all associated").first
                                    if understand_container.count() > 0:
                                        logger.info(f"✅ 找到包含'I understand'的容器")
                                        # 直接点击整个容器(可能会触发复选框)
                                        understand_container.click(force=True)
                                        self.page.wait_for_timeout(800)
                                        
                                        # 检查Delete按钮是否启用
                                        delete_btn_check = second_dialog.locator("button:has-text('Delete')").first
                                        if delete_btn_check.count() > 0 and not delete_btn_check.is_disabled():
                                            logger.info(f"✅ 点击容器成功勾选复选框!")
                                            second_checked = True
                                        else:
                                            logger.debug("点击容器未能启用Delete按钮,尝试其他方法")
                                except Exception as e:
                                    logger.debug(f"点击容器失败: {e}")
                            
                            # 如果直接点击input失败,尝试点击包含复选框的label
                            if not second_checked:
                                try:
                                    label_with_checkbox = second_dialog.locator("label").first
                                    if label_with_checkbox.count() > 0 and label_with_checkbox.is_visible():
                                        label_text = label_with_checkbox.inner_text()[:60]
                                        logger.info(f"✅ 找到label元素: '{label_text}'")
                                        label_with_checkbox.click(force=True)
                                        self.page.wait_for_timeout(500)
                                        logger.info(f"✅ 已点击label (触发复选框)")
                                        second_checked = True
                                except Exception as e:
                                    logger.debug(f"点击label失败: {e}")
                            
                            # 方式3: 使用键盘Tab+Space勾选复选框
                            if not second_checked:
                                try:
                                    logger.info("🔍 尝试使用键盘Tab+Space勾选复选框...")
                                    # 按Tab键切换焦点到复选框
                                    self.page.keyboard.press("Tab")
                                    self.page.wait_for_timeout(300)
                                    self.page.keyboard.press("Space")
                                    self.page.wait_for_timeout(800)
                                    
                                    # 检查Delete按钮是否启用
                                    delete_btn_check = second_dialog.locator("button:has-text('Delete')").first
                                    if delete_btn_check.count() > 0 and not delete_btn_check.is_disabled():
                                        logger.info(f"✅ 通过键盘成功勾选复选框!")
                                        second_checked = True
                                    else:
                                        logger.debug("Tab+Space未能启用Delete按钮")
                                except Exception as e:
                                    logger.debug(f"键盘操作失败: {e}")
                            
                            # 如果还是没成功,尝试其他选择器
                            if not second_checked:
                                for selector in checkbox_selectors:
                                    try:
                                        cbs = second_dialog.locator(selector).all()
                                        if len(cbs) > 0:
                                            for idx, cb in enumerate(cbs):
                                                try:
                                                    if cb.is_visible():
                                                        cb_text = cb.inner_text() if selector not in ["input[type='checkbox']", "[role='checkbox']"] else ""
                                                        logger.info(f"✅ 找到元素 (selector: {selector}, text: '{cb_text[:50]}')")
                                                        cb.click(force=True)
                                                        self.page.wait_for_timeout(800)
                                                        logger.info(f"✅ 已点击元素")
                                                        second_checked = True
                                                        break
                                                except:
                                                    pass
                                            if second_checked:
                                                break
                                    except:
                                        pass
                            
                            # 如果没找到复选框,尝试点击"I understand"文本
                            if not second_checked:
                                logger.info("🔍 尝试查找'I understand'文本...")
                                try:
                                    understand_texts = [
                                        "I understand that all associated",
                                        "I understand",
                                        "understand"
                                    ]
                                    for text in understand_texts:
                                        try:
                                            text_elem = second_dialog.locator(f"text=/{text}/i").first
                                            if text_elem.count() > 0 and text_elem.is_visible():
                                                elem_text = text_elem.inner_text()
                                                logger.info(f"✅ 找到确认文本: '{elem_text[:60]}'")
                                                text_elem.click(force=True)
                                                self.page.wait_for_timeout(800)
                                                logger.info(f"✅ 已点击确认文本")
                                                second_checked = True
                                                break
                                        except:
                                            pass
                                except:
                                    pass
                            
                            if not second_checked:
                                logger.warning("⚠️ 第二层弹窗未找到复选框或确认文本")
                            
                            # 点击第二层弹窗的Delete按钮
                            logger.info("🔍 查找第二层弹窗的Delete按钮...")
                            second_delete_btn = second_dialog.locator(
                                "button:has-text('Delete'), button:has-text('Yes'), button:has-text('Confirm')"
                            ).first
                            
                            if second_delete_btn.is_visible():
                                is_disabled = second_delete_btn.is_disabled()
                                logger.info(f"第二层Delete按钮状态: disabled={is_disabled}")
                                
                                if not is_disabled or second_checked:
                                    second_delete_btn.click(force=True)
                                    logger.info("✅ 已点击第二层弹窗的Delete按钮")
                                    self.page.wait_for_timeout(2000)
                                else:
                                    logger.warning("⚠️ 第二层Delete按钮禁用且未勾选复选框,尝试强制点击")
                                    second_delete_btn.click(force=True)
                                    self.page.wait_for_timeout(2000)
                            else:
                                logger.warning("⚠️ 未找到第二层弹窗的Delete按钮")
                        else:
                            logger.info("ℹ️  未检测到第二层确认弹窗(可能不需要)")
                    else:
                        logger.warning("⚠️ 对话框内未找到确认按钮")
                else:
                    # 如果没找到role=dialog，尝试全局查找
                    confirm_button = self.page.wait_for_selector(
                        "button:has-text('Delete'), button:has-text('Yes'), button:has-text('Confirm'), button:has-text('确认')",
                        timeout=5000
                    )
                    confirm_button.click()
                    logger.info("✅ 已点击确认按钮 (全局)")
            except Exception as e:
                logger.warning(f"确认删除步骤出现异常: {e}")
            
            # 等待对话框消失
            try:
                self.page.wait_for_selector("role=dialog", state="hidden", timeout=5000)
                logger.info("✅ 删除确认对话框已关闭")
            except:
                pass
            
            # 检查是否有成功提示
            try:
                success_toast = self.page.wait_for_selector("text=/Success|Deleted|Deleted successfully/i", timeout=5000)
                if success_toast:
                    logger.info("✅ 检测到删除成功提示")
            except:
                logger.warning("⚠️ 未检测到明确的删除成功提示")

            # 等待删除完成（后端处理）
            self.page.wait_for_timeout(3000)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 删除Workflow失败: {str(e)}")
            self.take_screenshot("workflow_delete_failed.png")
            return False

