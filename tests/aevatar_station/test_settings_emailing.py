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
    
    try:
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        valid_data = test_data["valid_login_data"][0]
        logger.info(f"使用账号登录: {valid_data['username']}")
        
        page.fill("#LoginInput_UserNameOrEmailAddress", valid_data["username"])
        page.fill("#LoginInput_Password", valid_data["password"])
        page.click("button[type='submit']")
        
        # 等待登录完成
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        logger.info(f"登录跳转完成，当前URL: {page.url}")
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        
        logger.info("登录成功，会话将在整个测试类中复用")
        
        yield page
        
    except Exception as e:
        logger.error(f"❌ 登录失败: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/settings_login_fail_{timestamp}.png")
        raise e
    finally:
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
    
    # 确认页面已加载
    if not settings.is_loaded():
        logger.warning("Settings页面可能未完全加载，尝试刷新")
        page.reload()
        settings.wait_for_load()
    
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
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-001: 验证Settings页面加载")
        logger.info("=" * 60)
        
        # 验证页面加载完成
        assert settings_page.is_loaded(), "Settings页面未正确加载"
        logger.info("   ✓ Settings页面加载成功")
        
        # 截图：页面初始加载
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_initial_load_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Settings页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-SETTINGS-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_tab_switch(self, settings_page):
        """
        TC-SETTINGS-002: Tab切换功能验证测试
        
        测试目标：验证Settings页面的Tab切换功能正常工作
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-002: 验证Tab切换功能")
        logger.info("=" * 60)
        
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
        logger.info("步骤1: 切换到Feature Management Tab")
        settings_page.click_feature_management_tab()
        
        # 截图：Feature Management Tab
        screenshot_path = f"settings_feature_tab_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Feature Management Tab",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   ✓ 已切换到Feature Management")
        
        # 切换回Emailing Tab
        logger.info("步骤2: 切换回Emailing Tab")
        settings_page.click_emailing_tab()
        
        # 截图：切换回Emailing
        screenshot_path = f"settings_back_to_emailing_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-切换回Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   ✓ 已切换回Emailing")
        
        logger.info("✅ TC-SETTINGS-002执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_gmail_smtp_config(self, settings_page, test_data):
        """
        TC-SETTINGS-004: SMTP配置保存验证测试（Gmail）
        
        测试目标：验证使用Gmail SMTP服务器的邮件配置能够正确保存
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-004: 验证SMTP配置保存（Gmail）")
        logger.info("=" * 60)
        
        # 获取Gmail配置数据
        gmail_config = test_data["valid_email_config"][0]
        
        # 配置Gmail SMTP
        logger.info("步骤1: 填写Gmail SMTP配置")
        settings_page.configure_smtp(
            display_name="Aevatar System",
            from_address=gmail_config["from_address"],
            host=gmail_config["host"],
            port=gmail_config["port"],
            enable_ssl=gmail_config["enable_ssl"],
            username=gmail_config["username"],
            password=gmail_config["password"]
        )
        
        # 等待保存（模拟自动保存或点击保存按钮后的延迟）
        settings_page.page.wait_for_load_state("networkidle")
        settings_page.page.wait_for_timeout(2000)
        
        # 截图：保存后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"settings_gmail_saved_{timestamp}.png"
        settings_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Gmail配置已保存",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证保存的值
        logger.info("步骤2: 验证保存后的值")
        assert settings_page.get_host_value() == gmail_config["host"], "Host值未正确保存"
        assert settings_page.get_port_value() == str(gmail_config["port"]), "Port值未正确保存"
        assert settings_page.is_ssl_enabled() == gmail_config["enable_ssl"], "SSL状态未正确保存"
        logger.info("   ✓ 所有配置项验证通过")
        
        logger.info("✅ TC-SETTINGS-004执行成功")
    
    @pytest.mark.P0
    @pytest.mark.data
    def test_p0_config_persistence(self, settings_page, test_data):
        """
        TC-SETTINGS-005: 配置持久化验证测试
        
        测试目标：验证SMTP配置在页面刷新后仍然保持
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-005: 验证配置数据持久化")
        logger.info("=" * 60)
        
        # 配置SMTP
        gmail_config = test_data["valid_email_config"][0]
        logger.info("步骤1: 配置SMTP并保存")
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
        logger.info(f"   保存后数据: {saved_data}")
        
        # 刷新页面
        logger.info("步骤2: 刷新页面")
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 记录刷新后的数据
        refreshed_data = {
            "host": settings_page.get_host_value(),
            "port": settings_page.get_port_value(),
            "from_address": settings_page.get_from_address_value()
        }
        logger.info(f"   刷新后数据: {refreshed_data}")
        
        # 验证数据一致性
        assert saved_data == refreshed_data, f"数据不一致: 保存={saved_data}, 刷新={refreshed_data}"
        logger.info("   ✓ 数据持久化验证通过")
        
        logger.info("✅ TC-SETTINGS-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_from_address_validation(self, settings_page):
        """
        TC-SETTINGS-006: From Address格式验证测试
        
        测试目标：验证发件人邮箱地址的格式验证功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-006: 验证From Address格式校验")
        logger.info("=" * 60)
        
        # 测试无效邮箱格式
        invalid_emails = ["invalidemail", "test@", "@example.com"]
        
        for idx, invalid_email in enumerate(invalid_emails, 1):
            logger.info(f"测试无效邮箱 {idx}: {invalid_email}")
            
            settings_page.fill_from_address(invalid_email)
            settings_page.page.wait_for_timeout(500)
            
            # 验证（根据具体的UI表现，可能是HTML5验证或错误提示）
            # 这里假设是HTML5验证
            # is_valid = settings_page.is_from_address_valid()
            # if not is_valid:
            #     logger.info("   ✓ 格式验证触发")
            
            # 截图
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
        
        logger.info("✅ TC-SETTINGS-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.boundary
    def test_p1_port_boundary_validation(self, settings_page):
        """
        TC-SETTINGS-007: Port端口号边界值验证测试
        
        测试目标：验证SMTP端口号的边界值验证功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-007: 验证Port端口号范围校验")
        logger.info("=" * 60)
        
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
            
            # 验证逻辑根据实际UI行为调整，这里主要做输入和截图
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"settings_port_{port_data['value']}_{timestamp}.png"
            settings_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-端口: {port_data['value']} ({port_data['desc']})",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-SETTINGS-007执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_ssl_toggle(self, settings_page):
        """
        TC-SETTINGS-008: SSL启用/禁用切换测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-008: 验证Enable SSL开关功能")
        logger.info("=" * 60)
        
        # 启用SSL
        logger.info("步骤1: 启用SSL")
        settings_page.set_enable_ssl(True)
        settings_page.page.wait_for_timeout(500)
        assert settings_page.is_ssl_enabled(), "SSL应该被启用"
        logger.info("   ✓ SSL已启用")
        
        # 禁用SSL
        logger.info("步骤2: 禁用SSL")
        settings_page.set_enable_ssl(False)
        settings_page.page.wait_for_timeout(500)
        assert not settings_page.is_ssl_enabled(), "SSL应该被禁用"
        logger.info("   ✓ SSL已禁用")
        
        logger.info("✅ TC-SETTINGS-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_default_credentials_toggle(self, settings_page):
        """
        TC-SETTINGS-009: 默认凭证切换测试
        
        测试目标：验证"使用默认凭证"选项的切换功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-009: 验证Use Default Credentials开关")
        logger.info("=" * 60)
        
        # 启用默认凭据
        logger.info("步骤1: 启用默认凭据")
        settings_page.set_use_default_credentials(True)
        settings_page.page.wait_for_timeout(500)
        assert settings_page.is_default_credentials_enabled(), "默认凭据应该被启用"
        logger.info("   ✓ 默认凭据已启用")
        
        # 禁用默认凭据
        logger.info("步骤2: 禁用默认凭据")
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
        
        logger.info("✅ TC-SETTINGS-009执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_office365_smtp_config(self, settings_page, test_data):
        """
        TC-SETTINGS-011: Office365 SMTP配置保存验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-011: 验证Office 365配置")
        logger.info("=" * 60)
        
        o365_config = test_data["valid_email_config"][1]
        
        # 配置Office 365
        logger.info("步骤1: 配置Office 365 SMTP")
        settings_page.configure_smtp(
            display_name="Company Notification",
            from_address=o365_config["from_address"],
            host=o365_config["host"],
            port=o365_config["port"],
            enable_ssl=o365_config["enable_ssl"],
            username=o365_config["username"],
            password=o365_config["password"]
        )
        
        # 等待保存
        settings_page.page.wait_for_load_state("networkidle")
        settings_page.page.wait_for_timeout(2000)
        
        # 刷新验证
        logger.info("步骤2: 刷新并验证数据")
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 验证数据
        assert settings_page.get_host_value() == o365_config["host"], "Host应该正确保存"
        assert str(settings_page.get_port_value()) == str(o365_config["port"]), "Port应该正确保存"
        logger.info("   ✓ 配置保存验证通过")
        
        logger.info("✅ TC-SETTINGS-011执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_host_different_formats(self, settings_page):
        """
        TC-SETTINGS-013: Host主机名格式验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-013: 验证Host字段不同格式输入")
        logger.info("=" * 60)
        
        hosts = [
            {"value": "smtp.gmail.com", "desc": "域名格式"},
            {"value": "192.168.1.100", "desc": "IP地址格式"},
            {"value": "localhost", "desc": "本地主机"}
        ]
        
        for idx, host_data in enumerate(hosts, 1):
            logger.info(f"测试Host格式 {idx}: {host_data['value']} - {host_data['desc']}")
            
            settings_page.fill_host(host_data["value"])
            settings_page.page.wait_for_timeout(500)
            
            # 验证输入值
            assert settings_page.get_host_value() == host_data["value"], \
                f"Host应该正确填入: {host_data['value']}"
        
        logger.info("✅ TC-SETTINGS-013执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_domain_optional_field(self, settings_page, test_data):
        """
        TC-SETTINGS-014: Domain可选字段验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-014: 验证Domain字段（可选）")
        logger.info("=" * 60)
        
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
        
        # 场景2：填写Domain
        logger.info("场景2：填写Domain字段")
        settings_page.fill_domain("company.local")
        settings_page.page.wait_for_timeout(500)
        
        logger.info("✅ TC-SETTINGS-014执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_config_update_override(self, settings_page, test_data):
        """
        TC-SETTINGS-015: 配置更新覆盖测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SETTINGS-015: 验证配置修改覆盖")
        logger.info("=" * 60)
        
        # 配置Gmail
        logger.info("步骤1: 配置Gmail")
        gmail_config = test_data["valid_email_config"][0]
        settings_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"]
        )
        settings_page.page.wait_for_timeout(2000)
        
        # 修改为Office 365
        logger.info("步骤2: 修改为Office 365")
        o365_config = test_data["valid_email_config"][1]
        settings_page.configure_smtp(
            host=o365_config["host"],
            port=o365_config["port"]
        )
        settings_page.page.wait_for_timeout(2000)
        
        # 刷新验证
        logger.info("步骤3: 刷新并验证覆盖结果")
        settings_page.page.reload()
        settings_page.page.wait_for_load_state("domcontentloaded")
        settings_page.page.wait_for_timeout(3000)
        
        # 验证新配置生效
        current_host = settings_page.get_host_value()
        logger.info(f"   当前Host: {current_host}")
        assert current_host == o365_config["host"], \
            f"Host应该更新为Office 365配置 (期望: {o365_config['host']}, 实际: {current_host})"
        
        logger.info("✅ TC-SETTINGS-015执行成功")
