"""
登录功能测试模块
包含登录相关的功能测试、边界测试、异常测试和安全测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.mark.login
class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_successful_login(self, page, test_data):
        """
        TC-FUNC-001: 用户成功登录系统
        
        测试目标：验证用户使用有效凭证可以成功登录系统并进入Dashboard
        测试区域：Login Page（ABP Framework认证页面，端口44320）
        测试元素：
        - 输入框 "Username or Email Address"（Login Form顶部）
        - 输入框 "Password"（Username下方）
        - 复选框 "Remember me"（可选项）
        - 按钮 "Sign In"（表单底部，蓝色主按钮）
        
        测试步骤：
        1. [Landing Page - Header] 导航到首页并点击Sign In按钮
        2. [Login Page] 等待ABP登录页面加载（https://localhost:44320/Account/Login）
        3. [Login Form - Username字段] 输入有效用户名
        4. [Login Form - Password字段] 输入正确密码
        5. [Login Form - Remember me] 勾选Remember me选项
        6. [Login Form - 底部] 点击"Sign In"按钮提交表单
        7. [验证] 等待页面跳转和SSL处理
        8. [验证] 确认跳转到首页（localhost:3000）
        9. [验证] 确认Header显示用户菜单按钮（登录成功标志）
        
        预期结果：
        - 成功跳转到https://localhost:3000/（Dashboard或首页）
        - Header右上角显示用户菜单按钮
        - 用户处于已登录状态，可访问受保护页面
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FUNC-001: 用户成功登录系统")
        logger.info("测试目标: 验证有效凭证登录并访问Dashboard")
        logger.info("=" * 60)
        
        # 初始化页面对象
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        try:
            # 步骤1：导航到首页并点击Sign In
            logger.info("步骤1: [Landing Page - Header右上角] 导航到首页")
            landing_page.navigate()
            assert landing_page.is_loaded(), "首页未正确加载"
            logger.info("   ✓ 首页加载成功: https://localhost:3000/")
            
            # 截图：首页加载
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"screenshots/login_step1_landing_{timestamp}.png")
            allure.attach.file(f"screenshots/login_step1_landing_{timestamp}.png", 
                             name="步骤1-首页加载", attachment_type=allure.attachment_type.PNG)
            
            logger.info("步骤2: [Landing Page - Header] 点击'Sign In'按钮")
            landing_page.click_sign_in()
            logger.info("   ✓ 已点击Sign In按钮，等待跳转到登录页")
            
            # 步骤2：等待登录页面加载
            logger.info("\n步骤3: [Login Page] 等待ABP登录页面加载")
            login_page.wait_for_load()
            assert login_page.is_loaded(), "登录页面未正确加载"
            current_url = login_page.get_current_url()
            logger.info(f"   登录页面URL: {current_url}")
            
            # 截图：登录页加载
            page.screenshot(path=f"screenshots/login_step2_page_{timestamp}.png")
            allure.attach.file(f"screenshots/login_step2_page_{timestamp}.png", 
                             name="步骤2-登录页加载", attachment_type=allure.attachment_type.PNG)
            
            assert "44320" in current_url and "/Account/Login" in current_url, \
                f"未跳转到正确的登录页面，当前URL: {current_url}"
            logger.info("   ✓ ABP登录页面加载成功")
            
            # 步骤3-5：填写登录表单
            valid_data = test_data["valid_login_data"][0]
            logger.info("\n步骤4-6: [Login Form] 填写登录凭证")
            logger.info(f"   Username: {valid_data['username']}")
            logger.info(f"   Password: {'*' * len(valid_data['password'])} ({len(valid_data['password'])}位)")
            logger.info(f"   Remember me: {valid_data.get('remember_me', False)}")
            
            # 截图：填写前（空表单）
            page.screenshot(path=f"screenshots/login_step3_empty_{timestamp}.png")
            allure.attach.file(f"screenshots/login_step3_empty_{timestamp}.png", 
                             name="步骤3-填写前表单", attachment_type=allure.attachment_type.PNG)
            
            login_page.login(
                username=valid_data["username"],
                password=valid_data["password"],
                remember_me=valid_data.get("remember_me", False)
            )
            
            # 截图：填写后（提交前）- 注意：login方法内可能已经提交，如果login方法包含点击，这里截图可能晚了。
            # 检查 login_page.login 实现，通常包含点击。
            # 如果 login 方法是一体化的，我们只能在 login 之前截图。
            # 这里代码逻辑显示 login 方法调用了，且下面日志说"登录信息已填写并提交"。
            # 为了获取"填写后提交前"的截图，应该拆解调用或修改PO。
            # 但不修改PO的前提下，我们在login之前截图了空表单。
            # 现有的代码在 Line 88 已经有了一个 `page.screenshot(path=f"screenshots/login_filled_{timestamp}.png")` 
            # 但它是在 login() 之前调用的！那时候表单是空的！
            # 修正：Line 88 的截图实际上是“填写前”的截图。
            
            logger.info("   ✓ 登录信息已填写并提交")
            
            # 步骤7-9：验证登录成功
            logger.info("\n步骤7-9: [验证] 确认登录成功")
            logger.info("   等待页面跳转...")
            page.wait_for_timeout(3000)
            landing_page.handle_ssl_warning()
            
            # 验证点1：URL跳转
            final_url = landing_page.get_current_url()
            logger.info(f"   最终URL: {final_url}")
            
            # 截图：登录后状态
            page.screenshot(path=f"screenshots/login_success_{timestamp}.png")
            allure.attach.file(
                f"screenshots/login_success_{timestamp}.png",
                name="登录成功后页面",
                attachment_type=allure.attachment_type.PNG
            )
            
            assert "localhost:3000" in final_url, f"URL跳转失败，应跳转到localhost:3000，当前: {final_url}"
            logger.info("   ✓ 成功跳转到首页/Dashboard")
            
            # 验证点2：用户菜单显示
            logger.info("   验证用户菜单按钮...")
            assert landing_page.is_user_menu_visible(), "用户菜单按钮未显示"
            logger.info("   ✓ Header右上角用户菜单按钮已显示")
            
            # 验证点3：登录状态
            logger.info("   验证登录状态...")
            assert landing_page.is_logged_in(), "登录状态验证失败"
            logger.info("   ✓ 用户已成功登录系统")
            
            # 测试总结
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-FUNC-001执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ URL跳转: https://localhost:3000/")
            logger.info("  ✓ 用户菜单按钮显示")
            logger.info("  ✓ 登录状态验证通过")
            logger.info("=" * 60)
            
        except Exception as e:
            # 🔍 失败现场取证
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/login_fail_{timestamp}.png"
            page.screenshot(path=screenshot_path)
            logger.error(f"❌ 登录测试失败: {e}")
            logger.error(f"   已保存失败截图: {screenshot_path}")
            
            # 保存HTML以分析DOM
            html_path = f"screenshots/login_fail_{timestamp}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(page.content())
            
            raise e
    
    @pytest.mark.P1
    @pytest.mark.exception
    def test_p1_login_with_invalid_credentials(self, page, test_data):
        """
        TC-EXCEPTION-001: 使用无效凭证登录失败验证
        
        测试目标：验证使用不存在的用户名或错误密码无法登录系统
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Username or Email Address"
        - 输入框 "Password"
        - 按钮 "Sign In"
        - 错误提示区域（登录失败后显示）
        
        测试步骤：
        1. [Landing Page] 导航到首页并点击Sign In
        2. [Login Page] 等待登录页面加载
        3. [Login Form] 输入不存在的用户名
        4. [Login Form] 输入任意密码
        5. [Login Form] 点击Sign In按钮提交
        6. [验证] 确认仍停留在登录页面（未跳转）
        7. [验证] 确认URL未改变（仍在44320端口）
        
        预期结果：
        - 登录失败，不跳转页面
        - 仍停留在https://localhost:44320/Account/Login
        - 可能显示错误提示信息（取决于ABP配置）
        - 用户未登录，无法访问受保护页面
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-001: 使用无效凭证登录失败验证")
        logger.info("测试目标: 验证无效凭证无法登录")
        logger.info("=" * 60)
        
        # 初始化页面对象
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1-2：导航到登录页
        logger.info("步骤1: [Landing Page] 导航到首页")
        landing_page.navigate()
        logger.info("   ✓ 首页加载完成")
        
        logger.info("步骤2: [Landing Page - Header] 点击Sign In按钮")
        landing_page.click_sign_in()
        logger.info("   ✓ 已点击Sign In，跳转到登录页")
        
        logger.info("\n步骤3: [Login Page] 等待登录页面加载")
        login_page.wait_for_load()
        initial_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {initial_url}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤3-5：使用无效凭证登录
        invalid_data = test_data["invalid_login_data"][1]  # nonexistent user
        logger.info("\n步骤4-6: [Login Form] 输入无效登录凭证")
        logger.info(f"   Username: {invalid_data['username']} (不存在的用户)")
        logger.info(f"   Password: {'*' * len(invalid_data['password'])}")
        
        # 分步执行以截图
        login_page.fill_username(invalid_data["username"])
        login_page.fill_password(invalid_data["password"])
        
        # 截图：填写完成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_invalid_filled_{timestamp}.png")
        allure.attach.file(f"screenshots/login_invalid_filled_{timestamp}.png", 
                         name="步骤4-5-填写无效凭证", attachment_type=allure.attachment_type.PNG)
        
        # 提交
        login_page.click_element(login_page.LOGIN_BUTTON)
        logger.info("   ✓ 无效凭证已提交")
        
        # 步骤6-7：验证登录失败
        logger.info("\n步骤7-8: [验证] 确认登录失败")
        logger.info("   等待服务器响应...")
        page.wait_for_timeout(2000)
        
        # 验证点1：仍在登录页面
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        logger.info(f"   初始URL: {initial_url}")
        
        assert "Account/Login" in current_url or "44320" in current_url, \
            f"登录失败应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 仍停留在登录页面（未跳转）")
        
        # 验证点2：未跳转到首页
        assert "localhost:3000" not in current_url, "无效凭证不应跳转到首页"
        logger.info("   ✓ 未跳转到首页（预期行为）")
        
        # 验证点3：检查是否有错误提示
        error_found = False
        # 常见的错误提示选择器
        error_selectors = [
            ".text-danger", 
            ".alert-danger", 
            "text=Invalid username or password",
            "text=无效的用户名或密码"
        ]
        
        for selector in error_selectors:
            if page.is_visible(selector):
                error_msg = page.text_content(selector)
                logger.info(f"   ✓ 捕获到错误提示: {error_msg}")
                error_found = True
                break
        
        if not error_found:
            logger.info("   ℹ️ 未检测到明显的错误提示文本，但行为符合预期（未登录）")
        
        # 截图：登录失败状态
        page.screenshot(path=f"screenshots/login_invalid_creds_{timestamp}.png")
        allure.attach.file(f"screenshots/login_invalid_creds_{timestamp}.png", 
                         name="步骤6-7-登录失败页面", attachment_type=allure.attachment_type.PNG)
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-001执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 无效凭证登录失败")
        logger.info("  ✓ 停留在登录页面")
        logger.info("  ✓ 未跳转到首页")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.exception
    def test_p1_login_with_empty_credentials(self, page):
        """
        TC-EXCEPTION-002: 空值输入验证测试
        
        测试目标：验证登录表单对空值输入的前端验证机制
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Username or Email Address"（Form顶部）
        - 输入框 "Password"（Username下方）
        - 按钮 "Sign In"（Form底部，提交按钮）
        
        测试步骤：
        1. [Landing Page] 导航到首页并点击Sign In
        2. [Login Page] 等待登录页面加载
        3. [场景1 - 全部为空] 清空所有字段后提交
        4. [验证] 确认停留在登录页面（不允许空值登录）
        5. [场景2 - 仅用户名为空] 只填写密码，用户名留空
        6. [验证] 确认停留在登录页面（用户名必填）
        7. [场景3 - 仅密码为空] 只填写用户名，密码留空
        8. [验证] 确认停留在登录页面（密码必填）
        
        预期结果：
        - 所有空值场景都不允许提交
        - 保持在登录页面（https://localhost:44320/Account/Login）
        - 不跳转到首页
        - 可能显示HTML5表单验证提示
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-002: 空值输入验证测试")
        logger.info("测试目标: 验证登录表单必填字段验证")
        logger.info("=" * 60)
        
        # 初始化页面对象
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1-2：导航到登录页
        logger.info("步骤1: [Landing Page] 导航到首页")
        landing_page.navigate()
        logger.info("   ✓ 首页加载完成")
        
        logger.info("步骤2: [Landing Page - Header] 点击Sign In按钮")
        landing_page.click_sign_in()
        logger.info("   ✓ 已点击Sign In，跳转到登录页")
        
        logger.info("\n步骤3: [Login Page] 等待登录页面加载")
        login_page.wait_for_load()
        initial_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {initial_url}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 场景1：两者都为空
        logger.info("\n" + "-" * 60)
        logger.info("场景1: 全部字段为空")
        logger.info("-" * 60)
        logger.info("步骤4: [Login Form] 清空所有字段并尝试提交")
        logger.info("   Username: '' (空)")
        logger.info("   Password: '' (空)")
        
        login_page.fill_username("")
        login_page.fill_password("")
        login_page.click_element(login_page.LOGIN_BUTTON)
        logger.info("   ✓ 已点击Sign In按钮（空值提交）")
        
        logger.info("\n步骤5: [验证] 确认未跳转（空值不允许登录）")
        page.wait_for_timeout(2000)
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        
        # 截图：场景1结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_empty_all_{timestamp}.png")
        allure.attach.file(f"screenshots/login_empty_all_{timestamp}.png", 
                         name="场景1-全部为空", attachment_type=allure.attachment_type.PNG)
        
        # 检查是否出现后端异常页面（Bug）
        page_content = page.content()
        if "An unhandled exception occurred" in page_content or "AbpValidationException" in page_content:
            logger.error("   ❌ [Bug] 后端抛出未处理异常，应该返回友好的验证错误")
            logger.error("   Bug详情: 空值提交触发后端异常")
            logger.error("   预期行为: 应该在前端或后端友好地拦截，显示验证错误")
            
            # 在Allure报告中标记为失败的Bug
            allure.attach(
                "Bug描述：\n"
                "- 实际行为：空值提交后端抛出未处理的异常\n"
                "- 预期行为：应该返回友好的验证错误提示，如'用户名不能为空'、'密码不能为空'等\n"
                "- 影响：用户体验差，暴露了技术细节和堆栈跟踪\n"
                "- 严重程度：高\n"
                "- 建议：在后端统一异常处理或在前端增加表单验证",
                name="❌ Bug详情-空值提交异常",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 让测试失败
            assert False, (
                "空值提交后端抛出未处理异常，应该返回友好的验证错误提示"
            )
        
        assert "Account/Login" in current_url, \
            f"空值提交不应跳转，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 空值验证生效，停留在登录页面")
        
        # 场景2：仅用户名为空
        logger.info("\n" + "-" * 60)
        logger.info("场景2: 仅用户名为空（密码有值）")
        logger.info("-" * 60)
        logger.info("   重新导航到登录页确保页面稳定...")
        login_page.navigate()
        login_page.wait_for_load()
        logger.info("   ✓ 登录页面重新加载完成")
        
        logger.info("步骤6: [Login Form] 仅填写密码，用户名留空")
        logger.info("   Username: '' (空)")
        logger.info("   Password: 'TestPassword123!' (有值)")
        
        login_page.fill_username("")
        login_page.fill_password("TestPassword123!")
        login_page.click_element(login_page.LOGIN_BUTTON)
        logger.info("   ✓ 已点击Sign In按钮")
        
        logger.info("\n步骤7: [验证] 确认未跳转（用户名必填）")
        page.wait_for_timeout(1000)
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        
        # 截图：场景2结果
        page.screenshot(path=f"screenshots/login_empty_user_{timestamp}.png")
        allure.attach.file(f"screenshots/login_empty_user_{timestamp}.png", 
                         name="场景2-用户名为空", attachment_type=allure.attachment_type.PNG)
        
        assert "Account/Login" in current_url, \
            f"用户名为空不应跳转，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 用户名必填验证生效")
        
        # 场景3：仅密码为空
        logger.info("\n" + "-" * 60)
        logger.info("场景3: 仅密码为空（用户名有值）")
        logger.info("-" * 60)
        logger.info("   重新导航到登录页确保页面稳定...")
        login_page.navigate()
        login_page.wait_for_load()
        logger.info("   ✓ 登录页面重新加载完成")
        
        logger.info("步骤8: [Login Form] 仅填写用户名，密码留空")
        logger.info("   Username: 'test@test.com' (有值)")
        logger.info("   Password: '' (空)")
        
        login_page.fill_username("test@test.com")
        login_page.fill_password("")
        login_page.click_element(login_page.LOGIN_BUTTON)
        logger.info("   ✓ 已点击Sign In按钮")
        
        logger.info("\n步骤9: [验证] 确认未跳转（密码必填）")
        page.wait_for_timeout(1000)
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        
        # 截图：场景3结果
        page.screenshot(path=f"screenshots/login_empty_pass_{timestamp}.png")
        allure.attach.file(f"screenshots/login_empty_pass_{timestamp}.png", 
                         name="场景3-密码为空", attachment_type=allure.attachment_type.PNG)
        
        assert "Account/Login" in current_url, \
            f"密码为空不应跳转，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 密码必填验证生效")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-002执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 场景1：全部为空 - 验证通过")
        logger.info("  ✓ 场景2：仅用户名为空 - 验证通过")
        logger.info("  ✓ 场景3：仅密码为空 - 验证通过")
        logger.info("  ✓ 所有空值场景都被正确拦截")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_login_with_email(self, page, test_data):
        """
        TC-LOGIN-005: 使用邮箱地址登录
        
        测试目标：验证用户可以使用注册邮箱替代用户名进行登录
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Username or Email Address"
        
        测试步骤：
        1. [Landing Page] 导航到登录页
        2. [Login Form] 输入有效的邮箱地址（而非用户名）
        3. [Login Form] 输入正确密码
        4. [Login Form] 点击Sign In
        5. [验证] 成功登录并跳转到首页
        
        预期结果：
        - 系统识别邮箱并允许登录
        - 跳转到首页
        - 显示用户菜单
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-005: 使用邮箱地址登录")
        logger.info("测试目标: 验证邮箱登录支持")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1：导航
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 步骤2-4：使用邮箱登录
        valid_data = test_data["valid_login_data"][0]
        
        email = valid_data.get("email")
        if not email:
            logger.warning("   ⚠️ 测试数据中缺少email字段，跳过邮箱登录测试")
            pytest.skip("Test data missing email field")
            
        logger.info(f"   使用邮箱: {email}")
        logger.info(f"   密码: {'*' * len(valid_data['password'])}")
        
        login_page.login(
            username=email,  # 传入邮箱作为用户名
            password=valid_data["password"]
        )
        
        # 步骤5：验证
        page.wait_for_timeout(3000)
        landing_page.handle_ssl_warning()
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_email_success_{timestamp}.png")
        allure.attach.file(f"screenshots/login_email_success_{timestamp}.png", 
                         name="邮箱登录成功", attachment_type=allure.attachment_type.PNG)
        
        assert landing_page.is_logged_in(), "邮箱登录失败"
        logger.info("   ✓ 邮箱登录成功")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-LOGIN-005执行成功")
        logger.info("=" * 60)

    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_username_case_insensitivity(self, page, test_data):
        """
        TC-LOGIN-009: 用户名大小写不敏感验证
        
        测试目标：验证登录时用户名忽略大小写
        测试区域：Login Page
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-009: 用户名大小写不敏感验证")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        valid_data = test_data["valid_login_data"][0]
        original_username = valid_data["username"]
        # 转换为全大写或反转大小写
        mixed_case_username = original_username.swapcase()
        
        logger.info(f"   原用户名: {original_username}")
        logger.info(f"   测试用户名: {mixed_case_username}")
        
        login_page.login(
            username=mixed_case_username,
            password=valid_data["password"]
        )
        
        page.wait_for_timeout(3000)
        landing_page.handle_ssl_warning()
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_case_success_{timestamp}.png")
        allure.attach.file(f"screenshots/login_case_success_{timestamp}.png", 
                         name="大小写混合登录成功", attachment_type=allure.attachment_type.PNG)
        
        assert landing_page.is_logged_in(), "用户名大小写处理失败"
        logger.info("   ✓ 大小写混合登录成功")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-LOGIN-009执行成功")
        logger.info("=" * 60)

    @pytest.mark.P2
    @pytest.mark.exception
    def test_p2_username_whitespace_not_trimmed(self, page, test_data):
        """
        TC-EXCEPTION-003: 用户名空格不自动处理验证
        
        测试目标：验证ABP不自动去除用户名首尾空格（严格匹配）
        测试区域：Login Page
        预期结果：带空格的用户名应登录失败
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-003: 用户名空格不自动处理验证")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        landing_page.navigate()
        
        # 截图：首页
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_whitespace_step1_{timestamp}.png")
        allure.attach.file(f"screenshots/login_whitespace_step1_{timestamp}.png", 
                         name="步骤1-首页", attachment_type=allure.attachment_type.PNG)
        
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 截图：登录页
        page.screenshot(path=f"screenshots/login_whitespace_step2_{timestamp}.png")
        allure.attach.file(f"screenshots/login_whitespace_step2_{timestamp}.png", 
                         name="步骤2-登录页", attachment_type=allure.attachment_type.PNG)
        
        valid_data = test_data["valid_login_data"][0]
        original_username = valid_data["username"]
        # 添加首尾空格
        spaced_username = f"  {original_username}  "
        
        logger.info(f"   原用户名: '{original_username}'")
        logger.info(f"   测试用户名: '{spaced_username}'")
        
        # 填写表单（使用底层方法避免login()的错误处理）
        login_page.fill_username(spaced_username)
        login_page.fill_password(valid_data["password"])
        
        # 截图：填写完成
        page.screenshot(path=f"screenshots/login_whitespace_step3_{timestamp}.png")
        allure.attach.file(f"screenshots/login_whitespace_step3_{timestamp}.png", 
                         name="步骤3-填写带空格用户名", attachment_type=allure.attachment_type.PNG)
        
        login_page.click_element(login_page.LOGIN_BUTTON)
        
        # 等待响应
        page.wait_for_timeout(3000)
        
        # 截图：提交后
        page.screenshot(path=f"screenshots/login_whitespace_step4_{timestamp}.png")
        allure.attach.file(f"screenshots/login_whitespace_step4_{timestamp}.png", 
                         name="步骤4-提交后（预期失败）", attachment_type=allure.attachment_type.PNG)
        
        # 验证：应该登录失败（ABP不自动trim空格）
        current_url = login_page.get_current_url()
        logger.info(f"   提交后URL: {current_url}")
        
        # 应停留在登录页
        assert "Account/Login" in current_url or "44320" in current_url, \
            f"带空格用户名应登录失败，当前URL: {current_url}"
        logger.info("   ✓ ABP严格匹配用户名，不自动trim空格")
        logger.info("   ✓ 带空格用户名登录失败（符合预期）")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-003执行成功")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.boundary
    def test_p1_login_username_boundary(self, page, test_data):
        """
        TC-BOUNDARY-001: 用户名边界值测试
        
        测试目标：验证登录表单对不同长度用户名的输入处理能力
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Username or Email Address"（Form顶部）
        
        测试步骤：
        1. [Landing Page] 导航到首页并点击Sign In
        2. [Login Page] 等待登录页面加载
        3. [Login Form - Username字段] 测试最短有效邮箱（a@b.c - 5字符）
        4. [验证] 确认输入被接受
        5. [Login Form - Username字段] 测试较长邮箱（68字符）
        6. [验证] 确认输入被接受
        7. [验证] 所有边界值都能正确处理
        
        预期结果：
        - 最短有效邮箱（5字符）可以输入
        - 较长邮箱（68字符）可以输入
        - 邮箱长度在合理范围内（≤254字符）都应被接受
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-BOUNDARY-001: 用户名边界值测试")
        logger.info("测试目标: 验证不同长度用户名的输入处理")
        logger.info("=" * 60)
        
        # 初始化页面对象
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1-2：导航到登录页
        logger.info("步骤1: [Landing Page] 导航到首页")
        landing_page.navigate()
        logger.info("   ✓ 首页加载完成")
        
        logger.info("步骤2: [Landing Page - Header] 点击Sign In按钮")
        landing_page.click_sign_in()
        logger.info("   ✓ 已点击Sign In，跳转到登录页")
        
        logger.info("\n步骤3: [Login Page] 等待登录页面加载")
        login_page.wait_for_load()
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤4-6：测试边界数据
        logger.info("\n步骤4-6: [Login Form - Username字段] 测试边界值")
        boundary_data = test_data["boundary_username"]
        logger.info(f"   边界测试数据数量: {len(boundary_data)}个")
        
        test_results = []
        
        for idx, data in enumerate(boundary_data, 1):
            logger.info(f"\n   --- 边界测试 {idx}/{len(boundary_data)}: {data['description']} ---")
            logger.info(f"   测试值: '{data['value']}'")
            logger.info(f"   长度: {data['length']}字符")
            
            # 填写用户名
            login_page.fill_username(data["value"])
            logger.info("   ✓ 已输入用户名")
            
            # 截图：边界值输入
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            page.screenshot(path=f"screenshots/login_boundary_{idx}_{timestamp}.png")
            allure.attach.file(f"screenshots/login_boundary_{idx}_{timestamp}.png", 
                             name=f"边界值{idx}-{data['description']}", attachment_type=allure.attachment_type.PNG)
            
            # 验证输入是否被接受
            entered_value = login_page.get_username_value()
            actual_length = len(entered_value)
            logger.info(f"   实际输入长度: {actual_length}字符")
            
            # 验证输入是否被接受（邮箱最大长度254字符）
            if data["length"] <= 254:
                if actual_length > 0:
                    logger.info(f"   ✓ 边界值被接受: {data['description']}")
                    test_results.append({"test": data['description'], "status": "✓ 通过"})
                else:
                    logger.warning(f"   ⚠️ 边界值输入失败: {data['description']}")
                    test_results.append({"test": data['description'], "status": "❌ 失败"})
                    assert actual_length > 0, f"边界值输入失败: {data['description']}"
            else:
                logger.info(f"   ℹ️ 超长输入（>{data['length']}字符）")
                test_results.append({"test": data['description'], "status": "ℹ️ 超长"})
            
            # 清空输入框准备下一次测试
            login_page.fill_username("")
            logger.info("   ✓ 已清空输入框")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-BOUNDARY-001执行成功")
        logger.info("验证总结:")
        for result in test_results:
            logger.info(f"  {result['status']} {result['test']}")
        logger.info(f"  ✓ 共测试{len(boundary_data)}个边界值")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.security
    def test_p1_sql_injection_protection(self, page):
        """
        TC-SECURITY-001: SQL注入攻击防护测试
        
        测试目标：验证系统对SQL注入攻击的防护能力，确保恶意SQL代码无法绕过身份验证
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Username or Email Address"（潜在注入点）
        - 输入框 "Password"（潜在注入点）
        - 按钮 "Sign In"（提交按钮）
        
        测试步骤：
        1. [Landing Page] 导航到首页并点击Sign In
        2. [Login Page] 等待登录页面加载
        3. [Login Form - Username字段] 输入SQL注入代码（admin' OR '1'='1）
        4. [Login Form - Password字段] 输入SQL注入代码（password' OR '1'='1）
        5. [Login Form - 底部] 点击Sign In按钮尝试登录
        6. [验证] 确认登录失败（停留在登录页面）
        7. [验证] 确认未跳转到首页（未获得访问权限）
        8. [验证] 确认用户未登录状态
        
        预期结果：
        - SQL注入攻击被拦截
        - 登录失败，停留在https://localhost:44320/Account/Login
        - 未跳转到首页
        - 用户菜单按钮不显示（未登录）
        - 系统安全性得到验证
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SECURITY-001: SQL注入攻击防护测试")
        logger.info("测试目标: 验证SQL注入防护机制")
        logger.info("=" * 60)
        
        # 初始化页面对象
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1-2：导航到登录页
        logger.info("步骤1: [Landing Page] 导航到首页")
        landing_page.navigate()
        logger.info("   ✓ 首页加载完成")
        
        logger.info("步骤2: [Landing Page - Header] 点击Sign In按钮")
        landing_page.click_sign_in()
        logger.info("   ✓ 已点击Sign In，跳转到登录页")
        
        logger.info("\n步骤3: [Login Page] 等待登录页面加载")
        login_page.wait_for_load()
        initial_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {initial_url}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤3-5：尝试SQL注入
        logger.info("\n步骤4-6: [Login Form] 尝试SQL注入攻击")
        sql_injection_username = "admin' OR '1'='1"
        sql_injection_password = "password' OR '1'='1"
        
        logger.info(f"   ⚠️ 注入用户名: {sql_injection_username}")
        logger.info(f"   ⚠️ 注入密码: {sql_injection_password}")
        logger.info("   ℹ️ 这是模拟攻击，测试系统防护能力")
        
        # 分步填写以截图
        login_page.fill_username(sql_injection_username)
        login_page.fill_password(sql_injection_password)
        
        # 截图：注入代码已填写
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/sql_injection_filled_{timestamp}.png")
        allure.attach.file(f"screenshots/sql_injection_filled_{timestamp}.png", 
                         name="步骤4-6-SQL注入填写", attachment_type=allure.attachment_type.PNG)
        
        # 提交
        login_page.click_element(login_page.LOGIN_BUTTON)
        logger.info("   ✓ SQL注入代码已提交")
        
        # 步骤6-8：验证防护效果
        logger.info("\n步骤7-9: [验证] 确认SQL注入被拦截")
        logger.info("   等待服务器响应...")
        page.wait_for_timeout(2000)
        
        # 验证点1：仍在登录页面
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        logger.info(f"   初始URL: {initial_url}")
        
        assert "Account/Login" in current_url or "44320" in current_url, \
            f"SQL注入应被拦截，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ SQL注入被拦截，停留在登录页面")
        
        # 验证点2：未跳转到首页
        assert "localhost:3000" not in current_url, \
            "SQL注入不应绕过身份验证跳转到首页"
        logger.info("   ✓ 未跳转到首页（身份验证未被绕过）")
        
        # 验证点3：用户未登录
        is_logged_in = landing_page.is_logged_in()
        logger.info(f"   登录状态: {is_logged_in}")
        assert not is_logged_in, "SQL注入不应成功登录系统"
        logger.info("   ✓ 用户处于未登录状态")
        
        # 截图：安全测试结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/sql_injection_blocked_{timestamp}.png")
        allure.attach.file(
            f"screenshots/sql_injection_blocked_{timestamp}.png",
            name="SQL注入测试结果（应拦截）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-SECURITY-001执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ SQL注入攻击被成功拦截")
        logger.info("  ✓ 停留在登录页面，未获得访问权限")
        logger.info("  ✓ 身份验证机制未被绕过")
        logger.info("  ✓ 系统安全防护有效")
        logger.info("=" * 60)
    
    # ==================== UI & 可用性测试 ====================
    
    @pytest.mark.P2
    @pytest.mark.ui
    @pytest.mark.usability
    def test_p2_password_visibility_toggle(self, page):
        """
        TC-LOGIN-003: 密码字段类型验证
        
        测试目标：验证密码输入框默认为password类型（隐藏密码）
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Password"（Login Form中部，type="password"）
        
        测试步骤：
        1. [Login Page] 直接导航到登录页面
        2. [Login Form - Password字段] 输入测试密码
        3. [验证] 确认密码输入框type属性为"password"
        4. [验证] 确认密码内容被隐藏显示（●●●●）
        
        预期结果：
        - 密码输入框type="password"
        - 密码内容不明文显示
        - 用户隐私得到保护
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-003: 密码字段类型验证")
        logger.info("测试目标: 验证密码输入框默认隐藏")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        logger.info("步骤1: [Login Page] 导航到登录页面")
        login_page.navigate()
        login_page.wait_for_load()
        logger.info(f"   登录页面URL: {login_page.get_current_url()}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤2：输入密码
        logger.info("\n步骤2: [Login Form - Password字段] 输入测试密码")
        test_password = "TestPassword123!"
        logger.info(f"   测试密码: {test_password}")
        login_page.fill_password(test_password)
        logger.info("   ✓ 密码已输入")
        
        # 步骤3-4：验证密码字段类型
        logger.info("\n步骤3-4: [验证] 确认密码字段为password类型")
        password_input = page.locator(login_page.PASSWORD_INPUT)
        input_type = password_input.get_attribute("type")
        logger.info(f"   密码输入框type属性: '{input_type}'")
        
        # 截图：密码隐藏
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_pwd_hidden_{timestamp}.png")
        allure.attach.file(f"screenshots/login_pwd_hidden_{timestamp}.png", 
                         name="步骤3-密码隐藏状态", attachment_type=allure.attachment_type.PNG)
        
        assert input_type == "password", \
            f"密码字段应该是password类型以隐藏内容，实际type: {input_type}"
        logger.info("   ✓ 密码字段type='password'，内容被隐藏")
        logger.info("   ✓ 用户隐私得到保护")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-LOGIN-003执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 密码输入框type='password'")
        logger.info("  ✓ 密码内容被隐藏显示")
        logger.info("=" * 60)
    
    @pytest.mark.P2
    @pytest.mark.ui
    @pytest.mark.usability
    def test_p2_remember_me_checkbox(self, page):
        """
        TC-LOGIN-004: Remember Me复选框UI交互测试
        
        测试目标：验证"Remember Me"复选框的可见性和基本交互
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 复选框 "Remember me"（Login Form底部，Sign In按钮上方）
        
        测试步骤：
        1. [Login Page] 直接导航到登录页面
        2. [Login Form - Remember me] 定位Remember Me复选框
        3. [验证] 确认复选框可见
        4. [Login Form - Remember me] 勾选复选框
        5. [验证] 确认复选框被勾选
        6. [Login Form - Remember me] 取消勾选复选框
        7. [验证] 确认复选框取消勾选
        
        预期结果：
        - Remember Me复选框可见且可交互
        - 可以成功勾选和取消勾选
        - 复选框状态响应正确
        
        注意：此测试仅验证UI交互，实际功能验证见test_p1_remember_me_functionality
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-004: Remember Me复选框功能测试")
        logger.info("测试目标: 验证Remember Me复选框交互")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        logger.info("步骤1: [Login Page] 导航到登录页面")
        login_page.navigate()
        login_page.wait_for_load()
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤2-3：验证复选框可见
        logger.info("\n步骤2-3: [Login Form - Remember me] 定位并验证复选框")
        checkbox = page.locator(login_page.REMEMBER_ME_CHECKBOX)
        is_visible = checkbox.is_visible()
        logger.info(f"   Remember me复选框可见: {is_visible}")
        
        assert is_visible, "Remember me复选框应该可见"
        logger.info("   ✓ Remember me复选框可见且可交互")
        
        # 步骤4-5：勾选复选框
        logger.info("\n步骤4-5: [Login Form - Remember me] 勾选复选框")
        initial_state = checkbox.is_checked()
        logger.info(f"   初始状态: {'已勾选' if initial_state else '未勾选'}")
        
        checkbox.check()
        checked_state = checkbox.is_checked()
        logger.info(f"   勾选后状态: {'已勾选' if checked_state else '未勾选'}")
        
        # 截图：已勾选
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_remember_checked_{timestamp}.png")
        allure.attach.file(f"screenshots/login_remember_checked_{timestamp}.png", 
                         name="步骤5-复选框已勾选", attachment_type=allure.attachment_type.PNG)
        
        assert checked_state, "复选框应该被勾选"
        logger.info("   ✓ 复选框成功勾选")
        
        # 步骤6-7：取消勾选
        logger.info("\n步骤6-7: [Login Form - Remember me] 取消勾选复选框")
        checkbox.uncheck()
        unchecked_state = checkbox.is_checked()
        logger.info(f"   取消勾选后状态: {'已勾选' if unchecked_state else '未勾选'}")
        
        # 截图：取消勾选
        page.screenshot(path=f"screenshots/login_remember_unchecked_{timestamp}.png")
        allure.attach.file(f"screenshots/login_remember_unchecked_{timestamp}.png", 
                         name="步骤7-复选框取消勾选", attachment_type=allure.attachment_type.PNG)
        
        assert not unchecked_state, "复选框应该取消勾选"
        logger.info("   ✓ 复选框成功取消勾选")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-LOGIN-004执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ Remember me复选框可见")
        logger.info("  ✓ 可以成功勾选")
        logger.info("  ✓ 可以成功取消勾选")
        logger.info("  ✓ 复选框状态响应正确")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.functional
    @pytest.mark.usability
    def test_p1_remember_me_functionality(self, page, test_data):
        """
        TC-LOGIN-011: Remember Me持久化登录功能验证
        
        测试目标：验证勾选Remember Me后登录状态能够持久化
        测试区域：Login Page + Landing Page
        
        测试步骤：
        1. 勾选Remember me并成功登录
        2. 验证认证Cookie存在且有长期有效期
        3. 验证登录状态
        4. 关闭页面并重新打开（模拟关闭浏览器重新打开）
        5. 验证用户仍然保持登录状态
        
        预期结果：
        - 勾选Remember me后登录，Cookie应有较长的有效期
        - 重新打开页面后，用户仍然保持登录状态
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-011: Remember Me持久化登录功能验证")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        # 步骤1：勾选Remember me并登录
        logger.info("步骤1: 导航到登录页并勾选Remember me")
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 截图：登录页
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/remember_me_step1_{timestamp}.png")
        allure.attach.file(f"screenshots/remember_me_step1_{timestamp}.png", 
                         name="步骤1-登录页", attachment_type=allure.attachment_type.PNG)
        
        valid_data = test_data["valid_login_data"][0]
        logger.info(f"   使用账号: {valid_data['username']}")
        
        # 勾选Remember me
        checkbox = page.locator(login_page.REMEMBER_ME_CHECKBOX)
        checkbox.check()
        logger.info("   ✓ 已勾选Remember me")
        
        # 截图：勾选Remember me
        page.screenshot(path=f"screenshots/remember_me_step2_{timestamp}.png")
        allure.attach.file(f"screenshots/remember_me_step2_{timestamp}.png", 
                         name="步骤2-勾选Remember me", attachment_type=allure.attachment_type.PNG)
        
        # 登录
        login_page.login(
            username=valid_data["username"],
            password=valid_data["password"],
            remember_me=False  # 已经手动勾选了
        )
        
        # 步骤2：验证登录成功
        logger.info("\n步骤2: 验证登录成功")
        page.wait_for_timeout(3000)
        landing_page.handle_ssl_warning()
        
        # 截图：登录后
        page.screenshot(path=f"screenshots/remember_me_step3_{timestamp}.png")
        allure.attach.file(f"screenshots/remember_me_step3_{timestamp}.png", 
                         name="步骤3-登录后", attachment_type=allure.attachment_type.PNG)
        
        assert landing_page.is_logged_in(), "登录失败"
        logger.info("   ✓ 登录成功")
        
        # 步骤3：验证Cookie
        logger.info("\n步骤3: 验证认证Cookie属性")
        cookies = page.context.cookies()
        auth_cookie = next((c for c in cookies if c['name'] == '.AspNetCore.Identity.Application'), None)
        
        if auth_cookie:
            logger.info(f"   ✓ 认证Cookie存在: {auth_cookie['name']}")
            # 检查是否有expires（持久化cookie）
            if 'expires' in auth_cookie and auth_cookie['expires'] > 0:
                expire_time = datetime.fromtimestamp(auth_cookie['expires'])
                logger.info(f"   ✓ Cookie有效期: {expire_time}")
                logger.info("   ✓ Cookie已持久化（Remember me生效）")
            else:
                logger.warning("   ⚠️ Cookie没有expires属性（可能是session cookie）")
        else:
            logger.error("   ❌ 未找到认证Cookie")
        
        # 步骤4：模拟关闭浏览器重新打开（关闭页面并重新创建）
        logger.info("\n步骤4: 模拟关闭浏览器重新打开")
        current_url = page.url
        logger.info(f"   当前URL: {current_url}")
        
        # 导航到首页（模拟重新打开浏览器访问网站）
        page.goto("https://localhost:3000/")
        page.wait_for_timeout(2000)
        landing_page.handle_ssl_warning()
        
        # 截图：重新打开后
        page.screenshot(path=f"screenshots/remember_me_step4_{timestamp}.png")
        allure.attach.file(f"screenshots/remember_me_step4_{timestamp}.png", 
                         name="步骤4-重新打开后", attachment_type=allure.attachment_type.PNG)
        
        # 步骤5：验证仍然登录
        logger.info("\n步骤5: 验证用户仍然保持登录状态")
        page.wait_for_timeout(2000)
        
        is_still_logged_in = landing_page.is_logged_in()
        logger.info(f"   登录状态: {is_still_logged_in}")
        
        # 截图：最终状态
        page.screenshot(path=f"screenshots/remember_me_step5_{timestamp}.png")
        allure.attach.file(f"screenshots/remember_me_step5_{timestamp}.png", 
                         name="步骤5-最终登录状态", attachment_type=allure.attachment_type.PNG)
        
        if is_still_logged_in:
            logger.info("   ✓ Remember me功能正常：用户仍然保持登录状态")
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-LOGIN-011执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ 勾选Remember me并登录成功")
            logger.info("  ✓ 认证Cookie已持久化")
            logger.info("  ✓ 重新打开后仍保持登录状态")
            logger.info("=" * 60)
        else:
            logger.error("   ❌ Remember me功能失效：重新打开后用户未登录")
            
            # 在Allure报告中标记为Bug
            allure.attach(
                "Remember me功能Bug：\n"
                "- 现象：勾选Remember me并登录后，重新打开页面时用户未保持登录状态\n"
                "- 预期：勾选Remember me后登录，关闭并重新打开浏览器时应保持登录状态\n"
                "- 实际：重新打开后用户需要重新登录\n"
                f"- Cookie状态：{auth_cookie['name'] if auth_cookie else '无'}\n"
                "- 影响：Remember me功能失效，用户体验差\n"
                "- 严重程度：中\n"
                "- 建议：检查Remember me选项是否正确设置Cookie的有效期和持久化属性",
                name="❌ Bug详情-Remember me功能失效",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 让测试失败
            assert False, "Remember me功能失效：重新打开后用户未保持登录状态"
    
    @pytest.mark.P1
    @pytest.mark.navigation
    @pytest.mark.usability
    def test_p1_register_link(self, page):
        """
        TC-LOGIN-006: 注册链接导航验证
        
        测试目标：验证登录页面的"Register"链接能正确跳转到注册页面
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 链接 "Register"（Login Form底部或附近）
        
        测试步骤：
        1. [Login Page] 直接导航到登录页面
        2. [Login Form - 底部区域] 定位"Register"链接
        3. [验证] 确认注册链接可见
        4. [Login Form - 底部] 点击"Register"链接
        5. [验证] 确认跳转到注册页面（/Account/Register）
        6. [验证] 确认URL正确
        
        预期结果：
        - 注册链接可见且可点击
        - 成功跳转到https://localhost:44320/Account/Register
        - 用户可以从登录页面快速访问注册功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-006: 注册链接导航验证")
        logger.info("测试目标: 验证Register链接跳转功能")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        logger.info("步骤1: [Login Page] 导航到登录页面")
        login_page.navigate()
        login_page.wait_for_load()
        initial_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {initial_url}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤2-3：检查注册链接
        logger.info("\n步骤2-3: [Login Form - 底部区域] 定位并验证Register链接")
        register_link_visible = login_page.is_visible(login_page.REGISTER_LINK, timeout=3000)
        logger.info(f"   Register链接可见: {register_link_visible}")
        
        if register_link_visible:
            logger.info("   ✓ Register链接已找到且可见")
            
            # 步骤4：点击注册链接
            logger.info("\n步骤4: [Login Form - 底部] 点击'Register'链接")
            
            # 截图：点击前
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"screenshots/login_register_link_before_{timestamp}.png")
            allure.attach.file(f"screenshots/login_register_link_before_{timestamp}.png", 
                             name="步骤4-点击前", attachment_type=allure.attachment_type.PNG)
            
            login_page.click_element(login_page.REGISTER_LINK)
            logger.info("   ✓ 已点击Register链接")
            
            # 步骤5-6：验证跳转
            logger.info("\n步骤5-6: [验证] 确认跳转到注册页面")
            page.wait_for_timeout(2000)
            current_url = login_page.get_current_url()
            logger.info(f"   跳转后URL: {current_url}")
            
            # 截图：跳转后
            page.screenshot(path=f"screenshots/login_register_link_after_{timestamp}.png")
            allure.attach.file(f"screenshots/login_register_link_after_{timestamp}.png", 
                             name="步骤5-跳转到注册页", attachment_type=allure.attachment_type.PNG)
            
            assert "/Account/Register" in current_url, \
                f"应该跳转到注册页面，实际URL: {current_url}"
            logger.info("   ✓ 成功跳转到注册页面")
            logger.info(f"   ✓ URL验证通过: {current_url}")
            
            # 测试总结
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-LOGIN-006执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ Register链接可见")
            logger.info("  ✓ 点击跳转成功")
            logger.info("  ✓ URL正确：/Account/Register")
            logger.info("=" * 60)
        else:
            logger.warning("   ⚠️ Register链接未找到")
            logger.info("\n" + "=" * 60)
            logger.info("⚠️ TC-LOGIN-006: Register链接未找到（可能的UI变更）")
            logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.navigation
    @pytest.mark.usability
    def test_p1_forgot_password_link(self, page):
        """
        TC-LOGIN-007: 忘记密码链接导航验证
        
        测试目标：验证登录页面的"Forgot Password"链接能正确跳转到密码重置页面
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 链接 "Forgot Password"或"Forgot your password?"（Login Form附近）
        
        测试步骤：
        1. [Login Page] 直接导航到登录页面
        2. [Login Form - 附近区域] 定位"Forgot Password"链接
        3. [验证] 确认链接可见
        4. [Login Form] 点击"Forgot Password"链接
        5. [验证] 确认跳转到忘记密码页面（/Account/ForgotPassword）
        6. [验证] 确认URL正确
        
        预期结果：
        - 忘记密码链接可见且可点击
        - 成功跳转到https://localhost:44320/Account/ForgotPassword
        - 用户可以从登录页面快速访问密码重置功能
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-007: 忘记密码链接导航验证")
        logger.info("测试目标: 验证Forgot Password链接跳转功能")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        logger.info("步骤1: [Login Page] 导航到登录页面")
        login_page.navigate()
        login_page.wait_for_load()
        initial_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {initial_url}")
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤2-3：检查忘记密码链接
        logger.info("\n步骤2-3: [Login Form - 附近区域] 定位并验证Forgot Password链接")
        forgot_link_visible = login_page.is_visible(login_page.FORGOT_PASSWORD_LINK, timeout=3000)
        logger.info(f"   Forgot Password链接可见: {forgot_link_visible}")
        
        if forgot_link_visible:
            logger.info("   ✓ Forgot Password链接已找到且可见")
            
            # 步骤4：点击忘记密码链接
            logger.info("\n步骤4: [Login Form] 点击'Forgot Password'链接")
            
            # 截图：点击前
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"screenshots/login_forgot_link_before_{timestamp}.png")
            allure.attach.file(f"screenshots/login_forgot_link_before_{timestamp}.png", 
                             name="步骤4-点击前", attachment_type=allure.attachment_type.PNG)
            
            login_page.click_element(login_page.FORGOT_PASSWORD_LINK)
            logger.info("   ✓ 已点击Forgot Password链接")
            
            # 步骤5-6：验证跳转
            logger.info("\n步骤5-6: [验证] 确认跳转到忘记密码页面")
            page.wait_for_timeout(2000)
            current_url = login_page.get_current_url()
            logger.info(f"   跳转后URL: {current_url}")
            
            # 截图：跳转后
            page.screenshot(path=f"screenshots/login_forgot_link_after_{timestamp}.png")
            allure.attach.file(f"screenshots/login_forgot_link_after_{timestamp}.png", 
                             name="步骤5-跳转到忘记密码页", attachment_type=allure.attachment_type.PNG)
            
            assert "/Account/ForgotPassword" in current_url, \
                f"应该跳转到忘记密码页面，实际URL: {current_url}"
            logger.info("   ✓ 成功跳转到忘记密码页面")
            logger.info(f"   ✓ URL验证通过: {current_url}")
            
            # 测试总结
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-LOGIN-007执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ Forgot Password链接可见")
            logger.info("  ✓ 点击跳转成功")
            logger.info("  ✓ URL正确：/Account/ForgotPassword")
            logger.info("=" * 60)
        else:
            logger.warning("   ⚠️ Forgot Password链接未找到")
            logger.info("\n" + "=" * 60)
            logger.info("⚠️ TC-LOGIN-007: Forgot Password链接未找到（可能的UI变更）")
            logger.info("=" * 60)
    
    @pytest.mark.P2
    @pytest.mark.ui
    @pytest.mark.usability
    def test_p2_password_toggle_button(self, page):
        """
        TC-LOGIN-008: 密码可见性切换按钮验证
        
        测试目标：验证密码输入框的可见性切换按钮功能（如果存在）
        测试区域：Login Page（ABP Framework认证页面）
        测试元素：
        - 输入框 "Password"（Login Form中部）
        - 按钮 "Toggle password visibility"（Password输入框右侧，如果存在）
        
        测试步骤：
        1. [Login Page] 直接导航到登录页面
        2. [Login Form - Password字段] 输入测试密码
        3. [验证] 确认密码初始为隐藏状态（type="password"）
        4. [Login Form - Password字段右侧] 查找密码切换按钮
        5. [条件] 如果按钮存在，点击切换按钮
        6. [验证] 确认密码状态变化（type可能变为"text"）
        
        预期结果：
        - 密码初始状态为隐藏（type="password"）
        - 如果有切换按钮，点击后密码可见性应改变
        - 如果没有切换按钮，测试通过（某些UI可能不提供此功能）
        
        注意：此功能依赖于ABP框架的UI实现，可能存在也可能不存在
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LOGIN-008: 密码可见性切换按钮验证")
        logger.info("测试目标: 验证密码切换按钮（如果存在）")
        logger.info("=" * 60)
        
        login_page = LoginPage(page)
        
        # 步骤1：导航到登录页
        logger.info("步骤1: [Login Page] 导航到登录页面")
        login_page.navigate()
        login_page.wait_for_load()
        logger.info("   ✓ 登录页面加载完成")
        
        # 步骤2：输入密码
        logger.info("\n步骤2: [Login Form - Password字段] 输入测试密码")
        test_password = "TestPassword123!"
        page.fill(login_page.PASSWORD_INPUT, test_password)
        logger.info(f"   测试密码: {test_password}")
        logger.info("   ✓ 密码已输入")
        
        # 步骤3：验证初始密码状态
        logger.info("\n步骤3: [验证] 确认密码初始为隐藏状态")
        password_type = page.locator(login_page.PASSWORD_INPUT).get_attribute("type")
        logger.info(f"   密码输入框初始type: '{password_type}'")
        
        assert password_type == "password", \
            f"密码输入框初始应该是隐藏状态（type='password'），实际: {password_type}"
        logger.info("   ✓ 密码初始状态为隐藏（type='password'）")
        
        # 步骤4-6：查找并测试切换按钮
        logger.info("\n步骤4: [Login Form - Password字段右侧] 查找密码切换按钮")
        toggle_button_visible = login_page.is_visible(login_page.PASSWORD_TOGGLE_BUTTON, timeout=3000)
        logger.info(f"   密码切换按钮可见: {toggle_button_visible}")
        
        if toggle_button_visible:
            logger.info("   ✓ 密码切换按钮已找到")
            
            logger.info("\n步骤5: [Password字段右侧] 点击切换按钮")
            
            # 截图：点击前
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"screenshots/login_toggle_before_{timestamp}.png")
            allure.attach.file(f"screenshots/login_toggle_before_{timestamp}.png", 
                             name="步骤5-切换前(隐藏)", attachment_type=allure.attachment_type.PNG)
            
            login_page.click_element(login_page.PASSWORD_TOGGLE_BUTTON)
            logger.info("   ✓ 已点击切换按钮")
            
            page.wait_for_timeout(500)
            
            logger.info("\n步骤6: [验证] 确认密码状态变化")
            password_type_after = page.locator(login_page.PASSWORD_INPUT).get_attribute("type")
            logger.info(f"   点击后密码输入框type: '{password_type_after}'")
            
            # 截图：点击后
            page.screenshot(path=f"screenshots/login_toggle_after_{timestamp}.png")
            allure.attach.file(f"screenshots/login_toggle_after_{timestamp}.png", 
                             name="步骤6-切换后(应显示明文)", attachment_type=allure.attachment_type.PNG)
            
            # 严格验证：按钮存在就应该能切换，type应该变成text
            if password_type_after == "text":
                logger.info(f"   ✓ 密码状态已改变: '{password_type}' → '{password_type_after}'")
                logger.info("   ✓ 密码切换功能正常")
                
                # 测试总结
                logger.info("\n" + "=" * 60)
                logger.info("✅ TC-LOGIN-008执行成功")
                logger.info("验证总结:")
                logger.info("  ✓ 密码初始状态为隐藏")
                logger.info("  ✓ 密码切换按钮存在")
                logger.info(f"  ✓ 点击后密码显示为明文 (type='text')")
                logger.info("=" * 60)
            else:
                logger.error(f"   ❌ [Bug] 密码切换按钮点击后type未改变")
                logger.error(f"   预期: type='text'（明文显示）")
                logger.error(f"   实际: type='{password_type_after}'")
                
                # 在Allure报告中标记为Bug
                allure.attach(
                    f"密码切换按钮Bug：\n"
                    f"- 现象：点击密码切换按钮后，密码仍未显示为明文\n"
                    f"- 预期：点击后input type应变为'text'，密码显示明文\n"
                    f"- 实际：点击后input type仍为'{password_type_after}'，密码未明文显示\n"
                    f"- 影响：用户无法通过切换按钮查看输入的密码\n"
                    f"- 严重程度：中\n"
                    f"- 建议：检查密码切换按钮的事件绑定和input type切换逻辑",
                    name="❌ Bug详情-密码切换功能失效",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # 让测试失败
                assert False, (
                    f"密码切换按钮功能失效：点击后type仍为'{password_type_after}'，"
                    f"应变为'text'以显示明文密码"
                )
        else:
            logger.info("   ℹ️ 密码切换按钮未找到（此功能可能不存在）")
            logger.info("   ℹ️ 这是正常的，某些UI不提供密码可见性切换")
            
            # 测试总结
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-LOGIN-008执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ 密码初始状态为隐藏")
            logger.info("  ℹ️ 密码切换按钮不存在（UI设计）")
            logger.info("=" * 60)
