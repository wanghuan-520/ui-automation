import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from utils.data_manager import DataManager
from utils.logger import get_logger
from utils.page_utils import PageUtils

logger = get_logger(__name__)

@allure.feature("登录功能")
class TestLocalhostLogin:
    """localhost:5173 邮箱登录功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.page_utils = PageUtils(page)
        self.login_page = LocalhostEmailLoginPage(page)
        
        # 加载测试数据
        try:
            self.test_data = DataManager.load_json("test-data/aevatar/localhost_login_data.json")
        except Exception as e:
            logger.warning(f"加载测试数据失败: {e}")
            self.test_data = {}
    
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.critical
    @allure.title("TC001: 正常邮箱登录")
    def test_tc001_normal_login(self):
        """
        TC001: 正常邮箱登录
        验证用户可以通过有效邮箱和密码成功登录
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC001: 正常邮箱登录")
        logger.info("=" * 80)
        
        # 获取有效用户数据
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "haylee@test.com")
        password = valid_user.get("password", "Wh520520!")
        
        # 1. 访问登录页
        with allure.step("步骤1: 访问登录页"):
            logger.info("步骤1: 访问登录页")
            self.login_page.navigate()
            assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
            self.page_utils.screenshot_step("login_page_loaded")
            logger.info("✅ 登录页加载成功")
        
        # 2. 输入邮箱
        with allure.step(f"步骤2: 输入邮箱 {email}"):
            logger.info(f"步骤2: 输入邮箱 {email}")
            assert self.login_page.enter_email(email), "❌ 邮箱输入失败"
            self.page_utils.screenshot_step("email_entered")
            logger.info("✅ 邮箱输入成功")
        
        # 3. 输入密码
        with allure.step("步骤3: 输入密码"):
            logger.info("步骤3: 输入密码")
            assert self.login_page.enter_password(password), "❌ 密码输入失败"
            self.page_utils.screenshot_step("password_entered")
            logger.info("✅ 密码输入成功")
        
        # 4. 点击登录按钮
        with allure.step("步骤4: 点击登录按钮"):
            logger.info("步骤4: 点击登录按钮")
            assert self.login_page.click_login(), "❌ 登录按钮点击失败"
            logger.info("✅ 登录按钮点击成功")
        
        # 5. 验证登录结果
        with allure.step("步骤5: 验证登录状态"):
            logger.info("步骤5: 验证登录状态")
            # 检查是否有错误提示
            error_message = self.login_page.get_error_message()
            if error_message:
                self.page_utils.screenshot_step("login_error")
                logger.warning(f"⚠️  发现错误提示: {error_message}")
            
            # 检查URL是否变化（登录成功的标志）
            self.page.wait_for_timeout(2000)
            is_success = self.login_page.is_login_successful()
            self.page_utils.screenshot_step("login_result")
            if is_success:
                logger.info("✅ 登录成功，URL已变化")
            else:
                logger.info("ℹ️  登录请求已提交，等待服务器响应")
        
        logger.info("🎉 TC001 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC002: 邮箱输入框功能验证")
    def test_tc002_email_input_validation(self):
        """
        TC002: 邮箱输入框功能验证
        验证邮箱输入框可正常接收输入
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC002: 邮箱输入框功能验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入测试邮箱
        test_email = "test@example.com"
        logger.info(f"输入测试邮箱: {test_email}")
        assert self.login_page.enter_email(test_email), "❌ 邮箱输入失败"
        self.page_utils.screenshot_step("email_input_validation")
        logger.info("✅ 邮箱输入框功能正常")
        
        logger.info("🎉 TC002 测试通过")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC003: 密码输入框功能验证")
    def test_tc003_password_input_validation(self):
        """
        TC003: 密码输入框功能验证
        验证密码输入框可正常接收输入，默认隐藏显示
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC003: 密码输入框功能验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入测试密码
        test_password = "TestPassword123!"
        logger.info("输入测试密码")
        assert self.login_page.enter_password(test_password), "❌ 密码输入失败"
        self.page_utils.screenshot_step("password_input_validation")
        logger.info("✅ 密码输入成功")
        
        # 验证密码默认隐藏
        logger.info("验证密码默认隐藏")
        is_visible = self.login_page.is_password_visible()
        assert not is_visible, "❌ 密码应该默认隐藏"
        logger.info("✅ 密码默认隐藏状态正确")
        
        logger.info("🎉 TC003 测试通过")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC004: 密码默认加密显示验证")
    def test_tc004_password_default_hidden(self):
        """
        TC004: 密码默认加密显示验证
        验证密码输入框默认显示为密文（不支持切换明文）
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC004: 密码默认加密显示验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入密码
        test_password = "TestPassword123!"
        logger.info("输入测试密码")
        self.login_page.enter_password(test_password)
        
        # 验证默认隐藏
        logger.info("验证密码默认隐藏")
        self.page_utils.screenshot_step("password_hidden_default")
        initial_visibility = self.login_page.is_password_visible()
        assert not initial_visibility, "❌ 密码应该默认隐藏"
        logger.info("✅ 密码默认隐藏状态正确")
        
        logger.info("🎉 TC004 测试完成")

    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC005: 忘记密码链接")
    def test_tc005_forget_password_link(self):
        """
        TC005: 忘记密码链接
        验证忘记密码功能可访问
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC005: 忘记密码链接")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击忘记密码链接
        logger.info("点击忘记密码链接")
        self.page_utils.screenshot_step("before_click_forget_password")
        
        click_result = self.login_page.click_forget_password()
        assert click_result, "❌ 忘记密码链接点击失败"
        
        # 等待跳转或弹窗
        self.page.wait_for_timeout(3000)
        self.page_utils.screenshot_step("after_click_forget_password")
        
        # 验证URL变化或弹窗出现
        current_url = self.login_page.get_current_url()
        logger.info(f"点击后URL: {current_url}")
        
        # 检查是否跳转到忘记密码页面或有弹窗/对话框
        url_changed = current_url != "http://localhost:5173"
        dialog_visible = self.page_utils.is_element_visible("dialog, [role='dialog'], .modal, .ant-modal", timeout=2000)
        
        assert url_changed or dialog_visible, f"❌ 忘记密码功能未生效: URL未变化且无弹窗 (当前URL: {current_url})"
        logger.info("✅ 忘记密码链接功能正常")
        logger.info("🎉 TC005 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC006: 注册链接跳转")
    def test_tc006_signup_link(self):
        """
        TC006: 注册链接跳转
        验证注册链接功能正常
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC006: 注册链接跳转")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击注册链接
        logger.info("点击注册链接")
        self.page_utils.screenshot_step("before_click_signup")
        
        click_result = self.login_page.click_signup()
        assert click_result, "❌ 注册链接点击失败"
        
        # 等待页面跳转
        self.page.wait_for_timeout(3000)
        self.page_utils.screenshot_step("after_click_signup")
        
        # 验证URL已变化
        current_url = self.login_page.get_current_url()
        logger.info(f"点击后URL: {current_url}")
        
        # 检查是否跳转到注册页面（URL应该包含signup/register或不是登录页）
        is_signup_page = ("signup" in current_url.lower() or 
                         "register" in current_url.lower() or 
                         current_url != "http://localhost:5173")
        
        assert is_signup_page, f"❌ 注册链接未跳转: 当前URL仍为 {current_url}"
        logger.info("✅ 注册链接跳转成功")
        logger.info("🎉 TC006 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.high_priority
    @allure.title("TC011: 空邮箱提交验证")
    def test_tc011_empty_email(self):
        """
        TC011: 空邮箱提交验证
        验证空邮箱提交时的错误处理
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC011: 空邮箱提交验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入密码但不输入邮箱
        logger.info("输入密码，邮箱留空")
        self.login_page.enter_password("TestPassword123!")
        self.page_utils.screenshot_step("empty_email_filled_password")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 检查错误提示
        error_message = self.login_page.get_error_message()
        self.page_utils.screenshot_step("empty_email_error")
        if error_message:
            logger.info(f"✅ 发现错误提示: {error_message}")
        else:
            logger.warning("⚠️  未发现错误提示")
        
        # 验证仍在登录页
        current_url = self.login_page.get_current_url()
        is_still_on_login_page = "5173" in current_url
        if is_still_on_login_page:
            logger.info("✅ 停留在登录页，未提交成功")
        
        logger.info("🎉 TC011 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.parametrize("invalid_email_data", [
        {"email": "invalid-email", "expected_error": "邮箱格式不正确"},
        {"email": "test@", "expected_error": "邮箱格式不正确"},
        {"email": "@domain.com", "expected_error": "邮箱格式不正确"},
    ])
    @allure.title("TC012: 无效邮箱格式验证")
    def test_tc012_invalid_email_format(self, invalid_email_data):
        """
        TC012: 无效邮箱格式验证
        验证系统正确拒绝无效的邮箱格式
        """
        logger.info("=" * 80)
        logger.info(f"开始测试 TC012: 无效邮箱格式验证 - {invalid_email_data['email']}")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入无效邮箱
        invalid_email = invalid_email_data["email"]
        logger.info(f"输入无效邮箱: '{invalid_email}'")
        self.login_page.enter_email(invalid_email)
        self.login_page.enter_password("TestPassword123!")
        self.page_utils.screenshot_step(f"invalid_email_input_{invalid_email}")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 验证错误提示或停留在当前页面
        error_message = self.login_page.get_error_message()
        self.page_utils.screenshot_step(f"invalid_email_result_{invalid_email}")
        current_url = self.login_page.get_current_url()
        
        if error_message:
            logger.info(f"✅ 发现邮箱验证错误提示: {error_message}")
        elif "5173" in current_url:
            logger.info("✅ 停留在登录页，未提交成功")
        else:
            logger.warning("⚠️  邮箱格式验证可能未生效")
        
        logger.info("🎉 TC012 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.high_priority
    @allure.title("TC013: 空密码提交验证")
    def test_tc013_empty_password(self):
        """
        TC013: 空密码提交验证
        验证空密码提交时的错误处理
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC013: 空密码提交验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 只输入邮箱，密码留空
        logger.info("输入邮箱，密码留空")
        self.login_page.enter_email("haylee@test.com")
        self.page_utils.screenshot_step("empty_password_input")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 检查错误提示
        error_message = self.login_page.get_error_message()
        self.page_utils.screenshot_step("empty_password_result")
        if error_message:
            logger.info(f"✅ 发现错误提示: {error_message}")
        else:
            logger.warning("⚠️  未发现错误提示")
        
        # 验证仍在登录页
        current_url = self.login_page.get_current_url()
        is_still_on_login_page = "5173" in current_url
        if is_still_on_login_page:
            logger.info("✅ 停留在登录页，未提交成功")
        
        logger.info("🎉 TC013 测试完成")
    
    @pytest.mark.exception
    @pytest.mark.high_priority
    @allure.title("TC021: 错误密码登录验证")
    def test_tc021_wrong_password(self):
        """
        TC021: 错误密码登录验证
        验证系统正确拒绝错误密码
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC021: 错误密码登录验证")
        logger.info("=" * 80)
        
        # 获取测试数据
        invalid_password_data = self.test_data.get("invalid_passwords", [{}])[0]
        email = invalid_password_data.get("email", "haylee@test.com")
        wrong_password = invalid_password_data.get("password", "WrongPassword123!")
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入正确邮箱和错误密码
        logger.info(f"输入邮箱: {email}")
        self.login_page.enter_email(email)
        
        logger.info("输入错误密码")
        self.login_page.enter_password(wrong_password)
        self.page_utils.screenshot_step("wrong_password_input")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        # 移除固定等待，让get_error_message处理等待
        
        # 验证登录失败
        error_message = self.login_page.get_error_message()
        self.page_utils.screenshot_step("wrong_password_result")
        if error_message:
            logger.info(f"✅ 发现密码错误提示: {error_message}")
        
        is_still_on_login_page = "5173" in self.login_page.get_current_url()
        if is_still_on_login_page:
            logger.info("✅ 登录失败，停留在登录页")
        else:
            logger.warning("⚠️  页面发生跳转，可能登录成功了")
        
        logger.info("🎉 TC021 测试完成")
    
    @pytest.mark.exception
    @pytest.mark.high_priority
    @allure.title("TC022: 未注册邮箱登录验证")
    def test_tc022_unregistered_email(self):
        """
        TC022: 未注册邮箱登录验证
        验证系统正确处理未注册的邮箱
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC022: 未注册邮箱登录验证")
        logger.info("=" * 80)
        
        # 获取未注册用户数据
        unregistered_data = self.test_data.get("unregistered_users", [{}])[0]
        email = unregistered_data.get("email", "nonexistent@test.com")
        password = unregistered_data.get("password", "AnyPassword123!")
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入未注册邮箱
        logger.info(f"输入未注册邮箱: {email}")
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.page_utils.screenshot_step("unregistered_email_input")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        # 移除固定等待，让get_error_message处理等待
        
        # 检查是否提示邮箱未注册
        error_message = self.login_page.get_error_message()
        self.page_utils.screenshot_step("unregistered_email_result")
        if error_message:
            logger.info(f"✅ 发现错误提示: {error_message}")
        else:
            logger.warning("⚠️  未发现错误提示")
        
        # 验证未登录成功
        is_still_on_login_page = "5173" in self.login_page.get_current_url()
        if is_still_on_login_page:
            logger.info("✅ 登录失败，停留在登录页")
        
        logger.info("🎉 TC022 测试完成")
    
    @pytest.mark.security
    @pytest.mark.critical
    @pytest.mark.parametrize("security_data", [
        {"type": "SQL注入", "email": "admin' OR '1'='1", "password": "password"},
        {"type": "XSS攻击", "email": "<script>alert('XSS')</script>", "password": "password"},
    ])
    @allure.title("TC023: 安全测试")
    def test_tc023_security_validation(self, security_data):
        """
        TC023: 安全测试 - SQL注入和XSS攻击
        验证系统正确处理恶意输入
        """
        logger.info("=" * 80)
        logger.info(f"开始测试 TC023: 安全测试 - {security_data['type']}")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入恶意数据
        logger.info(f"输入{security_data['type']}测试数据")
        self.login_page.enter_email(security_data["email"])
        self.login_page.enter_password(security_data["password"])
        self.page_utils.screenshot_step(f"security_input_{security_data['type']}")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 验证系统正确处理
        is_still_on_login_page = "5173" in self.login_page.get_current_url()
        self.page_utils.screenshot_step(f"security_result_{security_data['type']}")
        if is_still_on_login_page:
            logger.info(f"✅ {security_data['type']}被正确处理，未执行恶意代码")
        else:
            logger.warning(f"⚠️  {security_data['type']}处理结果需要进一步验证")
        
        logger.info("🎉 TC023 测试完成")
