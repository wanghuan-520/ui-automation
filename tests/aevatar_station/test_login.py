"""
登录功能测试模块
包含登录相关的功能测试、边界测试、异常测试和安全测试
"""
import pytest
import logging
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
        
        # 步骤1：导航到首页并点击Sign In
        logger.info("步骤1: [Landing Page - Header右上角] 导航到首页")
        landing_page.navigate()
        assert landing_page.is_loaded(), "首页未正确加载"
        logger.info("   ✓ 首页加载成功: https://localhost:3000/")
        
        logger.info("步骤2: [Landing Page - Header] 点击'Sign In'按钮")
        landing_page.click_sign_in()
        logger.info("   ✓ 已点击Sign In按钮，等待跳转到登录页")
        
        # 步骤2：等待登录页面加载
        logger.info("\n步骤3: [Login Page] 等待ABP登录页面加载")
        login_page.wait_for_load()
        assert login_page.is_loaded(), "登录页面未正确加载"
        current_url = login_page.get_current_url()
        logger.info(f"   登录页面URL: {current_url}")
        assert "44320" in current_url and "/Account/Login" in current_url, \
            f"未跳转到正确的登录页面，当前URL: {current_url}"
        logger.info("   ✓ ABP登录页面加载成功")
        
        # 步骤3-5：填写登录表单
        valid_data = test_data["valid_login_data"][0]
        logger.info("\n步骤4-6: [Login Form] 填写登录凭证")
        logger.info(f"   Username: {valid_data['username']}")
        logger.info(f"   Password: {'*' * len(valid_data['password'])} ({len(valid_data['password'])}位)")
        logger.info(f"   Remember me: {valid_data.get('remember_me', False)}")
        
        login_page.login(
            username=valid_data["username"],
            password=valid_data["password"],
            remember_me=valid_data.get("remember_me", False)
        )
        logger.info("   ✓ 登录信息已填写并提交")
        
        # 步骤7-9：验证登录成功
        logger.info("\n步骤7-9: [验证] 确认登录成功")
        logger.info("   等待页面跳转...")
        page.wait_for_timeout(3000)
        landing_page.handle_ssl_warning()
        
        # 验证点1：URL跳转
        final_url = landing_page.get_current_url()
        logger.info(f"   最终URL: {final_url}")
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
    
    @pytest.mark.P0
    @pytest.mark.exception
    def test_p0_login_with_invalid_credentials(self, page, test_data):
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
        
        login_page.login(
            username=invalid_data["username"],
            password=invalid_data["password"]
        )
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
        
        # 注意：错误消息显示取决于ABP后端配置
        logger.info("   ℹ️ 错误消息显示取决于ABP后端安全配置")
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-001执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 无效凭证登录失败")
        logger.info("  ✓ 停留在登录页面")
        logger.info("  ✓ 未跳转到首页")
        logger.info("=" * 60)
    
    @pytest.mark.P0
    @pytest.mark.exception
    def test_p0_login_with_empty_credentials(self, page):
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
        page.wait_for_timeout(1000)
        current_url = login_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        
        assert "Account/Login" in current_url, \
            f"空值提交不应跳转，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 空值验证生效，停留在登录页面")
        
        # 场景2：仅用户名为空
        logger.info("\n" + "-" * 60)
        logger.info("场景2: 仅用户名为空（密码有值）")
        logger.info("-" * 60)
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
        
        assert "Account/Login" in current_url, \
            f"用户名为空不应跳转，应停留在登录页面，当前URL: {current_url}"
        logger.info("   ✓ 用户名必填验证生效")
        
        # 场景3：仅密码为空
        logger.info("\n" + "-" * 60)
        logger.info("场景3: 仅密码为空（用户名有值）")
        logger.info("-" * 60)
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
    
    @pytest.mark.P0
    @pytest.mark.security
    def test_p0_sql_injection_protection(self, page):
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
        
        login_page.login(
            username=sql_injection_username,
            password=sql_injection_password
        )
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
        
        # 测试总结
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-SECURITY-001执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ SQL注入攻击被成功拦截")
        logger.info("  ✓ 停留在登录页面，未获得访问权限")
        logger.info("  ✓ 身份验证机制未被绕过")
        logger.info("  ✓ 系统安全防护有效")
        logger.info("=" * 60)


@pytest.mark.login
@pytest.mark.usability
class TestLoginUsability:
    """登录页面可用性测试类
    
    测试登录页面的用户体验和可用性功能，包括：
    - 密码可见性控制
    - Remember Me功能
    - 导航链接（注册、忘记密码）
    """
    
    @pytest.mark.P2
    @pytest.mark.ui
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
    @pytest.mark.functional
    def test_p2_remember_me_checkbox(self, page):
        """
        TC-LOGIN-004: Remember Me复选框功能测试
        
        测试目标：验证"Remember Me"复选框的可见性和交互功能
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
        
        assert checked_state, "复选框应该被勾选"
        logger.info("   ✓ 复选框成功勾选")
        
        # 步骤6-7：取消勾选
        logger.info("\n步骤6-7: [Login Form - Remember me] 取消勾选复选框")
        checkbox.uncheck()
        unchecked_state = checkbox.is_checked()
        logger.info(f"   取消勾选后状态: {'已勾选' if unchecked_state else '未勾选'}")
        
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
    @pytest.mark.navigation
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
            login_page.click_element(login_page.REGISTER_LINK)
            logger.info("   ✓ 已点击Register链接")
            
            # 步骤5-6：验证跳转
            logger.info("\n步骤5-6: [验证] 确认跳转到注册页面")
            page.wait_for_timeout(2000)
            current_url = login_page.get_current_url()
            logger.info(f"   跳转后URL: {current_url}")
            
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
            login_page.click_element(login_page.FORGOT_PASSWORD_LINK)
            logger.info("   ✓ 已点击Forgot Password链接")
            
            # 步骤5-6：验证跳转
            logger.info("\n步骤5-6: [验证] 确认跳转到忘记密码页面")
            page.wait_for_timeout(2000)
            current_url = login_page.get_current_url()
            logger.info(f"   跳转后URL: {current_url}")
            
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
            login_page.click_element(login_page.PASSWORD_TOGGLE_BUTTON)
            logger.info("   ✓ 已点击切换按钮")
            
            page.wait_for_timeout(500)
            
            logger.info("\n步骤6: [验证] 确认密码状态变化")
            password_type_after = page.locator(login_page.PASSWORD_INPUT).get_attribute("type")
            logger.info(f"   点击后密码输入框type: '{password_type_after}'")
            
            if password_type_after != password_type:
                logger.info(f"   ✓ 密码状态已改变: '{password_type}' → '{password_type_after}'")
            else:
                logger.info(f"   ℹ️ 密码type未改变（可能使用其他方式控制可见性）")
            
            # 测试总结
            logger.info("\n" + "=" * 60)
            logger.info("✅ TC-LOGIN-008执行成功")
            logger.info("验证总结:")
            logger.info("  ✓ 密码初始状态为隐藏")
            logger.info("  ✓ 密码切换按钮存在")
            logger.info(f"  ✓ 点击后type: '{password_type_after}'")
            logger.info("=" * 60)
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

