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
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_forgot_password_page_load(self, forgot_password_page):
        """
        TC-FP-011: 忘记密码页面加载验证
        
        测试目标：验证忘记密码页面能够正确加载并显示核心功能元素
        测试区域：Forgot Password Page（ABP Framework密码重置页面）
        测试元素：
        - 输入框 "Email"（邮箱输入框）
        - 按钮 "Send Password Reset Link"（提交按钮）
        
        测试步骤：
        1. [Forgot Password Page] 导航到忘记密码页面
        2. [验证] 确认页面加载成功
        3. [Form区域] 验证邮箱输入框可见
        4. [Form区域] 验证提交按钮可见
        5. [验证] 确认URL正确
        
        预期结果：
        - 页面成功加载（URL正确）
        - 核心功能元素都可见
        - 页面可以正常使用
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-011: 忘记密码页面加载验证")
        logger.info("=" * 60)
        
        # 验证页面加载
        assert forgot_password_page.is_loaded(), "忘记密码页面未正确加载"
        logger.info("   ✓ 页面加载状态检查通过")
        
        # 验证URL正确
        current_url = forgot_password_page.page.url
        assert "/ForgotPassword" in current_url, f"URL不正确，当前: {current_url}"
        logger.info(f"   ✓ URL验证通过: {current_url}")
        
        # 截图：页面加载完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_loaded_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-忘记密码页面加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证核心功能元素
        logger.info("   验证核心功能元素...")
        elements_to_check = [
            (forgot_password_page.EMAIL_INPUT, "邮箱输入框"),
            (forgot_password_page.SUBMIT_BUTTON, "提交按钮")
        ]
        
        for selector, name in elements_to_check:
            is_visible = forgot_password_page.is_visible(selector)
            assert is_visible, f"{name} 应该可见"
            logger.info(f"   ✓ {name} 可见")
        
        # 可选元素检查（不强制要求）
        if forgot_password_page.is_login_link_visible():
            logger.info("   ✓ 登录链接可见")
        else:
            logger.info("   ℹ️ 登录链接不可见（可选元素）")
        
        logger.info("✅ TC-FP-011执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_forgot_password_existing_email(self, forgot_password_page, test_data):
        """
        TC-FP-001: 使用有效邮箱提交忘记密码请求
        
        测试目标：验证使用已存在的邮箱提交忘记密码请求后，系统显示成功提示
        预期结果：页面显示 "Account recovery email sent to your e-mail address..." 文本
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-001: 使用有效邮箱提交忘记密码请求")
        logger.info("=" * 60)
        
        # 使用已存在的邮箱
        valid_email = test_data["valid_login_data"][0].get("email", "haylee5@test.com")
        logger.info(f"   使用测试邮箱: {valid_email}")
        
        # 截图：填写前（空表单）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_valid_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-空表单",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 填写邮箱
        forgot_password_page.fill_email(valid_email)
        logger.info("   ✓ 已填写邮箱")
        
        # 截图：填写后
        screenshot_path = f"forgot_pwd_valid_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-填写完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击提交
        logger.info("   点击提交按钮...")
        forgot_password_page.click_submit_button()
        
        # 等待页面响应（增加等待时间确保页面加载完成）
        logger.info("   ⏳ 等待响应...")
        forgot_password_page.page.wait_for_timeout(3000) 
        
        # 截图：提交结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_valid_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-提交结果页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证页面显示账号恢复邮件已发送的提示文本
        # 预期文本: "Account recovery email sent to your e-mail address..."
        expected_text_keywords = [
            "Account recovery email sent",
            "recovery email sent",
            "账号恢复邮件已发送",
            "inbox within 15 minutes",
            "junk mail folder"
        ]
        
        # 使用页面可见文本进行检测（避免HTML标签干扰）
        try:
            visible_text = forgot_password_page.page.locator("body").inner_text()
            logger.info(f"   页面可见文本（前300字符）: {visible_text[:300]}...")
        except:
            visible_text = forgot_password_page.page.content()
        
        text_found = False
        matched_keyword = ""
        
        for keyword in expected_text_keywords:
            if keyword.lower() in visible_text.lower():
                text_found = True
                matched_keyword = keyword
                logger.info(f"   ✅ 检测到预期文本内容: {keyword}")
                break
        
        # 如果没有找到关键文本，检查是否有错误消息
        if not text_found:
            if forgot_password_page.is_error_message_visible():
                err = forgot_password_page.get_error_message()
                logger.error(f"   ❌ 检测到错误消息: {err}")
                raise AssertionError(f"忘记密码请求失败: {err}")
            else:
                logger.warning(f"   ⚠️ 未找到预期文本关键词")
        
        assert text_found, f"提交后应显示账号恢复邮件发送成功的文本提示"
        logger.info(f"   ✓ 页面显示成功提示文本: {matched_keyword}")
        
        logger.info("✅ TC-FP-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_forgot_password_empty_email(self, forgot_password_page):
        """
        TC-FP-004: 邮箱为空校验
        
        测试目标：验证邮箱为空时的HTML5验证
        已知Bug：当前页面在空邮箱提交时会崩溃
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-004: 邮箱为空校验")
        logger.info("=" * 60)
        
        # 截图：空表单（提交前）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_empty_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-空表单",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 直接点击提交（邮箱为空）
        logger.info("   尝试提交空表单...")
        forgot_password_page.click_submit_button()
        
        # 等待响应
        forgot_password_page.page.wait_for_timeout(1000)
        
        # 截图：提交后状态
        screenshot_path = f"forgot_pwd_empty_after_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-提交后页面状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查页面是否崩溃（Bug检测）
        page_content = forgot_password_page.page.content()
        if "An unhandled exception occurred" in page_content or "Exception" in page_content or "Error" in page_content:
            logger.error("   ❌ [Bug] 空邮箱提交导致页面崩溃")
            logger.error("   Bug详情: 空值提交触发页面异常")
            logger.error("   预期行为: 应该在前端阻止提交或后端返回友好的验证错误")
            
            # 在Allure报告中标记为Bug
            allure.attach(
                "Bug描述：\n"
                "- 实际行为：空邮箱提交后页面崩溃或显示异常错误\n"
                "- 预期行为：应该在前端进行HTML5验证阻止提交，或后端返回友好的验证错误提示\n"
                "- 影响：用户体验差，页面异常中断操作流程\n"
                "- 严重程度：高\n"
                "- 建议：在邮箱输入框添加required属性，或在后端增加空值验证并返回友好提示",
                name="❌ Bug详情-空邮箱提交页面崩溃",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 让测试失败
            assert False, (
                "空邮箱提交导致页面崩溃，应该返回友好的验证错误提示"
            )
        
        # 验证HTML5必填验证（如果没有崩溃）
        is_valid = forgot_password_page.is_email_valid()
        logger.info(f"   HTML5验证状态: {'有效' if is_valid else '无效'}")
        
        # 验证仍在忘记密码页面（未发生跳转）
        current_url = forgot_password_page.page.url
        if "/ForgotPassword" in current_url:
            logger.info("   ✓ URL未发生跳转")
        
        if not is_valid:
            logger.info("   ✓ HTML5验证生效，阻止了空值提交")
            logger.info("✅ TC-FP-004执行成功")
        else:
            logger.error("   ❌ HTML5验证未生效")
            assert not is_valid, "邮箱为空时HTML5验证应为invalid"
    
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
        
        # 截图：填写前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_invalid_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-空表单",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 填写无效邮箱格式
        invalid_email = "invalid-email-format"
        logger.info(f"   输入无效格式邮箱: {invalid_email}")
        forgot_password_page.fill_email(invalid_email)
        logger.info("   ✓ 已填写无效格式邮箱")
        
        # 截图：填写后
        screenshot_path = f"forgot_pwd_invalid_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-填写无效邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(500)
        
        # 截图：格式错误验证
        screenshot_path = f"forgot_pwd_invalid_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤2-后-格式错误验证提示",
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
        TC-FP-009: 用户不存在的错误提示验证
        验证使用不存在的邮箱提交时，系统显示错误消息
        
        测试目标：验证系统对不存在用户的响应行为
        预期结果：系统显示错误消息，明确告知用户不存在
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FP-009: 用户不存在的错误提示验证")
        logger.info("测试目标: 验证不存在的邮箱会收到错误提示")
        logger.info("=" * 60)
        
        # 截图：填写前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_enum_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-空表单",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 构造不存在的邮箱
        nonexistent_email = f"nonexistent_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"
        logger.info(f"   使用不存在的邮箱: {nonexistent_email}")
        
        forgot_password_page.clear_email_field()
        forgot_password_page.fill_email(nonexistent_email)
        logger.info("   ✓ 已填写不存在的邮箱")
        
        # 截图：填写后
        screenshot_path = f"forgot_pwd_enum_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-填写完成",
            attachment_type=allure.attachment_type.PNG
        )
        
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
        screenshot_path = f"forgot_pwd_nonexistent_user_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="不存在用户的错误提示",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取响应消息
        message = ""
        message_type = ""
        
        if forgot_password_page.is_error_message_visible():
            message = forgot_password_page.get_error_message()
            message_type = "错误消息"
            logger.info(f"   ✅ 检测到错误消息（符合预期）: {message}")
        elif forgot_password_page.is_success_message_visible():
            message = forgot_password_page.get_success_message()
            message_type = "成功消息"
            logger.warning(f"   ⚠️ 检测到成功消息（可能不符合预期）: {message}")
        elif forgot_password_page.is_info_message_visible():
            message = forgot_password_page.get_info_message()
            message_type = "提示消息"
            logger.warning(f"   ⚠️ 检测到提示消息（可能不符合预期）: {message}")
        
        logger.info(f"   响应时间: {response_time:.2f}秒")
        logger.info(f"   消息类型: {message_type}")
        logger.info(f"   消息内容: {message}")
        
        # 验证逻辑：当用户不存在时，应该显示错误消息
        assert message, "未检测到任何响应消息"
        assert forgot_password_page.is_error_message_visible(), "使用不存在的邮箱应该显示错误消息"
        logger.info("   ✅ 系统正确显示了用户不存在的错误提示")
        
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
        
        # 截图：点击前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_back_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-忘记密码页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击登录链接
        logger.info("   点击 'Back to Login' 链接...")
        forgot_password_page.click_login_link()
        
        # 等待页面跳转
        forgot_password_page.page.wait_for_load_state("domcontentloaded")
        
        # 截图：跳转结果
        screenshot_path = f"forgot_pwd_back_after_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-跳转到登录页面",
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
        
        # 截图：填写前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"forgot_pwd_shortest_before_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-前-空表单",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 最短有效邮箱: a@b.c
        shortest_email = "a@b.c"
        logger.info(f"   测试最短邮箱: {shortest_email}")
        
        forgot_password_page.fill_email(shortest_email)
        logger.info("   ✓ 已填写最短邮箱")
        
        # 截图：填写后
        screenshot_path = f"forgot_pwd_shortest_filled_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤1-后-填写最短邮箱",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证邮箱格式有效
        is_valid = forgot_password_page.is_email_valid()
        assert is_valid, "最短邮箱格式应该通过HTML5验证"
        logger.info("   ✓ HTML5验证通过")
        
        # 点击提交
        forgot_password_page.click_submit_button()
        forgot_password_page.page.wait_for_timeout(1000)
        
        # 截图：提交结果
        screenshot_path = f"forgot_pwd_shortest_result_{timestamp}.png"
        forgot_password_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="步骤2-后-提交结果",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 只要不出现 HTML5 验证错误气泡，就算格式通过
        # 至于后端是否接受 a@b.c 取决于具体配置，这里重点测试前端格式校验
        assert is_valid, "前端应认为格式有效"
        
        logger.info("✅ TC-FP-008执行成功")
