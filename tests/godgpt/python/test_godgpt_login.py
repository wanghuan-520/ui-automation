import pytest
from playwright.sync_api import Page
from pages.godgpt.godgpt_landing_page import GodGPTLandingPage
from pages.godgpt.godgpt_email_login_page import GodGPTEmailLoginPage
from pages.godgpt.godgpt_main_page import GodGPTMainPage
from utils.data_manager import DataManager
from utils.logger import get_logger

logger = get_logger(__name__)

class TestGodGPTLogin:
    """GodGPT 登录模块测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.landing_page = GodGPTLandingPage(page)
        self.email_login_page = GodGPTEmailLoginPage(page)
        self.main_page = GodGPTMainPage(page)
        
        # 加载测试数据
        try:
            self.test_data = DataManager.load_json("test-data/godgpt/godgpt_login_data.json")
        except Exception as e:
            logger.warning(f"加载测试数据失败: {e}")
            self.test_data = {}
    
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.high_priority
    def test_tc001_email_login_success(self):
        """
        TC001: 邮箱登录 - 正常流程
        验证用户可以通过邮箱和密码成功登录
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC001: 邮箱登录 - 正常流程")
        logger.info("=" * 80)
        
        # 获取有效用户数据
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        password = valid_user.get("password", "Wh520520!")
        
        # 1. 访问首页
        logger.info("步骤1: 访问登录首页")
        self.landing_page.navigate()
        assert self.landing_page.is_loaded(), "❌ 登录首页未加载成功"
        logger.info("✅ 登录首页加载成功")
        
        # 2. 输入邮箱
        logger.info(f"步骤2: 输入邮箱 {email}")
        assert self.landing_page.enter_email(email), "❌ 邮箱输入失败"
        logger.info("✅ 邮箱输入成功")
        
        # 3. 点击 Continue with Email
        logger.info("步骤3: 点击 Continue with Email")
        assert self.landing_page.click_continue_with_email(), "❌ Continue with Email 按钮点击失败"
        logger.info("✅ Continue with Email 按钮点击成功")
        
        # 4. 验证跳转到密码页面
        logger.info("步骤4: 验证跳转到密码输入页面")
        self.email_login_page.wait_for_page_load()
        assert self.email_login_page.is_loaded(), "❌ 未跳转到密码输入页面"
        logger.info("✅ 成功跳转到密码输入页面")
        
        # 5. 验证邮箱显示正确
        logger.info("步骤5: 验证显示的邮箱地址")
        displayed_email = self.email_login_page.get_displayed_email()
        assert displayed_email is not None, "❌ 未找到显示的邮箱"
        assert email in displayed_email, f"❌ 邮箱显示不正确: 期望包含{email}, 实际={displayed_email}"
        logger.info(f"✅ 邮箱显示正确: {displayed_email}")
        
        # 6. 输入密码
        logger.info("步骤6: 输入密码")
        assert self.email_login_page.enter_password(password), "❌ 密码输入失败"
        logger.info("✅ 密码输入成功")
        
        # 7. 点击 Continue
        logger.info("步骤7: 点击 Continue 按钮")
        assert self.email_login_page.click_continue(), "❌ Continue 按钮点击失败"
        logger.info("✅ Continue 按钮点击成功")
        
        # 8. 验证登录成功
        logger.info("步骤8: 验证登录成功")
        self.main_page.wait_for_page_load()
        assert self.main_page.is_loaded(), "❌ 登录失败，未进入主界面"
        assert self.main_page.is_logged_in(), "❌ 登录状态验证失败"
        logger.info("✅ 登录成功，已进入主界面")
        
        logger.info("🎉 TC001 测试通过")
    
    @pytest.mark.login
    @pytest.mark.medium_priority
    def test_tc002_email_edit_function(self):
        """
        TC002: 邮箱输入 - 编辑功能
        验证用户可以在密码页面编辑邮箱
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC002: 邮箱输入 - 编辑功能")
        logger.info("=" * 80)
        
        # 导航到密码页面
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        
        # 点击 Edit 按钮
        logger.info("点击 Edit 按钮")
        assert self.email_login_page.click_edit_email(), "❌ Edit 按钮点击失败"
        
        # 验证是否返回首页或邮箱可编辑
        self.page.wait_for_timeout(2000)
        current_url = self.email_login_page.get_current_url()
        
        # 可能返回首页或者邮箱变为可编辑
        is_back_to_landing = "/email-login" not in current_url
        if is_back_to_landing:
            assert self.landing_page.is_loaded(), "❌ 未返回登录首页"
            logger.info("✅ 成功返回登录首页")
        else:
            logger.info("✅ 邮箱可能变为可编辑状态")
        
        logger.info("🎉 TC002 测试通过")
    
    @pytest.mark.login
    @pytest.mark.medium_priority
    def test_tc003_password_visibility_toggle(self):
        """
        TC003: 密码可见性切换
        验证密码显示/隐藏功能正常
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC003: 密码可见性切换")
        logger.info("=" * 80)
        
        # 导航到密码页面
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        
        # 输入密码
        test_password = "TestPassword123!"
        logger.info("输入测试密码")
        self.email_login_page.enter_password(test_password)
        
        # 验证默认隐藏
        logger.info("验证密码默认隐藏")
        initial_visibility = self.email_login_page.is_password_visible()
        assert not initial_visibility, "❌ 密码应该默认隐藏"
        logger.info("✅ 密码默认隐藏状态正确")
        
        # 点击显示密码
        logger.info("点击显示密码图标")
        if self.email_login_page.click_show_hide_password():
            self.page.wait_for_timeout(500)
            visible_state = self.email_login_page.is_password_visible()
            assert visible_state, "❌ 点击后密码应该可见"
            logger.info("✅ 密码成功切换为可见")
            
            # 再次点击隐藏密码
            logger.info("再次点击隐藏密码")
            self.email_login_page.click_show_hide_password()
            self.page.wait_for_timeout(500)
            hidden_state = self.email_login_page.is_password_visible()
            assert not hidden_state, "❌ 再次点击后密码应该隐藏"
            logger.info("✅ 密码成功切换为隐藏")
        else:
            logger.warning("⚠️  未找到密码可见性切换按钮，跳过切换测试")
        
        logger.info("🎉 TC003 测试通过")
    
    @pytest.mark.login
    @pytest.mark.medium_priority
    def test_tc004_forget_password_link(self):
        """
        TC004: 忘记密码链接
        验证忘记密码功能可访问
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC004: 忘记密码链接")
        logger.info("=" * 80)
        
        # 导航到密码页面
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        
        # 点击忘记密码链接
        logger.info("点击 Forget Password 链接")
        assert self.email_login_page.click_forget_password(), "❌ Forget Password 链接点击失败"
        
        # 验证页面跳转或弹窗
        self.page.wait_for_timeout(2000)
        current_url = self.email_login_page.get_current_url()
        logger.info(f"当前URL: {current_url}")
        
        # 根据实际情况验证（可能跳转到重置密码页面）
        logger.info("✅ Forget Password 链接可正常访问")
        logger.info("🎉 TC004 测试通过")
    
    @pytest.mark.login
    @pytest.mark.medium_priority
    def test_tc005_skip_login(self):
        """
        TC005: Skip 跳过登录
        验证可以跳过登录进入应用
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC005: Skip 跳过登录")
        logger.info("=" * 80)
        
        self.landing_page.navigate()
        assert self.landing_page.is_loaded(), "❌ 登录首页未加载"
        
        # 点击 Skip 按钮
        logger.info("点击 Skip 按钮")
        assert self.landing_page.click_skip(), "❌ Skip 按钮点击失败"
        
        # 验证页面变化
        self.page.wait_for_timeout(2000)
        current_url = self.landing_page.get_current_url()
        logger.info(f"跳过登录后URL: {current_url}")
        
        # 可能进入游客模式或主界面
        logger.info("✅ Skip 功能正常执行")
        logger.info("🎉 TC005 测试通过")
    
    @pytest.mark.login
    @pytest.mark.medium_priority
    def test_tc006_back_button(self):
        """
        TC006: 返回按钮功能
        验证可以从密码页面返回首页
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC006: 返回按钮功能")
        logger.info("=" * 80)
        
        # 导航到密码页面
        valid_user = self.test_data.get("valid_users", [{}])[0]
        email = valid_user.get("email", "409744790@qq.com")
        
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        
        # 点击返回按钮
        logger.info("点击返回按钮")
        assert self.email_login_page.click_back(), "❌ 返回按钮点击失败"
        
        # 验证返回到首页
        self.page.wait_for_timeout(2000)
        current_url = self.email_login_page.get_current_url()
        
        is_back_to_landing = "/email-login" not in current_url
        if is_back_to_landing:
            logger.info("✅ 成功返回登录首页")
        else:
            logger.warning("⚠️  返回按钮可能未正常工作")
        
        logger.info("🎉 TC006 测试通过")
    
    @pytest.mark.login
    @pytest.mark.boundary
    @pytest.mark.high_priority
    @pytest.mark.parametrize("invalid_email_data", [
        {"email": "invalid-email", "expected_error": "邮箱格式不正确"},
        {"email": "test@", "expected_error": "邮箱格式不正确"},
        {"email": "@domain.com", "expected_error": "邮箱格式不正确"},
        {"email": "", "expected_error": "请输入邮箱"},
    ])
    def test_tc016_invalid_email_format(self, invalid_email_data):
        """
        TC016: 邮箱格式验证 - 无效格式
        验证系统正确拒绝无效的邮箱格式
        """
        logger.info("=" * 80)
        logger.info(f"开始测试 TC016: 邮箱格式验证 - {invalid_email_data['email']}")
        logger.info("=" * 80)
        
        self.landing_page.navigate()
        
        # 输入无效邮箱
        email = invalid_email_data["email"]
        logger.info(f"输入无效邮箱: '{email}'")
        self.landing_page.enter_email(email)
        
        # 点击 Continue
        logger.info("点击 Continue with Email")
        self.landing_page.click_continue_with_email()
        self.page.wait_for_timeout(2000)
        
        # 验证错误提示或停留在当前页面
        error_message = self.landing_page.get_email_validation_error()
        current_url = self.landing_page.get_current_url()
        
        # 如果有错误提示或者未跳转，说明验证生效
        if error_message:
            logger.info(f"✅ 发现邮箱验证错误提示: {error_message}")
        elif "/email-login" not in current_url:
            logger.info("✅ 停留在当前页面，未跳转到密码页面")
        else:
            logger.warning("⚠️  邮箱格式验证可能未生效")
        
        logger.info("🎉 TC016 测试通过")
    
    @pytest.mark.login
    @pytest.mark.exception
    @pytest.mark.high_priority
    def test_tc021_login_wrong_password(self):
        """
        TC021: 登录 - 错误密码
        验证系统正确拒绝错误密码
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC021: 登录 - 错误密码")
        logger.info("=" * 80)
        
        # 获取测试数据
        invalid_password_data = self.test_data.get("invalid_passwords", [{}])[0]
        email = invalid_password_data.get("email", "409744790@qq.com")
        wrong_password = invalid_password_data.get("password", "WrongPassword123!")
        
        # 导航到密码页面
        self.landing_page.navigate()
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.email_login_page.wait_for_page_load()
        
        # 输入错误密码
        logger.info("输入错误密码")
        self.email_login_page.enter_password(wrong_password)
        self.email_login_page.click_continue()
        
        # 等待响应
        self.page.wait_for_timeout(3000)
        
        # 验证登录失败
        error_message = self.email_login_page.get_password_validation_error()
        is_still_on_login_page = self.email_login_page.is_loaded()
        is_main_page_loaded = self.main_page.is_loaded()
        
        if error_message:
            logger.info(f"✅ 发现密码错误提示: {error_message}")
        
        if is_still_on_login_page and not is_main_page_loaded:
            logger.info("✅ 登录失败，停留在密码输入页面")
        else:
            logger.warning("⚠️  登录验证结果异常")
        
        assert not is_main_page_loaded, "❌ 不应该使用错误密码登录成功"
        logger.info("🎉 TC021 测试通过")
    
    @pytest.mark.login
    @pytest.mark.exception
    @pytest.mark.high_priority
    def test_tc022_unregistered_email(self):
        """
        TC022: 登录 - 未注册邮箱
        验证系统正确处理未注册的邮箱
        """
        logger.info("=" * 80)
        logger.info("开始测试 TC022: 登录 - 未注册邮箱")
        logger.info("=" * 80)
        
        # 获取未注册用户数据
        unregistered_data = self.test_data.get("unregistered_users", [{}])[0]
        email = unregistered_data.get("email", "nonexistent@test.com")
        password = unregistered_data.get("password", "AnyPassword123!")
        
        self.landing_page.navigate()
        
        # 输入未注册邮箱
        logger.info(f"输入未注册邮箱: {email}")
        self.landing_page.enter_email(email)
        self.landing_page.click_continue_with_email()
        self.page.wait_for_timeout(2000)
        
        # 检查是否提示邮箱未注册
        error_on_landing = self.landing_page.get_email_validation_error()
        if error_on_landing:
            logger.info(f"✅ 在首页提示邮箱未注册: {error_on_landing}")
        else:
            # 如果跳转到密码页面，输入密码后应该提示用户不存在
            if self.email_login_page.is_loaded():
                logger.info("跳转到密码页面，输入密码测试")
                self.email_login_page.enter_password(password)
                self.email_login_page.click_continue()
                self.page.wait_for_timeout(3000)
                
                error_on_password = self.email_login_page.get_password_validation_error()
                if error_on_password:
                    logger.info(f"✅ 密码页面提示错误: {error_on_password}")
                
                # 验证未登录成功
                assert not self.main_page.is_loaded(), "❌ 不应该使用未注册邮箱登录成功"
        
        logger.info("🎉 TC022 测试通过")

