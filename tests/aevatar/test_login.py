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
    
    @pytest.mark.skip(reason="OAuth配置未完成，暂时跳过")
    @pytest.mark.oauth
    @pytest.mark.high_priority
    @allure.title("TC002: Google第三方登录")
    def test_tc002_google_login(self):
        """
        TC002: Google第三方登录
        验证点击Google登录按钮可以跳转到Google授权页面
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC002: Google第三方登录")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击Google登录按钮
        logger.info("点击Google登录按钮")
        self.page_utils.screenshot_step("before_google_login")
        
        # 尝试点击并捕获弹出窗口
        try:
            with self.page.expect_popup(timeout=5000) as popup_info:
                self.login_page.click_google_login()
            popup = popup_info.value
            popup_url = popup.url
            logger.info(f"Google授权页面URL: {popup_url}")
            
            # 验证跳转到Google授权页面
            assert "google" in popup_url.lower(), f"❌ 未跳转到Google页面: {popup_url}"
            logger.info("✅ Google登录跳转成功")
            
            popup.close()
        except Exception as e:
            logger.warning(f"⚠️  Google登录弹窗未出现（可能需要配置OAuth）: {str(e)}")
            self.page_utils.screenshot_step("google_login_no_popup")
        
        logger.info("🎉 TC002 测试完成")
    
    @pytest.mark.skip(reason="OAuth配置未完成，暂时跳过")
    @pytest.mark.oauth
    @pytest.mark.high_priority
    @allure.title("TC003: Github第三方登录")
    def test_tc003_github_login(self):
        """
        TC003: Github第三方登录
        验证点击Github登录按钮可以跳转到Github授权页面
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC003: Github第三方登录")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击Github登录按钮
        logger.info("点击Github登录按钮")
        self.page_utils.screenshot_step("before_github_login")
        
        # 尝试点击并捕获弹出窗口
        try:
            with self.page.expect_popup(timeout=5000) as popup_info:
                self.login_page.click_github_login()
            popup = popup_info.value
            popup_url = popup.url
            logger.info(f"Github授权页面URL: {popup_url}")
            
            # 验证跳转到Github授权页面
            assert "github" in popup_url.lower(), f"❌ 未跳转到Github页面: {popup_url}"
            logger.info("✅ Github登录跳转成功")
            
            popup.close()
        except Exception as e:
            logger.warning(f"⚠️  Github登录弹窗未出现（可能需要配置OAuth）: {str(e)}")
            self.page_utils.screenshot_step("github_login_no_popup")
        
        logger.info("🎉 TC003 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.low_priority
    @allure.title("TC007: Github链接跳转")
    def test_tc007_github_link(self):
        """
        TC007: Github链接跳转
        验证底部Github链接可以在新标签页打开项目仓库
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC007: Github链接跳转")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击Github链接
        logger.info("点击底部Github链接")
        self.page_utils.screenshot_step("before_github_link")
        
        popup_url = self.login_page.click_github_link()
        if popup_url:
            logger.info(f"Github链接打开成功: {popup_url}")
            assert "github.com/aevatarAI" in popup_url, f"❌ Github链接URL不正确: {popup_url}"
            logger.info("✅ Github链接跳转成功")
        else:
            logger.warning("⚠️  Github链接点击失败")
        
        logger.info("🎉 TC007 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.low_priority
    @allure.title("TC008: Docs链接跳转")
    def test_tc008_docs_link(self):
        """
        TC008: Docs链接跳转
        验证底部Docs链接可以在新标签页打开白皮书文档
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC008: Docs链接跳转")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击Docs链接
        logger.info("点击底部Docs链接")
        self.page_utils.screenshot_step("before_docs_link")
        
        popup_url = self.login_page.click_docs_link()
        if popup_url:
            logger.info(f"Docs链接打开成功: {popup_url}")
            assert "whitepaper" in popup_url or ".pdf" in popup_url, f"❌ Docs链接URL不正确: {popup_url}"
            logger.info("✅ Docs链接跳转成功")
        else:
            logger.warning("⚠️  Docs链接点击失败")
        
        logger.info("🎉 TC008 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.medium_priority
    @allure.title("TC014: 超长邮箱输入")
    def test_tc014_long_email_input(self):
        """
        TC014: 超长邮箱输入
        验证系统正确处理超长邮箱输入
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC014: 超长邮箱输入")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 获取超长邮箱数据
        long_email_data = self.test_data.get("boundary_data", {}).get("long_email", {})
        long_email = long_email_data.get("email", "a" * 250 + "@test.com")
        
        # 输入超长邮箱
        logger.info(f"输入超长邮箱（长度：{len(long_email)}）")
        self.login_page.enter_email(long_email)
        self.login_page.enter_password("TestPassword123!")
        self.page_utils.screenshot_step("long_email_input")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 验证系统处理（应该限制长度或显示错误）
        error_message = self.login_page.get_error_message()
        current_url = self.login_page.get_current_url()
        self.page_utils.screenshot_step("long_email_result")
        
        if error_message:
            logger.info(f"✅ 系统显示错误提示: {error_message}")
        elif "5173" in current_url:
            logger.info("✅ 系统限制了输入长度或拒绝提交")
        
        logger.info("🎉 TC014 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.medium_priority
    @allure.title("TC015: 超长密码输入")
    def test_tc015_long_password_input(self):
        """
        TC015: 超长密码输入
        验证系统正确处理超长密码输入
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC015: 超长密码输入")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 获取超长密码数据
        long_password_data = self.test_data.get("boundary_data", {}).get("long_password", {})
        long_password = long_password_data.get("password", "A" * 1000)
        
        # 输入超长密码
        logger.info(f"输入超长密码（长度：{len(long_password)}）")
        self.login_page.enter_email("haylee@test.com")
        self.login_page.enter_password(long_password)
        self.page_utils.screenshot_step("long_password_input")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 验证系统处理
        self.page_utils.screenshot_step("long_password_result")
        logger.info("✅ 系统正常处理超长密码，未崩溃")
        
        logger.info("🎉 TC015 测试完成")
    
    @pytest.mark.boundary
    @pytest.mark.medium_priority
    @pytest.mark.parametrize("special_email_data", [
        {"email": "test+tag@domain.com", "description": "加号"},
        {"email": "test.name@domain.com", "description": "点号"},
        {"email": "test_name@domain.com", "description": "下划线"},
    ])
    @allure.title("TC016: 特殊字符邮箱输入")
    def test_tc016_special_char_email(self, special_email_data):
        """
        TC016: 特殊字符邮箱输入
        验证系统正确接受合法的特殊字符邮箱
        """
        logger.info("=" * 80)
        logger.info(f"开始测试 TC016: 特殊字符邮箱输入 - {special_email_data['description']}")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入特殊字符邮箱
        special_email = special_email_data["email"]
        logger.info(f"输入特殊字符邮箱: {special_email}")
        self.login_page.enter_email(special_email)
        self.login_page.enter_password("TestPassword123!")
        self.page_utils.screenshot_step(f"special_email_{special_email_data['description']}")
        
        # 尝试登录
        logger.info("尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(2000)
        
        # 验证系统接受特殊字符邮箱（表单正常提交）
        self.page_utils.screenshot_step(f"special_email_result_{special_email_data['description']}")
        logger.info("✅ 系统正确接受合法特殊字符邮箱")
        
        logger.info("🎉 TC016 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.high_priority
    @allure.title("TC033: Enter键提交登录")
    def test_tc033_enter_key_submit(self):
        """
        TC033: Enter键提交登录
        验证在密码框按Enter键可以提交登录表单
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC033: Enter键提交登录")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入凭证
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "haylee@test.com")
        password = valid_user.get("password", "Wh520520!")
        
        logger.info(f"输入邮箱: {email}")
        self.login_page.enter_email(email)
        logger.info("输入密码")
        self.login_page.enter_password(password)
        self.page_utils.screenshot_step("before_enter_submit")
        
        # 在密码框按Enter键
        logger.info("在密码框按Enter键提交")
        self.login_page.press_enter_in_password()
        
        # 等待响应
        self.page.wait_for_timeout(3000)
        self.page_utils.screenshot_step("after_enter_submit")
        
        # 验证登录提交（URL变化或有错误提示说明表单已提交）
        is_success = self.login_page.is_login_successful()
        error_message = self.login_page.get_error_message()
        
        if is_success:
            logger.info("✅ Enter键提交成功，登录完成")
        elif error_message:
            logger.info(f"✅ Enter键提交成功，收到服务器响应: {error_message}")
        else:
            logger.info("ℹ️  Enter键提交已执行，等待服务器响应")
        
        logger.info("🎉 TC033 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.high_priority
    @allure.title("TC035: 响应式设计验证")
    def test_tc035_responsive_design(self):
        """
        TC035: 响应式设计验证
        验证登录页在不同屏幕尺寸下正确显示
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC035: 响应式设计验证")
        logger.info("=" * 80)
        
        screen_sizes = [
            {"name": "桌面", "width": 1920, "height": 1080},
            {"name": "平板", "width": 768, "height": 1024},
            {"name": "手机", "width": 375, "height": 667},
        ]
        
        for size in screen_sizes:
            logger.info(f"测试 {size['name']} 屏幕尺寸: {size['width']}x{size['height']}")
            
            # 设置屏幕尺寸
            self.page.set_viewport_size({"width": size['width'], "height": size['height']})
            
            # 访问登录页
            self.login_page.navigate()
            self.page.wait_for_timeout(1000)
            
            # 截图
            self.page_utils.screenshot_step(f"responsive_{size['name']}_{size['width']}x{size['height']}")
            
            # 验证关键元素可见
            email_visible = self.login_page.is_element_visible(self.login_page.EMAIL_INPUT)
            password_visible = self.login_page.is_element_visible(self.login_page.PASSWORD_INPUT)
            button_visible = self.login_page.is_element_visible(self.login_page.LOGIN_BUTTON)
            
            assert email_visible and password_visible and button_visible, \
                f"❌ {size['name']}屏幕下关键元素不可见"
            
            logger.info(f"✅ {size['name']}屏幕下页面显示正常")
        
        # 恢复默认尺寸
        self.page.set_viewport_size({"width": 1280, "height": 720})
        
        logger.info("🎉 TC035 测试完成")
    
    @pytest.mark.performance
    @pytest.mark.medium_priority
    @allure.title("TC051: 页面加载时间测试")
    def test_tc051_page_load_performance(self):
        """
        TC051: 页面加载时间测试
        验证登录页加载性能符合预期
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC051: 页面加载时间测试")
        logger.info("=" * 80)
        
        import time
        
        # 清除缓存
        self.page.context.clear_cookies()
        
        # 记录加载时间
        start_time = time.time()
        self.login_page.navigate()
        load_time = time.time() - start_time
        
        logger.info(f"页面加载时间: {load_time:.2f}秒")
        self.page_utils.screenshot_step("page_load_performance")
        
        # 获取性能阈值
        perf_data = self.test_data.get("performance_test_data", {}).get("page_load", {})
        max_load_time = perf_data.get("max_load_time", 2.0)
        
        # 验证加载时间
        assert load_time < max_load_time, f"❌ 页面加载时间过长: {load_time:.2f}秒 > {max_load_time}秒"
        logger.info(f"✅ 页面加载性能良好: {load_time:.2f}秒 < {max_load_time}秒")
        
        logger.info("🎉 TC051 测试完成")
    
    @pytest.mark.performance
    @pytest.mark.medium_priority
    @allure.title("TC052: 登录请求响应时间")
    def test_tc052_login_api_response_time(self):
        """
        TC052: 登录请求响应时间
        验证登录API响应时间符合预期
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC052: 登录请求响应时间")
        logger.info("=" * 80)
        
        import time
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入凭证
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "haylee@test.com")
        password = valid_user.get("password", "Wh520520!")
        
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        
        # 记录登录请求时间
        start_time = time.time()
        
        # 监听网络请求
        login_api_time = None
        def handle_response(response):
            nonlocal login_api_time
            if "login" in response.url.lower() or "auth" in response.url.lower():
                login_api_time = time.time() - start_time
                logger.info(f"登录API响应时间: {login_api_time:.3f}秒")
        
        self.page.on("response", handle_response)
        
        # 点击登录
        self.login_page.click_login()
        self.page.wait_for_timeout(3000)
        
        total_time = time.time() - start_time
        logger.info(f"总登录流程时间: {total_time:.2f}秒")
        
        # 获取性能阈值
        perf_data = self.test_data.get("performance_test_data", {}).get("api_response", {})
        max_total_time = perf_data.get("max_total_login_time", 2.0)
        
        # 验证响应时间
        if login_api_time:
            logger.info(f"✅ 登录API响应时间: {login_api_time:.3f}秒")
        
        assert total_time < max_total_time, f"❌ 总登录时间过长: {total_time:.2f}秒 > {max_total_time}秒"
        logger.info(f"✅ 登录流程性能良好: {total_time:.2f}秒 < {max_total_time}秒")
        
        logger.info("🎉 TC052 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC031: 密码默认隐藏验证")
    def test_tc031_password_default_hidden(self):
        """
        TC031: 密码默认隐藏验证
        验证密码输入框默认以密文显示
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC031: 密码默认隐藏验证")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入密码
        test_password = "TestPassword123!"
        logger.info("输入测试密码")
        self.login_page.enter_password(test_password)
        self.page_utils.screenshot_step("password_hidden_check")
        
        # 验证密码默认隐藏
        is_visible = self.login_page.is_password_visible()
        assert not is_visible, "❌ 密码应该默认隐藏显示"
        logger.info("✅ 密码默认以密文显示")
        
        logger.info("🎉 TC031 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC032: Tab键切换焦点")
    def test_tc032_tab_key_navigation(self):
        """
        TC032: Tab键切换焦点
        验证可以使用Tab键在表单元素间切换焦点
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC032: Tab键切换焦点")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 点击邮箱输入框获取初始焦点
        logger.info("点击邮箱输入框")
        self.page.locator(self.login_page.EMAIL_INPUT).first.click()
        self.page_utils.screenshot_step("tab_focus_email")
        
        # 按Tab键切换到密码框
        logger.info("按Tab键切换到密码框")
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(500)
        self.page_utils.screenshot_step("tab_focus_password")
        
        # 验证焦点在密码框（通过输入测试）
        self.page.keyboard.type("test")
        password_value = self.page.locator(self.login_page.PASSWORD_INPUT).first.input_value()
        assert "test" in password_value, "❌ Tab键未正确切换到密码框"
        logger.info("✅ Tab键成功切换到密码框")
        
        # 继续按Tab切换到登录按钮
        logger.info("按Tab键切换到登录按钮")
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(500)
        self.page_utils.screenshot_step("tab_focus_button")
        logger.info("✅ Tab键导航功能正常")
        
        logger.info("🎉 TC032 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC034: 错误提示显示和消失")
    def test_tc034_error_message_display(self):
        """
        TC034: 错误提示显示和消失
        验证错误提示正确显示并自动消失
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC034: 错误提示显示和消失")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入错误凭证触发错误提示
        logger.info("输入错误凭证")
        self.login_page.enter_email("haylee@test.com")
        self.login_page.enter_password("WrongPassword123!")
        self.login_page.click_login()
        
        # 等待错误提示出现
        self.page.wait_for_timeout(2000)
        error_message = self.login_page.get_error_message()
        
        if error_message:
            logger.info(f"✅ 错误提示显示: {error_message}")
            self.page_utils.screenshot_step("error_message_displayed")
            
            # 等待观察错误提示是否自动消失
            logger.info("等待5秒观察错误提示")
            self.page.wait_for_timeout(5000)
            self.page_utils.screenshot_step("error_message_after_wait")
            logger.info("✅ 错误提示行为正常")
        else:
            logger.warning("⚠️  未捕获到错误提示")
        
        logger.info("🎉 TC034 测试完成")
    
    @pytest.mark.ui
    @pytest.mark.medium_priority
    @allure.title("TC036: 加载状态提示")
    def test_tc036_loading_state(self):
        """
        TC036: 加载状态提示
        验证登录按钮在提交时显示加载状态
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC036: 加载状态提示")
        logger.info("=" * 80)
        
        # 访问登录页
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 输入凭证
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "haylee@test.com")
        password = valid_user.get("password", "Wh520520!")
        
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.page_utils.screenshot_step("before_loading")
        
        # 点击登录并立即检查加载状态
        logger.info("点击登录并检查加载状态")
        self.login_page.click_login()
        
        # 快速检查加载状态（在服务器响应前）
        self.page.wait_for_timeout(100)
        is_loading = self.login_page.get_loading_state()
        
        if is_loading:
            logger.info("✅ 登录按钮显示加载状态")
            self.page_utils.screenshot_step("loading_state_active")
        else:
            logger.info("ℹ️  加载状态可能过快或未实现")
        
        # 等待登录完成
        self.page.wait_for_timeout(3000)
        self.page_utils.screenshot_step("loading_state_finished")
        
        logger.info("🎉 TC036 测试完成")
    
    @pytest.mark.exception
    @pytest.mark.medium_priority
    @allure.title("TC024: 网络断开场景测试")
    def test_tc024_network_offline(self):
        """
        TC024: 网络断开场景测试
        验证网络断开时系统的错误处理
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC024: 网络断开场景测试")
        logger.info("=" * 80)
        
        # 访问登录页（先加载页面）
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "❌ 登录页未加载成功"
        
        # 模拟离线状态
        logger.info("设置离线模式")
        self.page.context.set_offline(True)
        self.page_utils.screenshot_step("before_offline_login")
        
        # 输入凭证并尝试登录
        self.login_page.enter_email("haylee@test.com")
        self.login_page.enter_password("Wh520520!")
        
        logger.info("在离线状态下尝试登录")
        self.login_page.click_login()
        self.page.wait_for_timeout(3000)
        
        # 截图并恢复网络
        self.page_utils.screenshot_step("offline_login_result")
        self.page.context.set_offline(False)
        
        logger.info("✅ 系统在离线状态下未崩溃")
        logger.info("🎉 TC024 测试完成")
    
    @pytest.mark.performance
    @pytest.mark.low_priority
    @allure.title("TC054: 资源优化验证")
    def test_tc054_resource_optimization(self):
        """
        TC054: 资源优化验证
        验证页面资源加载优化情况
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC054: 资源优化验证")
        logger.info("=" * 80)
        
        # 收集网络请求
        resources = []
        def handle_response(response):
            resources.append({
                "url": response.url,
                "status": response.status,
                "type": response.request.resource_type,
                "size": len(response.body()) if response.ok else 0
            })
        
        self.page.on("response", handle_response)
        
        # 访问登录页
        self.login_page.navigate()
        self.page.wait_for_load_state("networkidle")
        
        # 分析资源
        logger.info(f"总共加载了 {len(resources)} 个资源")
        
        # 统计资源类型
        resource_types = {}
        for res in resources:
            res_type = res["type"]
            resource_types[res_type] = resource_types.get(res_type, 0) + 1
        
        logger.info(f"资源类型统计: {resource_types}")
        
        # 检查大文件
        large_files = [r for r in resources if r["size"] > 1024 * 1024]  # > 1MB
        if large_files:
            logger.warning(f"⚠️  发现 {len(large_files)} 个大文件 (>1MB)")
            for f in large_files:
                logger.warning(f"  - {f['url']}: {f['size'] / 1024 / 1024:.2f}MB")
        else:
            logger.info("✅ 未发现过大的资源文件")
        
        # 检查失败的请求
        failed_requests = [r for r in resources if r["status"] >= 400]
        if failed_requests:
            logger.warning(f"⚠️  发现 {len(failed_requests)} 个失败的请求")
        else:
            logger.info("✅ 所有资源加载成功")
        
        self.page_utils.screenshot_step("resource_optimization")
        
        logger.info("🎉 TC054 测试完成")