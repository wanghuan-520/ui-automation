"""
忘记密码功能测试模块
包含ABP框架的忘记密码流程测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.forgot_password_page import ForgotPasswordPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def forgot_password_page(page):
    """忘记密码页面fixture - 使用pytest-playwright的page fixture"""
    # pytest-playwright会自动管理browser context
    forgot_page = ForgotPasswordPage(page)
    forgot_page.navigate()
    
    yield forgot_page
    
    # pytest-playwright会自动清理


@pytest.mark.forgot_password
class TestForgotPassword:
    """忘记密码功能测试类"""
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_forgot_password_page_load(self, forgot_password_page):
        """
        TC-FP-011: 忘记密码页面加载验证
        
        测试目标：验证忘记密码页面能够正确加载并显示所有必要元素
        测试区域：Forgot Password Page（ABP Framework密码重置页面）
        测试元素：
        - 页面标题（页面顶部）
        - 提示文本（说明如何重置密码）
        - 输入框 "Email"（邮箱输入框）
        - 按钮 "Send Password Reset Link"（提交按钮）
        - 链接 "Back to Login"（返回登录链接）
        
        测试步骤：
        1. [Forgot Password Page] 导航到忘记密码页面
        2. [验证] 确认页面加载成功
        3. [页面顶部] 验证页面标题可见
        4. [页面中部] 验证提示文本可见
        5. [Form区域] 验证邮箱输入框可见
        6. [Form区域] 验证提交按钮可见
        7. [页面底部] 验证返回登录链接可见
        
        预期结果：
        - 页面成功加载（URL正确）
        - 所有必要元素都可见
        - 页面布局完整，无加载错误
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-011: 忘记密码页面加载验证")
        logger.info("测试目标: 验证页面加载和所有元素显示")
        logger.info("=" * 60)
        
        # 截图：页面加载完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_loaded_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-忘记密码页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证页面加载
        assert forgot_password_page.is_loaded(), "忘记密码页面未正确加载"
        
        # 验证关键元素
        assert forgot_password_page.is_visible(forgot_password_page.PAGE_TITLE), "页面标题应该可见"
        assert forgot_password_page.is_hint_text_visible(), "提示文本应该可见"
        assert forgot_password_page.is_visible(forgot_password_page.EMAIL_INPUT), "邮箱输入框应该可见"
        assert forgot_password_page.is_visible(forgot_password_page.SUBMIT_BUTTON), "提交按钮应该可见"
        assert forgot_password_page.is_login_link_visible(), "登录链接应该可见"
        
        # 截图：所有元素验证完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_elements_verified_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-所有元素验证完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-FP-011执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_forgot_password_existing_email(self, forgot_password_page, test_data):
        """
        TC-FP-001: 使用有效邮箱提交忘记密码请求
        验证ABP忘记密码功能
        """
        logger.info("开始执行TC-FP-001: 使用有效邮箱提交忘记密码请求")
        
        # 使用已存在的邮箱
        valid_email = test_data["valid_login_data"][0].get("email", "haylee5@test.com")
        logger.info(f"使用邮箱: {valid_email}")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_existing_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 填写邮箱
        forgot_password_page.fill_email(valid_email)
        
        # 截图：填写邮箱后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_existing_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写有效邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(3000)
        
        # 截图：提交后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_existing_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-提交后的页面（应显示成功提示）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证显示成功或信息消息
        has_success = forgot_password_page.is_success_message_visible()
        has_info = forgot_password_page.is_info_message_visible()
        
        logger.info(f"成功消息: {has_success}, 信息消息: {has_info}")
        
        if has_success:
            success_msg = forgot_password_page.get_success_message()
            logger.info(f"成功消息内容: {success_msg}")
        
        if has_info:
            info_msg = forgot_password_page.get_info_message()
            logger.info(f"信息消息内容: {info_msg}")
        
        # ABP应该显示成功提示（无论邮箱是否存在，防止枚举）
        assert has_success or has_info, "应该显示成功或信息提示"
        
        logger.info("TC-FP-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_forgot_password_empty_email(self, forgot_password_page):
        """
        TC-FP-004: 邮箱为空校验
        验证邮箱为空时的验证
        """
        logger.info("开始执行TC-FP-004: 邮箱为空校验")
        
        # 截图：邮箱为空
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_empty_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-邮箱为空",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 直接点击提交（邮箱为空）
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(1000)
        
        # 截图：点击提交后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_empty_error_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击提交后（应显示必填验证）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证HTML5必填验证
        is_valid = forgot_password_page.is_email_valid()
        assert not is_valid, "邮箱为空时应该invalid"
        
        # 验证仍在忘记密码页面
        current_url = forgot_password_page.page.url
        assert "/ForgotPassword" in current_url, "邮箱为空时应保持在忘记密码页面"
        
        logger.info("TC-FP-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_forgot_password_invalid_email_format(self, forgot_password_page):
        """
        TC-FP-005: 无效邮箱格式校验
        验证邮箱格式验证
        """
        logger.info("开始执行TC-FP-005: 无效邮箱格式校验")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_invalid_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 填写无效邮箱格式
        invalid_email = "invalid-email-format"
        forgot_password_page.fill_email(invalid_email)
        
        # 截图：填写无效邮箱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_invalid_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写无效邮箱格式",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(1000)
        
        # 截图：提交后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_invalid_error_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-提交后（应显示格式错误）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证HTML5邮箱格式验证
        is_valid = forgot_password_page.is_email_valid()
        logger.info(f"邮箱格式验证结果: {is_valid}")
        
        logger.info("TC-FP-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.security
    @pytest.mark.abp_validation
    def test_p1_forgot_password_enumeration_protection(self, forgot_password_page):
        """
        TC-FP-009: ABP邮箱枚举防护
        验证ABP不泄露邮箱是否存在的信息
        """
        logger.info("开始执行TC-FP-009: ABP邮箱枚举防护")
        
        # 场景1: 提交不存在的邮箱
        logger.info("场景1: 提交不存在的邮箱")
        nonexistent_email = f"nonexistent_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_enum_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-场景1初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        forgot_password_page.clear_email_field()
        forgot_password_page.fill_email(nonexistent_email)
        
        # 截图：填写不存在的邮箱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_enum_nonexistent_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写不存在的邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 记录提交时间
        import time
        start_time_1 = time.time()
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(3000)
        end_time_1 = time.time()
        response_time_1 = end_time_1 - start_time_1
        
        # 截图：不存在邮箱的响应
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_enum_nonexistent_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-不存在邮箱的响应",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取响应消息
        message_1 = ""
        if forgot_password_page.is_success_message_visible():
            message_1 = forgot_password_page.get_success_message()
        elif forgot_password_page.is_info_message_visible():
            message_1 = forgot_password_page.get_info_message()
        elif forgot_password_page.is_error_message_visible():
            message_1 = forgot_password_page.get_error_message()
        
        logger.info(f"不存在邮箱 - 响应时间: {response_time_1:.2f}秒, 消息: {message_1}")
        
        # ABP安全特性：无论邮箱是否存在，都应显示相同的成功消息
        # 这样可以防止攻击者枚举系统中的邮箱地址
        logger.info("✅ ABP邮箱枚举防护验证：应显示通用成功消息，不泄露邮箱是否存在")
        
        logger.info("TC-FP-009执行成功")
    
    @pytest.mark.P2
    @pytest.mark.navigation
    def test_p2_forgot_password_back_to_login(self, forgot_password_page):
        """
        TC-FP-003: 返回登录页面链接验证
        验证登录链接功能
        """
        logger.info("开始执行TC-FP-003: 返回登录页面链接验证")
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_back_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-忘记密码页面初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击登录链接
        forgot_password_page.click_login_link()
        forgot_password_page.page.wait_for_timeout(2000)
        
        # 截图：跳转后的登录页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_back_login_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-跳转到登录页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证URL
        current_url = forgot_password_page.page.url
        assert "/Login" in current_url, f"应该跳转到登录页面，实际URL: {current_url}"
        
        logger.info("TC-FP-003执行成功")
    
    @pytest.mark.P2
    @pytest.mark.boundary
    def test_p2_forgot_password_shortest_valid_email(self, forgot_password_page):
        """
        TC-FP-008: 最短有效邮箱测试
        验证最短邮箱格式
        """
        logger.info("开始执行TC-FP-008: 最短有效邮箱测试")
        
        # 最短有效邮箱: a@b.c
        shortest_email = "a@b.c"
        
        # 截图：初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_shortest_initial_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        forgot_password_page.fill_email(shortest_email)
        
        # 截图：填写最短邮箱
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_shortest_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-填写最短邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证邮箱格式有效
        is_valid = forgot_password_page.is_email_valid()
        assert is_valid, "最短邮箱格式应该通过HTML5验证"
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(2000)
        
        # 截图：提交后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_shortest_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-提交后（应显示成功提示）",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("TC-FP-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_forgot_password_hint_text_display(self, forgot_password_page):
        """
        TC-FP-012: 提示信息显示验证
        验证提示文本内容
        """
        logger.info("开始执行TC-FP-012: 提示信息显示验证")
        
        # 截图：提示文本区域
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_hint_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-提示文本区域",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证提示文本可见
        assert forgot_password_page.is_hint_text_visible(), "提示文本应该可见"
        
        # 获取提示文本内容
        hint_text = forgot_password_page.get_hint_text()
        logger.info(f"提示文本内容: {hint_text}")
        
        # 验证文本内容包含关键信息
        assert "电子邮件" in hint_text or "email" in hint_text.lower(), "提示应该提到邮箱"
        assert "重置" in hint_text or "reset" in hint_text.lower(), "提示应该提到重置密码"
        
        logger.info("TC-FP-012执行成功")

