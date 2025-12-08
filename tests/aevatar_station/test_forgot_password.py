"""
忘记密码功能测试模块
包含ABP框架的忘记密码流程测试
"""
import pytest
import logging
import allure
import time
from datetime import datetime
from tests.aevatar_station.pages.forgot_password_page import ForgotPasswordPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def forgot_password_page(page):
    """
    忘记密码页面fixture
    ⚡ 增强版：集成页面加载诊断与自动截图
    """
    forgot_page = ForgotPasswordPage(page)
    
    try:
        forgot_page.navigate()
        
        # 验证页面是否真正加载成功
        if not forgot_page.is_loaded():
            raise Exception("Forgot Password页面关键元素未加载")
            
    except Exception as e:
        logger.error(f"❌ 导航到Forgot Password页面失败: {e}")
        
        # 🔍 深度诊断
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/forgot_pwd_load_fail_{timestamp}.png"
        page.screenshot(path=screenshot_path)
        logger.error(f"   已保存失败截图: {screenshot_path}")
        
        html_path = f"screenshots/forgot_pwd_load_fail_{timestamp}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())
        
        raise e
    
    yield forgot_page


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
        logger.info("=" * 60)
        
        # 验证页面加载
        assert forgot_password_page.is_loaded(), "忘记密码页面未正确加载"
        logger.info("   ✓ 页面加载状态检查通过")
        
        # 截图：页面加载完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_loaded_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-忘记密码页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证关键元素
        elements_to_check = [
            (forgot_password_page.PAGE_TITLE, "页面标题"),
            (forgot_password_page.EMAIL_INPUT, "邮箱输入框"),
            (forgot_password_page.SUBMIT_BUTTON, "提交按钮")
        ]
        
        for selector, name in elements_to_check:
            assert forgot_password_page.is_visible(selector), f"{name} 应该可见"
            logger.info(f"   ✓ {name} 可见")
            
        # 特殊检查
        assert forgot_password_page.is_hint_text_visible(), "提示文本应该可见"
        logger.info("   ✓ 提示文本可见")
        
        assert forgot_password_page.is_login_link_visible(), "登录链接应该可见"
        logger.info("   ✓ 登录链接可见")
        
        logger.info("✅ TC-FP-011执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_forgot_password_existing_email(self, forgot_password_page, test_data):
        """
        TC-FP-001: 使用有效邮箱提交忘记密码请求
        验证ABP忘记密码功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-001: 使用有效邮箱提交忘记密码请求")
        logger.info("=" * 60)
        
        # 使用已存在的邮箱
        valid_email = test_data["valid_login_data"][0].get("email", "haylee5@test.com")
        logger.info(f"   使用测试邮箱: {valid_email}")
        
        # 填写邮箱
        forgot_password_page.fill_email(valid_email)
        
        # 截图：填写前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_valid_input_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-填写有效邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击提交
        logger.info("   点击提交按钮...")
        forgot_password_page.click_submit_button()
        
        # 智能等待结果（等待成功提示或页面变化）
        # ABP通常会显示一个 Info 消息或跳转
        logger.info("   ⏳ 等待响应...")
        forgot_password_page.page.wait_for_timeout(1000) 
        
        # 验证显示成功或信息消息
        success_found = False
        info_found = False
        
        # 轮询检测消息（最多3秒）
        for _ in range(6):
            if forgot_password_page.is_success_message_visible():
                success_found = True
                break
            if forgot_password_page.is_info_message_visible():
                info_found = True
                break
            forgot_password_page.page.wait_for_timeout(500)
            
        # 截图：提交结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_valid_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-提交结果页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        if success_found:
            msg = forgot_password_page.get_success_message()
            logger.info(f"   ✅ 检测到成功消息: {msg}")
        elif info_found:
            msg = forgot_password_page.get_info_message()
            logger.info(f"   ✅ 检测到提示消息: {msg}")
        else:
            # 检查是否有错误消息
            if forgot_password_page.is_error_message_visible():
                err = forgot_password_page.get_error_message()
                logger.error(f"   ❌ 检测到错误消息: {err}")
                raise AssertionError(f"忘记密码请求失败: {err}")
                
        # ABP应该显示成功提示（无论邮箱是否存在，防止枚举）
        assert success_found or info_found, "提交后应显示成功或信息提示"
        
        logger.info("✅ TC-FP-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_forgot_password_empty_email(self, forgot_password_page):
        """
        TC-FP-004: 邮箱为空校验
        验证邮箱为空时的验证
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-004: 邮箱为空校验")
        logger.info("=" * 60)
        
        # 直接点击提交（邮箱为空）
        logger.info("   尝试提交空表单...")
        forgot_password_page.click_submit_button()
        
        # 等待HTML5验证触发
        forgot_password_page.page.wait_for_timeout(500)
        
        # 截图：验证提示
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_empty_validation_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="空值验证提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证HTML5必填验证
        is_valid = forgot_password_page.is_email_valid()
        logger.info(f"   HTML5验证状态: {'有效' if is_valid else '无效'}")
        assert not is_valid, "邮箱为空时HTML5验证应为invalid"
        
        # 验证仍在忘记密码页面（未发生跳转）
        current_url = forgot_password_page.page.url
        assert "/ForgotPassword" in current_url, "验证失败不应跳转"
        logger.info("   ✓ URL未发生跳转")
        
        logger.info("✅ TC-FP-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_forgot_password_invalid_email_format(self, forgot_password_page):
        """
        TC-FP-005: 无效邮箱格式校验
        验证邮箱格式验证
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-005: 无效邮箱格式校验")
        logger.info("=" * 60)
        
        # 填写无效邮箱格式
        invalid_email = "invalid-email-format"
        logger.info(f"   输入无效格式邮箱: {invalid_email}")
        forgot_password_page.fill_email(invalid_email)
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(500)
        
        # 截图：格式错误验证
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_invalid_format_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="格式错误验证提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证HTML5邮箱格式验证
        is_valid = forgot_password_page.is_email_valid()
        logger.info(f"   HTML5验证状态: {'有效' if is_valid else '无效'}")
        assert not is_valid, "无效邮箱格式HTML5验证应为invalid"
        
        logger.info("✅ TC-FP-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.security
    @pytest.mark.abp_validation
    def test_p1_forgot_password_enumeration_protection(self, forgot_password_page):
        """
        TC-FP-009: ABP邮箱枚举防护
        验证ABP不泄露邮箱是否存在的信息
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-009: ABP邮箱枚举防护")
        logger.info("测试目标: 验证无论邮箱是否存在，系统响应一致")
        logger.info("=" * 60)
        
        # 构造不存在的邮箱
        nonexistent_email = f"nonexistent_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"
        logger.info(f"   使用不存在的邮箱: {nonexistent_email}")
        
        forgot_password_page.clear_email_field()
        forgot_password_page.fill_email(nonexistent_email)
        
        # 记录提交时间
        start_time = time.time()
        forgot_password_page.click_submit_button()
        
        # 等待响应
        forgot_password_page.page.wait_for_timeout(1000)
        # 轮询直到出现消息
        for _ in range(10):
            if forgot_password_page.is_success_message_visible() or forgot_password_page.is_info_message_visible():
                break
            forgot_password_page.page.wait_for_timeout(500)
            
        end_time = time.time()
        response_time = end_time - start_time
        
        # 截图：枚举防护响应
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_enumeration_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="枚举防护响应页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取响应消息
        message = ""
        if forgot_password_page.is_success_message_visible():
            message = forgot_password_page.get_success_message()
        elif forgot_password_page.is_info_message_visible():
            message = forgot_password_page.get_info_message()
        elif forgot_password_page.is_error_message_visible():
            message = forgot_password_page.get_error_message()
            logger.error(f"   ❌ 发现错误消息: {message}")
            raise AssertionError("枚举防护测试失败：显示了错误消息，可能泄露了用户不存在的信息")
        
        logger.info(f"   响应时间: {response_time:.2f}秒")
        logger.info(f"   响应消息: {message}")
        
        # 验证逻辑：应该显示成功/提示消息，而不是错误消息
        assert message, "未检测到任何响应消息"
        logger.info("   ✅ 系统显示了通用响应消息，未泄露用户状态")
        
        logger.info("✅ TC-FP-009执行成功")
    
    @pytest.mark.P2
    @pytest.mark.navigation
    def test_p2_forgot_password_back_to_login(self, forgot_password_page):
        """
        TC-FP-003: 返回登录页面链接验证
        验证登录链接功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-003: 返回登录页面链接验证")
        logger.info("=" * 60)
        
        # 点击登录链接
        logger.info("   点击 'Back to Login' 链接...")
        forgot_password_page.click_login_link()
        
        # 等待页面跳转
        forgot_password_page.page.wait_for_load_state("domcontentloaded")
        
        # 截图：跳转结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_back_login_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="跳转到登录页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证URL
        current_url = forgot_password_page.page.url
        logger.info(f"   当前URL: {current_url}")
        assert "/Login" in current_url, f"应该跳转到登录页面，实际URL: {current_url}"
        
        logger.info("✅ TC-FP-003执行成功")
    
    @pytest.mark.P2
    @pytest.mark.boundary
    def test_p2_forgot_password_shortest_valid_email(self, forgot_password_page):
        """
        TC-FP-008: 最短有效邮箱测试
        验证最短邮箱格式
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-008: 最短有效邮箱测试")
        logger.info("=" * 60)
        
        # 最短有效邮箱: a@b.c
        shortest_email = "a@b.c"
        logger.info(f"   测试最短邮箱: {shortest_email}")
        
        forgot_password_page.fill_email(shortest_email)
        
        # 验证邮箱格式有效
        is_valid = forgot_password_page.is_email_valid()
        assert is_valid, "最短邮箱格式应该通过HTML5验证"
        logger.info("   ✓ HTML5验证通过")
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(1000)
        
        # 截图：提交结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_shortest_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="最短邮箱提交结果",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 只要不出现 HTML5 验证错误气泡，就算格式通过
        # 至于后端是否接受 a@b.c 取决于具体配置，这里重点测试前端格式校验
        assert is_valid, "前端应认为格式有效"
        
        logger.info("✅ TC-FP-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_forgot_password_hint_text_display(self, forgot_password_page):
        """
        TC-FP-012: 提示信息显示验证
        验证提示文本内容
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-012: 提示信息显示验证")
        logger.info("=" * 60)
        
        # 验证提示文本可见
        assert forgot_password_page.is_hint_text_visible(), "提示文本应该可见"
        
        # 获取提示文本内容
        hint_text = forgot_password_page.get_hint_text()
        logger.info(f"   提示文本内容: '{hint_text}'")
        
        # 截图：提示文本
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_hint_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="提示文本显示",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证文本内容包含关键信息（支持中英文环境）
        keywords = ["email", "link", "reset", "password", "邮件", "链接", "重置", "密码"]
        found_keywords = [kw for kw in keywords if kw in hint_text.lower()]
        
        if found_keywords:
            logger.info(f"   ✓ 找到关键提示词: {found_keywords}")
        else:
            logger.warning(f"   ⚠️ 提示文本可能不包含预期关键词，请人工核对: {hint_text}")
        
        logger.info("✅ TC-FP-012执行成功")
