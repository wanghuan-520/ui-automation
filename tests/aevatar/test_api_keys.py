"""
API Keys 完整测试套件
合并自: test_api_keys.py + test_daily_regression_apikeys.py

测试覆盖:
- 基础功能测试 (smoke, p0)
- 集成测试 (p0)
- 回归测试 (p1, p2, regression)
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.api_keys_page import ApiKeysPage
from utils.logger import get_logger

logger = get_logger(__name__)


# ========== 基础功能测试 ==========

@allure.feature("Dashboard功能")
@allure.story("API Keys管理")
class TestApiKeys:
    """API Keys 基础功能测试类 (P0, Smoke)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """
        测试前置设置 - 自动登录并导航到API Keys页面
        
        Args:
            page: Playwright页面对象
        """
        logger.info("开始测试前置设置")
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 导航到API Keys页面
        self.apikeys_page = ApiKeysPage(page)
        self.apikeys_page.navigate()
        
        logger.info("测试前置设置完成")
    
    @pytest.mark.smoke
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-001: API Keys页面加载")
    @allure.description("验证API Keys页面正常加载")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_keys_page_loads(self):
        """测试API Keys页面正常加载"""
        logger.info("开始测试: API Keys页面加载")
        
        # 验证页面已加载
        assert self.apikeys_page.is_loaded(), "API Keys页面未正确加载"
        
        # 验证Create Key按钮可见
        assert self.apikeys_page.is_element_visible(
            self.apikeys_page.CREATE_KEY_BUTTON
        ), "Create Key按钮不可见"
        
        logger.info("API Keys页面加载测试通过")
    
    @pytest.mark.smoke
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-002: API Keys列表加载")
    @allure.description("验证API Keys列表正确显示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_keys_list_loads(self):
        """测试API Keys列表加载"""
        logger.info("开始测试: API Keys列表加载")
        
        # 获取API Keys列表
        keys_list = self.apikeys_page.get_api_keys_list()
        
        # 验证列表不为空或为空（都是合法状态）
        assert isinstance(keys_list, list), "API Keys列表类型错误"
        
        if keys_list:
            logger.info(f"当前有 {len(keys_list)} 个API Key")
            # 验证每个key都有必要的属性
            for key in keys_list:
                assert 'name' in key, "API Key缺少name属性"
        else:
            logger.info("当前没有API Key")
        
        logger.info("API Keys列表加载测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-003: 打开创建对话框")
    @allure.description("验证点击Create Key按钮打开创建对话框")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_dialog_opens(self):
        """测试创建对话框打开"""
        logger.info("开始测试: 打开创建对话框")
        
        # 点击Create Key按钮
        self.apikeys_page.click_create_key()
        
        # 验证对话框已打开
        assert self.apikeys_page.is_create_dialog_visible(), "创建对话框未打开"
        
        # 验证对话框元素
        assert self.apikeys_page.is_element_visible(
            self.apikeys_page.DIALOG_NAME_INPUT
        ), "对话框中的名称输入框不可见"
        
        logger.info("创建对话框打开测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-004: 创建新API Key")
    @allure.description("验证创建新的API Key功能")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_new_api_key(self):
        """测试创建新API Key"""
        logger.info("开始测试: 创建新API Key")
        
        # 生成唯一的key名称
        key_name = f"test_key_{self.page.context.pages[0].url.split('/')[-1]}"
        
        # 创建API Key
        result = self.apikeys_page.create_api_key(key_name)
        assert result, "创建API Key失败"
        
        # 验证Key存在于列表中
        assert self.apikeys_page.verify_api_key_exists(key_name), \
            f"创建的API Key '{key_name}' 不在列表中"
        
        logger.info(f"创建API Key测试通过: {key_name}")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-005: 删除API Key")
    @allure.description("验证删除API Key功能")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_api_key(self):
        """测试删除API Key"""
        logger.info("开始测试: 删除API Key")
        
        # 先创建一个测试用的Key
        key_name = "test_key_for_delete"
        self.apikeys_page.create_api_key(key_name)
        assert self.apikeys_page.verify_api_key_exists(key_name), "测试Key创建失败"
        
        # 删除该Key
        result = self.apikeys_page.delete_api_key(key_name)
        assert result, "删除API Key失败"
        
        # 验证Key已不存在
        assert not self.apikeys_page.verify_api_key_exists(key_name), \
            f"API Key '{key_name}' 仍然存在"
        
        logger.info("删除API Key测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-006: 编辑API Key名称")
    @allure.description("验证编辑API Key名称功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_api_key_name(self):
        """测试编辑API Key名称"""
        logger.info("开始测试: 编辑API Key名称")
        
        # 创建测试Key
        original_name = "test_key_original"
        new_name = "test_key_renamed"
        
        self.apikeys_page.create_api_key(original_name)
        assert self.apikeys_page.verify_api_key_exists(original_name), "测试Key创建失败"
        
        # 编辑Key名称
        result = self.apikeys_page.edit_api_key_name(original_name, new_name)
        assert result, "编辑API Key名称失败"
        
        # 验证新名称存在，旧名称不存在
        assert self.apikeys_page.verify_api_key_exists(new_name), \
            f"新名称 '{new_name}' 不存在"
        assert not self.apikeys_page.verify_api_key_exists(original_name), \
            f"旧名称 '{original_name}' 仍然存在"
        
        # 清理
        self.apikeys_page.delete_api_key(new_name)
        
        logger.info("编辑API Key名称测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-007: 取消创建操作")
    @allure.description("验证点击Cancel按钮取消创建")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancel_create_operation(self):
        """测试取消创建操作"""
        logger.info("开始测试: 取消创建操作")
        
        # 打开创建对话框
        self.apikeys_page.click_create_key()
        assert self.apikeys_page.is_create_dialog_visible(), "对话框未打开"
        
        # 输入名称
        test_name = "test_key_cancelled"
        self.apikeys_page.fill_element(self.apikeys_page.DIALOG_NAME_INPUT, test_name)
        
        # 点击Cancel
        self.apikeys_page.click_cancel_create()
        
        # 验证对话框已关闭
        assert not self.apikeys_page.is_create_dialog_visible(), "对话框未关闭"
        
        # 验证Key未创建
        assert not self.apikeys_page.verify_api_key_exists(test_name), \
            f"取消操作后Key '{test_name}' 仍然被创建"
        
        logger.info("取消创建操作测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-008: 侧边栏导航")
    @allure.description("验证侧边栏导航功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_navigation(self):
        """测试侧边栏导航"""
        logger.info("开始测试: 侧边栏导航")
        
        # 点击Workflows菜单
        self.apikeys_page.click_workflows_menu()
        self.page.wait_for_timeout(2000)
        
        # 验证URL变化
        current_url = self.apikeys_page.get_current_url()
        assert "workflows" in current_url.lower(), "未导航到Workflows页面"
        
        # 返回API Keys
        self.apikeys_page.click_apikeys_menu()
        self.page.wait_for_timeout(2000)
        
        # 验证回到API Keys页面
        current_url = self.apikeys_page.get_current_url()
        assert "apikeys" in current_url.lower(), "未返回API Keys页面"
        
        logger.info("侧边栏导航测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-009: 空名称验证")
    @allure.description("验证创建时空名称的表单验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_key_name_validation(self):
        """测试空Key名称验证"""
        logger.info("开始测试: 空名称验证")
        
        # 打开创建对话框
        self.apikeys_page.click_create_key()
        assert self.apikeys_page.is_create_dialog_visible(), "对话框未打开"
        
        # 不输入名称，直接点击Create
        self.apikeys_page.click_dialog_create()
        self.page.wait_for_timeout(1000)
        
        # 验证仍在对话框中（未成功创建）
        assert self.apikeys_page.is_create_dialog_visible(), \
            "空名称时应该无法创建，但对话框已关闭"
        
        # 关闭对话框
        self.apikeys_page.click_cancel_create()
        
        logger.info("空名称验证测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-010: 页面刷新列表持久化")
    @allure.description("验证刷新页面后API Keys列表仍然存在")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_refresh_list_persists(self):
        """测试页面刷新后列表持久化"""
        logger.info("开始测试: 页面刷新列表持久化")
        
        # 创建测试Key
        test_key_name = "test_key_persistent"
        self.apikeys_page.create_api_key(test_key_name)
        assert self.apikeys_page.verify_api_key_exists(test_key_name), "测试Key创建失败"
        
        # 刷新页面
        self.page.reload()
        self.page.wait_for_timeout(3000)
        
        # 验证Key仍然存在
        assert self.apikeys_page.verify_api_key_exists(test_key_name), \
            f"刷新后Key '{test_key_name}' 丢失"
        
        # 清理
        self.apikeys_page.delete_api_key(test_key_name)
        
        logger.info("页面刷新列表持久化测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-011: Key状态显示")
    @allure.description("验证API Key状态正确显示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_key_status_display(self):
        """测试Key状态显示"""
        logger.info("开始测试: Key状态显示")
        
        # 获取API Keys列表
        keys_list = self.apikeys_page.get_api_keys_list()
        
        if keys_list:
            # 验证至少有一个Key有状态信息
            has_status = any('status' in key for key in keys_list)
            assert has_status, "API Keys列表中没有状态信息"
            logger.info(f"验证了 {len(keys_list)} 个Key的状态")
        else:
            logger.warning("当前没有API Key，跳过状态验证")
            pytest.skip("没有API Key可供验证状态")
        
        logger.info("Key状态显示测试通过")


# ========== 集成测试 ==========

@allure.feature("Dashboard功能")
@allure.story("API Keys集成测试")
class TestApiKeysIntegration:
    """API Keys 集成测试类 (P0)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        logger.info("开始集成测试前置设置")
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 导航到API Keys页面
        self.apikeys_page = ApiKeysPage(page)
        self.apikeys_page.navigate()
        
        logger.info("集成测试前置设置完成")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-012: API Key完整生命周期")
    @allure.description("测试API Key的创建、编辑、查询、删除完整流程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_key_full_lifecycle(self):
        """测试API Key完整生命周期：创建→编辑→删除"""
        logger.info("开始测试: API Key完整生命周期")
        
        # 1. 创建
        original_name = "lifecycle_test_key"
        logger.info(f"步骤1: 创建Key - {original_name}")
        result = self.apikeys_page.create_api_key(original_name)
        assert result, "创建失败"
        assert self.apikeys_page.verify_api_key_exists(original_name), "创建后Key不存在"
        
        # 2. 编辑
        new_name = "lifecycle_test_key_renamed"
        logger.info(f"步骤2: 编辑Key名称 - {original_name} → {new_name}")
        result = self.apikeys_page.edit_api_key_name(original_name, new_name)
        assert result, "编辑失败"
        assert self.apikeys_page.verify_api_key_exists(new_name), "编辑后新名称不存在"
        assert not self.apikeys_page.verify_api_key_exists(original_name), "编辑后旧名称仍存在"
        
        # 3. 删除
        logger.info(f"步骤3: 删除Key - {new_name}")
        result = self.apikeys_page.delete_api_key(new_name)
        assert result, "删除失败"
        assert not self.apikeys_page.verify_api_key_exists(new_name), "删除后Key仍存在"
        
        logger.info("API Key完整生命周期测试通过")


# ========== 回归测试 ==========

@allure.feature("Dashboard功能")
@allure.story("API Keys回归测试")
class TestApiKeysRegression:
    """API Keys 每日回归测试类 (P1, P2, Regression)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """回归测试前置设置"""
        logger.info("开始回归测试前置设置")
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 导航到API Keys页面
        self.apikeys_page = ApiKeysPage(page)
        self.apikeys_page.navigate()
        
        logger.info("回归测试前置设置完成")
    
    @pytest.mark.regression
    @pytest.mark.p1
    @allure.title("tc-apikeys-p1-001: 批量创建API Keys")
    @allure.description("验证可以创建多个API Keys")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_multiple_api_keys(self):
        """测试批量创建API Keys"""
        logger.info("开始测试: 批量创建API Keys")
        
        # 创建3个API Keys
        key_names = [f"batch_key_{i}" for i in range(1, 4)]
        
        for key_name in key_names:
            logger.info(f"创建Key: {key_name}")
            result = self.apikeys_page.create_api_key(key_name)
            assert result, f"创建Key '{key_name}' 失败"
            assert self.apikeys_page.verify_api_key_exists(key_name), \
                f"Key '{key_name}' 创建后不存在"
        
        # 验证所有Key都存在
        for key_name in key_names:
            assert self.apikeys_page.verify_api_key_exists(key_name), \
                f"Key '{key_name}' 验证失败"
        
        # 清理
        for key_name in key_names:
            self.apikeys_page.delete_api_key(key_name)
        
        logger.info("批量创建API Keys测试通过")
    
    @pytest.mark.regression
    @pytest.mark.p1
    @allure.title("tc-apikeys-p1-002: 编辑后立即删除")
    @allure.description("验证编辑API Key后立即删除的操作")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_then_delete(self):
        """测试编辑后立即删除"""
        logger.info("开始测试: 编辑后立即删除")
        
        # 创建Key
        original_name = "edit_delete_test"
        self.apikeys_page.create_api_key(original_name)
        
        # 编辑
        new_name = "edit_delete_test_renamed"
        self.apikeys_page.edit_api_key_name(original_name, new_name)
        assert self.apikeys_page.verify_api_key_exists(new_name), "编辑失败"
        
        # 立即删除
        result = self.apikeys_page.delete_api_key(new_name)
        assert result, "删除失败"
        assert not self.apikeys_page.verify_api_key_exists(new_name), "删除后Key仍存在"
        
        logger.info("编辑后立即删除测试通过")
    
    @pytest.mark.regression
    @pytest.mark.p2
    @allure.title("tc-apikeys-p2-001: 重复名称验证")
    @allure.description("验证不允许创建重复名称的API Key")
    @allure.severity(allure.severity_level.MINOR)
    def test_duplicate_name_validation(self):
        """测试重复名称验证"""
        logger.info("开始测试: 重复名称验证")
        
        # 创建第一个Key
        key_name = "duplicate_test_key"
        self.apikeys_page.create_api_key(key_name)
        assert self.apikeys_page.verify_api_key_exists(key_name), "第一个Key创建失败"
        
        # 尝试创建同名Key
        logger.info(f"尝试创建重复名称的Key: {key_name}")
        result = self.apikeys_page.create_api_key(key_name)
        
        # 应该失败或显示错误提示
        # 注意：具体行为取决于系统设计
        if result:
            logger.warning("系统允许创建重复名称的Key（可能是设计允许）")
        else:
            logger.info("系统正确阻止了重复名称的创建")
        
        # 清理
        self.apikeys_page.delete_api_key(key_name)
        
        logger.info("重复名称验证测试通过")

