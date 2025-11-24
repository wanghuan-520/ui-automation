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
    @allure.title("E2E-P0: Workflow完整生命周期测试")
    @allure.description("端到端测试：创建 → 配置 → 连接 → 运行 → 验证 → 删除")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_workflow_full_lifecycle_e2e(self):
        """
        E2E测试: Workflow完整生命周期
        整合验证点：创建、Agent拖拽、连线、配置、运行、验证执行、删除
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: Workflow完整生命周期 [P0]")
        logger.info("=" * 80)
        
        # 定义Agent坐标 (确保间距足够，避免节点重叠遮挡Handle)
        # 之前失败原因：节点间距太小，导致目标节点遮挡了源节点的输出Handle
        input_pos = (400, 400) 
        chat_pos = (1000, 400)
        
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
        
        # 不再重命名，使用默认名称以提高稳定性
        logger.info("📍 步骤1.1: 使用默认工作流名称（untitled_workflow）")
        
        self.page_utils.screenshot_step("01-Workflow编辑器页面")
        logger.info("✅ Workflow创建页面已打开")
        
        # ✅ 验证点2: InputGAgent拖拽
        with allure.step("步骤2: 拖拽InputGAgent到画布"):
            logger.info(f"📍 步骤2: 拖拽InputGAgent到 {input_pos}")
            success = self.workflows_page.add_agent_to_canvas("InputGAgent", drop_x=input_pos[0], drop_y=input_pos[1])
            assert success, "InputGAgent拖拽到画布失败"
            
            # 增加等待，确保Agent渲染完成
            self.page.wait_for_timeout(2000)
            
            # 验证Agent是否真的在画布上
            agent_on_canvas = self.workflows_page.get_agent_on_canvas("InputGAgent")
            assert agent_on_canvas, "InputGAgent未在画布上找到"
            
            self.page_utils.screenshot_step("02-InputGAgent添加到画布")
            logger.info("✅ InputGAgent成功添加到画布")
        
        # ✅ 验证点3: InputGAgent参数配置
        with allure.step("步骤3: 配置InputGAgent参数"):
            logger.info("📍 步骤3: 配置InputGAgent参数")
            config = {
                "member_name": "e2e_test",
                "input": "中国美食推荐"
            }
            success = self.workflows_page.configure_agent(config)
            assert success, "InputGAgent参数配置失败"
            self.page_utils.screenshot_step("03-InputGAgent配置完成")
            logger.info("✅ InputGAgent配置完成")
        
        # ✅ 验证点4: ChatAIGAgent拖拽
        with allure.step("步骤4: 拖拽ChatAIGAgent到画布"):
            logger.info(f"📍 步骤4: 拖拽ChatAIGAgent到 {chat_pos}")
            success = self.workflows_page.add_agent_to_canvas("ChatAIGAgent", drop_x=chat_pos[0], drop_y=chat_pos[1])
            assert success, "ChatAIGAgent拖拽到画布失败"
            self.page_utils.screenshot_step("04-ChatAIGAgent添加到画布")
            
            # 如果出现配置弹窗，关闭它（这里只需连接，暂不配置）
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
            logger.info("✅ ChatAIGAgent添加完成")

        # ✅ 验证点5: 连接Agent
        with allure.step("步骤5: 连接InputGAgent和ChatAIGAgent"):
            logger.info("📍 步骤5: 连接InputGAgent -> ChatAIGAgent")
            
            # 获取连接前的连线数量
            edges_before = self.workflows_page.get_edge_count()
            logger.info(f"连接前连线数量: {edges_before}")
            
            # 使用名称进行连接，不再依赖硬编码坐标
            success = self.workflows_page.connect_agents("InputGAgent", "ChatAIGAgent")
            assert success, "Agent连接操作失败"
            
            # 验证连接是否真正成功（检查连线数量增加）
            self.page.wait_for_timeout(1000) # 等待连线渲染
            edges_after = self.workflows_page.get_edge_count()
            logger.info(f"连接后连线数量: {edges_after}")
            
            assert edges_after > edges_before, f"连接未创建成功! 连线数量未增加: {edges_before} -> {edges_after}"
            
            self.page_utils.screenshot_step("05-Agent已连接")
            logger.info("✅ Agent连接完成并验证通过")
        
        # ✅ 验证点6: 运行Workflow
        with allure.step("步骤6: 运行Workflow"):
            logger.info("📍 步骤6: 运行Workflow")
            
            # 在运行前点击Format Layout
            self.workflows_page.click_format_layout()
            self.page_utils.screenshot_step("06-1-FormatLayout完成")
            logger.info("✅ Format Layout布局整理完成")
            
            success = self.workflows_page.run_workflow()
            assert success, "Workflow运行失败"
            self.page_utils.screenshot_step("06-2-Workflow运行中")
            logger.info("✅ Workflow已触发运行")
        
        # ✅ 验证点7: 验证执行结果
        with allure.step("步骤7: 验证执行结果"):
            logger.info("📍 步骤7: 验证执行结果")
            # 增加超时时间到60秒，因为LLM处理可能较慢
            success = self.workflows_page.verify_workflow_execution(timeout=60000)
            assert success, "Workflow执行验证失败"
            self.page_utils.screenshot_step("07-Workflow执行完成")
            logger.info("✅ Workflow执行验证通过")
        
        # ✅ 验证点8: 返回列表页并删除刚创建的工作流
        with allure.step("步骤8: 删除刚创建的工作流并验证"):
            logger.info("📍 步骤8: 返回列表页")
            self.workflows_page.navigate()
            self.page.wait_for_timeout(2000)
            self.workflows_page.refresh_page()
            self.page.wait_for_timeout(2000)
            self.page_utils.screenshot_step("08-1-返回列表页")
            
            # 记录删除前的总数
            logger.info("📍 步骤8.1: 记录删除前工作流总数")
            workflows_before_delete = self.workflows_page.get_workflow_list()
            total_count_before = len(workflows_before_delete)
            logger.info(f"删除前工作流总数: {total_count_before}")
            self.page_utils.screenshot_step("08-2-删除前列表")
            
            # 执行删除
            logger.info("📍 步骤8.2: 删除第一个untitled_workflow")
            delete_success = self.workflows_page.delete_workflow("untitled_workflow")
            assert delete_success, "❌ 删除工作流操作失败"
            logger.info("✅ 删除操作执行完成")
            
            # 等待后端处理删除请求
            logger.info("⏳ 等待5秒让后端处理删除...")
            self.page.wait_for_timeout(5000)
            self.page_utils.screenshot_step("08-3-删除操作完成")
            
            # 刷新页面并验证删除结果
            logger.info("📍 步骤8.3: 刷新页面验证删除结果")
            self.workflows_page.refresh_page()
            logger.info("⏳ 等待页面刷新完成...")
            self.page.wait_for_timeout(3000)
            
            workflows_after_delete = self.workflows_page.get_workflow_list()
            total_count_after = len(workflows_after_delete)
            logger.info(f"刷新后工作流总数: {total_count_after}")
            
            self.page_utils.screenshot_step("08-4-删除后列表")
            
            # 强制断言：删除后数量必须减少
            assert total_count_after < total_count_before, \
                f"❌ 删除验证失败: 工作流总数未减少 (删除前:{total_count_before}, 删除后:{total_count_after})"
            
            logger.info(f"✅ 删除验证成功: 总数减少 {total_count_before} -> {total_count_after}")
            logger.info("✅ 删除功能验证完成")
        
        logger.info("=" * 80)
        logger.info("⚠️  注意: 删除功能存在已知问题")
        logger.info("   - 第二层弹窗的复选框无法通过自动化勾选")
        logger.info("   - 需要手动验证或等待UI组件修复")
        logger.info("   - 核心生命周期(创建→配置→运行→验证)已完成")
        logger.info("🎉 E2E测试完成: Workflow生命周期核心流程测试通过")
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
    @allure.description("端到端测试：验证Import功能 → 导入文件 → 验证导入成功 → 清理")
    @allure.severity(allure.severity_level.NORMAL)
    def test_import_workflow_e2e(self):
        """
        E2E测试: Import Workflow功能
        整合验证点：按钮可见性、文件上传、导入结果强制验证
        """
        logger.info("=" * 80)
        logger.info("🧪 开始E2E测试: Import Workflow功能 [P2]")
        logger.info("=" * 80)
        
        import os
        import json
        
        # ✅ 验证点1: 验证Import按钮可见
        logger.info("📍 验证点1: 验证Import按钮")
        assert self.workflows_page.is_element_visible(
            self.workflows_page.IMPORT_WORKFLOW_BUTTON
        ), "Import Workflow按钮不可见"
        self.page_utils.screenshot_step("01-1-Import按钮可见")
        logger.info("✅ Import按钮验证通过")
        
        # 准备测试文件
        file_path = os.path.abspath("test_data/workflow_import_template.json")
        assert os.path.exists(file_path), f"测试文件不存在: {file_path}"
        
        # 读取预期的workflow名称
        with open(file_path, 'r') as f:
            data = json.load(f)
            expected_name = data.get("name", "Auto_Imported_Workflow")
        logger.info(f"预期导入的workflow名称: {expected_name}")
        
        # ✅ 验证点2: 记录导入前状态
        logger.info("📍 验证点2: 记录导入前列表状态")
        initial_workflows = self.workflows_page.get_workflow_list()
        initial_count = len(initial_workflows)
        logger.info(f"导入前工作流数量: {initial_count}")
        self.page_utils.screenshot_step("01-2-导入前列表")
        
        # ✅ 验证点3: 执行导入操作
        logger.info("📍 验证点3: 点击Import按钮并选择文件")
        self.page_utils.screenshot_step("02-1-准备导入")
        
        import_success = self.workflows_page.import_workflow_from_file(file_path)
        assert import_success, "❌ 导入操作失败"
        
        self.page.wait_for_timeout(2000)
        self.page_utils.screenshot_step("02-2-导入操作执行完成")
        logger.info("✅ 导入操作执行成功")
        
        # ✅ 验证点4: 刷新并验证数量增加
        logger.info("📍 验证点4: 验证导入结果")
        self.workflows_page.refresh_page()
        self.page.wait_for_timeout(3000)
        
        current_workflows = self.workflows_page.get_workflow_list()
        current_count = len(current_workflows)
        logger.info(f"导入后工作流数量: {current_count}")
        self.page_utils.screenshot_step("03-1-导入后列表")
        
        # 强制断言：数量必须增加
        assert current_count > initial_count, \
            f"❌ 导入验证失败: 工作流数量未增加 ({initial_count} -> {current_count})"
        logger.info(f"✅ 数量验证通过: {initial_count} -> {current_count}")
        
        # ✅ 验证点5: 验证特定workflow存在
        logger.info(f"📍 验证点5: 验证workflow '{expected_name}' 存在")
        found = False
        imported_workflow_name = None
        
        for wf in current_workflows:
            if expected_name in wf["name"]:
                found = True
                imported_workflow_name = wf["name"]
                logger.info(f"✅ 找到导入的workflow: {imported_workflow_name}")
                break
        
        assert found, f"❌ 未在列表中找到导入的workflow: {expected_name}"
        self.page_utils.screenshot_step("03-2-导入验证成功")
        
        # ✅ 验证点6: 清理 - 删除导入的workflow
        logger.info("📍 验证点6: 清理导入的workflow")
        if found and imported_workflow_name:
            delete_success = self.workflows_page.delete_workflow(imported_workflow_name)
            assert delete_success, f"清理失败: 无法删除 {imported_workflow_name}"
            
            self.page.wait_for_timeout(2000)
            self.workflows_page.refresh_page()
            self.page.wait_for_timeout(2000)
            
            # 验证清理成功
            final_workflows = self.workflows_page.get_workflow_list()
            final_count = len(final_workflows)
            logger.info(f"清理后工作流数量: {final_count}")
            
            assert final_count == initial_count, \
                f"清理验证失败: 数量未恢复 (初始:{initial_count}, 当前:{final_count})"
            
            self.page_utils.screenshot_step("04-清理完成")
            logger.info("✅ 清理验证成功")
        
        logger.info("=" * 80)
        logger.info("🎉 E2E测试完成: Import Workflow功能验证通过")
        logger.info("=" * 80)

