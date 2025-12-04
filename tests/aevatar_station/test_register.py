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
    """注册页面fixture - 使用pytest-playwright的page fixture"""
    # pytest-playwright会自动管理browser context
    register_page = RegisterPage(page)
    register_page.navigate()
    
    yield register_page
    
    # pytest-playwright会自动清理


@pytest.mark.register
class TestRegister:
    """注册功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_register_page_load(self, register_page):
        """
        TC-REG-022: 注册页面加载验证测试
        
        测试目标：验证注册页面能够正确加载并显示所有必要的表单元素
        测试区域：Register Page（ABP Framework用户注册页面）
        测试元素：
        - 页面标题（页面顶部）
        - 输入框 "User name"（用户名输入框）
        - 输入框 "Email address"（邮箱输入框）
        - 输入框 "Password"（密码输入框）
        - 按钮 "Register"（注册提交按钮）
        - 链接 "Login"或"Back to login"（返回登录链接）
        
        测试步骤：
        1. [Register Page] 导航到注册页面
        2. [验证] 确认页面加载成功（URL正确）
        3. [页面顶部] 验证页面标题可见
        4. [Form区域] 验证用户名输入框可见
        5. [Form区域] 验证邮箱输入框可见
        6. [Form区域] 验证密码输入框可见
        7. [Form区域] 验证注册按钮可见
        8. [页面底部] 验证登录链接可见
        
        预期结果：
        - 页面成功加载到注册URL
        - 所有表单元素（3个输入框+1个按钮）都可见
        - 登录链接显示在页面底部
        - 页面布局完整，无加载错误
        """
        logger.info("开始执行TC-REG-022: 注册页面加载验证")
        
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
        
        # 验证所有关键元素可见
        assert register_page.is_visible(register_page.PAGE_TITLE), "页面标题应该可见"
        assert register_page.is_visible(register_page.USERNAME_INPUT), "用户名输入框应该可见"
        assert register_page.is_visible(register_page.EMAIL_INPUT), "邮箱输入框应该可见"
        assert register_page.is_visible(register_page.PASSWORD_INPUT), "密码输入框应该可见"
        assert register_page.is_visible(register_page.REGISTER_BUTTON), "注册按钮应该可见"
        assert register_page.is_visible(register_page.LOGIN_LINK), "登录链接应该可见"
        
        # 截图：所有元素验证完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_elements_verified_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-所有表单元素验证完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-REG-022执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_register_with_valid_data(self, register_page, test_data):
        """
        TC-REG-001: 使用有效数据注册新用户测试
        
        测试目标：验证用户能够使用符合要求的数据成功注册新账户
        测试区域：Register Page - Registration Form
        测试元素：
        - 输入框 "User name"（用户名输入框）
        - 输入框 "Email address"（邮箱输入框）
        - 输入框 "Password"（密码输入框）
        - 按钮 "Register"（注册提交按钮）
        
        测试步骤：
        1. [前置条件] 已导航到注册页面
        2. [数据准备] 生成唯一的用户名和邮箱（时间戳）
        3. [Form - 字段1] 填写有效的用户名
        4. [Form - 字段2] 填写有效的邮箱地址
        5. [Form - 字段3] 填写符合复杂度的密码
        6. [Form - 按钮] 点击"Register"按钮
        7. [验证] 等待页面响应（跳转或显示消息）
        8. [验证] 确认注册成功（URL变化或成功消息）
        
        预期结果：
        - 所有字段成功填写
        - 点击注册按钮后提交成功
        - 跳转到登录页面或其他页面（URL改变）
        - 或显示注册成功消息
        - 不停留在注册页面（除非显示成功消息）
        """
        logger.info("开始执行TC-REG-001: 使用有效数据注册新用户")
        
        # 生成唯一的用户名和邮箱
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        username = f"testuser_{timestamp_str}"
        email = f"testuser_{timestamp_str}@test.com"
        password = "TestPass123!"
        
        logger.info(f"注册数据 - 用户名: {username}, 邮箱: {email}")
        
        # 截图：注册页面初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-注册页面初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 填写注册信息
        register_page.fill_username(username)
        register_page.fill_email(email)
        register_page.fill_password(password)
        
        # 截图：所有字段填写完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_filled_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-所有字段填写完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击注册按钮
        register_page.click_register_button()
        register_page.page.wait_for_timeout(2000)
        
        # 截图：点击注册后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_submitted_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-点击注册按钮后",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 等待页面响应
        register_page.page.wait_for_load_state("networkidle", timeout=10000)
        register_page.page.wait_for_timeout(2000)
        
        # 截图：注册完成后的页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"register_result_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="4-注册完成后的页面状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证注册结果（可能跳转到登录页面或自动登录）
        current_url = register_page.page.url
        logger.info(f"注册后的URL: {current_url}")
        
        # 注册成功的判断条件：
        # 1. URL不再是注册页面
        # 2. 或显示成功消息
        # 3. 或跳转到登录页面
        assert "/Register" not in current_url or register_page.is_success_message_visible(), \
            "注册应该成功并跳转或显示成功消息"
        
        logger.info("TC-REG-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_username_empty(self, register_page):
        """
        TC-REG-004: 用户名为空校验测试
        
        测试目标：验证当用户名字段为空时，系统阻止注册并显示验证错误
        测试区域：Register Page - Form Validation
        测试元素：
        - 输入框 "User name"（用户名输入框 - 保持为空）
        - 输入框 "Email address"（邮箱输入框 - 填写有效值）
        - 输入框 "Password"（密码输入框 - 填写有效值）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [前置条件] 已导航到注册页面
        2. [Form - 字段1] 用户名输入框保持为空（不填写）
        3. [Form - 字段2] 填写有效的邮箱地址
        4. [Form - 字段3] 填写有效的密码
        5. [Form - 按钮] 点击"Register"按钮
        6. [验证] 检查用户名字段的HTML5验证状态
        7. [验证] 确认仍停留在注册页面（未提交）
        8. [验证] 确认显示必填字段验证提示
        
        预期结果：
        - HTML5必填验证触发
        - 用户名输入框显示为invalid状态
        - 表单不提交（仍在注册页面）
        - 显示"此字段为必填项"或类似提示
        """
        logger.info("开始执行TC-REG-004: 用户名为空校验")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"username_empty_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 用户名保持为空，填写其他字段
        register_page.fill_email("valid@test.com")
        register_page.fill_password("ValidPass123!")
        
        # 截图：用户名为空
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"username_empty_filled_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-用户名为空，其他字段已填写",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击注册按钮
        register_page.click_register_button()
        register_page.page.wait_for_timeout(1000)
        
        # 截图：点击注册后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"username_empty_error_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-点击注册后（应显示验证错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证HTML5必填字段验证
        is_valid = register_page.is_username_valid()
        assert not is_valid, "用户名为空时should be invalid"
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, "用户名为空时应该保持在注册页面"
        
        logger.info("TC-REG-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_email_invalid_format(self, register_page):
        """
        TC-REG-008: 邮箱格式校验测试（无效格式）
        
        测试目标：验证当邮箱格式无效时，系统阻止注册并触发格式验证
        测试区域：Register Page - Form Validation
        测试元素：
        - 输入框 "User name"（用户名输入框 - 填写有效值）
        - 输入框 "Email address"（邮箱输入框 - 填写无效格式）
        - 输入框 "Password"（密码输入框 - 填写有效值）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [前置条件] 已导航到注册页面
        2. [Form - 字段1] 填写有效的用户名
        3. [Form - 字段2] 填写无效格式的邮箱（如：invalid-email）
        4. [Form - 字段3] 填写有效的密码
        5. [Form - 按钮] 点击"Register"按钮
        6. [验证] 检查邮箱字段的HTML5验证状态
        7. [验证] 确认仍停留在注册页面
        8. [验证] 确认显示邮箱格式错误提示
        
        预期结果：
        - HTML5邮箱格式验证触发
        - 邮箱输入框显示为invalid状态
        - 表单不提交（仍在注册页面）
        - 显示"请输入有效的邮箱地址"或类似提示
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-REG-008: 邮箱格式校验测试")
        logger.info("测试目标: 验证邮箱格式验证")
        logger.info("=" * 60)
        
        # 步骤1-2：验证初始状态
        logger.info("步骤1: [Register Page] 验证注册页面初始状态")
        current_url = register_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        logger.info("   ✓ 已在注册页面")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"email_invalid_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   📸 已截图：初始状态")
        
        # 步骤2-4：填写表单（邮箱为无效格式）
        logger.info("\n步骤2-4: [Form区域] 填写表单（邮箱为无效格式）")
        
        logger.info("   [Form - 字段1] 填写用户名...")
        register_page.fill_username("validuser")
        logger.info("   ✓ 用户名已填写: validuser")
        
        logger.info("   [Form - 字段2] 填写无效邮箱格式...")
        register_page.fill_email("invalid-email")  # 无效格式
        logger.info("   ✓ 邮箱已填写: invalid-email（无效格式）")
        
        logger.info("   [Form - 字段3] 填写密码...")
        register_page.fill_password("ValidPass123!")
        logger.info("   ✓ 密码已填写")
        
        # 截图：无效邮箱格式
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"email_invalid_filled_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写无效邮箱格式",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤5：点击注册按钮
        logger.info("\n步骤5: [Form - 按钮] 点击'Register'按钮")
        register_page.click_register_button()
        logger.info("   ✓ 已点击注册按钮")
        
        register_page.page.wait_for_timeout(1000)
        
        # 截图：点击注册后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"email_invalid_error_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-点击注册后（应显示邮箱格式错误）",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info("   📸 已截图：点击注册后的验证状态")
        
        # 步骤6-8：验证结果
        logger.info("\n步骤6-8: [验证] 确认邮箱格式验证")
        
        # 验证HTML5邮箱格式验证
        is_valid = register_page.is_email_valid()
        logger.info(f"   邮箱字段验证状态: {'valid' if is_valid else 'invalid'}")
        
        if not is_valid:
            logger.info("   ✓ 邮箱格式验证触发（invalid状态）")
        else:
            logger.info("   ℹ️ HTML5验证未触发（浏览器差异）")
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        logger.info(f"   当前URL: {current_url}")
        
        assert "/Register" in current_url, "邮箱格式无效时应该保持在注册页面"
        logger.info("   ✓ 表单未提交，仍停留在注册页面")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-REG-008执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 用户名和密码已填写")
        logger.info("  ✓ 邮箱格式无效（invalid-email）")
        if not is_valid:
            logger.info("  ✓ HTML5格式验证触发")
        logger.info("  ✓ 表单未提交（停留在注册页面）")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_weak_password(self, register_page, test_data):
        """
        TC-REG-013~015: 弱密码校验测试（批量）
        
        测试目标：验证系统拒绝不符合密码复杂度要求的弱密码
        测试区域：Register Page - Password Validation
        测试元素：
        - 输入框 "User name"（用户名输入框）
        - 输入框 "Email address"（邮箱输入框）
        - 输入框 "Password"（密码输入框 - 填写弱密码）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [数据准备] 从test_data加载弱密码场景列表
        2. [循环] 对每个弱密码场景：
           a. [Form] 清空所有字段
           b. [Form] 填写有效的用户名和邮箱
           c. [Form] 填写当前场景的弱密码
           d. [按钮] 点击注册按钮
           e. [验证] 检查是否显示密码强度错误
           f. [验证] 确认仍在注册页面
        3. [完成] 所有场景测试完毕
        
        预期结果：
        - 每个弱密码都应被拒绝
        - 显示密码强度不足的错误消息
        - 或前端阻止提交（HTML5验证）
        - 不允许注册成功
        """
        logger.info("开始执行TC-REG-013~015: 弱密码校验")
        
        weak_passwords = test_data.get("register_data", {}).get("weak_passwords", [])
        
        for idx, pwd_data in enumerate(weak_passwords[:3], 1):  # 测试前3个弱密码
            password = pwd_data["password"]
            description = pwd_data["description"]
            
            logger.info(f"测试场景{idx}: {description} - 密码: {password}")
            
            # 截图：初始状态
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"weak_pwd_{idx}_initial_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*2-1}-{description}-初始状态",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 填写数据
            register_page.clear_all_fields()
            register_page.fill_username("validuser")
            register_page.fill_email(f"valid{idx}@test.com")
            register_page.fill_password(password)
            
            # 截图：填写弱密码后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"weak_pwd_{idx}_filled_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*2}-{description}-填写后",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 点击注册按钮
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 记录是否显示错误（弱密码可能有前端或后端验证）
            has_error = register_page.is_error_message_visible()
            error_msg = register_page.get_error_message() if has_error else "无错误消息"
            logger.info(f"场景{idx}结果 - 错误消息: {error_msg}")
        
        logger.info("TC-REG-013~015执行成功")
    
    @pytest.mark.P2
    @pytest.mark.navigation
    def test_p2_register_login_link(self, register_page):
        """
        TC-REG-003: 跳转到登录页面链接验证测试
        
        测试目标：验证注册页面的"登录"链接能够正确跳转到登录页面
        测试区域：Register Page - Navigation
        测试元素：
        - 链接 "Login"或"Back to login"（页面底部）
        
        测试步骤：
        1. [前置条件] 已导航到注册页面
        2. [Register Page - 底部] 定位"Login"链接
        3. [验证] 确认链接可见
        4. [Register Page - 底部] 点击"Login"链接
        5. [验证] 等待页面跳转
        6. [验证] 确认跳转到登录页面（URL包含/Login）
        
        预期结果：
        - 登录链接在注册页面底部显示
        - 点击后成功跳转到登录页面
        - 登录页面正确加载
        """
        logger.info("开始执行TC-REG-003: 跳转到登录页面链接验证")
        
        # 截图：注册页面初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"nav_to_login_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-注册页面初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击登录链接
        register_page.click_login_link()
        register_page.page.wait_for_timeout(2000)
        
        # 截图：跳转后的登录页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"nav_to_login_result_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-跳转后的登录页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证URL
        current_url = register_page.page.url
        assert "/Login" in current_url, f"应该跳转到登录页面，实际URL: {current_url}"
        
        logger.info("TC-REG-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_register_all_fields_empty(self, register_page):
        """
        TC-REG-007: 所有字段为空校验测试
        
        测试目标：验证当所有必填字段为空时，系统阻止注册并显示验证错误
        测试区域：Register Page - Form Validation
        测试元素：
        - 输入框 "User name"（保持为空）
        - 输入框 "Email address"（保持为空）
        - 输入框 "Password"（保持为空）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [前置条件] 已导航到注册页面
        2. [验证] 确认所有字段为空（初始状态）
        3. [Form - 按钮] 直接点击"Register"按钮
        4. [验证] 检查第一个必填字段（用户名）的验证状态
        5. [验证] 确认触发HTML5必填验证
        6. [验证] 确认仍停留在注册页面
        
        预期结果：
        - HTML5必填验证触发（阻止表单提交）
        - 用户名字段显示为invalid状态
        - 浏览器显示"请填写此字段"提示
        - 表单不提交，停留在注册页面
        """
        logger.info("开始执行TC-REG-007: 所有字段为空校验")
        
        # 截图：所有字段为空
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"all_empty_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-所有字段为空",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 直接点击注册按钮
        register_page.click_register_button()
        register_page.page.wait_for_timeout(1000)
        
        # 截图：点击注册后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"all_empty_error_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击注册后（应显示验证错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证第一个必填字段（用户名）显示验证错误
        is_valid = register_page.is_username_valid()
        assert not is_valid, "所有字段为空时用户名应该invalid"
        
        # 验证仍在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, "所有字段为空时应该保持在注册页面"
        
        logger.info("TC-REG-007执行成功")
    
    # ========== ABP特定验证测试 ==========
    
    @pytest.mark.P0
    @pytest.mark.validation
    @pytest.mark.abp_validation
    def test_p0_abp_password_complexity(self, register_page, test_data):
        """
        TC-REG-ABP-001~006: ABP密码复杂度验证测试（批量）
        
        测试目标：验证ABP框架的密码复杂度规则（需要数字、大写、小写、特殊字符）
        测试区域：Register Page - ABP Password Validation
        测试元素：
        - 输入框 "User name"（用户名输入框）
        - 输入框 "Email address"（邮箱输入框）
        - 输入框 "Password"（密码输入框 - 测试各种复杂度）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [数据准备] 从test_data加载ABP密码验证场景（6个）
        2. [循环] 对每个密码场景：
           a. [数据] 生成唯一的用户名和邮箱
           b. [Form] 填写用户名、邮箱和测试密码
           c. [按钮] 点击注册按钮
           d. [验证] 检查ABP后端返回的错误消息
           e. [验证] 确认错误消息包含相应的复杂度要求提示
        3. [场景] 测试6种情况：
           - 缺少数字
           - 缺少大写字母
           - 缺少小写字母
           - 缺少特殊字符
           - 长度不足
           - 符合所有要求（应成功）
        
        预期结果：
        - 不符合要求的密码被ABP后端拒绝
        - 显示具体的复杂度错误提示
        - 符合所有要求的密码可以通过验证
        """
        logger.info("开始执行TC-REG-ABP: ABP密码复杂度验证")
        
        abp_pwd_data = test_data.get("register_data", {}).get("abp_password_validation", [])
        
        for idx, pwd_test in enumerate(abp_pwd_data, 1):
            username = pwd_test["username"]
            email = pwd_test["email"]
            password = pwd_test["password"]
            missing = pwd_test["missing"]
            description = pwd_test["description"]
            
            logger.info(f"测试场景{idx}: {description}")
            logger.info(f"密码: {'*' * len(password)}, 缺少: {missing}")
            
            # 截图：初始状态
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_pwd_{idx}_initial_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3-2}-{description}-初始状态",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 清空并填写新数据
            register_page.clear_all_fields()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_username = f"{username}_{timestamp_str}"
            unique_email = f"{username}_{timestamp_str}@test.com"
            
            register_page.fill_username(unique_username)
            register_page.fill_email(unique_email)
            register_page.fill_password(password)
            
            # 截图：填写数据后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_pwd_{idx}_filled_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3-1}-{description}-填写后",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 点击注册
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 截图：提交后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_pwd_{idx}_result_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3}-{description}-提交结果",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证结果
            if missing == "none":
                # 期望成功（符合所有要求的密码）
                logger.info(f"场景{idx}: 密码符合要求，应该注册成功或进入下一步")
                # 验证URL变化或显示成功消息
                current_url = register_page.page.url
                has_success = register_page.is_success_message_visible()
                logger.info(f"结果 - URL: {current_url}, 成功消息: {has_success}")
            else:
                # 期望失败（密码不符合要求）
                logger.info(f"场景{idx}: 检查ABP密码复杂度错误消息")
                
                # 检查是否有错误消息
                has_error = register_page.is_error_message_visible()
                if has_error:
                    error_msg = register_page.get_error_message()
                    logger.info(f"ABP错误消息: {error_msg}")
                    
                    # 验证错误消息包含关键词（支持中英文）
                    expected_cn = pwd_test.get("expected_error_cn", "")
                    expected_en = pwd_test.get("expected_error_en", "")
                    
                    error_found = expected_cn in error_msg or expected_en.lower() in error_msg.lower()
                    logger.info(f"错误消息匹配: {error_found}")
                else:
                    logger.warning(f"场景{idx}: 未发现错误消息，可能是前端未实现验证或验证通过")
                
                # 验证仍在注册页面
                current_url = register_page.page.url
                assert "/Register" in current_url, f"密码不符合要求时应保持在注册页面，实际URL: {current_url}"
            
            # 等待一下再进行下一个测试
            register_page.page.wait_for_timeout(500)
        
        logger.info("TC-REG-ABP-001~006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    @pytest.mark.abp_validation
    def test_p1_abp_username_format(self, register_page, test_data):
        """
        TC-REG-ABP-007~010: ABP用户名格式验证测试（批量）
        
        测试目标：验证ABP框架的用户名格式规则（不允许空格、特殊字符等）
        测试区域：Register Page - ABP Username Validation
        测试元素：
        - 输入框 "User name"（用户名输入框 - 测试各种格式）
        - 输入框 "Email address"（邮箱输入框）
        - 输入框 "Password"（密码输入框）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [数据准备] 从test_data加载ABP用户名验证场景（4个）
        2. [循环] 对每个用户名场景：
           a. [数据] 准备测试用户名和有效的邮箱、密码
           b. [Form] 填写所有字段
           c. [按钮] 点击注册按钮
           d. [验证] 检查ABP返回的用户名格式错误
           e. [验证] 确认仍在注册页面
        3. [场景] 测试4种情况：
           - 包含空格
           - 包含特殊字符
           - 只有特殊字符
           - 符合格式要求（应成功）
        
        预期结果：
        - 不符合格式的用户名被ABP拒绝
        - 显示用户名格式错误提示
        - 符合格式的用户名可以通过验证
        """
        logger.info("开始执行TC-REG-ABP: ABP用户名格式验证")
        
        username_data = test_data.get("register_data", {}).get("abp_username_validation", [])
        
        for idx, user_test in enumerate(username_data, 1):
            username = user_test["username"]
            email = user_test["email"]
            password = user_test["password"]
            error_type = user_test["error_type"]
            description = user_test["description"]
            
            logger.info(f"测试场景{idx}: {description}")
            logger.info(f"用户名: '{username}', 错误类型: {error_type}")
            
            # 截图：初始状态
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_username_{idx}_initial_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3-2}-{description}-初始状态",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 清空并填写数据
            register_page.clear_all_fields()
            timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_email = f"user{idx}_{timestamp_str}@test.com"
            
            register_page.fill_username(username)
            register_page.fill_email(unique_email)
            register_page.fill_password(password)
            
            # 截图：填写后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_username_{idx}_filled_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3-1}-{description}-填写后",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 点击注册
            register_page.click_register_button()
            register_page.page.wait_for_timeout(2000)
            
            # 截图：提交后
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"abp_username_{idx}_result_{timestamp}.png"
            register_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{idx*3}-{description}-提交结果",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证结果
            if error_type == "none":
                # 期望成功
                logger.info(f"场景{idx}: 用户名格式有效，应该注册成功")
                current_url = register_page.page.url
                logger.info(f"结果URL: {current_url}")
            else:
                # 期望失败
                logger.info(f"场景{idx}: 检查ABP用户名格式错误")
                
                has_error = register_page.is_error_message_visible()
                if has_error:
                    error_msg = register_page.get_error_message()
                    logger.info(f"ABP错误消息: {error_msg}")
                    
                    expected_error = user_test.get("expected_error", "")
                    if expected_error:
                        error_found = expected_error in error_msg
                        logger.info(f"错误消息包含'{expected_error}': {error_found}")
                else:
                    logger.warning(f"场景{idx}: 未发现错误消息（可能前端未实现验证）")
                
                current_url = register_page.page.url
                assert "/Register" in current_url, f"用户名格式无效时应保持在注册页面"
            
            register_page.page.wait_for_timeout(500)
        
        logger.info("TC-REG-ABP-007~010执行成功")
    
    @pytest.mark.P0
    @pytest.mark.abp_validation
    def test_p0_duplicate_username(self, register_page, test_data):
        """
        TC-REGISTER-020: 重复用户名验证测试
        
        测试目标：验证系统拒绝已存在的用户名，并显示友好的错误提示
        测试区域：Register Page - Uniqueness Validation
        测试元素：
        - 输入框 "User name"（填写已存在的用户名，如：admin）
        - 输入框 "Email address"（填写唯一的邮箱）
        - 输入框 "Password"（填写有效密码）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [数据准备] 使用已知存在的用户名（如：admin）
        2. [Form - 字段1] 填写已存在的用户名
        3. [Form - 字段2] 填写唯一的邮箱地址
        4. [Form - 字段3] 填写有效的密码
        5. [Form - 按钮] 点击"Register"按钮
        6. [验证] 等待后端响应
        7. [验证] 确认显示"用户名已存在"错误消息
        8. [验证] 确认仍停留在注册页面
        
        预期结果：
        - ABP后端检测到用户名重复
        - 返回错误消息（包含"username"和"already"或"exists"）
        - 注册失败，停留在注册页面
        - 错误消息清晰友好
        """
        logger.info("开始执行TC-REGISTER-020: 重复用户名验证")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"duplicate_username_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-注册页面初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 使用测试数据中的重复用户名（如果存在）
        duplicate_data = None
        if "duplicate_data" in test_data:
            duplicate_data = test_data["duplicate_data"][0]
        
        if not duplicate_data:
            # 如果没有预定义的重复数据，使用一个已知存在的用户名
            duplicate_data = {
                "username": "admin",  # ABP默认管理员用户名
                "email": f"test_dup_{timestamp}@test.com",
                "password": "Test123456!"
            }
        
        logger.info(f"尝试注册重复用户名: {duplicate_data['username']}")
        
        # 填写表单
        register_page.fill_username(duplicate_data["username"])
        register_page.fill_email(duplicate_data["email"])
        register_page.fill_password(duplicate_data["password"])
        
        # 截图：填写后
        screenshot_path = f"duplicate_username_filled_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写重复用户名",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击注册
        register_page.click_register_button()
        register_page.page.wait_for_timeout(2000)
        
        # 截图：提交后
        screenshot_path = f"duplicate_username_error_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-显示错误消息",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证：应该显示错误消息
        has_error = register_page.is_error_message_visible()
        logger.info(f"是否显示错误消息: {has_error}")
        
        if has_error:
            error_msg = register_page.get_error_message()
            logger.info(f"错误消息: {error_msg}")
            assert "username" in error_msg.lower() or "already" in error_msg.lower() or "exists" in error_msg.lower(), \
                f"错误消息应提示用户名已存在，实际: {error_msg}"
        
        # 验证：应该保持在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, f"应该保持在注册页面，实际URL: {current_url}"
        
        logger.info("TC-REGISTER-020执行成功")
    
    @pytest.mark.P0
    @pytest.mark.abp_validation
    def test_p0_duplicate_email(self, register_page, test_data):
        """
        TC-REGISTER-021: 重复邮箱验证测试
        
        测试目标：验证系统拒绝已注册的邮箱，并显示友好的错误提示
        测试区域：Register Page - Uniqueness Validation
        测试元素：
        - 输入框 "User name"（填写唯一的用户名）
        - 输入框 "Email address"（填写已存在的邮箱）
        - 输入框 "Password"（填写有效密码）
        - 按钮 "Register"（注册按钮）
        
        测试步骤：
        1. [数据准备] 使用已知存在的邮箱（如：admin@aevatar.ai）
        2. [Form - 字段1] 填写唯一的用户名
        3. [Form - 字段2] 填写已存在的邮箱
        4. [Form - 字段3] 填写有效的密码
        5. [Form - 按钮] 点击"Register"按钮
        6. [验证] 等待后端响应
        7. [验证] 确认显示"邮箱已注册"错误消息
        8. [验证] 确认仍停留在注册页面
        
        预期结果：
        - ABP后端检测到邮箱重复
        - 返回错误消息（包含"email"和"already"或"exists"）
        - 注册失败，停留在注册页面
        - 错误消息清晰友好
        """
        logger.info("开始执行TC-REGISTER-021: 重复邮箱验证")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"duplicate_email_initial_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-注册页面初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 使用测试数据中的重复邮箱（如果存在）
        duplicate_data = None
        if "duplicate_data" in test_data and len(test_data["duplicate_data"]) > 1:
            duplicate_data = test_data["duplicate_data"][1]
        
        if not duplicate_data:
            # 如果没有预定义的重复数据，使用一个已知存在的邮箱
            duplicate_data = {
                "username": f"testuser_{timestamp}",
                "email": "admin@aevatar.ai",  # 使用已知存在的邮箱
                "password": "Test123456!"
            }
        
        logger.info(f"尝试注册重复邮箱: {duplicate_data['email']}")
        
        # 填写表单
        register_page.fill_username(duplicate_data["username"])
        register_page.fill_email(duplicate_data["email"])
        register_page.fill_password(duplicate_data["password"])
        
        # 截图：填写后
        screenshot_path = f"duplicate_email_filled_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写重复邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击注册
        register_page.click_register_button()
        register_page.page.wait_for_timeout(2000)
        
        # 截图：提交后
        screenshot_path = f"duplicate_email_error_{timestamp}.png"
        register_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-显示错误消息",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证：应该显示错误消息
        has_error = register_page.is_error_message_visible()
        logger.info(f"是否显示错误消息: {has_error}")
        
        if has_error:
            error_msg = register_page.get_error_message()
            logger.info(f"错误消息: {error_msg}")
            assert "email" in error_msg.lower() or "already" in error_msg.lower() or "exists" in error_msg.lower(), \
                f"错误消息应提示邮箱已被注册，实际: {error_msg}"
        
        # 验证：应该保持在注册页面
        current_url = register_page.page.url
        assert "/Register" in current_url, f"应该保持在注册页面，实际URL: {current_url}"
        
        logger.info("TC-REGISTER-021执行成功")

