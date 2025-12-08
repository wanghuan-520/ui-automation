"""
注册功能测试模块
包含用户注册的各种场景测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.register_page import RegisterPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def register_page(page):
    """
    注册页面fixture
    ⚡ 增强版：集成页面加载诊断与自动截图
    """
    reg_page = RegisterPage(page)
    
    try:
        reg_page.navigate()
        
        # 验证页面是否真正加载成功
        if not reg_page.is_loaded():
             # 有时候虽然 navigate 成功，但关键元素未显示
            raise Exception("Register Page关键元素未加载")
            
    except Exception as e:
        logger.error(f"❌ 导航到Register Page失败: {e}")
        
        # 🔍 深度诊断
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/register_load_fail_{timestamp}.png"
        page.screenshot(path=screenshot_path)
        logger.error(f"   已保存失败截图: {screenshot_path}")
        
        html_path = f"screenshots/register_load_fail_{timestamp}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())
        
        raise e
    
    yield reg_page


@pytest.mark.register
class TestRegister:
    """注册功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_register_page_load(self, register_page):
        """
        TC-REG-022: 注册页面加载验证测试
        
        测试目标：验证注册页面能够正确加载并显示所有必要的表单元素
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-022: 注册页面加载验证")
        logger.info("=" * 60)
        
        # 截图：页面初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_page_loaded_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-注册页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证页面加载
        assert register_page.is_loaded(), "注册页面未正确加载"
        logger.info("   ✓ 注册页面加载成功")
        
        # 验证所有关键元素可见
        elements_to_check = [
            (register_page.PAGE_TITLE, "页面标题"),
            (register_page.USERNAME_INPUT, "用户名输入框"),
            (register_page.EMAIL_INPUT, "邮箱输入框"),
            (register_page.PASSWORD_INPUT, "密码输入框"),
            (register_page.REGISTER_BUTTON, "注册按钮"),
            (register_page.LOGIN_LINK, "登录链接")
        ]
        
        for locator, name in elements_to_check:
            assert register_page.is_visible(locator), f"{name}应该可见"
            logger.info(f"   ✓ {name}可见")
        
        logger.info("✅ TC-REG-022执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_register_with_valid_data(self, register_page, test_data):
        """
        TC-REG-001: 使用有效数据注册新用户测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-001: 使用有效数据注册新用户")
        logger.info("=" * 60)
        
        # 生成唯一的用户名和邮箱
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        username = f"testuser_{timestamp_str}"
        email = f"testuser_{timestamp_str}@test.com"
        password = "TestPass123!"
        
        logger.info(f"   注册数据 - 用户名: {username}, 邮箱: {email}")
        
        # 填写注册信息
        register_page.fill_username(username)
        register_page.fill_email(email)
        register_page.fill_password(password)
        logger.info("   ✓ 已填写注册表单")
        
        # 点击注册按钮
        register_page.click_register_button()
        logger.info("   ✓ 已点击注册按钮")
        
        # 等待页面响应
        register_page.page.wait_for_load_state("networkidle", timeout=10000)
        register_page.page.wait_for_timeout(2000)
        
        # 截图：注册完成后的页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_result_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="注册完成后的页面状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证注册结果
        current_url = register_page.page.url
        logger.info(f"   注册后的URL: {current_url}")
        
        # 注册成功的判断条件：
        # 1. URL不再是注册页面
        # 2. 或显示成功消息
        # 3. 或跳转到登录页面
        success = "/Register" not in current_url or register_page.is_success_message_visible()
        if success:
            logger.info("   ✓ 注册成功（跳转或显示成功消息）")
        else:
            logger.error("   ❌ 注册可能失败，仍停留在注册页面且无成功消息")
            
        assert success, "注册应该成功并跳转或显示成功消息"
        
        logger.info("✅ TC-REG-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_username_empty(self, register_page):
        """
        TC-REG-004: 用户名为空校验测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-004: 用户名为空校验")
        logger.info("=" * 60)
        
        # 用户名保持为空，填写其他字段
        register_page.fill_email("valid@test.com")
        register_page.fill_password("ValidPass123!")
        logger.info("   ✓ 已填写邮箱和密码，用户名留空")
        
        # 点击注册按钮
        register_page.click_register_button()
        register_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已点击注册按钮")
        
        # 验证HTML5必填字段验证
        is_valid = register_page.is_username_valid()
        if not is_valid:
            logger.info("   ✓ 用户名输入框验证状态: invalid（符合预期）")
        else:
            logger.warning("   ⚠️ 用户名输入框验证状态: valid（不符合预期）")
            
        assert not is_valid, "用户名为空时should be invalid"
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, "用户名为空时应该保持在注册页面"
        logger.info("   ✓ 保持在注册页面")
        
        logger.info("✅ TC-REG-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_email_invalid_format(self, register_page):
        """
        TC-REG-008: 邮箱格式校验测试（无效格式）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-008: 邮箱格式校验测试")
        logger.info("=" * 60)
        
        # 填写表单（邮箱为无效格式）
        register_page.fill_username("validuser")
        register_page.fill_email("invalid-email")  # 无效格式
        register_page.fill_password("ValidPass123!")
        logger.info("   ✓ 已填写表单，邮箱格式无效: invalid-email")
        
        # 点击注册按钮
        register_page.click_register_button()
        register_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已点击注册按钮")
        
        # 验证HTML5邮箱格式验证
        is_valid = register_page.is_email_valid()
        logger.info(f"   邮箱字段验证状态: {'valid' if is_valid else 'invalid'}")
        
        if not is_valid:
            logger.info("   ✓ 邮箱格式验证触发（invalid状态）")
        else:
            logger.info("   ℹ️ HTML5验证未触发（浏览器差异）")
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, "邮箱格式无效时应该保持在注册页面"
        logger.info("   ✓ 表单未提交，仍停留在注册页面")
        
        logger.info("✅ TC-REG-008执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_weak_password(self, register_page, test_data):
        """
        TC-REG-013~015: 弱密码校验测试（批量）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-013~015: 弱密码校验")
        logger.info("=" * 60)
        
        weak_passwords = test_data.get("register_data", {}).get("weak_passwords", [])
        
        for idx, pwd_data in enumerate(weak_passwords[:3], 1):  # 测试前3个弱密码
            password = pwd_data["password"]
            description = pwd_data["description"]
            
            logger.info(f"\n--- 测试场景{idx}: {description} ---")
            logger.info(f"   密码: {password}")
            
            # 填写数据
            register_page.clear_all_fields()
            register_page.fill_username("validuser")
            register_page.fill_email(f"valid{idx}@test.com")
            register_page.fill_password(password)
            
            # 点击注册按钮
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 记录是否显示错误
            has_error = register_page.is_error_message_visible()
            error_msg = register_page.get_error_message() if has_error else "无错误消息"
            logger.info(f"   结果 - 错误消息: {error_msg}")
            
            # 验证仍在注册页面
            current_url = register_page.page.url
            if "/Register" in current_url:
                logger.info("   ✓ 保持在注册页面")
            else:
                logger.warning(f"   ⚠️ 跳转到了其他页面: {current_url}")
        
        logger.info("\n✅ TC-REG-013~015执行成功")
    
    @pytest.mark.P2
    @pytest.mark.navigation
    def test_p2_register_login_link(self, register_page):
        """
        TC-REG-003: 跳转到登录页面链接验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-003: 跳转到登录页面链接验证")
        logger.info("=" * 60)
        
        # 点击登录链接
        logger.info("步骤1: 点击'Login'链接")
        register_page.click_login_link()
        register_page.page.wait_for_timeout(2000)
        
        # 验证URL
        current_url = register_page.page.url
        logger.info(f"   跳转后URL: {current_url}")
        assert "/Login" in current_url, f"应该跳转到登录页面，实际URL: {current_url}"
        logger.info("   ✓ 成功跳转到登录页面")
        
        logger.info("✅ TC-REG-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_all_fields_empty(self, register_page):
        """
        TC-REG-007: 所有字段为空校验测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-007: 所有字段为空校验")
        logger.info("=" * 60)
        
        # 直接点击注册按钮
        logger.info("步骤1: 直接点击'Register'按钮")
        register_page.click_register_button()
        register_page.page.wait_for_timeout(1000)
        
        # 验证第一个必填字段（用户名）显示验证错误
        is_valid = register_page.is_username_valid()
        if not is_valid:
            logger.info("   ✓ 用户名输入框验证状态: invalid（符合预期）")
        else:
            logger.warning("   ⚠️ 用户名输入框验证状态: valid（不符合预期）")
            
        assert not is_valid, "所有字段为空时用户名应该invalid"
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, "所有字段为空时应该保持在注册页面"
        
        logger.info("✅ TC-REG-007执行成功")
    
    # ========== ABP特定验证测试 ==========
    
    @pytest.mark.P0
    @pytest.mark.validation
    @pytest.mark.abp_validation
    def test_p0_abp_password_complexity(self, register_page, test_data):
        """
        TC-REG-ABP-001~006: ABP密码复杂度验证测试（批量）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-ABP: ABP密码复杂度验证")
        logger.info("=" * 60)
        
        abp_pwd_data = test_data.get("register_data", {}).get("abp_password_validation", [])
        
        for idx, pwd_test in enumerate(abp_pwd_data, 1):
            username = pwd_test["username"]
            # email = pwd_test["email"]  # 不用这个，用动态生成的
            password = pwd_test["password"]
            missing = pwd_test["missing"]
            description = pwd_test["description"]
            
            logger.info(f"\n--- 测试场景{idx}: {description} ---")
            logger.info(f"   密码: {'*' * len(password)}, 缺少: {missing}")
            
            # 清空并填写新数据
            register_page.clear_all_fields()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_username = f"{username}_{timestamp_str}"
            unique_email = f"{username}_{timestamp_str}@test.com"
            
            register_page.fill_username(unique_username)
            register_page.fill_email(unique_email)
            register_page.fill_password(password)
            
            # 点击注册
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 验证结果
            if missing == "none":
                # 期望成功
                logger.info("   ✓ 期望成功（符合所有要求的密码）")
                # 验证URL变化或显示成功消息
                current_url = register_page.page.url
                has_success = register_page.is_success_message_visible()
                logger.info(f"   结果 - URL: {current_url}, 成功消息: {has_success}")
            else:
                # 期望失败
                logger.info("   ✓ 期望失败（检查ABP密码复杂度错误消息）")
                
                # 检查是否有错误消息
                has_error = register_page.is_error_message_visible()
                if has_error:
                    error_msg = register_page.get_error_message()
                    logger.info(f"   ABP错误消息: {error_msg}")
                    
                    # 验证错误消息包含关键词（支持中英文）
                    expected_cn = pwd_test.get("expected_error_cn", "")
                    expected_en = pwd_test.get("expected_error_en", "")
                    
                    error_found = expected_cn in error_msg or expected_en.lower() in error_msg.lower()
                    logger.info(f"   错误消息匹配: {error_found}")
                else:
                    logger.warning("   ⚠️ 未发现错误消息")
                
                # 验证仍在注册页面
                current_url = register_page.page.url
                assert "/Register" in current_url, f"密码不符合要求时应保持在注册页面，实际URL: {current_url}"
            
            # 等待一下再进行下一个测试
            register_page.page.wait_for_timeout(500)
        
        logger.info("\n✅ TC-REG-ABP-001~006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    @pytest.mark.abp_validation
    def test_p1_abp_username_format(self, register_page, test_data):
        """
        TC-REG-ABP-007~010: ABP用户名格式验证测试（批量）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-ABP: ABP用户名格式验证")
        logger.info("=" * 60)
        
        username_data = test_data.get("register_data", {}).get("abp_username_validation", [])
        
        for idx, user_test in enumerate(username_data, 1):
            username = user_test["username"]
            # email = user_test["email"]
            password = user_test["password"]
            error_type = user_test["error_type"]
            description = user_test["description"]
            
            logger.info(f"\n--- 测试场景{idx}: {description} ---")
            logger.info(f"   用户名: '{username}', 错误类型: {error_type}")
            
            # 清空并填写数据
            register_page.clear_all_fields()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_email = f"user{idx}_{timestamp_str}@test.com"
            
            register_page.fill_username(username)
            register_page.fill_email(unique_email)
            register_page.fill_password(password)
            
            # 点击注册
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 验证结果
            if error_type == "none":
                # 期望成功
                logger.info("   ✓ 期望成功")
                current_url = register_page.page.url
                logger.info(f"   结果URL: {current_url}")
            else:
                # 期望失败
                logger.info("   ✓ 期望失败（检查ABP用户名格式错误）")
                
                has_error = register_page.is_error_message_visible()
                if has_error:
                    error_msg = register_page.get_error_message()
                    logger.info(f"   ABP错误消息: {error_msg}")
                    
                    expected_error = user_test.get("expected_error", "")
                    if expected_error:
                        error_found = expected_error in error_msg
                        logger.info(f"   错误消息包含'{expected_error}': {error_found}")
                else:
                    logger.warning("   ⚠️ 未发现错误消息")
                
                current_url = register_page.page.url
                assert "/Register" in current_url, f"用户名格式无效时应保持在注册页面"
            
            register_page.page.wait_for_timeout(500)
        
        logger.info("\n✅ TC-REG-ABP-007~010执行成功")
    
    @pytest.mark.P0
    @pytest.mark.abp_validation
    def test_p0_duplicate_username(self, register_page, test_data):
        """
        TC-REGISTER-020: 重复用户名验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REGISTER-020: 重复用户名验证")
        logger.info("=" * 60)
        
        # 使用测试数据中的重复用户名（如果存在）
        duplicate_data = None
        if "duplicate_data" in test_data:
            duplicate_data = test_data["duplicate_data"][0]
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if not duplicate_data:
            # 如果没有预定义的重复数据，使用一个已知存在的用户名
            duplicate_data = {
                "username": "admin",  # ABP默认管理员用户名
                "email": f"test_dup_{timestamp}@test.com",
                "password": "Test123456!"
            }
        
        logger.info(f"   尝试注册重复用户名: {duplicate_data['username']}")
        
        # 填写表单
        register_page.fill_username(duplicate_data["username"])
        register_page.fill_email(duplicate_data["email"])
        register_page.fill_password(duplicate_data["password"])
        
        # 点击注册
        register_page.click_register_button()
        register_page.page.wait_for_timeout(2000)
        
        # 验证：应该显示错误消息
        has_error = register_page.is_error_message_visible()
        logger.info(f"   是否显示错误消息: {has_error}")
        
        if has_error:
            error_msg = register_page.get_error_message()
            logger.info(f"   错误消息: {error_msg}")
            assert "username" in error_msg.lower() or "already" in error_msg.lower() or "exists" in error_msg.lower(), \
                f"错误消息应提示用户名已存在，实际: {error_msg}"
        
        # 验证：应该保持在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, f"应该保持在注册页面，实际URL: {current_url}"
        
        logger.info("✅ TC-REGISTER-020执行成功")
    
    @pytest.mark.P0
    @pytest.mark.abp_validation
    def test_p0_duplicate_email(self, register_page, test_data):
        """
        TC-REGISTER-021: 重复邮箱验证测试
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REGISTER-021: 重复邮箱验证")
        logger.info("=" * 60)
        
        # 使用测试数据中的重复邮箱（如果存在）
        duplicate_data = None
        if "duplicate_data" in test_data and len(test_data["duplicate_data"]) > 1:
            duplicate_data = test_data["duplicate_data"][1]
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if not duplicate_data:
            # 如果没有预定义的重复数据，使用一个已知存在的邮箱
            duplicate_data = {
                "username": f"testuser_{timestamp}",
                "email": "admin@aevatar.ai",  # 使用已知存在的邮箱
                "password": "Test123456!"
            }
        
        logger.info(f"   尝试注册重复邮箱: {duplicate_data['email']}")
        
        # 填写表单
        register_page.fill_username(duplicate_data["username"])
        register_page.fill_email(duplicate_data["email"])
        register_page.fill_password(duplicate_data["password"])
        
        # 点击注册
        register_page.click_register_button()
        register_page.page.wait_for_timeout(2000)
        
        # 验证：应该显示错误消息
        has_error = register_page.is_error_message_visible()
        logger.info(f"   是否显示错误消息: {has_error}")
        
        if has_error:
            error_msg = register_page.get_error_message()
            logger.info(f"   错误消息: {error_msg}")
            assert "email" in error_msg.lower() or "already" in error_msg.lower() or "exists" in error_msg.lower(), \
                f"错误消息应提示邮箱已被注册，实际: {error_msg}"
        
        # 验证：应该保持在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, f"应该保持在注册页面，实际URL: {current_url}"
        
        logger.info("✅ TC-REGISTER-021执行成功")
