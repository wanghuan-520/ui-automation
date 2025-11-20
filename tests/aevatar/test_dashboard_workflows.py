"""
Dashboard Workflows页面E2E测试
整合UI验证点到端到端测试流程中
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.dashboard_workflows_page import DashboardWorkflowsPage
from utils.logger import get_logger
from utils.page_utils import PageUtils

logger = get_logger(__name__)


@allure.feature("Dashboard功能")
@allure.story("工作流管理 - E2E测试")
class TestDashboardWorkflowsE2E:
    """Dashboard Workflows端到端测试类 - 整合所有UI验证点"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.page_utils = PageUtils(page)  # 初始化PageUtils用于截图
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        self.page_utils.screenshot_step("01-导航到登录页")
        
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        self.page_utils.screenshot_step("02-登录完成")
        
        # 初始化页面对象（登录后已经自动跳转到workflows页面，不需要再次navigate）
        self.workflows_page = DashboardWorkflowsPage(page)
        # 等待页面加载完成
        self.page.wait_for_timeout(2000)  # 等待跳转完成
        self.page_utils.screenshot_step("03-进入Workflows页面")
        
        logger.info("E2E测试前置设置完成")
    
    @pytest.mark.e2e
    @pytest.mark.p0
    @pytest.mark.smoke
    @allure.title("E2E-P0: 登录并浏览工作流列表")
    @allure.description("端到端测试：登录 → 验证跳转 → 加载列表 → 验证UI元素")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_and_browse_workflows_e2e(self):
        """
        E2E测试: 登录并浏览工作流列表
        核心验证点：登录跳转、列表加载、UI按钮元素
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: 登录并浏览工作流列表 [P0]")
        logger.info("=" * 80)
        
        # ✅ 验证点1: 登录后跳转到Workflows页面
        logger.info("📍 验证点1: 登录跳转")
        assert self.workflows_page.verify_url_contains("/dashboard/workflows"), \
            "登录后未跳转到Workflows页面"
        assert self.workflows_page.is_loaded(), "Workflows页面未正确加载"
        self.page_utils.screenshot_step("04-验证Workflows页面加载")
        logger.info("✅ 登录跳转验证通过")
        
        # ✅ 验证点2: 工作流列表加载
        logger.info("📍 验证点2: 工作流列表加载")
        workflows = self.workflows_page.get_workflow_list()
        assert isinstance(workflows, list), "工作流列表格式不正确"
        self.page_utils.screenshot_step("05-工作流列表展示")
        logger.info(f"✅ 工作流列表加载成功，包含 {len(workflows)} 个工作流")
        
        # ✅ 验证点3: 列表数据结构
        if len(workflows) > 0:
            logger.info("📍 验证点3: 列表数据结构")
            first_workflow = workflows[0]
            assert "name" in first_workflow, "工作流缺少name字段"
            assert "last_updated" in first_workflow, "工作流缺少last_updated字段"
            assert "status" in first_workflow, "工作流缺少status字段"
            logger.info(f"✅ 工作流数据结构验证通过: {first_workflow['name']}")
        
        # ✅ 验证点4: UI按钮元素
        logger.info("📍 验证点4: UI按钮元素")
        assert self.workflows_page.is_element_visible(
            self.workflows_page.NEW_WORKFLOW_BUTTON
        ), "New Workflow按钮不可见"
        assert self.workflows_page.is_element_visible(
            self.workflows_page.IMPORT_WORKFLOW_BUTTON
        ), "Import Workflow按钮不可见"
        self.page_utils.screenshot_step("06-UI按钮元素")
        logger.info("✅ UI按钮元素验证通过")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: 登录并浏览工作流列表测试通过")
        logger.info("=" * 80)
    
    @pytest.mark.e2e
    @pytest.mark.p0
    @allure.title("E2E-P0: 创建并运行Workflow完整流程")
    @allure.description("端到端测试：创建Workflow → 添加Agent → 配置参数 → 运行 → 验证结果")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_run_workflow_e2e(self):
        """
        E2E测试: 创建并运行Workflow完整流程
        整合验证点：按钮点击、Agent拖拽、配置弹窗、运行执行
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: 创建并运行Workflow [P0]")
        logger.info("=" * 80)
        
        # ✅ 验证点1: New Workflow按钮
        logger.info("📍 步骤1: 点击New Workflow按钮")
        assert self.workflows_page.is_element_visible(
            self.workflows_page.NEW_WORKFLOW_BUTTON
        ), "New Workflow按钮不可见"
        
        self.workflows_page.click_new_workflow()
        self.page.wait_for_timeout(2000)
        
        # 关闭AI弹窗
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(2000)
        self.page_utils.screenshot_step("01-Workflow编辑器页面")
        logger.info("✅ Workflow创建页面已打开")
        
        # ✅ 验证点2: Agent拖拽添加
        logger.info("📍 步骤2: 拖拽Agent到画布")
        success = self.workflows_page.add_agent_to_canvas("InputGAgent")
        assert success, "Agent拖拽到画布失败"
        self.page_utils.screenshot_step("02-Agent添加到画布")
        logger.info("✅ Agent成功添加到画布，配置弹窗已打开")
        
        # ✅ 验证点3: Agent参数配置
        logger.info("📍 步骤3: 配置Agent参数")
        config = {
            "member_name": "e2e_test",
            "input": "中国美食推荐"
        }
        success = self.workflows_page.configure_agent(config)
        assert success, "Agent参数配置失败"
        self.page_utils.screenshot_step("03-Agent配置完成")
        logger.info("✅ Agent配置完成")
        
        # ✅ 验证点4: 运行Workflow
        logger.info("📍 步骤4: 运行Workflow")
        success = self.workflows_page.run_workflow()
        assert success, "Workflow运行失败"
        self.page_utils.screenshot_step("04-Workflow运行中")
        logger.info("✅ Workflow已触发运行")
        
        # ✅ 验证点5: 验证执行结果
        logger.info("📍 步骤5: 验证执行结果")
        success = self.workflows_page.verify_workflow_execution(timeout=15000)
        assert success, "Workflow执行验证失败"
        self.page_utils.screenshot_step("05-Workflow执行完成")
        logger.info("✅ Workflow执行验证通过")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: 创建并运行Workflow流程测试通过")
        logger.info("=" * 80)
    
    @pytest.mark.e2e
    @pytest.mark.p1
    @allure.title("E2E-P1: Workflow列表数据持久化验证")
    @allure.description("端到端测试：验证列表加载 → 数据结构 → 页面刷新后数据保持")
    @allure.severity(allure.severity_level.NORMAL)
    def test_workflow_list_persistence_e2e(self):
        """
        E2E测试: Workflow列表数据持久化验证
        专注验证：列表加载、数据持久化、页面刷新
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: Workflow列表数据持久化 [P1]")
        logger.info("=" * 80)
        
        # ✅ 验证点1: 获取初始列表
        logger.info("📍 验证点1: 获取Workflow列表")
        workflows_before = self.workflows_page.get_workflow_list()
        assert isinstance(workflows_before, list), "工作流列表格式不正确"
        self.page_utils.screenshot_step("01-初始Workflows列表")
        logger.info(f"✅ 初始列表加载成功，包含 {len(workflows_before)} 个工作流")
        
        # ✅ 验证点2: 验证列表数据完整性
        if len(workflows_before) > 0:
            logger.info("📍 验证点2: 验证列表数据完整性")
            for i, workflow in enumerate(workflows_before[:3], 1):  # 验证前3个
                assert "name" in workflow, f"第{i}个工作流缺少name字段"
                assert "last_updated" in workflow, f"第{i}个工作流缺少last_updated字段"
                assert "status" in workflow, f"第{i}个工作流缺少status字段"
                logger.info(f"  ✓ 工作流{i}: {workflow['name']}")
            logger.info("✅ 列表数据完整性验证通过")
        
        # ✅ 验证点3: 页面刷新后数据持久化
        logger.info("📍 验证点3: 验证页面刷新后数据持久化")
        self.workflows_page.refresh_page()
        self.workflows_page.wait_for_page_load()
        self.page.wait_for_timeout(2000)
        
        workflows_after = self.workflows_page.get_workflow_list()
        assert isinstance(workflows_after, list), "刷新后无法获取工作流列表"
        self.page_utils.screenshot_step("02-刷新后Workflows列表")
        logger.info(f"✅ 刷新后列表加载成功，包含 {len(workflows_after)} 个工作流")
        
        # ✅ 验证点4: 验证数据数量一致性（允许±1的误差，因为可能有其他测试在并行运行）
        logger.info("📍 验证点4: 验证数据一致性")
        count_diff = abs(len(workflows_after) - len(workflows_before))
        assert count_diff <= 1, \
            f"刷新后工作流数量变化过大: {len(workflows_before)} → {len(workflows_after)}"
        logger.info("✅ 数据持久化验证通过")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: Workflow列表数据持久化验证通过")
        logger.info("=" * 80)
    
    @pytest.mark.e2e
    @pytest.mark.p2
    @allure.title("E2E-P2: Import Workflow功能验证")
    @allure.description("端到端测试：验证Import Workflow按钮和导入流程")
    @allure.severity(allure.severity_level.MINOR)
    def test_import_workflow_e2e(self):
        """
        E2E测试: Import Workflow功能
        整合验证点：按钮可见性、点击交互
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: Import Workflow功能 [P2]")
        logger.info("=" * 80)
        
        # ✅ 验证点1: 按钮可见
        logger.info("📍 验证点1: Import Workflow按钮")
        assert self.workflows_page.is_element_visible(
            self.workflows_page.IMPORT_WORKFLOW_BUTTON
        ), "Import Workflow按钮不可见"
        self.page_utils.screenshot_step("01-Import-Workflow按钮")
        
        # ✅ 验证点2: 点击功能
        logger.info("📍 验证点2: 点击Import按钮")
        self.workflows_page.click_import_workflow()
        self.page.wait_for_timeout(2000)
        self.page_utils.screenshot_step("02-点击Import后")
        logger.info("✅ Import Workflow按钮点击成功")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: Import Workflow功能验证通过")
        logger.info("=" * 80)
