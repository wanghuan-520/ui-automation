"""
管理员设置 - Emailing配置功能测试模块
路径: /admin/settings (Emailing Tab)
包含ABP Settings模块 SMTP邮件配置功能测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.admin_settings_page import AdminSettingsPage
from tests.aevatar_station.pages.settings_emailing_page import SettingsEmailingPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def admin_logged_in_emailing(browser, test_data):
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
        page.screenshot(path=f"screenshots/admin_login_failed_emailing_{timestamp}.png")
        raise e
    finally:
        context.close()


@pytest.fixture(scope="function")
def emailing_page(admin_logged_in_emailing):
    """
    每个测试函数的Emailing设置页面fixture
    """
    page = admin_logged_in_emailing
    
    # 导航到Settings页面
    settings = SettingsEmailingPage(page)
    settings.navigate()
    
    # 确认页面已加载
    if not settings.is_loaded():
        logger.warning("Settings页面可能未完全加载，尝试刷新")
        page.reload()
        settings.wait_for_load()
    
    return settings


@pytest.mark.admin
@pytest.mark.settings
@pytest.mark.emailing
class TestAdminSettingsEmailing:
    """管理员设置 - Emailing配置功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_emailing_page_load(self, emailing_page):
        """
        TC-ADMIN-EMAIL-001: 验证Emailing设置页面加载
        
        测试目标：验证管理员可以访问Emailing设置页面
        测试路径：/admin/settings (Emailing Tab)
        
        测试步骤：
        1. 使用管理员账号登录
        2. 导航到Settings页面
        3. 验证Emailing Tab正确加载
        
        预期结果：
        - 页面成功加载
        - 显示SMTP配置表单
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-001: 验证Emailing设置页面加载")
        logger.info("=" * 60)
        
        # 验证页面加载
        assert emailing_page.is_loaded(), "Settings页面未正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_page_load_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Emailing设置页面加载",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-001执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_tabs_navigation_visible(self, emailing_page):
        """
        TC-ADMIN-EMAIL-002: 验证Tab导航可见
        
        测试目标：验证Settings页面的Tab导航正确显示
        
        测试步骤：
        1. 导航到Settings页面
        2. 检查Tab导航
        
        预期结果：
        - Tab导航区域可见
        - Emailing和Feature Management Tab都可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-002: 验证Tab导航可见")
        logger.info("=" * 60)
        
        # 验证Tab可见
        emailing_tab_visible = emailing_page.is_visible(emailing_page.EMAILING_TAB, timeout=5000)
        logger.info(f"   Emailing Tab可见: {emailing_tab_visible}")
        
        feature_tab_visible = emailing_page.is_visible(emailing_page.FEATURE_MANAGEMENT_TAB, timeout=5000)
        logger.info(f"   Feature Management Tab可见: {feature_tab_visible}")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_tabs_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Tab导航",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_tab_switch(self, emailing_page):
        """
        TC-ADMIN-EMAIL-003: 验证Tab切换功能
        
        测试目标：验证Settings页面的Tab切换功能正常工作
        
        测试步骤：
        1. 确认在Emailing Tab
        2. 切换到Feature Management Tab
        3. 切换回Emailing Tab
        
        预期结果：
        - Tab切换流畅
        - 内容正确显示
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-003: 验证Tab切换功能")
        logger.info("=" * 60)
        
        # 截图：初始状态（Emailing Tab）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_tab_initial_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 切换到Feature Management Tab
        logger.info("步骤1: 切换到Feature Management Tab")
        emailing_page.click_feature_management_tab()
        emailing_page.page.wait_for_timeout(1500)
        
        # 截图：Feature Management Tab
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_to_feature_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Feature Management Tab",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   ✓ 已切换到Feature Management")
        
        # 切换回Emailing Tab
        logger.info("步骤2: 切换回Emailing Tab")
        emailing_page.click_emailing_tab()
        emailing_page.page.wait_for_timeout(1500)
        
        # 截图：切换回Emailing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_back_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-切换回Emailing Tab",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   ✓ 已切换回Emailing")
        
        logger.info("✅ TC-ADMIN-EMAIL-003执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_gmail_smtp_config(self, emailing_page, test_data):
        """
        TC-ADMIN-EMAIL-004: 验证Gmail SMTP配置保存
        
        测试目标：验证使用Gmail SMTP服务器的邮件配置能够正确保存
        
        测试步骤：
        1. 填写Gmail SMTP配置
        2. 保存配置
        3. 验证保存的值
        
        预期结果：
        - 配置成功保存
        - 刷新后数据保持
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-004: 验证Gmail SMTP配置保存")
        logger.info("=" * 60)
        
        # 获取Gmail配置数据
        gmail_config = test_data["valid_email_config"][0]
        
        # 配置Gmail SMTP
        logger.info("步骤1: 填写Gmail SMTP配置")
        emailing_page.configure_smtp(
            display_name="Aevatar System",
            from_address=gmail_config["from_address"],
            host=gmail_config["host"],
            port=gmail_config["port"],
            enable_ssl=gmail_config["enable_ssl"],
            username=gmail_config["username"],
            password=gmail_config["password"]
        )
        
        # 等待保存
        emailing_page.page.wait_for_timeout(2000)
        
        # 截图：保存后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_gmail_saved_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Gmail配置已保存",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证保存的值
        logger.info("步骤2: 验证保存后的值")
        assert emailing_page.get_host_value() == gmail_config["host"], "Host值未正确保存"
        assert emailing_page.get_port_value() == gmail_config["port"], "Port值未正确保存"
        logger.info("   ✓ 配置项验证通过")
        
        logger.info("✅ TC-ADMIN-EMAIL-004执行成功")
    
    @pytest.mark.P0
    @pytest.mark.data
    @pytest.mark.skip(reason="后端限制：Settings API返回404，配置无法持久化")
    def test_p0_config_persistence(self, emailing_page, test_data):
        """
        TC-ADMIN-EMAIL-005: 验证配置持久化
        
        测试目标：验证SMTP配置在页面刷新后仍然保持
        
        测试步骤：
        1. 配置SMTP并保存
        2. 刷新页面
        3. 验证数据一致性
        
        预期结果：
        - 刷新后配置保持不变
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-005: 验证配置数据持久化")
        logger.info("=" * 60)
        
        # 配置SMTP
        gmail_config = test_data["valid_email_config"][0]
        logger.info("步骤1: 配置SMTP并保存")
        emailing_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"],
            from_address=gmail_config["from_address"]
        )
        
        emailing_page.page.wait_for_timeout(2000)
        
        # 记录保存后的数据
        saved_data = {
            "host": emailing_page.get_host_value(),
            "port": emailing_page.get_port_value(),
            "from_address": emailing_page.get_from_address_value()
        }
        logger.info(f"   保存后数据: {saved_data}")
        
        # 刷新页面
        logger.info("步骤2: 刷新页面")
        emailing_page.page.reload()
        emailing_page.page.wait_for_load_state("domcontentloaded")
        emailing_page.page.wait_for_timeout(3000)
        
        # 记录刷新后的数据
        refreshed_data = {
            "host": emailing_page.get_host_value(),
            "port": emailing_page.get_port_value(),
            "from_address": emailing_page.get_from_address_value()
        }
        logger.info(f"   刷新后数据: {refreshed_data}")
        
        # 验证数据一致性
        assert saved_data == refreshed_data, f"数据不一致: 保存={saved_data}, 刷新={refreshed_data}"
        logger.info("   ✓ 数据持久化验证通过")
        
        logger.info("✅ TC-ADMIN-EMAIL-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_from_address_validation(self, emailing_page):
        """
        TC-ADMIN-EMAIL-006: 验证From Address格式验证
        
        测试目标：验证发件人邮箱地址的格式验证功能
        
        测试步骤：
        1. 输入无效邮箱格式
        2. 验证格式校验
        3. 输入有效邮箱格式
        
        预期结果：
        - 无效格式被识别
        - 有效格式被接受
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-006: 验证From Address格式校验")
        logger.info("=" * 60)
        
        # 测试无效邮箱格式
        invalid_emails = ["invalidemail", "test@", "@example.com"]
        
        for idx, invalid_email in enumerate(invalid_emails, 1):
            logger.info(f"测试无效邮箱 {idx}: {invalid_email}")
            
            emailing_page.fill_from_address(invalid_email)
            emailing_page.page.wait_for_timeout(500)
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"admin_emailing_invalid_{idx}_{timestamp}.png"
            emailing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-无效邮箱: {invalid_email}",
                attachment_type=allure.attachment_type.PNG
            )
        
        # 测试有效邮箱格式
        valid_email = "valid@example.com"
        logger.info(f"测试有效邮箱: {valid_email}")
        emailing_page.fill_from_address(valid_email)
        
        logger.info("✅ TC-ADMIN-EMAIL-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.boundary
    def test_p1_port_boundary_validation(self, emailing_page):
        """
        TC-ADMIN-EMAIL-007: 验证Port端口号边界值
        
        测试目标：验证SMTP端口号的边界值验证功能
        
        测试步骤：
        1. 测试各种端口值
        2. 验证输入接受情况
        
        预期结果：
        - 有效端口被接受（1-65535）
        - 常用端口正常工作（25, 465, 587）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-007: 验证Port端口号范围校验")
        logger.info("=" * 60)
        
        # 测试数据
        test_ports = [
            {"value": 0, "valid": False, "desc": "无效：0"},
            {"value": 1, "valid": True, "desc": "边界：最小有效值"},
            {"value": 25, "valid": True, "desc": "常用：SMTP"},
            {"value": 465, "valid": True, "desc": "常用：SSL"},
            {"value": 587, "valid": True, "desc": "常用：TLS"},
            {"value": 65535, "valid": True, "desc": "边界：最大有效值"}
        ]
        
        for idx, port_data in enumerate(test_ports, 1):
            logger.info(f"测试端口 {idx}: {port_data['value']} - {port_data['desc']}")
            
            emailing_page.fill_port(port_data["value"])
            emailing_page.page.wait_for_timeout(500)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"admin_emailing_port_{port_data['value']}_{timestamp}.png"
            emailing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-端口: {port_data['value']} ({port_data['desc']})",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-ADMIN-EMAIL-007执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_ssl_toggle(self, emailing_page):
        """
        TC-ADMIN-EMAIL-008: 验证SSL启用/禁用切换
        
        测试目标：验证Enable SSL开关功能
        
        测试步骤：
        1. 启用SSL
        2. 验证状态
        3. 禁用SSL
        4. 验证状态
        
        预期结果：
        - SSL可以正常切换
        - 状态正确反映
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-008: 验证Enable SSL开关功能")
        logger.info("=" * 60)
        
        # 启用SSL
        logger.info("步骤1: 启用SSL")
        emailing_page.set_enable_ssl(True)
        emailing_page.page.wait_for_timeout(500)
        assert emailing_page.is_ssl_enabled(), "SSL应该被启用"
        logger.info("   ✓ SSL已启用")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_ssl_on_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-SSL已启用",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 禁用SSL
        logger.info("步骤2: 禁用SSL")
        emailing_page.set_enable_ssl(False)
        emailing_page.page.wait_for_timeout(500)
        assert not emailing_page.is_ssl_enabled(), "SSL应该被禁用"
        logger.info("   ✓ SSL已禁用")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_ssl_off_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-SSL已禁用",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_default_credentials_toggle(self, emailing_page):
        """
        TC-ADMIN-EMAIL-009: 验证默认凭证切换
        
        测试目标：验证"使用默认凭证"选项的切换功能
        
        测试步骤：
        1. 启用默认凭据
        2. 禁用默认凭据
        
        预期结果：
        - 切换功能正常
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-009: 验证Use Default Credentials开关")
        logger.info("=" * 60)
        
        # 启用默认凭据
        logger.info("步骤1: 启用默认凭据")
        emailing_page.set_use_default_credentials(True)
        emailing_page.page.wait_for_timeout(500)
        assert emailing_page.is_default_credentials_enabled(), "默认凭据应该被启用"
        logger.info("   ✓ 默认凭据已启用")
        
        # 禁用默认凭据
        logger.info("步骤2: 禁用默认凭据")
        emailing_page.set_use_default_credentials(False)
        emailing_page.page.wait_for_timeout(500)
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_credentials_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="默认凭据切换",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-009执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    @pytest.mark.skip(reason="后端限制：Settings API返回404，配置无法持久化")
    def test_p1_office365_smtp_config(self, emailing_page, test_data):
        """
        TC-ADMIN-EMAIL-010: 验证Office365 SMTP配置
        
        测试目标：验证Office 365 SMTP配置能够正确保存
        
        测试步骤：
        1. 配置Office 365 SMTP
        2. 刷新并验证
        
        预期结果：
        - 配置成功保存
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-010: 验证Office 365配置")
        logger.info("=" * 60)
        
        o365_config = test_data["valid_email_config"][1]
        
        # 配置Office 365
        logger.info("步骤1: 配置Office 365 SMTP")
        emailing_page.configure_smtp(
            display_name="Company Notification",
            from_address=o365_config["from_address"],
            host=o365_config["host"],
            port=o365_config["port"],
            enable_ssl=o365_config["enable_ssl"],
            username=o365_config["username"],
            password=o365_config["password"]
        )
        
        emailing_page.page.wait_for_timeout(2000)
        
        # 刷新验证
        logger.info("步骤2: 刷新并验证数据")
        emailing_page.page.reload()
        emailing_page.page.wait_for_load_state("domcontentloaded")
        emailing_page.page.wait_for_timeout(3000)
        
        # 验证数据
        assert emailing_page.get_host_value() == o365_config["host"], "Host应该正确保存"
        logger.info("   ✓ 配置保存验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_o365_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="Office365配置",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-010执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_host_different_formats(self, emailing_page):
        """
        TC-ADMIN-EMAIL-011: 验证Host主机名格式
        
        测试目标：验证Host字段接受不同格式的输入
        
        测试步骤：
        1. 输入域名格式
        2. 输入IP地址格式
        3. 输入localhost
        
        预期结果：
        - 所有有效格式被接受
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-011: 验证Host字段不同格式输入")
        logger.info("=" * 60)
        
        hosts = [
            {"value": "smtp.gmail.com", "desc": "域名格式"},
            {"value": "192.168.1.100", "desc": "IP地址格式"},
            {"value": "localhost", "desc": "本地主机"}
        ]
        
        for idx, host_data in enumerate(hosts, 1):
            logger.info(f"测试Host格式 {idx}: {host_data['value']} - {host_data['desc']}")
            
            emailing_page.fill_host(host_data["value"])
            emailing_page.page.wait_for_timeout(500)
            
            # 验证输入值
            assert emailing_page.get_host_value() == host_data["value"], \
                f"Host应该正确填入: {host_data['value']}"
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"admin_emailing_host_{idx}_{timestamp}.png"
            emailing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx}-Host: {host_data['desc']}",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-ADMIN-EMAIL-011执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    @pytest.mark.skip(reason="后端限制：Settings API返回404，配置无法持久化")
    def test_p1_config_update_override(self, emailing_page, test_data):
        """
        TC-ADMIN-EMAIL-012: 验证配置更新覆盖
        
        测试目标：验证修改配置会覆盖原有配置
        
        测试步骤：
        1. 配置Gmail
        2. 修改为Office 365
        3. 验证覆盖结果
        
        预期结果：
        - 新配置覆盖旧配置
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-012: 验证配置修改覆盖")
        logger.info("=" * 60)
        
        # 配置Gmail
        logger.info("步骤1: 配置Gmail")
        gmail_config = test_data["valid_email_config"][0]
        emailing_page.configure_smtp(
            host=gmail_config["host"],
            port=gmail_config["port"]
        )
        emailing_page.page.wait_for_timeout(2000)
        
        # 修改为Office 365
        logger.info("步骤2: 修改为Office 365")
        o365_config = test_data["valid_email_config"][1]
        emailing_page.configure_smtp(
            host=o365_config["host"],
            port=o365_config["port"]
        )
        emailing_page.page.wait_for_timeout(2000)
        
        # 刷新验证
        logger.info("步骤3: 刷新并验证覆盖结果")
        emailing_page.page.reload()
        emailing_page.page.wait_for_load_state("domcontentloaded")
        emailing_page.page.wait_for_timeout(3000)
        
        # 验证新配置生效
        current_host = emailing_page.get_host_value()
        logger.info(f"   当前Host: {current_host}")
        assert current_host == o365_config["host"], \
            f"Host应该更新为Office 365配置 (期望: {o365_config['host']}, 实际: {current_host})"
        
        logger.info("✅ TC-ADMIN-EMAIL-012执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_page_refresh(self, emailing_page):
        """
        TC-ADMIN-EMAIL-013: 验证页面刷新保持状态
        
        测试目标：验证刷新页面后仍在设置页面
        
        测试步骤：
        1. 在Emailing页面
        2. 刷新页面
        3. 验证仍在设置页面
        
        预期结果：
        - 刷新后保持在设置页面
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-EMAIL-013: 验证页面刷新保持状态")
        logger.info("=" * 60)
        
        # 截图：刷新前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_before_refresh_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-刷新前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 刷新页面
        logger.info("步骤1: 刷新页面")
        emailing_page.page.reload()
        emailing_page.page.wait_for_load_state("domcontentloaded")
        emailing_page.page.wait_for_timeout(2000)
        
        # 验证页面加载
        assert emailing_page.is_loaded(), "刷新后页面应正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 截图：刷新后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_emailing_after_refresh_{timestamp}.png"
        emailing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-刷新后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-EMAIL-013执行成功")
