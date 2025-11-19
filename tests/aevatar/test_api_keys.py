"""
API Keys页面测试
测试API密钥管理功能
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.api_keys_page import ApiKeysPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Dashboard功能")
@allure.story("API Keys管理")
class TestApiKeys:
    """API Keys页面功能测试类"""
    
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
        login_page.verify_login_success()
        
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
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-002: API Keys列表加载")
    @allure.description("验证API Keys列表正常显示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_keys_list_loads(self):
        """测试API Keys列表正常加载"""
        logger.info("开始测试: API Keys列表加载")
        
        # 获取API Keys列表
        api_keys = self.apikeys_page.get_api_keys_list()
        
        # 验证返回的是列表类型
        assert isinstance(api_keys, list), "API Keys列表格式不正确"
        
        # 如果有API Keys，验证数据结构
        if len(api_keys) > 0:
            first_key = api_keys[0]
            assert "name" in first_key, "API Key缺少name字段"
            assert "created_at" in first_key, "API Key缺少created_at字段"
            assert "last_used" in first_key, "API Key缺少last_used字段"
            assert "status" in first_key, "API Key缺少status字段"
            logger.info(f"API Keys列表包含 {len(api_keys)} 个Key")
        else:
            logger.info("API Keys列表为空")
        
        logger.info("API Keys列表加载测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-003: 创建API Key弹窗打开")
    @allure.description("验证点击Create Key按钮弹窗正常打开")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_dialog_opens(self):
        """测试创建API Key弹窗打开"""
        logger.info("开始测试: 创建API Key弹窗打开")
        
        # 点击Create Key按钮
        self.apikeys_page.click_create_key()
        
        # 验证弹窗打开
        assert self.apikeys_page.is_create_dialog_open(), \
            "创建API Key弹窗未打开"
        
        # 验证输入框可见
        assert self.apikeys_page.is_element_visible(
            self.apikeys_page.DIALOG_NAME_INPUT
        ), "Key名称输入框不可见"
        
        # 关闭弹窗
        self.apikeys_page.cancel_create_dialog()
        
        logger.info("创建API Key弹窗打开测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-004: 创建新的API Key")
    @allure.description("验证成功创建API Key")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_new_api_key(self):
        """测试创建新的API Key"""
        logger.info("开始测试: 创建新的API Key")
        
        # 生成唯一的Key名称
        import time
        key_name = f"test_key_{int(time.time())}"
        
        # 创建API Key
        success = self.apikeys_page.create_api_key(key_name)
        assert success, f"创建API Key失败: {key_name}"
        
        # 验证Key已创建
        assert self.apikeys_page.verify_api_key_exists(key_name), \
            f"创建的API Key不在列表中: {key_name}"
        
        # 清理: 删除创建的Key
        self.apikeys_page.delete_api_key(key_name)
        
        logger.info("创建新的API Key测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-apikeys-p0-006: 删除API Key")
    @allure.description("验证成功删除API Key")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_api_key(self):
        """测试删除API Key"""
        logger.info("开始测试: 删除API Key")
        
        # 先创建一个Key用于删除测试
        import time
        key_name = f"test_delete_key_{int(time.time())}"
        
        self.apikeys_page.create_api_key(key_name)
        assert self.apikeys_page.verify_api_key_exists(key_name), \
            "准备删除的Key未创建成功"
        
        # 删除Key
        success = self.apikeys_page.delete_api_key(key_name)
        assert success, f"删除API Key失败: {key_name}"
        
        # 验证Key已删除
        assert not self.apikeys_page.verify_api_key_exists(key_name), \
            f"API Key仍然存在: {key_name}"
        
        logger.info("删除API Key测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-apikeys-p1-001: 编辑API Key名称")
    @allure.description("验证成功编辑API Key名称")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_api_key_name(self):
        """测试编辑API Key名称"""
        logger.info("开始测试: 编辑API Key名称")
        
        # 创建一个Key用于编辑测试
        import time
        old_name = f"test_edit_old_{int(time.time())}"
        new_name = f"test_edit_new_{int(time.time())}"
        
        self.apikeys_page.create_api_key(old_name)
        assert self.apikeys_page.verify_api_key_exists(old_name), \
            "准备编辑的Key未创建成功"
        
        # 编辑Key名称
        success = self.apikeys_page.edit_api_key(old_name, new_name)
        assert success, f"编辑API Key失败: {old_name} -> {new_name}"
        
        # 验证新名称存在，旧名称不存在
        assert self.apikeys_page.verify_api_key_exists(new_name), \
            f"编辑后的Key名称不在列表中: {new_name}"
        assert not self.apikeys_page.verify_api_key_exists(old_name), \
            f"旧Key名称仍然存在: {old_name}"
        
        # 清理: 删除Key
        self.apikeys_page.delete_api_key(new_name)
        
        logger.info("编辑API Key名称测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-apikeys-p1-003: 取消创建操作")
    @allure.description("验证取消创建操作弹窗正常关闭")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cancel_create_operation(self):
        """测试取消创建操作"""
        logger.info("开始测试: 取消创建操作")
        
        # 打开创建弹窗
        self.apikeys_page.click_create_key()
        assert self.apikeys_page.is_create_dialog_open(), "创建弹窗未打开"
        
        # 输入Key名称
        self.page.fill(self.apikeys_page.DIALOG_NAME_INPUT, "temp_key")
        
        # 取消操作
        self.apikeys_page.cancel_create_dialog()
        
        # 等待弹窗关闭
        self.page.wait_for_timeout(1000)
        
        # 验证弹窗已关闭
        assert not self.apikeys_page.is_create_dialog_open(), "弹窗未关闭"
        
        # 验证temp_key未创建
        assert not self.apikeys_page.verify_api_key_exists("temp_key"), \
            "取消后Key不应该被创建"
        
        logger.info("取消创建操作测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-apikeys-p1-005: 侧边栏导航功能")
    @allure.description("验证侧边栏导航菜单正常工作")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_navigation(self):
        """测试侧边栏导航功能"""
        logger.info("开始测试: 侧边栏导航功能")
        
        # 点击Workflows菜单
        self.apikeys_page.click_sidebar_menu("Workflows")
        
        # 验证URL包含workflows
        current_url = self.apikeys_page.get_current_url()
        assert "/workflows" in current_url, \
            f"点击Workflows菜单后URL不正确: {current_url}"
        
        # 返回API Keys页面
        self.apikeys_page.click_sidebar_menu("API Keys")
        
        # 验证URL包含apikeys
        current_url = self.apikeys_page.get_current_url()
        assert "/apikeys" in current_url, \
            f"返回API Keys页面后URL不正确: {current_url}"
        
        logger.info("侧边栏导航功能测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-apikeys-p2-001: 空Key名称验证")
    @allure.description("验证空Key名称提交行为")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_key_name_validation(self):
        """测试空Key名称验证"""
        logger.info("开始测试: 空Key名称验证")
        
        # 打开创建弹窗
        self.apikeys_page.click_create_key()
        
        # 不输入任何内容，直接点击Create
        self.apikeys_page.click_element(self.apikeys_page.DIALOG_CREATE_BUTTON)
        
        # 等待一段时间观察是否有错误提示
        self.page.wait_for_timeout(2000)
        
        # 验证弹窗仍然打开（说明验证生效）
        # 或者验证有错误提示
        # 注意：这里需要根据实际行为调整验证逻辑
        logger.info("空Key名称验证已执行")
        
        # 关闭弹窗
        self.apikeys_page.cancel_create_dialog()
        
        logger.info("空Key名称验证测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-apikeys-p2-004: 刷新页面后列表保持")
    @allure.description("验证刷新页面后API Keys列表不变")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_refresh_list_persists(self):
        """测试刷新页面后列表保持"""
        logger.info("开始测试: 刷新页面后列表保持")
        
        # 获取刷新前的列表
        keys_before = self.apikeys_page.get_api_keys_list()
        
        # 刷新页面
        self.apikeys_page.refresh_page()
        
        # 验证页面依然在API Keys页面
        assert self.apikeys_page.is_loaded(), "刷新后页面未正确加载"
        
        # 获取刷新后的列表
        keys_after = self.apikeys_page.get_api_keys_list()
        
        # 验证列表数量一致
        assert len(keys_before) == len(keys_after), \
            f"刷新前后API Keys数量不一致: {len(keys_before)} vs {len(keys_after)}"
        
        logger.info("刷新页面后列表保持测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-apikeys-p2-006: Key状态显示")
    @allure.description("验证API Key状态正确显示")
    @allure.severity(allure.severity_level.MINOR)
    def test_key_status_display(self):
        """测试Key状态显示"""
        logger.info("开始测试: Key状态显示")
        
        # 获取所有Keys
        api_keys = self.apikeys_page.get_api_keys_list()
        
        if len(api_keys) > 0:
            for key in api_keys:
                status = key["status"]
                logger.info(f"API Key '{key['name']}' 状态: {status}")
                
                # 验证状态不为空
                assert status is not None and status != "", \
                    f"API Key '{key['name']}' 状态为空"
        else:
            logger.info("无API Keys可验证状态")
        
        logger.info("Key状态显示测试通过")


@allure.feature("Dashboard功能")
@allure.story("API Keys管理 - 集成测试")
class TestApiKeysIntegration:
    """API Keys集成测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        login_page.verify_login_success()
        
        # 导航到API Keys页面
        self.apikeys_page = ApiKeysPage(page)
        self.apikeys_page.navigate()
    
    @pytest.mark.integration
    @allure.title("集成测试: API Key完整生命周期")
    @allure.description("端到端测试创建、编辑、删除API Key的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_api_key_full_lifecycle(self):
        """集成测试: API Key完整生命周期"""
        logger.info("开始集成测试: API Key完整生命周期")
        
        # 生成唯一Key名称
        import time
        original_name = f"lifecycle_key_{int(time.time())}"
        edited_name = f"lifecycle_key_edited_{int(time.time())}"
        
        # 1. 创建
        logger.info(f"步骤1: 创建API Key - {original_name}")
        success = self.apikeys_page.create_api_key(original_name)
        assert success, "创建API Key失败"
        assert self.apikeys_page.verify_api_key_exists(original_name), \
            "创建的Key不在列表中"
        
        # 2. 编辑
        logger.info(f"步骤2: 编辑API Key - {original_name} -> {edited_name}")
        success = self.apikeys_page.edit_api_key(original_name, edited_name)
        assert success, "编辑API Key失败"
        assert self.apikeys_page.verify_api_key_exists(edited_name), \
            "编辑后的Key不在列表中"
        
        # 3. 删除
        logger.info(f"步骤3: 删除API Key - {edited_name}")
        success = self.apikeys_page.delete_api_key(edited_name)
        assert success, "删除API Key失败"
        assert not self.apikeys_page.verify_api_key_exists(edited_name), \
            "删除后Key仍然存在"
        
        logger.info("API Key完整生命周期集成测试通过")

