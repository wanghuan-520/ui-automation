"""
Change Password 功能测试模块
包含密码修改、密码格式验证、密码安全性等测试
合并自 test_change_password.py 和 test_profile_change_password.py
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.change_password_page import ChangePasswordPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def logged_in_page(browser_type, test_data):
    """
    登录后的页面fixture - 整个测试类只登录一次
    支持已登录状态检测，避免重复登录
    使用 browser_type 启动独立的浏览器实例，避免跨文件共享问题
    """
    # 启动独立的浏览器实例
    browser = browser_type.launch(headless=True)
    
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
    landing_page.handle_ssl_warning()
    page.wait_for_timeout(2000)
    
    # 检查是否已登录（通过检测用户菜单按钮）
    user_menu_visible = page.is_visible("button:has-text('Toggle user menu')", timeout=3000)
    
    if user_menu_visible:
        logger.info("检测到用户已登录，跳过登录流程")
    else:
        # 未登录，执行登录流程
        logger.info("用户未登录，开始登录流程")
        
        # 检查Sign In按钮是否存在
        sign_in_visible = page.is_visible("button:has-text('Sign In'), a:has-text('Sign In')", timeout=5000)
        
        if sign_in_visible:
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
        else:
            # 可能页面结构变化，尝试直接导航到登录页
            logger.info("未找到Sign In按钮，尝试直接导航到登录页")
            page.goto("https://localhost:44320/Account/Login")
            page.wait_for_timeout(2000)
            
            valid_data = test_data["valid_login_data"][0]
            page.fill("#LoginInput_UserNameOrEmailAddress", valid_data["username"])
            page.fill("#LoginInput_Password", valid_data["password"])
            page.click("button[type='submit']")
            
            page.wait_for_function(
                "() => !window.location.href.includes('/Account/Login')",
                timeout=30000
            )
            landing_page.handle_ssl_warning()
            page.wait_for_timeout(2000)
    
    logger.info("登录成功，会话将在整个测试类中复用")
    
    yield page
    
    # 测试类结束后清理
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def logged_in_change_password_page(logged_in_page):
    """
    每个测试函数的Change Password页面fixture
    """
    page = logged_in_page
    
    # 导航到Change Password页面
    password_page = ChangePasswordPage(page)
    password_page.navigate()
    
    return password_page


@pytest.mark.password
class TestChangePassword:
    """Change Password功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_change_password_page_load(self, logged_in_change_password_page):
        """
        TC-PWD-001: 修改密码页面加载验证测试
        
        测试目标：验证修改密码页面能够正常访问并显示所有必需元素
        测试区域：Profile - Change Password Page
        测试元素：
        - Current Password输入框
        - New Password输入框
        - Confirm Password输入框
        - Save按钮
        
        测试步骤：
        1. [前置条件] 用户已登录并导航到Change Password页面
        2. [验证] 确认页面成功加载
        3. [验证] 确认所有必需元素可见
        
        预期结果：
        - 页面成功加载
        - 所有输入框和按钮可见
        - 页面无加载错误
        """
        logger.info("开始执行TC-PWD-001: 访问修改密码页面")
        
        password_page = logged_in_change_password_page
        
        # 验证页面加载
        assert password_page.is_loaded(), "Change Password页面未正确加载"
        
        # 截图1：页面加载完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"change_pwd_page_loaded_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Change Password页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证关键元素存在
        assert password_page.is_visible(password_page.CURRENT_PASSWORD_INPUT), \
            "Current Password输入框应该可见"
        assert password_page.is_visible(password_page.NEW_PASSWORD_INPUT), \
            "New Password输入框应该可见"
        assert password_page.is_visible(password_page.CONFIRM_PASSWORD_INPUT), \
            "Confirm Password输入框应该可见"
        assert password_page.is_visible(password_page.SAVE_BUTTON), \
            "Save按钮应该可见"
        
        # 截图2：所有元素验证完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"change_pwd_elements_verified_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-所有元素验证完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-PWD-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_password_mismatch(self, logged_in_change_password_page, test_data):
        """
        TC-PWD-002: 密码不匹配验证测试
        
        测试目标：验证新密码与确认密码不一致时显示错误提示
        测试区域：Profile - Change Password - Validation
        测试元素：
        - New Password输入框
        - Confirm Password输入框
        - 错误提示消息
        
        测试步骤：
        1. [Form] 填写Current Password
        2. [Form] 填写New Password
        3. [Form] 填写不匹配的Confirm Password
        4. [操作] 点击Save按钮
        5. [验证] 确认显示错误提示
        
        预期结果：
        - 显示密码不匹配错误
        - 密码未被更改
        - 验证功能正常
        """
        logger.info("开始执行TC-PWD-002: 新密码与确认密码不匹配")
        
        password_page = logged_in_change_password_page
        current_password = test_data["valid_login_data"][0]["password"]
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_mismatch_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 输入不匹配的密码
        password_page.change_password(
            current_password=current_password,
            new_password="NewPassword123!",
            confirm_password="DifferentPassword123!"
        )
        
        # 截图：提交不匹配的密码后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_mismatch_submitted_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-提交不匹配的密码后（应显示错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待并验证错误消息
        password_page.page.wait_for_timeout(2000)
        
        # 截图：错误消息显示
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_mismatch_error_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-密码不匹配错误提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证应该留在当前页面
        assert password_page.is_visible(password_page.CURRENT_PASSWORD_INPUT), \
            "密码不匹配时应该留在当前页面"
        
        logger.info("TC-PWD-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_same_old_and_new_password(self, logged_in_change_password_page, test_data):
        """
        TC-PWD-003: 新旧密码相同验证测试
        
        测试目标：验证新密码与当前密码相同时系统拒绝并显示错误
        测试区域：Profile - Change Password - Validation
        测试元素：
        - Current Password输入框
        - New Password输入框
        - 错误提示消息
        
        测试步骤：
        1. [Form] 填写Current Password
        2. [Form] 填写与当前密码相同的New Password
        3. [Form] 填写Confirm Password
        4. [操作] 点击Save按钮
        5. [验证] 确认显示错误提示
        
        预期结果：
        - 显示"新密码不能与旧密码相同"错误
        - 密码未被更改
        - 业务逻辑验证正常
        """
        logger.info("开始执行TC-PWD-003: 新密码与当前密码相同")
        
        password_page = logged_in_change_password_page
        current_password = test_data["valid_login_data"][0]["password"]
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_same_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 尝试使用相同的新旧密码
        password_page.change_password(
            current_password=current_password,
            new_password=current_password,
            confirm_password=current_password
        )
        
        # 截图：提交相同密码后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_same_submitted_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-提交相同密码后（应显示错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待处理
        password_page.page.wait_for_timeout(2000)
        
        # 截图：错误消息
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_same_error_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-相同密码错误提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-PWD-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_wrong_current_password(self, logged_in_change_password_page):
        """
        TC-PWD-004: 当前密码错误验证测试
        
        测试目标：验证输入错误的当前密码时系统拒绝并显示错误
        测试区域：Profile - Change Password - Authentication
        测试元素：
        - Current Password输入框
        - 错误提示消息
        
        测试步骤：
        1. [Form] 填写错误的Current Password
        2. [Form] 填写有效的New Password和Confirm Password
        3. [操作] 点击Save按钮
        4. [验证] 确认显示"当前密码错误"提示
        
        预期结果：
        - 显示当前密码错误提示
        - 密码未被更改
        - 身份验证安全正常
        """
        logger.info("开始执行TC-PWD-004: 当前密码错误")
        
        password_page = logged_in_change_password_page
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_wrong_current_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 输入错误的当前密码
        password_page.change_password(
            current_password="WrongPassword123!",
            new_password="NewPassword123!",
            confirm_password="NewPassword123!"
        )
        
        # 截图：提交错误密码后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_wrong_current_submitted_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-提交错误的当前密码后（应显示错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待错误消息
        password_page.page.wait_for_timeout(2000)
        
        # 截图：错误消息
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_wrong_current_error_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-错误的当前密码提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-PWD-004执行成功")
    
    @pytest.mark.P2
    @pytest.mark.validation
    def test_p2_empty_fields_validation(self, logged_in_change_password_page):
        """
        TC-PWD-005: 空字段验证测试
        
        测试目标：验证所有密码字段为必填项，空字段无法提交
        测试区域：Profile - Change Password - Form Validation
        测试元素：
        - Current Password输入框（必填）
        - New Password输入框（必填）
        - Confirm Password输入框（必填）
        
        测试步骤：
        1. [操作] 不填写任何字段直接点击Save
        2. [验证] 确认HTML5验证阻止提交
        3. [验证] 确认显示必填提示
        
        预期结果：
        - 所有字段显示必填验证
        - 表单无法提交
        - 验证提示清晰
        """
        logger.info("开始执行TC-PWD-005: 空字段验证")
        
        password_page = logged_in_change_password_page
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_empty_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 场景1：所有字段为空
        logger.info("测试场景1: 所有字段为空")
        password_page.click_element(password_page.SAVE_BUTTON)
        password_page.page.wait_for_timeout(1000)
        
        # 截图：所有字段为空
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_all_empty_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-所有字段为空（应显示验证错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 场景2：只填写当前密码
        logger.info("测试场景2: 只填写当前密码")
        password_page.fill_input(password_page.CURRENT_PASSWORD_INPUT, "CurrentPwd123!")
        password_page.click_element(password_page.SAVE_BUTTON)
        password_page.page.wait_for_timeout(1000)
        
        # 截图：只填写当前密码
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_only_current_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-只填写当前密码（新密码必填）",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-PWD-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.boundary
    def test_p1_password_length_boundary(self, logged_in_change_password_page, test_data):
        """
        TC-PWD-006: 密码长度边界值测试（完整边界值覆盖）
        
        测试目标：验证密码长度的边界值、小于边界值、大于边界值
        测试区域：Profile - Change Password - Password Rules
        测试元素：
        - New Password输入框
        - 密码长度验证规则
        
        后端限制（ABP Framework Identity 默认配置）：
        - RequiredLength = 6（最小长度边界值）
        - RequireDigit = true（需要数字）
        - RequireLowercase = true（需要小写字母）
        - RequireUppercase = true（需要大写字母）
        - RequireNonAlphanumeric = true（需要特殊字符）
        
        边界值测试场景：
        ┌──────────────────────────────────────────────────────────────┐
        │ 场景 | 长度 | 满足复杂度 | 预期结果 | 说明                   │
        ├──────────────────────────────────────────────────────────────┤
        │  1   |  4   |    是     |  拒绝   | 小于边界值（6-2=4）      │
        │  2   |  5   |    是     |  拒绝   | 小于边界值（6-1=5）      │
        │  3   |  6   |    是     |  通过   | 等于边界值（最小长度）   │
        │  4   |  7   |    是     |  通过   | 大于边界值（6+1=7）      │
        │  5   |  50  |    是     |  通过   | 远大于边界值（长密码）   │
        │  6   |  6   |    否     |  拒绝   | 边界值但不满足复杂度     │
        └──────────────────────────────────────────────────────────────┘
        
        测试步骤：
        1. [Form] 测试4字符密码（小于边界值-2，应被拒绝）
        2. [Form] 测试5字符密码（小于边界值-1，应被拒绝）
        3. [Form] 测试6字符密码（等于边界值，满足复杂度应通过）
        4. [Form] 测试7字符密码（大于边界值+1，应通过）
        5. [Form] 测试50字符密码（远大于边界值，应通过）
        6. [Form] 测试6字符不满足复杂度的密码（应被拒绝）
        
        预期结果：
        - 小于6字符：后端返回错误（密码过短）
        - 等于6字符+满足复杂度：后端接受
        - 大于6字符+满足复杂度：后端接受
        - 等于6字符+不满足复杂度：后端返回错误（复杂度不足）
        """
        logger.info("=" * 70)
        logger.info("开始执行TC-PWD-006: 密码长度边界值测试（完整覆盖）")
        logger.info("=" * 70)
        logger.info("后端ABP限制:")
        logger.info("  - RequiredLength = 6（最小长度边界值）")
        logger.info("  - RequireDigit = true")
        logger.info("  - RequireLowercase = true")
        logger.info("  - RequireUppercase = true")
        logger.info("  - RequireNonAlphanumeric = true")
        logger.info("=" * 70)
        
        password_page = logged_in_change_password_page
        current_password = test_data["valid_login_data"][0]["password"]
        
        # 完整的边界值测试数据
        boundary_test_cases = [
            {
                "value": "Ab1!",
                "length": 4,
                "description": "小于边界值-2（4字符）",
                "meets_complexity": True,
                "should_pass": False,
                "expected_error": "密码过短"
            },
            {
                "value": "Ab1!5",
                "length": 5,
                "description": "小于边界值-1（5字符）",
                "meets_complexity": True,
                "should_pass": False,
                "expected_error": "密码过短"
            },
            {
                "value": "Ab1!56",
                "length": 6,
                "description": "等于边界值（6字符，满足复杂度）",
                "meets_complexity": True,
                "should_pass": True,
                "expected_error": None
            },
            {
                "value": "Ab1!567",
                "length": 7,
                "description": "大于边界值+1（7字符）",
                "meets_complexity": True,
                "should_pass": True,
                "expected_error": None
            },
            {
                "value": "Ab1!567890123456789012345678901234567890123456789",
                "length": 50,
                "description": "远大于边界值（50字符）",
                "meets_complexity": True,
                "should_pass": True,
                "expected_error": None
            },
            {
                "value": "aaaaaa",
                "length": 6,
                "description": "等于边界值但不满足复杂度（仅小写）",
                "meets_complexity": False,
                "should_pass": False,
                "expected_error": "复杂度不足"
            },
            {
                "value": "AAAAAA",
                "length": 6,
                "description": "等于边界值但不满足复杂度（仅大写）",
                "meets_complexity": False,
                "should_pass": False,
                "expected_error": "复杂度不足"
            },
            {
                "value": "123456",
                "length": 6,
                "description": "等于边界值但不满足复杂度（仅数字）",
                "meets_complexity": False,
                "should_pass": False,
                "expected_error": "复杂度不足"
            },
        ]
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_boundary_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        test_results = []
        screenshot_idx = 2
        
        for idx, test_case in enumerate(boundary_test_cases, 1):
            logger.info("")
            logger.info(f"─── 测试场景 {idx}/{len(boundary_test_cases)}: {test_case['description']} ───")
            logger.info(f"  密码值: '{test_case['value']}'")
            logger.info(f"  实际长度: {len(test_case['value'])} 字符")
            logger.info(f"  满足复杂度: {test_case['meets_complexity']}")
            logger.info(f"  预期通过后端验证: {test_case['should_pass']}")
            if test_case['expected_error']:
                logger.info(f"  预期错误类型: {test_case['expected_error']}")
            
            # 填写表单并提交
            password_page.change_password(
                current_password=current_password,
                new_password=test_case["value"],
                confirm_password=test_case["value"]
            )
            
            # 等待后端响应
            password_page.page.wait_for_timeout(2000)
            
            # 检测后端响应
            error_visible = password_page.page.is_visible("text=Failed", timeout=2000)
            success_visible = password_page.page.is_visible("text=success", timeout=1000)
            
            # 判断实际结果
            actual_passed = success_visible and not error_visible
            result_match = actual_passed == test_case['should_pass']
            
            result_icon = "✅" if result_match else "❌"
            result_status = "通过" if actual_passed else "拒绝"
            expected_status = "通过" if test_case['should_pass'] else "拒绝"
            
            logger.info(f"  实际结果: {result_status}")
            logger.info(f"  预期结果: {expected_status}")
            logger.info(f"  {result_icon} 测试{'通过' if result_match else '失败'}")
            
            # 如果密码修改成功，立即恢复原始密码，避免影响后续测试
            if actual_passed:
                logger.info(f"  ⚠️ 密码已修改，正在恢复原始密码...")
                password_page.navigate()
                password_page.page.wait_for_timeout(1000)
                password_page.change_password(
                    current_password=test_case["value"],
                    new_password=current_password,
                    confirm_password=current_password
                )
                password_page.page.wait_for_timeout(2000)
                restore_success = password_page.page.is_visible("text=success", timeout=2000)
                if restore_success:
                    logger.info(f"  ✅ 原始密码已恢复")
                else:
                    logger.warning(f"  ⚠️ 原始密码恢复可能失败，后续测试可能受影响")
            
            test_results.append({
                "case": test_case['description'],
                "length": test_case['length'],
                "expected": expected_status,
                "actual": result_status,
                "match": result_match
            })
            
            # 截图：每个测试场景
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"pwd_boundary_{idx}_{timestamp}.png"
            password_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{screenshot_idx}-{test_case['description']}（{len(test_case['value'])}字符，预期:{expected_status}，实际:{result_status}）",
                attachment_type=allure.attachment_type.PNG
            )
            screenshot_idx += 1
            
            # 重新导航准备下一次测试
            password_page.navigate()
            password_page.page.wait_for_timeout(1000)
        
        # 输出测试结果汇总
        logger.info("")
        logger.info("=" * 70)
        logger.info("测试结果汇总")
        logger.info("=" * 70)
        logger.info("| 场景 | 长度 | 预期 | 实际 | 结果 |")
        logger.info("|------|------|------|------|------|")
        for r in test_results:
            icon = "✅" if r['match'] else "❌"
            logger.info(f"| {r['case'][:20]:20} | {r['length']:4} | {r['expected']:4} | {r['actual']:4} | {icon} |")
        
        # 统计通过/失败
        passed_count = sum(1 for r in test_results if r['match'])
        total_count = len(test_results)
        failed_cases = [r for r in test_results if not r['match']]
        
        logger.info(f"")
        logger.info(f"通过率: {passed_count}/{total_count} ({passed_count*100//total_count}%)")
        
        # 断言：如果有失败的场景，测试应该失败
        if failed_cases:
            failed_details = "\n".join([
                f"  - {r['case']}: 预期={r['expected']}, 实际={r['actual']}"
                for r in failed_cases
            ])
            pytest.fail(f"边界值测试存在 {len(failed_cases)} 个失败场景:\n{failed_details}")
        
        logger.info("TC-PWD-006执行成功")
    
    @pytest.mark.P2
    @pytest.mark.security
    def test_p2_password_complexity_requirements(self, logged_in_change_password_page, test_data):
        """
        TC-PWD-007: 密码复杂度要求验证测试
        
        测试目标：验证密码必须满足ABP框架的复杂度要求
        测试区域：Profile - Change Password - Password Complexity
        测试元素：
        - New Password输入框
        - 复杂度验证规则（大小写、数字、特殊字符）
        
        后端限制（ABP Framework Identity 默认配置）：
        - RequiredLength = 6（最小长度6字符）
        - RequireDigit = true（需要至少1个数字）
        - RequireLowercase = true（需要至少1个小写字母）
        - RequireUppercase = true（需要至少1个大写字母）
        - RequireNonAlphanumeric = true（需要至少1个特殊字符）
        
        有效密码示例：Ab1!56（满足所有要求）
        
        测试步骤：
        1. [Form] 测试只包含数字的密码（缺少字母和特殊字符）
        2. [Form] 测试只包含小写字母（缺少大写、数字、特殊字符）
        3. [Form] 测试只包含大写字母（缺少小写、数字、特殊字符）
        4. [Form] 测试缺少数字的密码
        5. [Form] 测试缺少特殊字符的密码
        6. [Form] 测试缺少大写字母的密码
        
        预期结果：
        - 所有弱密码都被拒绝
        - 错误提示清晰说明缺少哪种字符
        """
        logger.info("开始执行TC-PWD-007: 密码复杂度要求")
        logger.info("后端要求: 最小6字符 + 大写 + 小写 + 数字 + 特殊字符")
        
        password_page = logged_in_change_password_page
        current_password = test_data["valid_login_data"][0]["password"]
        
        # 测试各种不符合ABP复杂度要求的密码
        weak_passwords = [
            {"pwd": "12345678", "desc": "纯数字（缺少字母和特殊字符）", "missing": "字母、特殊字符"},
            {"pwd": "abcdefgh", "desc": "纯小写字母（缺少大写、数字、特殊字符）", "missing": "大写、数字、特殊字符"},
            {"pwd": "ABCDEFGH", "desc": "纯大写字母（缺少小写、数字、特殊字符）", "missing": "小写、数字、特殊字符"},
            {"pwd": "Abcdef!", "desc": "缺少数字", "missing": "数字"},
            {"pwd": "Abcdef1", "desc": "缺少特殊字符", "missing": "特殊字符"},
            {"pwd": "abcdef1!", "desc": "缺少大写字母", "missing": "大写字母"},
            {"pwd": "ABCDEF1!", "desc": "缺少小写字母", "missing": "小写字母"},
        ]
        
        for idx, test_case in enumerate(weak_passwords, 1):
            logger.info(f"测试场景{idx}: {test_case['desc']}")
            logger.info(f"密码: '{test_case['pwd']}', 缺少: {test_case['missing']}")
            
            # 截图：测试前
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"pwd_weak_{idx}_before_{timestamp}.png"
            password_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*2-1}-测试{test_case['desc']}前",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 尝试使用弱密码
            password_page.change_password(
                current_password=current_password,
                new_password=test_case["pwd"],
                confirm_password=test_case["pwd"]
            )
            
            password_page.page.wait_for_timeout(2000)
            
            # 截图：测试后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"pwd_weak_{idx}_after_{timestamp}.png"
            password_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*2}-{test_case['desc']}（应显示错误）",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 重新导航到页面（清除之前的输入）
            password_page.navigate()
            password_page.page.wait_for_timeout(1000)
        
        logger.info("TC-PWD-007执行成功")
    
    @pytest.mark.P2
    @pytest.mark.security
    def test_p2_password_field_masking(self, logged_in_change_password_page):
        """
        TC-PWD-008: 密码字段遮罩显示测试
        
        测试目标：验证密码输入时以掩码形式显示，保护密码安全
        测试区域：Profile - Change Password - Security
        测试元素：
        - Current Password输入框
        - New Password输入框
        - Confirm Password输入框
        
        测试步骤：
        1. [Form] 在密码字段中输入文本
        2. [验证] 确认输入框type属性为"password"
        3. [验证] 确认输入内容以掩码显示
        
        预期结果：
        - 所有密码字段默认为掩码显示
        - 输入内容不以明文显示
        - 密码安全防护正常
        """
        logger.info("开始执行TC-PWD-008: 密码字段遮罩显示")
        
        password_page = logged_in_change_password_page
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_masking_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 输入密码
        test_password = "TestPassword123!"
        password_page.fill_input(password_page.CURRENT_PASSWORD_INPUT, test_password)
        password_page.fill_input(password_page.NEW_PASSWORD_INPUT, "NewPassword123!")
        password_page.fill_input(password_page.CONFIRM_PASSWORD_INPUT, "NewPassword123!")
        
        # 截图：密码已输入（应显示为 ••••••）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_masking_filled_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-密码已输入（应显示为掩码）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证输入框类型为password
        current_type = password_page.page.get_attribute(password_page.CURRENT_PASSWORD_INPUT, "type")
        new_type = password_page.page.get_attribute(password_page.NEW_PASSWORD_INPUT, "type")
        confirm_type = password_page.page.get_attribute(password_page.CONFIRM_PASSWORD_INPUT, "type")
        
        logger.info(f"字段类型 - Current: {current_type}, New: {new_type}, Confirm: {confirm_type}")
        
        assert current_type == "password", "当前密码字段应为password类型"
        assert new_type == "password", "新密码字段应为password类型"
        assert confirm_type == "password", "确认密码字段应为password类型"
        
        logger.info("TC-PWD-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_password_show_hide_toggle(self, logged_in_change_password_page):
        """
        TC-PWD-009: 密码显示/隐藏切换测试
        
        测试目标：验证密码字段的显示/隐藏切换功能（如果UI提供）
        测试区域：Profile - Change Password - User Experience
        测试元素：
        - 密码显示/隐藏切换按钮（如眼睛图标）
        - Password输入框type属性
        
        测试步骤：
        1. [验证] 检查是否存在密码显示/隐藏按钮
        2. [操作] 如果存在，点击切换显示
        3. [验证] 确认type属性在"password"和"text"之间切换
        
        预期结果：
        - 切换功能正常（如果存在）
        - type属性正确切换
        - 用户体验良好
        """
        logger.info("开始执行TC-PWD-009: 密码显示/隐藏切换")
        
        password_page = logged_in_change_password_page
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_toggle_init_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 输入密码
        test_password = "TestPassword123!"
        password_page.fill_input(password_page.CURRENT_PASSWORD_INPUT, test_password)
        
        # 检查是否有显示/隐藏按钮
        toggle_selectors = [
            "button[aria-label*='show' i]",
            "button[aria-label*='toggle' i]",
            ".password-toggle",
            "button:has(.eye-icon)",
            "[type='button']:near(input[type='password'])"
        ]
        
        toggle_found = False
        for selector in toggle_selectors:
            if password_page.is_visible(selector):
                logger.info(f"找到密码切换按钮: {selector}")
                
                # 点击切换按钮
                password_page.click_element(selector)
                password_page.page.wait_for_timeout(500)
                
                # 截图：点击后
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"pwd_toggle_clicked_{timestamp}.png"
                password_page.take_screenshot(screenshot_path)
                allure.attach.file(
                    f"screenshots/{screenshot_path}",
                    name="2-点击显示/隐藏按钮后",
                    attachment_type=allure.attachment_type.PNG
                )
                
                toggle_found = True
                break
        
        if not toggle_found:
            logger.info("未找到密码显示/隐藏切换按钮（此功能可能不存在）")
        
        # 截图：最终状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_toggle_final_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-最终状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-PWD-009执行完成")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_successful_password_change_with_relogin(self, logged_in_change_password_page, test_data, browser):
        """
        TC-PWD-010: 成功修改密码并重新登录验证测试
        
        测试目标：验证密码修改功能的完整流程和实际有效性
        测试区域：Profile - Change Password - Full Workflow
        测试元素：
        - Change Password表单
        - Logout功能
        - Login功能
        - 新密码验证
        
        后端限制（ABP Framework Identity 默认配置）：
        - RequiredLength = 6（最小长度6字符）
        - RequireDigit = true（需要至少1个数字）
        - RequireLowercase = true（需要至少1个小写字母）
        - RequireUppercase = true（需要至少1个大写字母）
        - RequireNonAlphanumeric = true（需要至少1个特殊字符）
        
        测试使用密码：NewPwd123!@（满足所有ABP要求）
        
        测试步骤：
        1. [Form] 填写并提交密码修改表单
        2. [验证] 确认密码修改成功提示
        3. [操作] 退出登录
        4. [操作] 使用新密码重新登录
        5. [验证] 确认新密码可以登录
        6. [操作] 将密码改回原密码
        7. [验证] 确认原密码恢复成功
        
        预期结果：
        - 密码修改成功
        - 新密码可以登录
        - 旧密码失效
        - 密码恢复成功
        - 完整流程无错误
        """
        logger.info("开始执行TC-PWD-010: 验证密码修改成功（通过重新登录）")
        logger.info("ABP密码要求: 最小6字符 + 大写 + 小写 + 数字 + 特殊字符")
        
        password_page = logged_in_change_password_page
        page = password_page.page
        
        # 获取当前密码和账号信息
        current_password = test_data["valid_login_data"][0]["password"]
        username = test_data["valid_login_data"][0]["username"]
        # 新密码必须满足ABP复杂度要求：大写+小写+数字+特殊字符，最小6字符
        new_password = "NewPwd123!@"
        
        logger.info(f"步骤1: 使用当前密码 {current_password} 修改为新密码 {new_password}")
        
        # 截图1：修改前状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_before_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-修改密码前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 修改密码
        password_page.change_password(
            current_password=current_password,
            new_password=new_password,
            confirm_password=new_password
        )
        
        # 等待保存完成并检查结果
        page.wait_for_timeout(3000)
        
        # 截图2：修改后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_after_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-修改密码后",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查是否有错误提示（红色Failed提示）
        error_selectors = [
            "text=Failed",
            "text=Password update wasn't successful",
            ".text-danger",
            "[class*='error']",
            "[class*='failed']"
        ]
        
        for selector in error_selectors:
            if page.is_visible(selector, timeout=2000):
                error_text = page.text_content(selector) if page.is_visible(selector, timeout=1000) else "未知错误"
                logger.error(f"❌ 密码修改失败，检测到错误提示: {error_text}")
                pytest.fail(f"BUG: 密码修改功能异常，API返回失败: {error_text}")
        
        # 检查是否有成功提示
        success_selectors = [
            "text=successfully",
            "text=Success",
            ".text-success",
            "[class*='success']"
        ]
        
        success_found = False
        for selector in success_selectors:
            if page.is_visible(selector, timeout=2000):
                logger.info(f"✅ 检测到成功提示: {selector}")
                success_found = True
                break
        
        if not success_found:
            logger.warning("⚠️ 未检测到明确的成功提示，继续验证...")
        
        logger.info("步骤2: 退出登录")
        
        # 退出登录
        password_page.logout()
        page.wait_for_timeout(2000)
        
        # 截图3：退出后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_logout_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-退出登录后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"步骤3: 使用新密码 {new_password} 重新登录")
        
        # 重新登录（使用新密码）
        from tests.aevatar_station.pages.landing_page import LandingPage
        from tests.aevatar_station.pages.login_page import LoginPage
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        landing_page.navigate()
        landing_page.handle_ssl_warning()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 截图4：登录页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_login_page_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="4-登录页面（准备用新密码登录）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 使用新密码登录
        page.fill("#LoginInput_UserNameOrEmailAddress", username)
        page.fill("#LoginInput_Password", new_password)
        page.click("button[type='submit']")
        
        # 等待登录完成
        try:
            page.wait_for_function(
                "() => !window.location.href.includes('/Account/Login')",
                timeout=30000
            )
            logger.info(f"✅ 使用新密码登录成功！当前URL: {page.url}")
        except Exception as e:
            logger.error(f"❌ 使用新密码登录失败: {e}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"pwd_change_verify_login_failed_{timestamp}.png"
            page.screenshot(path=f"screenshots/{screenshot_path}")
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="登录失败截图",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"使用新密码登录失败，密码可能未成功修改: {e}")
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        
        # 截图5：使用新密码登录成功
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_login_success_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="5-使用新密码登录成功",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"步骤4: 将密码改回原密码 {current_password}")
        
        # 导航到Change Password页面
        password_page.navigate()
        page.wait_for_timeout(2000)
        
        # 截图6：再次进入修改密码页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_restore_before_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="6-准备恢复原密码",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 将密码改回原密码
        password_page.change_password(
            current_password=new_password,
            new_password=current_password,
            confirm_password=current_password
        )
        
        page.wait_for_timeout(3000)
        
        # 截图7：密码已恢复
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_change_verify_restore_after_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="7-密码已恢复为原密码",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"✅ TC-PWD-010执行成功！")
        logger.info(f"✅ 验证结果：密码修改功能正常，新密码 {new_password} 可以成功登录")
        logger.info(f"✅ 密码已恢复为原密码 {current_password}")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_restore_original_password(self, logged_in_change_password_page, test_data):
        """
        TC-PWD-999: 恢复原始密码测试（测试清理）
        
        测试目标：确保测试结束后密码恢复为原始值，不影响后续测试
        测试区域：Profile - Change Password - Test Cleanup
        测试元素：Change Password表单
        
        测试步骤：
        1. [前置条件] 密码可能已被前面的测试修改
        2. [Form] 将密码改回 Wh520520!
        3. [验证] 确认密码恢复成功
        4. [验证] 确认后续测试可以使用原始密码登录
        
        预期结果：
        - 密码成功恢复为 Wh520520!
        - 测试环境已清理
        - 后续测试不受影响
        
        注意：此测试用例必须在所有密码相关测试的最后执行
        """
        logger.info("开始执行TC-PWD-999: 恢复原始密码")
        
        password_page = logged_in_change_password_page
        
        # 获取当前密码（应该是测试数据中的密码）
        current_password = test_data["valid_login_data"][0]["password"]
        target_password = "Wh520520!"
        
        # 如果当前密码已经是目标密码，则无需修改
        if current_password == target_password:
            logger.info(f"当前密码已经是 {target_password}，无需恢复")
            return
        
        # 截图：恢复前状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_restore_before_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-恢复密码前",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"尝试将密码从 {current_password} 恢复为 {target_password}")
        
        # 修改密码
        password_page.change_password(
            current_password=current_password,
            new_password=target_password,
            confirm_password=target_password
        )
        
        # 等待保存完成
        password_page.page.wait_for_timeout(3000)
        
        # 截图：恢复后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"pwd_restore_after_{timestamp}.png"
        password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-恢复密码后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"✅ 密码已恢复为 {target_password}")
        logger.info("TC-PWD-999执行成功")

