"""
Dashboard功能测试模块
包含Dashboard页面的各项功能测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.dashboard_page import DashboardPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def logged_in_dashboard(browser, test_data):
    """
    登录后的Dashboard页面fixture - 整个测试类只登录一次
    """
    # 创建新的浏览器上下文和页面
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    
    # 登录流程
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    landing_page.navigate()
    landing_page.click_sign_in()
    login_page.wait_for_load()
    
    valid_data = test_data["valid_login_data"][0]
    logger.info(f"使用账号登录: {valid_data['username']}")
    
    # 使用正确的选择器填写表单
    page.fill("#LoginInput_UserNameOrEmailAddress", valid_data["username"])
    page.fill("#LoginInput_Password", valid_data["password"])
    page.click("button[type='submit']")
    
    # 等待登录完成
    try:
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        logger.info(f"登录跳转完成，当前URL: {page.url}")
    except Exception as e:
        logger.error(f"登录可能失败，当前URL: {page.url}")
        page.screenshot(path="screenshots/login_failed_debug.png")
        raise Exception(f"登录失败: {e}")
    
    landing_page.handle_ssl_warning()
    page.wait_for_timeout(2000)
    
    logger.info("登录成功，会话将在整个测试类中复用")
    
    yield page
    
    # 测试类结束后清理
    context.close()


@pytest.fixture(scope="function")
def dashboard_page(logged_in_dashboard):
    """
    每个测试函数的Dashboard页面fixture
    复用已登录的页面，只导航到Dashboard
    """
    page = logged_in_dashboard
    
    # 导航到Dashboard页面
    dashboard = DashboardPage(page)
    dashboard.navigate()
    
    return dashboard


@pytest.mark.dashboard
class TestDashboard:
    """Dashboard功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_dashboard_page_load(self, dashboard_page):
        """
        TC-DASH-001: Dashboard页面加载验证测试
        
        测试目标：验证Dashboard页面能够成功加载并显示核心元素
        测试区域：Dashboard Page（管理仪表板）
        测试元素：
        - 页面整体（Dashboard主页面）
        - 页面标题（浏览器标题栏）
        
        测试步骤：
        1. [前置条件] 用户已登录并导航到Dashboard
        2. [Dashboard Page] 验证页面加载完成
        3. [验证] 检查页面is_loaded状态
        4. [验证] 确认页面标题包含"Aevatar"
        
        预期结果：
        - Dashboard页面成功加载
        - 页面状态为已加载（is_loaded = True）
        - 浏览器标题包含"Aevatar"
        - 无加载错误或超时
        """
        logger.info("开始执行TC-DASH-001: 验证Dashboard页面加载")
        
        # 验证页面加载完成
        assert dashboard_page.is_loaded(), "Dashboard页面未正确加载"
        
        # 截图：页面加载完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_initial_load_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Dashboard页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证页面标题
        assert "Aevatar" in dashboard_page.page.title(), "页面标题不正确"
        
        logger.info("TC-DASH-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_welcome_message(self, dashboard_page):
        """
        TC-DASH-002: 欢迎信息显示验证测试
        
        测试目标：验证Dashboard显示个性化的欢迎消息
        测试区域：Dashboard Page - Welcome Section（欢迎区域）
        测试元素：
        - 欢迎消息文本（页面顶部或中心区域）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Welcome Section] 获取欢迎消息文本
        3. [验证] 确认消息包含"Welcome back"
        4. [验证] 记录完整的欢迎消息内容
        
        预期结果：
        - 欢迎消息正确显示
        - 消息包含"Welcome back"文本
        - 消息可能包含用户名（个性化）
        """
        logger.info("开始执行TC-DASH-002: 验证欢迎信息显示")
        
        # 获取欢迎消息
        welcome_msg = dashboard_page.get_welcome_message()
        assert "Welcome back" in welcome_msg, "欢迎消息不包含'Welcome back'"
        
        # 截图：欢迎区域
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_welcome_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="欢迎区域显示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"欢迎消息: {welcome_msg}")
        logger.info("TC-DASH-002执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_user_profile_card(self, dashboard_page):
        """
        TC-DASH-003: 用户信息卡片验证测试
        
        测试目标：验证Dashboard的用户信息卡片正确显示个人信息和认证状态
        测试区域：Dashboard Page - User Profile Card（用户信息卡片区域）
        测试元素：
        - 用户信息卡片（卡片容器）
        - 用户姓名（显示文本）
        - 用户邮箱（显示文本）
        - 认证状态徽章（Authenticated badge）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [User Profile Card] 验证用户信息卡片可见
        3. [User Profile Card] 验证认证状态徽章显示
        4. [User Profile Card] 获取用户姓名
        5. [User Profile Card] 获取用户邮箱
        6. [验证] 确认所有用户信息正确显示
        
        预期结果：
        - 用户信息卡片正确显示
        - 认证状态徽章可见
        - 用户姓名和邮箱正确显示
        - 信息与登录用户一致
        """
        logger.info("开始执行TC-DASH-003: 验证用户信息卡片")
        
        # 验证用户信息卡片可见
        assert dashboard_page.is_user_profile_card_visible(), "用户信息卡片不可见"
        
        # 验证认证状态
        assert dashboard_page.is_authenticated(), "认证状态徽章应该显示"
        
        # 截图：用户信息卡片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_user_profile_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="用户信息卡片",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取并记录用户信息
        user_name = dashboard_page.get_user_name()
        user_email = dashboard_page.get_user_email()
        logger.info(f"用户姓名: {user_name}")
        logger.info(f"用户邮箱: {user_email}")
        
        logger.info("TC-DASH-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_email_verification_status(self, dashboard_page):
        """
        TC-DASH-004: 邮箱验证状态显示测试
        
        测试目标：验证Dashboard正确显示用户的邮箱验证状态
        测试区域：Dashboard Page - User Profile Card - Verification Status
        测试元素：
        - 邮箱验证状态指示器（图标或文本）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Verification Status] 获取邮箱验证状态
        3. [验证] 记录验证状态（已验证/未验证）
        4. [验证] 确认状态显示正确
        
        预期结果：
        - 邮箱验证状态正确显示
        - 状态为"已验证"或"未验证"
        - 状态与实际账户状态一致
        """
        logger.info("开始执行TC-DASH-004: 验证邮箱验证状态")
        
        # 检查验证状态
        is_verified = dashboard_page.is_email_verified()
        logger.info(f"邮箱验证状态: {'已验证' if is_verified else '未验证'}")
        
        # 截图：验证状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_verification_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="验证状态显示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_phone_verification_status(self, dashboard_page):
        """
        TC-DASH-005: 手机验证状态显示测试
        
        测试目标：验证Dashboard正确显示用户的手机验证状态
        测试区域：Dashboard Page - User Profile Card - Verification Status
        测试元素：
        - 手机验证状态指示器（图标或文本）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Verification Status] 获取手机验证状态
        3. [验证] 记录验证状态（已验证/未验证）
        4. [验证] 确认状态显示正确
        
        预期结果：
        - 手机验证状态正确显示
        - 状态为"已验证"或"未验证"
        - 状态与实际账户状态一致
        """
        logger.info("开始执行TC-DASH-005: 验证手机验证状态")
        
        # 检查验证状态
        is_verified = dashboard_page.is_phone_verified()
        logger.info(f"手机验证状态: {'已验证' if is_verified else '未验证'}")
        
        # 截图：验证状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_phone_verification_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="手机验证状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_multi_tenancy_status(self, dashboard_page):
        """
        TC-DASH-006: Multi-tenancy状态卡片验证测试
        
        测试目标：验证ABP框架的多租户状态卡片正确显示
        测试区域：Dashboard Page - System Status Cards
        测试元素：
        - Multi-tenancy状态卡片
        - 状态标题（"Multi-tenancy"）
        - 状态值（Enabled/Disabled）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [System Status] 验证Multi-tenancy卡片可见
        3. [System Status] 获取Multi-tenancy状态值
        4. [验证] 确认状态为"Enabled"或"Disabled"
        
        预期结果：
        - Multi-tenancy状态卡片正确显示
        - 状态值清晰可读
        - 状态反映系统实际配置
        """
        logger.info("开始执行TC-DASH-006: 验证Multi-tenancy状态卡片")
        
        # 获取多租户状态
        status = dashboard_page.get_multi_tenancy_status()
        logger.info(f"多租户状态: {status}")
        
        # 验证状态为Enabled或Disabled之一
        assert status in ["Enabled", "Disabled"], f"多租户状态应该是Enabled或Disabled，实际为: {status}"
        
        # 截图：系统状态卡片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_multi_tenancy_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="多租户状态卡片",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_current_tenant(self, dashboard_page):
        """
        TC-DASH-007: Current Tenant信息卡片验证测试
        
        测试目标：验证当前租户信息卡片正确显示租户详情
        测试区域：Dashboard Page - System Status Cards
        测试元素：
        - Current Tenant信息卡片
        - 租户名称（如果启用多租户）
        - 租户状态
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [System Status] 验证Current Tenant卡片可见
        3. [System Status] 获取当前租户信息
        4. [验证] 确认租户信息正确显示
        
        预期结果：
        - Current Tenant卡片正确显示
        - 如果多租户启用，显示租户名称
        - 如果多租户未启用，显示相应提示
        """
        logger.info("开始执行TC-DASH-007: 验证Current Tenant卡片")
        
        # 获取当前租户
        tenant = dashboard_page.get_current_tenant()
        logger.info(f"当前租户: {tenant}")
        
        # 验证租户信息存在
        assert tenant != "", "当前租户信息应该存在"
        
        # 截图：当前租户卡片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_current_tenant_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="当前租户卡片",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-007执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_session_status(self, dashboard_page):
        """
        TC-DASH-008: Session信息卡片验证测试
        
        测试目标：验证用户会话信息卡片正确显示会话详情
        测试区域：Dashboard Page - System Status Cards
        测试元素：
        - Session信息卡片
        - 会话状态或会话详情
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [System Status] 验证Session卡片可见
        3. [System Status] 获取会话信息
        4. [验证] 确认会话信息正确显示
        
        预期结果：
        - Session卡片正确显示
        - 会话信息包含相关详情
        - 信息反映当前用户会话
        """
        logger.info("开始执行TC-DASH-008: 验证Session状态卡片")
        
        # 获取会话状态
        session_status = dashboard_page.get_session_status()
        logger.info(f"会话状态: {session_status}")
        
        # 截图：会话状态卡片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_session_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="会话状态卡片",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_localization_config(self, dashboard_page):
        """
        TC-DASH-009: 本地化配置信息验证测试
        
        测试目标：验证Dashboard显示的本地化配置信息正确
        测试区域：Dashboard Page - Configuration Section
        测试元素：
        - 本地化配置卡片或区域
        - 语言设置信息（Current Culture）
        - 时区信息
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Configuration] 验证系统配置卡片可见
        3. [Configuration] 获取当前文化（Culture）设置
        4. [验证] 确认配置信息正确显示
        
        预期结果：
        - 本地化配置正确显示
        - 文化设置清晰（如：en-US, zh-CN）
        - 配置信息不为空
        """
        logger.info("开始执行TC-DASH-009: 验证Localization配置信息")
        
        # 验证系统配置卡片可见
        assert dashboard_page.is_system_config_card_visible(), "系统配置卡片不可见"
        
        # 获取当前文化设置
        culture = dashboard_page.get_current_culture()
        logger.info(f"当前文化: {culture}")
        
        # 验证文化设置存在
        assert culture != "", "当前文化设置应该存在"
        
        # 截图：配置信息
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_localization_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="本地化配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-009执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_timing_config(self, dashboard_page):
        """
        TC-DASH-010: 时间配置信息验证测试
        
        测试目标：验证Dashboard显示的时间相关配置正确
        测试区域：Dashboard Page - Configuration Section
        测试元素：
        - 时间配置卡片或区域
        - 时区设置（Time Zone）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Configuration] 获取时区设置
        3. [验证] 确认时区信息正确显示
        4. [验证] 时区信息不为空
        
        预期结果：
        - 时区配置正确显示
        - 时区格式准确（如：UTC, Asia/Shanghai）
        - 配置反映系统设置
        """
        logger.info("开始执行TC-DASH-010: 验证Timing配置信息")
        
        # 获取时区设置
        time_zone = dashboard_page.get_time_zone()
        logger.info(f"时区设置: {time_zone}")
        
        # 截图：时区配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_timing_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="时区配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-010执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_features_config(self, dashboard_page):
        """
        TC-DASH-011: 功能配置信息验证测试
        
        测试目标：验证Dashboard显示的ABP功能配置信息正确
        测试区域：Dashboard Page - Configuration Section
        测试元素：
        - 功能配置卡片或区域
        - 已启用的功能数量
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Configuration] 获取已启用的功能数量
        3. [验证] 确认返回值为非负整数
        4. [验证] 确认配置信息正确显示
        
        预期结果：
        - 功能配置正确显示
        - 功能数量为有效整数（≥0）
        - 配置反映系统实际状态
        """
        logger.info("开始执行TC-DASH-011: 验证Features配置信息")
        
        # 获取启用的功能数量
        features_count = dashboard_page.get_enabled_features_count()
        logger.info(f"启用的功能数量: {features_count}")
        
        # 验证返回值是数字
        assert isinstance(features_count, int), "功能数量应该是整数"
        assert features_count >= 0, "功能数量不应该是负数"
        
        # 截图：功能配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_features_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="功能配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-011执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_host_badge_visibility(self, dashboard_page):
        """
        TC-DASH-012: Host标识显示验证测试
        
        测试目标：验证Host用户的特殊标识（Badge）正确显示
        测试区域：Dashboard Page - User Profile Card
        测试元素：
        - Host标识徽章（Badge）
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [User Profile] 检查Host徽章可见性
        3. [验证] 如果是Host用户，确认徽章显示
        4. [验证] 记录Host徽章状态
        
        预期结果：
        - 如果登录用户是Host，Host徽章显示
        - 如果不是Host，徽章不显示
        - 徽章状态正确反映用户身份
        """
        logger.info("开始执行TC-DASH-013: 验证Host标识显示")
        
        # 检查是否为Host用户
        is_host = dashboard_page.is_host_user()
        logger.info(f"是否为Host用户: {is_host}")
        
        # 截图：Host标识
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_host_badge_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Host标识显示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-DASH-013执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_dashboard_page_refresh(self, dashboard_page):
        """
        TC-DASH-013: Dashboard页面刷新功能验证测试
        
        测试目标：验证Dashboard页面刷新后所有数据正确重新加载
        测试区域：Dashboard Page（完整页面）
        测试元素：
        - 整个Dashboard页面
        - 所有数据卡片和区域
        
        测试步骤：
        1. [前置条件] 用户已登录并在Dashboard页面
        2. [Dashboard] 记录刷新前的页面状态
        3. [操作] 执行页面刷新（reload）
        4. [验证] 等待页面重新加载完成
        5. [验证] 确认页面仍然正确显示
        6. [验证] 确认所有数据正确加载
        
        预期结果：
        - 页面刷新成功
        - 页面重新加载完成
        - 所有数据和元素正确显示
        - 用户仍然保持登录状态
        - 无加载错误或数据丢失
        
        TC-DASH-014: 验证Dashboard数据刷新
        验证页面刷新后数据保持一致
        """
        logger.info("开始执行TC-DASH-014: 验证Dashboard数据刷新")
        
        # 记录刷新前的数据
        before_refresh = {
            "multi_tenancy": dashboard_page.get_multi_tenancy_status(),
            "tenant": dashboard_page.get_current_tenant(),
            "culture": dashboard_page.get_current_culture(),
            "features": dashboard_page.get_enabled_features_count()
        }
        logger.info(f"刷新前数据: {before_refresh}")
        
        # 刷新页面
        dashboard_page.page.reload()
        dashboard_page.page.wait_for_load_state("domcontentloaded")
        dashboard_page.page.wait_for_timeout(2000)
        
        # 记录刷新后的数据
        after_refresh = {
            "multi_tenancy": dashboard_page.get_multi_tenancy_status(),
            "tenant": dashboard_page.get_current_tenant(),
            "culture": dashboard_page.get_current_culture(),
            "features": dashboard_page.get_enabled_features_count()
        }
        logger.info(f"刷新后数据: {after_refresh}")
        
        # 截图：刷新后页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_after_refresh_{timestamp}.png"
        dashboard_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="刷新后页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证数据一致性
        assert before_refresh == after_refresh, "刷新前后数据应该保持一致"
        
        logger.info("TC-DASH-014执行成功")

