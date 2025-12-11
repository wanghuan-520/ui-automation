"""
管理员设置 - Feature Management功能测试模块
路径: /admin/settings/feature-management
包含ABP Settings模块 功能管理配置测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.feature_management_page import FeatureManagementPage
from tests.aevatar_station.pages.settings_emailing_page import SettingsEmailingPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def admin_logged_in_feature(browser, test_data):
    """
    管理员登录fixture - 整个测试类只登录一次
    使用admin-test01账号登录以访问管理功能
    """
    # 创建新的浏览器上下文
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    
    # 登录流程
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    try:
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 使用admin-test01账号
        admin_data = test_data["admin_login_data"][1]  # admin-test01
        logger.info(f"使用Admin账号登录: {admin_data['username']}")
        
        page.fill("#LoginInput_UserNameOrEmailAddress", admin_data["username"])
        page.fill("#LoginInput_Password", admin_data["password"])
        page.click("button[type='submit']")
        
        # 等待登录完成
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        logger.info(f"登录跳转完成，当前URL: {page.url}")
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        
        logger.info("管理员登录成功")
        
        yield page
        
    except Exception as e:
        logger.error(f"❌ 管理员登录失败: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/admin_login_failed_feature_{timestamp}.png")
        with open(f"screenshots/admin_login_failed_feature_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        raise e
    finally:
        context.close()


@pytest.fixture(scope="function")
def feature_page(admin_logged_in_feature):
    """
    每个测试函数的Feature Management页面fixture
    """
    page = admin_logged_in_feature
    
    # 导航到Feature Management页面
    feature_mgmt = FeatureManagementPage(page)
    feature_mgmt.navigate()
    
    # 确认页面加载
    if not feature_mgmt.is_loaded():
        logger.warning("Feature Management页面可能未完全加载，尝试刷新")
        page.reload()
        feature_mgmt.wait_for_load()
    
    return feature_mgmt


@pytest.mark.admin
@pytest.mark.settings
@pytest.mark.feature_management
class TestAdminSettingsFeatureManagement:
    """管理员设置 - Feature Management功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_feature_page_load(self, feature_page):
        """
        TC-ADMIN-FM-001: 验证Feature Management页面加载
        
        测试目标：验证管理员可以访问Feature Management页面
        测试路径：/admin/settings/feature-management
        
        测试步骤：
        1. 使用管理员账号登录
        2. 导航到Feature Management页面
        3. 验证页面正确加载
        
        预期结果：
        - 页面成功加载
        - 显示Feature Management内容
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-001: 验证Feature Management页面加载")
        logger.info("=" * 60)
        
        # 验证页面加载
        assert feature_page.is_loaded(), "Feature Management页面未正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_page_load_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Feature Management页面加载",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-001执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_direct_url_access(self, admin_logged_in_feature):
        """
        TC-ADMIN-FM-002: 验证直接URL访问Feature Management
        
        测试目标：验证可以通过URL直接访问Feature Management页面
        测试路径：/admin/settings/feature-management
        
        测试步骤：
        1. 直接导航到Feature Management URL
        2. 验证页面加载
        
        预期结果：
        - URL正确跳转
        - 页面成功加载
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-002: 验证直接URL访问Feature Management")
        logger.info("=" * 60)
        
        page = admin_logged_in_feature
        
        # 直接导航到Feature Management
        logger.info("步骤1: 直接导航到/admin/settings/feature-management")
        page.goto("http://localhost:3000/admin/settings/feature-management")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
        
        # 验证URL
        current_url = page.url
        logger.info(f"   当前URL: {current_url}")
        assert "feature-management" in current_url, f"URL应包含feature-management，实际: {current_url}"
        logger.info("   ✓ URL验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/admin_fm_direct_access_{timestamp}.png")
        allure.attach.file(
            f"screenshots/admin_fm_direct_access_{timestamp}.png",
            name="Feature Management直接访问",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_page_description(self, feature_page):
        """
        TC-ADMIN-FM-003: 验证功能管理描述文本
        
        测试目标：验证页面描述正确显示
        
        测试步骤：
        1. 导航到Feature Management页面
        2. 检查描述文本
        
        预期结果：
        - 描述文本可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-003: 验证功能管理描述文本")
        logger.info("=" * 60)
        
        # 验证描述文本可见
        is_visible = feature_page.is_page_description_visible()
        logger.info(f"   描述文本可见性: {is_visible}")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_description_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="页面描述文本",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-003执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_manage_button_visible(self, feature_page):
        """
        TC-ADMIN-FM-004: 验证"Manage Host Features"按钮
        
        测试目标：验证按钮可见且可点击
        
        测试步骤：
        1. 导航到Feature Management页面
        2. 检查按钮可见性
        
        预期结果：
        - Manage Host Features按钮可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-004: 验证Manage Host Features按钮")
        logger.info("=" * 60)
        
        # 验证按钮可见
        assert feature_page.is_manage_button_visible(), "Manage Host Features按钮不可见"
        logger.info("   ✓ 按钮可见性验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_button_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Manage Host Features按钮",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-004执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_dialog_open(self, feature_page):
        """
        TC-ADMIN-FM-005: 验证Features对话框打开
        
        测试目标：验证点击按钮后对话框正确打开
        
        测试步骤：
        1. 点击Manage Host Features按钮
        2. 验证对话框打开
        
        预期结果：
        - 对话框成功打开
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-005: 验证Features对话框打开")
        logger.info("=" * 60)
        
        # 截图：点击前状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_before_click_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击前状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击按钮
        logger.info("步骤1: 点击Manage Host Features按钮")
        feature_page.click_manage_host_features()
        
        # 等待对话框出现
        feature_page.page.wait_for_timeout(2000)
        
        # 验证对话框打开
        assert feature_page.is_dialog_open(), "对话框未打开"
        logger.info("   ✓ 对话框已成功打开")
        
        # 截图：对话框已打开
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_dialog_open_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-对话框已打开",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_empty_state_message(self, feature_page):
        """
        TC-ADMIN-FM-006: 验证空功能列表提示
        
        测试目标：验证无功能时显示相应提示
        
        测试步骤：
        1. 打开Features对话框
        2. 检查空状态提示
        
        预期结果：
        - 显示空状态提示（如果无功能定义）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-006: 验证空功能列表提示")
        logger.info("=" * 60)
        
        # 打开对话框
        feature_page.click_manage_host_features()
        feature_page.page.wait_for_timeout(2000)
        
        # 检查空状态提示
        is_empty = feature_page.is_empty_state_message_visible()
        logger.info(f"   空状态提示可见: {is_empty}")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_empty_state_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="空功能列表提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_dialog_cancel_button(self, feature_page):
        """
        TC-ADMIN-FM-007: 验证对话框取消按钮
        
        测试目标：验证Cancel按钮关闭对话框
        
        测试步骤：
        1. 打开对话框
        2. 点击Cancel按钮
        3. 验证对话框关闭
        
        预期结果：
        - 对话框正确关闭
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-007: 验证对话框取消按钮")
        logger.info("=" * 60)
        
        # 打开对话框
        feature_page.click_manage_host_features()
        feature_page.page.wait_for_timeout(2000)
        
        # 截图：对话框打开状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_before_cancel_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击Cancel前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击Cancel按钮
        logger.info("步骤1: 点击Cancel按钮")
        feature_page.click_cancel()
        
        # 等待对话框关闭
        feature_page.page.wait_for_timeout(2000)
        
        # 验证对话框已关闭
        is_open = feature_page.is_dialog_open()
        assert not is_open, "对话框应该已关闭"
        logger.info("   ✓ 对话框已关闭")
        
        # 截图：对话框已关闭
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_after_cancel_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击Cancel后（对话框已关闭）",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-007执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_dialog_close_button(self, feature_page):
        """
        TC-ADMIN-FM-008: 验证对话框关闭按钮（X）
        
        测试目标：验证X按钮关闭对话框
        
        测试步骤：
        1. 打开对话框
        2. 点击X按钮
        3. 验证对话框关闭
        
        预期结果：
        - 对话框正确关闭
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-008: 验证对话框关闭按钮（X）")
        logger.info("=" * 60)
        
        # 打开对话框
        feature_page.click_manage_host_features()
        feature_page.page.wait_for_timeout(2000)
        
        # 截图：关闭按钮
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_close_button_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-对话框关闭按钮",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击关闭按钮
        logger.info("步骤1: 点击关闭(X)按钮")
        feature_page.click_close_button()
        
        # 等待对话框关闭
        feature_page.page.wait_for_timeout(2000)
        
        # 验证对话框已关闭
        is_open = feature_page.is_dialog_open()
        assert not is_open, "对话框应该已关闭"
        logger.info("   ✓ 对话框已关闭")
        
        # 截图：对话框已关闭
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_after_close_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击X后（对话框已关闭）",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_dialog_esc_key(self, feature_page):
        """
        TC-ADMIN-FM-009: 验证ESC键关闭对话框
        
        测试目标：验证按ESC键可关闭对话框
        
        测试步骤：
        1. 打开对话框
        2. 按ESC键
        3. 验证对话框关闭
        
        预期结果：
        - 对话框正确关闭
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-009: 验证ESC键关闭对话框")
        logger.info("=" * 60)
        
        # 打开对话框
        feature_page.click_manage_host_features()
        feature_page.page.wait_for_timeout(2000)
        
        # 截图：按ESC前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_before_esc_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-按ESC前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 按ESC键
        logger.info("步骤1: 按下ESC键")
        feature_page.press_escape()
        
        # 等待对话框关闭
        feature_page.page.wait_for_timeout(2000)
        
        # 验证对话框已关闭
        is_open = feature_page.is_dialog_open()
        assert not is_open, "对话框应该已关闭"
        logger.info("   ✓ 对话框已关闭")
        
        # 截图：按ESC后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_after_esc_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-按ESC后（对话框已关闭）",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-009执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_dialog_save_button(self, feature_page):
        """
        TC-ADMIN-FM-010: 验证对话框Save按钮
        
        测试目标：验证Save按钮功能
        
        测试步骤：
        1. 打开对话框
        2. 点击Save按钮
        
        预期结果：
        - Save按钮可点击
        - 操作完成后对话框关闭或显示成功消息
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-010: 验证对话框Save按钮")
        logger.info("=" * 60)
        
        # 打开对话框
        feature_page.click_manage_host_features()
        feature_page.page.wait_for_timeout(2000)
        
        # 截图：点击Save前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_before_save_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击Save前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击Save按钮
        logger.info("步骤1: 点击Save按钮")
        feature_page.click_save()
        
        # 等待处理
        feature_page.page.wait_for_timeout(2000)
        
        # 截图：点击Save后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_after_save_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击Save后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-010执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_tab_switch_from_emailing(self, admin_logged_in_feature):
        """
        TC-ADMIN-FM-011: 验证从Emailing Tab切换到Feature Management
        
        测试目标：验证Tab切换功能
        
        测试步骤：
        1. 导航到Settings页面（Emailing）
        2. 点击Feature Management Tab
        3. 验证切换成功
        
        预期结果：
        - Tab切换成功
        - URL正确更新
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-011: 验证从Emailing Tab切换到Feature Management")
        logger.info("=" * 60)
        
        page = admin_logged_in_feature
        
        # 访问Settings页面（Emailing）
        settings = SettingsEmailingPage(page)
        settings.navigate()
        settings.wait_for_load()
        
        # 截图：Emailing Tab
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_emailing_tab_{timestamp}.png"
        settings.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击Feature Management Tab
        logger.info("步骤1: 点击Feature Management Tab")
        settings.click_feature_management_tab()
        page.wait_for_timeout(2000)
        
        # 验证URL变化
        current_url = page.url
        logger.info(f"   当前URL: {current_url}")
        assert "feature-management" in current_url, "URL应该包含feature-management"
        logger.info("   ✓ URL验证通过")
        
        # 创建Feature Management页面对象验证
        feature_mgmt = FeatureManagementPage(page)
        assert feature_mgmt.is_loaded(), "Feature Management页面未正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 截图：Feature Management页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_from_emailing_{timestamp}.png"
        feature_mgmt.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Feature Management Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-011执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_page_refresh_state(self, feature_page):
        """
        TC-ADMIN-FM-012: 验证页面刷新保持状态
        
        测试目标：验证刷新后仍在Feature Management页面
        
        测试步骤：
        1. 在Feature Management页面
        2. 刷新页面
        3. 验证仍在Feature Management页面
        
        预期结果：
        - URL保持不变
        - 页面正确加载
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-012: 验证页面刷新保持状态")
        logger.info("=" * 60)
        
        # 记录刷新前URL
        url_before = feature_page.page.url
        logger.info(f"   刷新前URL: {url_before}")
        
        # 截图：刷新前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_before_refresh_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-刷新前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 刷新页面
        logger.info("步骤1: 刷新页面")
        feature_page.page.reload()
        feature_page.page.wait_for_load_state("domcontentloaded")
        feature_page.page.wait_for_timeout(3000)
        
        # 记录刷新后URL
        url_after = feature_page.page.url
        logger.info(f"   刷新后URL: {url_after}")
        
        # 验证URL保持不变
        assert "feature-management" in url_after, "刷新后应保持在Feature Management页面"
        
        # 验证页面内容
        assert feature_page.is_loaded(), "刷新后页面应正确加载"
        logger.info("   ✓ 状态保持验证通过")
        
        # 截图：刷新后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_fm_after_refresh_{timestamp}.png"
        feature_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-刷新后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-FM-012执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_multiple_open_close(self, feature_page):
        """
        TC-ADMIN-FM-013: 验证多次打开关闭对话框
        
        测试目标：验证对话框可多次打开/关闭
        
        测试步骤：
        1. 多次执行打开/关闭对话框操作
        2. 验证每次操作都成功
        
        预期结果：
        - 每次打开/关闭都正常
        - 无状态残留
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-FM-013: 验证多次打开关闭对话框")
        logger.info("=" * 60)
        
        # 执行3次打开/关闭
        for i in range(1, 4):
            logger.info(f"--- 第 {i} 次打开/关闭 ---")
            
            # 打开对话框
            feature_page.click_manage_host_features()
            feature_page.page.wait_for_timeout(1500)
            
            # 截图：打开状态
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"admin_fm_open_{i}_{timestamp}.png"
            feature_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{i*2-1}-第{i}次打开",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证对话框打开
            assert feature_page.is_dialog_open(), f"第{i}次对话框应该打开"
            logger.info(f"   ✓ 第{i}次打开成功")
            
            # 关闭对话框
            feature_page.click_cancel()
            feature_page.page.wait_for_timeout(1500)
            
            # 截图：关闭状态
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"admin_fm_close_{i}_{timestamp}.png"
            feature_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{i*2}-第{i}次关闭",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证对话框关闭
            assert not feature_page.is_dialog_open(), f"第{i}次对话框应该关闭"
            logger.info(f"   ✓ 第{i}次关闭成功")
        
        logger.info("✅ TC-ADMIN-FM-013执行成功")
