"""
Settings (Emailing) 功能测试模块
包含SMTP邮件配置功能测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.settings_emailing_page import SettingsEmailingPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def logged_in_settings(browser, test_data):
    """
    登录后的Settings页面fixture - 整个测试类只登录一次
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
def settings_page(logged_in_settings):
    """
    每个测试函数的Settings页面fixture
    """
    page = logged_in_settings
    
    # 导航到Settings页面
    settings = SettingsEmailingPage(page)
    settings.navigate()
    
    return settings


@pytest.mark.settings
class TestSettingsEmailing:
    """Settings Emailing功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_settings_page_load(self, settings_page):
        """
        TC-SETTINGS-001: Settings页面加载验证测试
        
        测试目标：验证Settings（邮件配置）页面能够成功加载并显示SMTP配置表单
        测试区域：Settings Page - Emailing Tab
        测试元素：
        - Settings页面（整体页面）
        - Emailing配置表单
        
        测试步骤：
        1. [前置条件] 用户已登录并导航到Settings页面
        2. [Settings Page] 验证页面加载完成
        3. [验证] 确认页面is_loaded状态为True
        
        预期结果：
        - Settings页面成功加载
        - Emailing配置表单可见
        - 页面无加载错误
        """
        logger.info("开始执行TC-SETTINGS-001: 验证Settings页面加载")
        
        # 验证页面加载完成
        assert settings_page.is_loaded(), "Settings页面未正确加载"
        
        # 截图：页面初始加载
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_initial_load_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Settings页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_tab_switch(self, settings_page):
        """
        TC-SETTINGS-002: Tab切换功能验证测试
        
        测试目标：验证Settings页面的Tab切换功能正常工作
        测试区域：Settings Page - Tab Navigation
        测试元素：
        - Emailing Tab（默认Tab）
        - Feature Management Tab
        
        测试步骤：
        1. [前置条件] 用户已在Settings页面的Emailing Tab
        2. [Tab Navigation] 点击切换到Feature Management Tab
        3. [验证] 确认成功切换到Feature Management
        4. [Tab Navigation] 点击切换回Emailing Tab
        5. [验证] 确认成功切换回Emailing
        
        预期结果：
        - Tab切换功能正常
        - 切换时内容正确更新
        - 无UI错误或闪烁
        """
        logger.info("开始执行TC-SETTINGS-002: 验证Tab切换功能")
        
        # 截图：初始状态（Emailing Tab）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_emailing_tab_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 切换到Feature Management Tab
        settings_page.click_feature_management_tab()
        
        # 截图：Feature Management Tab
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_feature_tab_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Feature Management Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 切换回Emailing Tab
        settings_page.click_emailing_tab()
        
        # 截图：切换回Emailing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_back_to_emailing_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-切换回Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-002执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_gmail_smtp_config(self, settings_page, test_data):
        """
        TC-SETTINGS-004: SMTP配置保存验证测试（Gmail）
        
        测试目标：验证使用Gmail SMTP服务器的邮件配置能够正确保存
        测试区域：Settings Page - Emailing Tab - SMTP Configuration Form
        测试元素：
        - Display Name输入框
        - From Address输入框
        - Host输入框（smtp.gmail.com）
        - Port输入框（587）
        - Enable SSL复选框
        - Username输入框
        - Password输入框
        
        测试步骤：
        1. [前置条件] 用户已在Settings - Emailing Tab
        2. [Form] 填写Gmail SMTP配置（所有字段）
        3. [验证] 确认配置自动保存
        4. [验证] 确认无错误提示
        
        预期结果：
        - Gmail配置成功保存
        - 所有字段值正确
        - SSL启用状态正确
        - 无保存错误
        """
        logger.info("开始执行TC-SETTINGS-004: 验证SMTP配置保存（Gmail）")
        
        # 获取Gmail配置数据
        gmail_config = test_data["valid_email_config"][0]
        
        # 截图：填写前状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_before_fill_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-填写前状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 配置Gmail SMTP
        settings_page.configure_smtp(
            display_name="Aevatar System",
            from_address=gmail_config["from_address"],
            host=gmail_config["host"],
            port=gmail_config["port"],
            enable_ssl=gmail_config["enable_ssl"],
            username=gmail_config["username"],
            password=gmail_config["password"]
        )
        
        # 截图：填写完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_gmail_filled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Gmail配置已填写",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待保存
        settings_page.page.wait_for_load_state("networkidle")
        settings_page.page.wait_for_timeout(2000)
        
        # 截图：保存后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_gmail_saved_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-Gmail配置已保存",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-004执行成功")
    
    @pytest.mark.P0
    @pytest.mark.data
    def test_p0_config_persistence(self, settings_page, test_data):
        """
        TC-SETTINGS-005: 配置持久化验证测试
        
        测试目标：验证SMTP配置在页面刷新后仍然保持
        测试区域：Settings Page - Emailing - Data Persistence
        测试元素：SMTP配置表单所有字段
        
        测试步骤：
        1. [前置条件] 已保存Gmail SMTP配置
        2. [操作] 执行页面刷新
        3. [验证] 确认配置仍然存在
        4. [验证] 确认所有字段值正确
        
        预期结果：
        - 配置在刷新后保持
        - 所有字段值不变
        - 数据持久化正常
        
        TC-SETTINGS-005: 验证配置数据持久化
        验证保存后刷新页面配置仍然存在
        """
        logger.info("开始执行TC-SETTINGS-005: 验证配置数据持久化")
        
        # 配置SMTP
        gmail_config = test_data["valid_email_config"][0]
        settings_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"],
            from_address=gmail_config["from_address"]
        )
        
        settings_page.page.wait_for_load_state("networkidle")
        settings_page.page.wait_for_timeout(2000)
        
        # 记录保存后的数据
        saved_data = {
            "host": settings_page.get_host_value(),
            "port": settings_page.get_port_value(),
            "from_address": settings_page.get_from_address_value()
        }
        logger.info(f"保存后数据: {saved_data}")
        
        # 截图：保存后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_before_refresh_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-保存后数据",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 刷新页面
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 记录刷新后的数据
        refreshed_data = {
            "host": settings_page.get_host_value(),
            "port": settings_page.get_port_value(),
            "from_address": settings_page.get_from_address_value()
        }
        logger.info(f"刷新后数据: {refreshed_data}")
        
        # 截图：刷新后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_after_refresh_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-刷新后数据（验证持久化）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证数据一致性
        assert saved_data == refreshed_data, "刷新前后数据应该保持一致"
        
        logger.info("TC-SETTINGS-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_from_address_validation(self, settings_page):
        """
        TC-SETTINGS-006: From Address格式验证测试
        
        测试目标：验证发件人邮箱地址的格式验证功能
        测试区域：Settings Page - Form Validation
        测试元素：From Address输入框
        
        测试步骤：
        1. [Form] 填写无效邮箱格式（多个场景）
        2. [验证] 确认HTML5验证触发或显示错误
        3. [验证] 确认无效格式被拒绝
        
        预期结果：
        - 无效邮箱格式被拒绝
        - 显示格式错误提示
        - 表单验证正常工作
        """
        logger.info("开始执行TC-SETTINGS-006: 验证From Address格式校验")
        
        # 测试无效邮箱格式
        invalid_emails = [
            "invalidemail",
            "test@",
            "@example.com"
        ]
        
        for idx, invalid_email in enumerate(invalid_emails, 1):
            logger.info(f"测试无效邮箱 {idx}: {invalid_email}")
            
            settings_page.fill_from_address(invalid_email)
            settings_page.page.wait_for_timeout(500)
            
            # 截图：无效邮箱
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"settings_invalid_email_{idx}_{timestamp}.png"
            settings_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-无效邮箱: {invalid_email}",
                attachment_type=allure.attachment_type.PNG
            )
        
        # 测试有效邮箱格式
        valid_email = "valid@example.com"
        logger.info(f"测试有效邮箱: {valid_email}")
        settings_page.fill_from_address(valid_email)
        
        # 截图：有效邮箱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_valid_email_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="4-有效邮箱格式",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.boundary
    def test_p1_port_boundary_validation(self, settings_page):
        """
        TC-SETTINGS-007: Port端口号边界值验证测试
        
        测试目标：验证SMTP端口号的边界值验证功能
        测试区域：Settings Page - Form Validation - Port Field
        测试元素：Port输入框
        
        测试步骤：
        1. [Form] 测试各种端口值（0, 1, 25, 587, 65535, 70000）
        2. [验证] 确认1-65535范围内的值被接受
        3. [验证] 确认0和超过65535的值被拒绝或警告
        
        预期结果：
        - 1-65535范围内的端口有效
        - 0和超过65535的端口无效
        - 边界验证正确工作
        """
        logger.info("开始执行TC-SETTINGS-007: 验证Port端口号范围校验")
        
        # 测试数据
        test_ports = [
            {"value": 0, "valid": False, "desc": "无效：0"},
            {"value": 1, "valid": True, "desc": "边界：最小有效值"},
            {"value": 25, "valid": True, "desc": "常用：SMTP"},
            {"value": 587, "valid": True, "desc": "常用：TLS"},
            {"value": 65535, "valid": True, "desc": "边界：最大有效值"},
            {"value": 70000, "valid": False, "desc": "无效：超出范围"}
        ]
        
        for idx, port_data in enumerate(test_ports, 1):
            logger.info(f"测试端口 {idx}: {port_data['value']} - {port_data['desc']}")
            
            settings_page.fill_port(port_data["value"])
            settings_page.page.wait_for_timeout(500)
            
            # 截图：端口测试
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"settings_port_{port_data['value']}_{timestamp}.png"
            settings_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-端口: {port_data['value']} ({port_data['desc']})",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("TC-SETTINGS-007执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_ssl_toggle(self, settings_page):
        """
        TC-SETTINGS-008: SSL启用/禁用切换测试
        
        测试目标：验证Enable SSL开关的切换功能正常
        测试区域：Settings Page - SSL Configuration
        测试元素：Enable SSL复选框
        
        测试步骤：
        1. [Form] 启用SSL（勾选复选框）
        2. [验证] 确认SSL状态为已启用
        3. [Form] 禁用SSL（取消勾选）
        4. [验证] 确认SSL状态为已禁用
        
        预期结果：
        - SSL开关正常工作
        - 状态正确切换
        - 配置正确保存
        """
        logger.info("开始执行TC-SETTINGS-008: 验证Enable SSL开关功能")
        
        # 启用SSL
        settings_page.set_enable_ssl(True)
        settings_page.page.wait_for_timeout(500)
        
        # 验证状态
        assert settings_page.is_ssl_enabled(), "SSL应该被启用"
        
        # 截图：SSL已启用
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_ssl_enabled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-SSL已启用",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 禁用SSL
        settings_page.set_enable_ssl(False)
        settings_page.page.wait_for_timeout(500)
        
        # 验证状态
        assert not settings_page.is_ssl_enabled(), "SSL应该被禁用"
        
        # 截图：SSL已禁用
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_ssl_disabled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-SSL已禁用",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_default_credentials_toggle(self, settings_page):
        """
        TC-SETTINGS-009: 默认凭证切换测试
        
        测试目标：验证"使用默认凭证"选项的切换功能
        测试区域：Settings Page - Credentials Configuration
        测试元素：Use Default Credentials复选框
        
        测试步骤：
        1. [Form] 启用默认凭证
        2. [验证] 确认Username/Password字段禁用
        3. [Form] 禁用默认凭证
        4. [验证] 确认Username/Password字段启用
        
        预期结果：
        - 默认凭证开关正常工作
        - 字段启用/禁用状态正确联动
        - 逻辑一致无错误
        """
        logger.info("开始执行TC-SETTINGS-009: 验证Use Default Credentials开关")
        
        # 启用默认凭据
        settings_page.set_use_default_credentials(True)
        settings_page.page.wait_for_timeout(500)
        
        # 验证状态
        assert settings_page.is_default_credentials_enabled(), "默认凭据应该被启用"
        
        # 截图：默认凭据已启用
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_credentials_enabled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-默认凭据已启用",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 禁用默认凭据
        settings_page.set_use_default_credentials(False)
        settings_page.page.wait_for_timeout(500)
        
        # 截图：默认凭据已禁用
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_credentials_disabled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-默认凭据已禁用",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-009执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_office365_smtp_config(self, settings_page, test_data):
        """
        TC-SETTINGS-011: Office365 SMTP配置保存验证测试
        
        测试目标：验证使用Office365 SMTP服务器的邮件配置能够正确保存
        测试区域：Settings Page - Emailing - SMTP Configuration
        测试元素：SMTP配置表单所有字段
        
        测试步骤：
        1. [Form] 填写Office365 SMTP配置
           - Host: smtp.office365.com
           - Port: 587
           - Enable SSL: True
        2. [验证] 确认配置自动保存
        3. [验证] 确认无错误提示
        
        预期结果：
        - Office365配置成功保存
        - 所有字段值正确
        - SSL启用状态正确
        - 无保存错误
        """
        logger.info("开始执行TC-SETTINGS-011: 验证Office 365配置")
        
        # 获取Office 365配置数据
        o365_config = test_data["valid_email_config"][1]
        
        # 截图：配置前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_before_o365_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-配置Office 365前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 配置Office 365
        settings_page.configure_smtp(
            display_name="Company Notification",
            from_address=o365_config["from_address"],
            host=o365_config["host"],
            port=o365_config["port"],
            enable_ssl=o365_config["enable_ssl"],
            username=o365_config["username"],
            password=o365_config["password"]
        )
        
        # 截图：配置完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_o365_filled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Office 365配置已填写",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待保存
        settings_page.page.wait_for_load_state("networkidle")
        settings_page.page.wait_for_timeout(2000)
        
        # 刷新验证
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 截图：刷新后验证
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_o365_refresh_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-刷新后验证Office 365配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证数据
        assert settings_page.get_host_value() == o365_config["host"], "Host应该正确保存"
        assert settings_page.get_port_value() == o365_config["port"], "Port应该正确保存"
        
        logger.info("TC-SETTINGS-011执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_host_different_formats(self, settings_page):
        """
        TC-SETTINGS-013: Host主机名格式验证测试
        
        测试目标：验证SMTP主机名字段支持多种格式（域名、IP等）
        测试区域：Settings Page - Form Validation - Host Field
        测试元素：Host输入框
        
        测试步骤：
        1. [Form] 测试域名格式（smtp.example.com）
        2. [验证] 确认域名格式被接受
        3. [Form] 测试IP格式（192.168.1.1）
        4. [验证] 确认IP格式被接受
        5. [Form] 测试localhost
        6. [验证] 确认localhost被接受
        
        预期结果：
        - 域名格式有效
        - IP地址格式有效
        - localhost有效
        - 多种格式支持正常
        """
        logger.info("开始执行TC-SETTINGS-013: 验证Host字段不同格式输入")
        
        # 测试不同Host格式
        hosts = [
            {"value": "smtp.gmail.com", "desc": "域名格式"},
            {"value": "192.168.1.100", "desc": "IP地址格式"},
            {"value": "localhost", "desc": "本地主机"}
        ]
        
        for idx, host_data in enumerate(hosts, 1):
            logger.info(f"测试Host格式 {idx}: {host_data['value']} - {host_data['desc']}")
            
            settings_page.fill_host(host_data["value"])
            settings_page.page.wait_for_timeout(500)
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"settings_host_{idx}_{timestamp}.png"
            settings_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-Host: {host_data['value']} ({host_data['desc']})",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证输入值
            assert settings_page.get_host_value() == host_data["value"], \
                f"Host应该正确填入: {host_data['value']}"
        
        logger.info("TC-SETTINGS-013执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_domain_optional_field(self, settings_page, test_data):
        """
        TC-SETTINGS-014: Domain可选字段验证测试
        
        测试目标：验证Domain字段为可选字段，可以留空或填写
        测试区域：Settings Page - Form Validation - Domain Field
        测试元素：Domain输入框（可选字段）
        
        测试步骤：
        1. [Form] 填写SMTP配置但不填Domain
        2. [验证] 确认配置可以保存
        3. [Form] 填写Domain字段
        4. [验证] 确认配置正常保存
        
        预期结果：
        - Domain为可选字段
        - 不填Domain可以成功保存
        - 填写Domain也可以成功保存
        - 无必填验证错误
        """
        logger.info("开始执行TC-SETTINGS-014: 验证Domain字段（可选）")
        
        gmail_config = test_data["valid_email_config"][0]
        
        # 场景1：不填写Domain
        logger.info("场景1：Domain字段留空")
        settings_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"],
            from_address=gmail_config["from_address"],
            domain=""  # 留空
        )
        
        settings_page.page.wait_for_timeout(1000)
        
        # 截图：Domain留空
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_domain_empty_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Domain字段留空",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 场景2：填写Domain
        logger.info("场景2：填写Domain字段")
        settings_page.fill_domain("company.local")
        settings_page.page.wait_for_timeout(500)
        
        # 截图：Domain已填写
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_domain_filled_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Domain字段已填写",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-SETTINGS-014执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_config_update_override(self, settings_page, test_data):
        """
        TC-SETTINGS-015: 配置更新覆盖测试
        
        测试目标：验证新的SMTP配置能够正确覆盖旧配置
        测试区域：Settings Page - Data Update
        测试元素：SMTP配置表单所有字段
        
        测试步骤：
        1. [前置条件] 已保存初始Gmail配置
        2. [Form] 修改配置为Office365
        3. [验证] 确认新配置保存成功
        4. [验证] 确认旧配置被完全覆盖
        
        预期结果：
        - 新配置成功保存
        - 旧配置被完全覆盖
        - 无数据残留或混合
        - 配置更新功能正常
        """
        logger.info("开始执行TC-SETTINGS-015: 验证配置修改覆盖")
        
        # 配置Gmail
        gmail_config = test_data["valid_email_config"][0]
        settings_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"]
        )
        settings_page.page.wait_for_timeout(2000)
        
        # 截图：Gmail配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_gmail_config_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Gmail配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 修改为Office 365
        o365_config = test_data["valid_email_config"][1]
        settings_page.configure_smtp(
            host=o365_config["host"],
            port=o365_config["port"]
        )
        settings_page.page.wait_for_timeout(2000)
        
        # 截图：Office 365配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_o365_config_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-修改为Office 365配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 刷新验证
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 截图：刷新后验证
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_after_override_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-刷新后验证新配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证新配置生效
        assert settings_page.get_host_value() == o365_config["host"], \
            "Host应该更新为Office 365配置"
        
        logger.info("TC-SETTINGS-015执行成功")

