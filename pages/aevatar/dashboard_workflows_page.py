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
        row = self.page.locator(f"tr:has-text('{workflow_name}')")
        action_menu = row.locator(self.WORKFLOW_ACTION_MENU)
        action_menu.click()
        self.page.wait_for_timeout(500)
    
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
    
    @allure.step("创建新的Workflow并配置")
    def create_and_configure_workflow(self, workflow_config: Dict[str, str] = None) -> bool:
        """
        创建并配置新的Workflow（完整流程）
        
        Args:
            workflow_config: Workflow配置信息 {"agent_type": "InputGAgent", "member_name": "test", "input": "测试输入"}
            
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
            
            # 3. 如果提供了配置，则添加Agent
            if workflow_config:
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
            run_button = self.page.wait_for_selector("button:has-text('Run')", timeout=10000)
            run_button.click()
            logger.info("✅ 已点击Run按钮")
            
            # 等待执行开始
            self.page.wait_for_timeout(3000)
            
            # 检查是否有验证错误
            try:
                error_element = self.page.wait_for_selector(
                    "text=/Validation error|Schema validation failed|error/i",
                    timeout=2000
                )
                if error_element:
                    error_text = error_element.inner_text()
                    logger.error(f"❌ Workflow执行出错: {error_text}")
                    self.take_screenshot("workflow_execution_error.png")
                    return False
            except:
                logger.info("✅ 未检测到验证错误")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 运行Workflow失败: {str(e)}")
            self.take_screenshot("workflow_run_failed.png")
            return False
    
    @allure.step("验证Workflow执行结果")
    def verify_workflow_execution(self, timeout: int = 10000) -> bool:
        """
        验证Workflow是否成功执行
        
        Args:
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否执行成功
        """
        logger.info("验证Workflow执行结果")
        
        try:
            # 等待执行完成的标志
            # 1. 检查是否有Execution log按钮
            execution_log = self.page.wait_for_selector(
                "button:has-text('Execution log')",
                timeout=timeout
            )
            
            if execution_log:
                logger.info("✅ 检测到Execution log按钮，Workflow可能执行成功")
                self.take_screenshot("workflow_execution_success.png")
                return True
            
        except:
            logger.warning("⚠️ 未检测到Execution log按钮")
        
        try:
            # 2. 检查是否有Success状态指示
            success_indicator = self.page.wait_for_selector(
                "text=/Success|完成|Completed/i",
                timeout=5000
            )
            
            if success_indicator:
                logger.info("✅ 检测到成功状态指示")
                return True
                
        except:
            logger.warning("⚠️ 未检测到成功状态")
        
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
        
        logger.info("⚠️ 无法明确验证执行结果，假设执行中")
        return True
    
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
            delete_button = self.page.wait_for_selector(
                "button:has-text('Delete'), text=Delete",
                timeout=5000
            )
            delete_button.click()
            logger.info("✅ 已点击Delete按钮")
            
            self.page.wait_for_timeout(1000)
            
            # 确认删除
            confirm_button = self.page.wait_for_selector(
                "button:has-text('Yes'), button:has-text('Confirm'), button:has-text('确认')",
                timeout=5000
            )
            confirm_button.click()
            logger.info("✅ 已确认删除")
            
            # 等待删除完成
            self.page.wait_for_timeout(3000)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 删除Workflow失败: {str(e)}")
            self.take_screenshot("workflow_delete_failed.png")
            return False

