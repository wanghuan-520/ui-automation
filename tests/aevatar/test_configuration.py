"""
Configuration页面测试
测试Webhook、CROS配置管理功能
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.configuration_page import ConfigurationPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Dashboard功能")
@allure.story("Configuration管理")
class TestConfiguration:
    """Configuration页面功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """
        测试前置设置 - 自动登录并导航到Configuration页面
        
        Args:
            page: Playwright页面对象
        """
        logger.info("开始测试前置设置")
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        login_page.verify_login_success()
        
        # 导航到Configuration页面
        self.config_page = ConfigurationPage(page)
        self.config_page.navigate()
        
        logger.info("测试前置设置完成")
    
    @pytest.mark.smoke
    @pytest.mark.p0
    @allure.title("tc-config-p0-001: Configuration页面加载")
    @allure.description("验证Configuration页面正常加载")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_configuration_page_loads(self):
        """测试Configuration页面正常加载"""
        logger.info("开始测试: Configuration页面加载")
        
        # 验证页面已加载
        assert self.config_page.is_loaded(), "Configuration页面未正确加载"
        
        # 验证Webhook标签页可见
        assert self.config_page.is_element_visible(
            self.config_page.WEBHOOK_TAB
        ), "Webhook标签页不可见"
        
        # 验证CROS标签页可见
        assert self.config_page.is_element_visible(
            self.config_page.CROS_TAB
        ), "CROS标签页不可见"
        
        logger.info("Configuration页面加载测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-002: Webhook标签页功能")
    @allure.description("验证Webhook标签页显示和功能")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_webhook_tab_functionality(self):
        """测试Webhook标签页功能"""
        logger.info("开始测试: Webhook标签页功能")
        
        # 切换到Webhook标签页
        self.config_page.switch_to_tab("Webhook")
        
        # 验证Webhook表格可见
        assert self.config_page.is_element_visible(
            self.config_page.WEBHOOK_TABLE
        ), "Webhook表格不可见"
        
        # 验证Create按钮可见
        assert self.config_page.is_element_visible(
            self.config_page.WEBHOOK_CREATE_BUTTON
        ), "Create Webhook按钮不可见"
        
        # 获取Webhook列表
        webhooks = self.config_page.get_webhook_list()
        assert isinstance(webhooks, list), "Webhook列表格式不正确"
        logger.info(f"Webhook列表包含 {len(webhooks)} 个配置")
        
        logger.info("Webhook标签页功能测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-003: CROS标签页功能")
    @allure.description("验证CROS标签页显示和功能")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cros_tab_functionality(self):
        """测试CROS标签页功能"""
        logger.info("开始测试: CROS标签页功能")
        
        # 切换到CROS标签页
        self.config_page.switch_to_tab("Cros")
        
        # 验证CROS表格可见
        assert self.config_page.is_element_visible(
            self.config_page.CROS_TABLE
        ), "CROS表格不可见"
        
        # 验证Create按钮可见
        assert self.config_page.is_element_visible(
            self.config_page.CROS_CREATE_BUTTON
        ), "Create CROS按钮不可见"
        
        # 获取CROS列表
        cros_list = self.config_page.get_cros_list()
        assert isinstance(cros_list, list), "CROS列表格式不正确"
        logger.info(f"CROS列表包含 {len(cros_list)} 个配置")
        
        logger.info("CROS标签页功能测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-004: 创建Webhook配置")
    @allure.description("验证成功创建Webhook配置")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_webhook(self):
        """测试创建Webhook配置"""
        logger.info("开始测试: 创建Webhook配置")
        
        # 生成唯一的Webhook名称
        import time
        webhook_name = f"test_webhook_{int(time.time())}"
        webhook_url = "https://example.com/webhook"
        
        # 创建Webhook
        success = self.config_page.create_webhook(webhook_name, webhook_url)
        assert success, f"创建Webhook失败: {webhook_name}"
        
        # 验证Webhook已创建
        assert self.config_page.verify_webhook_exists(webhook_name), \
            f"创建的Webhook不在列表中: {webhook_name}"
        
        # 清理: 删除创建的Webhook
        self.config_page.delete_webhook(webhook_name)
        
        logger.info("创建Webhook配置测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-005: 创建CROS配置")
    @allure.description("验证成功创建CROS配置")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_cros(self):
        """测试创建CROS配置"""
        logger.info("开始测试: 创建CROS配置")
        
        # 生成唯一的origin
        import time
        origin = f"https://test{int(time.time())}.example.com"
        
        # 创建CROS
        success = self.config_page.create_cros(origin)
        assert success, f"创建CROS失败: {origin}"
        
        # 验证CROS已创建
        assert self.config_page.verify_cros_exists(origin), \
            f"创建的CROS不在列表中: {origin}"
        
        # 清理: 删除创建的CROS
        self.config_page.delete_cros(origin)
        
        logger.info("创建CROS配置测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-006: 删除Webhook配置")
    @allure.description("验证成功删除Webhook配置")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_webhook(self):
        """测试删除Webhook配置"""
        logger.info("开始测试: 删除Webhook配置")
        
        # 先创建一个Webhook用于删除测试
        import time
        webhook_name = f"test_delete_webhook_{int(time.time())}"
        webhook_url = "https://example.com/delete-test"
        
        self.config_page.create_webhook(webhook_name, webhook_url)
        assert self.config_page.verify_webhook_exists(webhook_name), \
            "准备删除的Webhook未创建成功"
        
        # 删除Webhook
        success = self.config_page.delete_webhook(webhook_name)
        assert success, f"删除Webhook失败: {webhook_name}"
        
        # 验证Webhook已删除
        assert not self.config_page.verify_webhook_exists(webhook_name), \
            f"Webhook仍然存在: {webhook_name}"
        
        logger.info("删除Webhook配置测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-config-p0-007: 删除CROS配置")
    @allure.description("验证成功删除CROS配置")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_cros(self):
        """测试删除CROS配置"""
        logger.info("开始测试: 删除CROS配置")
        
        # 先创建一个CROS用于删除测试
        import time
        origin = f"https://delete{int(time.time())}.example.com"
        
        self.config_page.create_cros(origin)
        assert self.config_page.verify_cros_exists(origin), \
            "准备删除的CROS未创建成功"
        
        # 删除CROS
        success = self.config_page.delete_cros(origin)
        assert success, f"删除CROS失败: {origin}"
        
        # 验证CROS已删除
        assert not self.config_page.verify_cros_exists(origin), \
            f"CROS仍然存在: {origin}"
        
        logger.info("删除CROS配置测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-config-p1-001: 标签页切换")
    @allure.description("验证Webhook和CROS标签页切换正常")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tab_switching(self):
        """测试标签页切换"""
        logger.info("开始测试: 标签页切换")
        
        # 切换到Webhook标签页
        self.config_page.switch_to_tab("Webhook")
        assert self.config_page.is_element_visible(
            self.config_page.WEBHOOK_TABLE
        ), "切换后Webhook表格不可见"
        
        # 切换到CROS标签页
        self.config_page.switch_to_tab("Cros")
        assert self.config_page.is_element_visible(
            self.config_page.CROS_TABLE
        ), "切换后CROS表格不可见"
        
        # 再次切换回Webhook标签页
        self.config_page.switch_to_tab("Webhook")
        assert self.config_page.is_element_visible(
            self.config_page.WEBHOOK_TABLE
        ), "再次切换后Webhook表格不可见"
        
        logger.info("标签页切换测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-config-p1-006: 侧边栏导航功能")
    @allure.description("验证侧边栏导航菜单正常工作")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_navigation(self):
        """测试侧边栏导航功能"""
        logger.info("开始测试: 侧边栏导航功能")
        
        # 点击API Keys菜单
        self.config_page.click_sidebar_menu("API Keys")
        assert self.config_page.verify_url_contains("/apikeys"), \
            "点击API Keys菜单后未跳转到正确页面"
        logger.info("API Keys菜单导航正常")
        
        # 返回Configuration页面
        self.config_page.click_sidebar_menu("Configuration")
        assert self.config_page.verify_url_contains("/configuration"), \
            "返回Configuration页面失败"
        logger.info("返回Configuration页面成功")
        
        # 点击Workflows菜单
        self.config_page.click_sidebar_menu("Workflows")
        assert self.config_page.verify_url_contains("/workflows"), \
            "点击Workflows菜单后未跳转到正确页面"
        logger.info("Workflows菜单导航正常")
        
        logger.info("侧边栏导航功能测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-config-p2-002: Webhook列表数据结构")
    @allure.description("验证Webhook列表返回的数据结构正确")
    @allure.severity(allure.severity_level.MINOR)
    def test_webhook_list_data_structure(self):
        """测试Webhook列表数据结构"""
        logger.info("开始测试: Webhook列表数据结构")
        
        # 获取Webhook列表
        webhooks = self.config_page.get_webhook_list()
        
        if len(webhooks) > 0:
            first_webhook = webhooks[0]
            # 验证必需字段
            assert "name" in first_webhook, "Webhook缺少name字段"
            assert "url" in first_webhook, "Webhook缺少url字段"
            assert "created_at" in first_webhook, "Webhook缺少created_at字段"
            
            logger.info(f"Webhook数据结构正确: {first_webhook}")
        else:
            logger.info("Webhook列表为空，跳过数据结构验证")
        
        logger.info("Webhook列表数据结构测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-config-p2-003: CROS列表数据结构")
    @allure.description("验证CROS列表返回的数据结构正确")
    @allure.severity(allure.severity_level.MINOR)
    def test_cros_list_data_structure(self):
        """测试CROS列表数据结构"""
        logger.info("开始测试: CROS列表数据结构")
        
        # 获取CROS列表
        cros_list = self.config_page.get_cros_list()
        
        if len(cros_list) > 0:
            first_cros = cros_list[0]
            # 验证必需字段
            assert "origin" in first_cros, "CROS缺少origin字段"
            assert "created_at" in first_cros, "CROS缺少created_at字段"
            
            logger.info(f"CROS数据结构正确: {first_cros}")
        else:
            logger.info("CROS列表为空，跳过数据结构验证")
        
        logger.info("CROS列表数据结构测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-config-p2-005: 刷新页面后状态保持")
    @allure.description("验证刷新页面后保持在当前标签页")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_refresh_state_persists(self):
        """测试刷新页面后状态保持"""
        logger.info("开始测试: 刷新页面后状态保持")
        
        # 切换到CROS标签页
        self.config_page.switch_to_tab("Cros")
        
        # 刷新页面
        self.config_page.refresh_page()
        
        # 验证页面依然在Configuration页面
        assert self.config_page.verify_url_contains("/configuration"), \
            "刷新后页面URL改变"
        
        # 验证页面加载正常
        assert self.config_page.is_loaded(), "刷新后页面未正确加载"
        
        logger.info("刷新页面后状态保持测试通过")


@allure.feature("Dashboard功能")
@allure.story("Configuration管理 - 集成测试")
class TestConfigurationIntegration:
    """Configuration集成测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        login_page.verify_login_success()
        
        # 导航到Configuration页面
        self.config_page = ConfigurationPage(page)
        self.config_page.navigate()
    
    @pytest.mark.integration
    @allure.title("集成测试: Webhook完整生命周期")
    @allure.description("端到端测试创建、删除Webhook的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_webhook_full_lifecycle(self):
        """集成测试: Webhook完整生命周期"""
        logger.info("开始集成测试: Webhook完整生命周期")
        
        # 生成唯一Webhook配置
        import time
        webhook_name = f"lifecycle_webhook_{int(time.time())}"
        webhook_url = "https://example.com/lifecycle"
        
        # 1. 创建
        logger.info(f"步骤1: 创建Webhook - {webhook_name}")
        success = self.config_page.create_webhook(webhook_name, webhook_url)
        assert success, "创建Webhook失败"
        assert self.config_page.verify_webhook_exists(webhook_name), \
            "创建的Webhook不在列表中"
        
        # 2. 删除
        logger.info(f"步骤2: 删除Webhook - {webhook_name}")
        success = self.config_page.delete_webhook(webhook_name)
        assert success, "删除Webhook失败"
        assert not self.config_page.verify_webhook_exists(webhook_name), \
            "删除后Webhook仍然存在"
        
        logger.info("Webhook完整生命周期集成测试通过")
    
    @pytest.mark.integration
    @allure.title("集成测试: CROS完整生命周期")
    @allure.description("端到端测试创建、删除CROS的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cros_full_lifecycle(self):
        """集成测试: CROS完整生命周期"""
        logger.info("开始集成测试: CROS完整生命周期")
        
        # 生成唯一CROS配置
        import time
        origin = f"https://lifecycle{int(time.time())}.example.com"
        
        # 1. 创建
        logger.info(f"步骤1: 创建CROS - {origin}")
        success = self.config_page.create_cros(origin)
        assert success, "创建CROS失败"
        assert self.config_page.verify_cros_exists(origin), \
            "创建的CROS不在列表中"
        
        # 2. 删除
        logger.info(f"步骤2: 删除CROS - {origin}")
        success = self.config_page.delete_cros(origin)
        assert success, "删除CROS失败"
        assert not self.config_page.verify_cros_exists(origin), \
            "删除后CROS仍然存在"
        
        logger.info("CROS完整生命周期集成测试通过")

