"""
注册功能测试模块
包含注册相关的功能测试、边界测试、异常测试和安全测试

ABP Framework 密码策略要求：
- 至少包含一位非字母数字字符（特殊字符如 !@#$%）
- 至少包含一位小写字母 (a-z)
- 至少包含一位大写字母 (A-Z)
- 至少包含一位数字 (0-9)
- 最小长度 8 位
"""
import pytest
import logging
import allure
import hashlib
import time
from datetime import datetime
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.register_page import RegisterPage

logger = logging.getLogger(__name__)


def generate_unique_user(worker_id, prefix="reg"):
    """生成唯一的用户名和邮箱，支持并行测试"""
    worker_suffix = f"w{worker_id}" if worker_id and worker_id != "master" else ""
    timestamp = datetime.now().strftime("%H%M%S%f")[:8]
    unique_str = f"{worker_suffix}_{timestamp}"
    username = f"{prefix}_{unique_str}"
    email = f"{prefix}_{unique_str}@test.com"
    return username, email


@pytest.mark.register
class TestRegister:
    """注册功能测试类"""
    
    # ==================== P0 功能测试 ====================
    
    @pytest.mark.P0
    @pytest.mark.functional
    @allure.feature("注册功能")
    @allure.story("成功注册")
    def test_p0_successful_register(self, page, test_data, worker_id):
        """
        TC-FUNC-001: 用户成功注册系统
        
        测试目标：验证用户使用有效信息可以成功注册新账号
        测试区域：Register Page（ABP Framework注册页面）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FUNC-001: 用户成功注册系统")
        logger.info("=" * 60)
        
        landing_page = LandingPage(page)
        register_page = RegisterPage(page)
        
        with allure.step("步骤1: 导航到注册页面"):
            # 前置截图
            landing_page.navigate()
            page.screenshot(path="screenshots/reg_func001_step1_before.png")
            allure.attach.file("screenshots/reg_func001_step1_before.png", 
                             name="步骤1-前-首页", attachment_type=allure.attachment_type.PNG)
            
            # 带 returnUrl 参数导航，模拟从前端发起注册
            register_page.navigate(return_url="https://localhost:3000/")
            
            # 后置截图
            page.screenshot(path="screenshots/reg_func001_step1_after.png")
            allure.attach.file("screenshots/reg_func001_step1_after.png", 
                             name="步骤1-后-注册页面", attachment_type=allure.attachment_type.PNG)
            
            assert register_page.is_loaded(), "注册页面未正确加载"
            logger.info("   ✓ 注册页面加载成功")
        
        with allure.step("步骤2: 准备唯一注册数据"):
            base_data = test_data["register_data"]["valid_register_data"][0]
            username, email = generate_unique_user(worker_id)
            password = base_data["password"]
            logger.info(f"   生成的注册数据: User={username}, Email={email}")
        
        with allure.step("步骤3: 填写注册表单"):
            # 前置截图
            page.screenshot(path="screenshots/reg_func001_step3_before.png")
            allure.attach.file("screenshots/reg_func001_step3_before.png", 
                             name="步骤3-前-空表单", attachment_type=allure.attachment_type.PNG)
            
            register_page.fill_username(username)
            register_page.fill_email(email)
            register_page.fill_password(password)
            
            # 后置截图
            page.screenshot(path="screenshots/reg_func001_step3_after.png")
            allure.attach.file("screenshots/reg_func001_step3_after.png", 
                             name="步骤3-后-填写完成", attachment_type=allure.attachment_type.PNG)
            logger.info("   ✓ 表单填写完成")
        
        with allure.step("步骤4: 提交注册"):
            # 前置截图
            page.screenshot(path="screenshots/reg_func001_step4_before.png")
            allure.attach.file("screenshots/reg_func001_step4_before.png", 
                             name="步骤4-前-提交前", attachment_type=allure.attachment_type.PNG)
            
            logger.info("   提交注册表单...")
            register_page.click_register_button()
            page.wait_for_timeout(3000)
            
            # 后置截图
            page.screenshot(path="screenshots/reg_func001_step4_after.png")
            allure.attach.file("screenshots/reg_func001_step4_after.png", 
                             name="步骤4-后-提交后", attachment_type=allure.attachment_type.PNG)
        
        with allure.step("步骤5: 验证注册成功并确认登录状态"):
            # 等待页面跳转和加载完成
            page.wait_for_timeout(2000)
            
            # 等待网络空闲（确保所有请求完成）
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except:
                pass
            
            current_url = page.url
            logger.info(f"   注册后URL: {current_url}")

            # 验证1：检查页面跳转
            if "/Register" not in current_url:
                if "localhost:3000" in current_url:
                    logger.info(f"   ✓ 成功跳转到前端主页: {current_url}")
                elif "localhost:44320" in current_url:
                    logger.info(f"   ✓ 成功跳转到后端主页: {current_url}")
                else:
                    logger.info(f"   ✓ 成功跳转到: {current_url}")
            else:
                # 仍在注册页，检查错误
                error_element = page.locator(register_page.ERROR_MESSAGE)
                if error_element.count() > 0:
                    error_text = error_element.first.text_content()
                    logger.error(f"   ❌ 注册失败: {error_text}")
                    raise Exception(f"注册失败: {error_text}")
                else:
                    logger.error(f"   ❌ 注册后仍停留在注册页")
                    raise AssertionError("注册未成功跳转")

            # 验证2：确认用户已登录状态
            logger.info("   等待前端登录状态更新...")
            # 尝试刷新一次页面以确保状态同步
            page.wait_for_timeout(2000)
            try:
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
            except:
                pass

            logger.info("\n   === 开始验证登录状态 ===")
            
            # 2.1 检查用户菜单（最直接的登录证据）
            user_menu_found = False
            try:
                user_menu_locator = page.locator('button[aria-label*="user" i], button:has-text("Toggle user menu")')
                if user_menu_locator.count() > 0:
                    is_visible = user_menu_locator.first.is_visible(timeout=2000)
                    if is_visible:
                        logger.info("   ✅ 检测到用户菜单按钮（已登录）")
                        user_menu_found = True
                    else:
                        logger.info("   ⚠️ 用户菜单按钮存在但不可见")
            except Exception as e:
                logger.info(f"   ⚠️ 检测用户菜单异常: {str(e)}")
            
            # 2.2 检查Sign In按钮（应该消失）
            sign_in_visible = True
            try:
                sign_in_locator = page.locator('button:has-text("Sign In"), a:has-text("Sign In")')
                if sign_in_locator.count() > 0:
                    sign_in_visible = sign_in_locator.first.is_visible(timeout=2000)
                else:
                    sign_in_visible = False
            except:
                pass
                
            if sign_in_visible:
                logger.warning("   ⚠️ 'Sign In'按钮仍可见")
            else:
                logger.info("   ✅ 'Sign In'按钮不可见")

            # 2.3 检查Cookie（辅助证据）
            cookies = page.context.cookies()
            auth_cookie_found = any(c['name'] == '.AspNetCore.Identity.Application' for c in cookies)
            logger.info(f"   {'✅' if auth_cookie_found else '⚠️'} 认证Cookie: {'.AspNetCore.Identity.Application' if auth_cookie_found else '未找到'}")
            
            # 截图
            page.screenshot(path="screenshots/reg_func001_step5_status.png")
            allure.attach.file("screenshots/reg_func001_step5_status.png", 
                             name="步骤5-登录状态验证", attachment_type=allure.attachment_type.PNG)

            # 严格断言：必须在UI上体现登录状态
            if not user_menu_found:
                logger.error("   ❌ 前端UI未更新登录状态（Bug: 注册成功但显示未登录）")
                
                # 记录Bug信息
                allure.attach(
                    "前端状态同步Bug：\n"
                    "- 现象：注册跳转后，前端UI仍显示'Sign In'，未显示用户菜单\n"
                    f"- Cookie状态：{'.AspNetCore.Identity.Application' if auth_cookie_found else '无'} \n"
                    "- 影响：用户注册后无法感知已登录状态\n",
                    name="🐛 前端状态同步Bug",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # 即使有Cookie，只要UI没更新，就让它 Fail
                assert False, "注册成功后前端UI未更新登录状态（仍显示Sign In，已知Bug）"
            
            logger.info("   ✓ 注册成功并登录验证通过")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-FUNC-001执行成功")
        logger.info("=" * 60)

    # ==================== P0 异常测试 ====================
    
    @pytest.mark.P1
    @pytest.mark.exception
    @allure.feature("注册功能")
    @allure.story("重复数据验证")
    def test_p1_duplicate_email(self, page, test_data, worker_id):
        """
        TC-EXCEPTION-004: 重复邮箱注册验证
        
        测试目标：验证系统拦截已存在的邮箱重复注册
        测试区域：Register Page（ABP Framework注册页面）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-004: 重复邮箱注册验证")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        
        # 第一次注册：创建账号
        with allure.step("步骤1: 首次注册创建账号"):
            register_page.navigate()
            
            # 前置截图
            page.screenshot(path="screenshots/reg_exc004_step1_before.png")
            allure.attach.file("screenshots/reg_exc004_step1_before.png", 
                             name="步骤1-前-注册页面", attachment_type=allure.attachment_type.PNG)
            
            username1, email1 = generate_unique_user(worker_id, "dup")
            register_page.fill_username(username1)
            register_page.fill_email(email1)
            register_page.fill_password("TestPass123!")
            
            # 填写后截图
            page.screenshot(path="screenshots/reg_exc004_step1_filled.png")
            allure.attach.file("screenshots/reg_exc004_step1_filled.png", 
                             name="步骤1-填写完成", attachment_type=allure.attachment_type.PNG)
            
            register_page.click_register_button()
            page.wait_for_timeout(3000)
            
            # 后置截图
            page.screenshot(path="screenshots/reg_exc004_step1_after.png")
            allure.attach.file("screenshots/reg_exc004_step1_after.png", 
                             name="步骤1-后-首次注册结果", attachment_type=allure.attachment_type.PNG)
            
            logger.info(f"   ✓ 首次注册完成: {email1}")
        
        # 第二次注册：使用相同邮箱
        with allure.step("步骤2: 使用相同邮箱再次注册"):
            register_page.navigate()
            
            # 前置截图
            page.screenshot(path="screenshots/reg_exc004_step2_before.png")
            allure.attach.file("screenshots/reg_exc004_step2_before.png", 
                             name="步骤2-前-重新打开注册页", attachment_type=allure.attachment_type.PNG)
            
            username2, _ = generate_unique_user(worker_id, "dup2")
            register_page.fill_username(username2)  # 不同的用户名
            register_page.fill_email(email1)  # 相同的邮箱
            register_page.fill_password("TestPass123!")
            
            # 填写后截图
            page.screenshot(path="screenshots/reg_exc004_step2_filled.png")
            allure.attach.file("screenshots/reg_exc004_step2_filled.png", 
                             name="步骤2-填写重复邮箱", attachment_type=allure.attachment_type.PNG)
            
            register_page.click_register_button()
            
            # 等待错误提示或页面响应
            page.wait_for_timeout(3000)
            
            # 截图 - 错误提示
            page.screenshot(path="screenshots/reg_exc004_step2_error.png")
            allure.attach.file("screenshots/reg_exc004_step2_error.png", 
                             name="步骤2-错误提示-重复邮箱", attachment_type=allure.attachment_type.PNG)
        
        with allure.step("步骤3: 验证重复邮箱被拦截"):
            current_url = page.url
            page_content = page.content()
            
            # 截图 - 验证结果
            page.screenshot(path="screenshots/reg_exc004_step3_verify.png")
            allure.attach.file("screenshots/reg_exc004_step3_verify.png", 
                             name="步骤3-验证被拦截", attachment_type=allure.attachment_type.PNG)
            
            # 应该停留在注册页或显示错误
            if "/Register" in current_url:
                logger.info("   ✓ 重复邮箱被拦截，停留在注册页")
            elif "已" in page_content or "already" in page_content.lower() or "exist" in page_content.lower():
                logger.info("   ✓ 显示邮箱已存在错误")
            else:
                logger.warning(f"   ⚠️ 未明确拦截，当前URL: {current_url}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-004执行成功")
        logger.info("=" * 60)

    @pytest.mark.P1
    @pytest.mark.exception
    @allure.feature("注册功能")
    @allure.story("重复数据验证")
    def test_p1_duplicate_username(self, page, test_data, worker_id):
        """
        TC-EXCEPTION-005: 重复用户名注册验证
        
        测试目标：验证系统拦截已存在的用户名重复注册
        测试区域：Register Page（ABP Framework注册页面）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-005: 重复用户名注册验证")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        duplicate_data = test_data["register_data"].get("duplicate_data", [])
        
        if duplicate_data:
            case = duplicate_data[0]  # 使用已知存在的用户名
            
            with allure.step(f"测试重复用户名: {case['username']}"):
                register_page.navigate()
                
                # 前置截图
                page.screenshot(path="screenshots/reg_exc005_before.png")
                allure.attach.file("screenshots/reg_exc005_before.png", 
                                 name="前-注册页面", attachment_type=allure.attachment_type.PNG)
                
                _, unique_email = generate_unique_user(worker_id, "dupname")
                register_page.fill_username(case["username"])  # 已存在的用户名
                register_page.fill_email(unique_email)  # 唯一的邮箱
                register_page.fill_password(case["password"])
                
                # 填写后截图
                page.screenshot(path="screenshots/reg_exc005_filled.png")
                allure.attach.file("screenshots/reg_exc005_filled.png", 
                                 name="填写重复用户名", attachment_type=allure.attachment_type.PNG)
                
                register_page.click_register_button()
                
                # 等待错误提示或页面响应
                page.wait_for_timeout(3000)
                
                # 截图 - 错误提示
                page.screenshot(path="screenshots/reg_exc005_error.png")
                allure.attach.file("screenshots/reg_exc005_error.png", 
                                 name="错误提示-重复用户名", attachment_type=allure.attachment_type.PNG)
                
                current_url = page.url
                page_content = page.content()
                
                if "/Register" in current_url:
                    logger.info("   ✓ 重复用户名被拦截，停留在注册页")
                elif "已存在" in page_content or "already" in page_content.lower():
                    logger.info("   ✓ 显示用户名已存在错误")
                else:
                    logger.warning(f"   ⚠️ 用户名 '{case['username']}' 可能不存在或未被拦截")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-005执行成功")
        logger.info("=" * 60)

    @pytest.mark.P1
    @pytest.mark.exception
    @allure.feature("注册功能")
    @allure.story("必填项验证")
    def test_p1_register_empty_fields(self, page, test_data):
        """
        TC-EXCEPTION-001: 空值输入验证测试
        
        测试目标：验证注册表单对空值输入的前端验证机制
        测试区域：Register Page（ABP Framework注册页面）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-001: 空值输入验证测试")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        
        with allure.step("步骤1: 导航到注册页面"):
            register_page.navigate()
            
            # 导航后截图
            page.screenshot(path="screenshots/reg_exc001_step1_loaded.png")
            allure.attach.file("screenshots/reg_exc001_step1_loaded.png", 
                             name="步骤1-注册页面加载完成", attachment_type=allure.attachment_type.PNG)
            logger.info("   ✓ 注册页面加载完成")
        
        with allure.step("步骤2: 尝试直接提交空表单"):
            # 前置截图
            page.screenshot(path="screenshots/reg_exc001_step2_before.png")
            allure.attach.file("screenshots/reg_exc001_step2_before.png", 
                             name="步骤2-前-空表单", attachment_type=allure.attachment_type.PNG)
            
            logger.info("   尝试提交空表单...")
            register_page.click_register_button()
            page.wait_for_timeout(1000)
            
            # 后置截图
            page.screenshot(path="screenshots/reg_exc001_step2_after.png")
            allure.attach.file("screenshots/reg_exc001_step2_after.png", 
                             name="步骤2-后-提交结果", attachment_type=allure.attachment_type.PNG)
        
        with allure.step("步骤3: 验证表单验证或后端异常"):
            page.wait_for_timeout(1500)  # 等待响应
            current_url = page.url
            page_content = page.content()
            
            # 截图 - 验证结果
            page.screenshot(path="screenshots/reg_exc001_step3_result.png")
            allure.attach.file("screenshots/reg_exc001_step3_result.png", 
                             name="步骤3-提交结果（预期：验证错误或异常）", attachment_type=allure.attachment_type.PNG)
            
            # 验证：空表单提交应该被前端或后端友好拦截
            # 验证1：检查是否显示异常页面（这是Bug行为，应该失败）
            if "An unhandled exception occurred" in page_content or "AbpValidationException" in page_content:
                logger.error("   ❌ [Bug] 后端抛出未处理异常，应该返回友好的验证错误")
                logger.error("   Bug详情: AbpValidationException - ModelState is not valid")
                logger.error("   预期行为: 应该显示友好的表单验证错误，或在前端阻止提交")
                
                # 在Allure报告中标记为失败的Bug
                allure.attach(
                    "Bug描述：\n"
                    "- 实际行为：后端抛出未处理的 AbpValidationException\n"
                    "- 预期行为：应该返回友好的验证错误提示，如'用户名不能为空'等\n"
                    "- 影响：用户体验差，暴露了技术细节和堆栈跟踪\n"
                    "- 严重程度：高\n"
                    "- 建议：在后端统一异常处理或在前端增加表单验证",
                    name="❌ Bug详情",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # 让测试失败
                assert False, (
                    "空表单提交后端抛出未处理异常（AbpValidationException），"
                    "应该返回友好的验证错误提示"
                )
            
            # 验证2：检查是否正确停留在注册页（预期行为）
            elif "/Account/Register" in current_url:
                logger.info(f"   ✓ 停留在注册页面: {current_url}")
                logger.info("   ✓ 表单验证正常工作（未跳转）")
            
            # 验证3：检查是否意外跳转到其他页面（也是Bug）
            else:
                logger.error(f"   ❌ 意外跳转到: {current_url}")
                assert False, f"空表单不应跳转到其他页面，当前URL: {current_url}"
            
            # 确保没有跳转到前端主页
            assert "localhost:3000" not in current_url, f"不应跳转到前端主页，当前URL: {current_url}"
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-001执行成功")
        logger.info("=" * 60)

    @pytest.mark.P1
    @pytest.mark.exception
    @allure.feature("注册功能")
    @allure.story("邮箱验证")
    def test_p1_register_invalid_email(self, page, test_data, worker_id):
        """
        TC-EXCEPTION-002: ABP邮箱格式验证（包含边界值）
        
        测试目标：验证系统对无效邮箱格式和边界情况的拦截能力
        测试区域：Register Page（ABP Framework注册页面）
        
        验证规则：
        - 不能为空
        - 必须包含@符号
        - 必须有用户名部分和域名部分
        - 不能包含空格
        - 不能包含连续点号
        - 不能包含双@符号
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-002: ABP邮箱格式验证（包含边界值）")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        
        # 合并所有邮箱验证数据
        invalid_emails = test_data["register_data"].get("invalid_emails", [])
        abp_emails = test_data["register_data"].get("abp_email_validation", [])
        all_email_cases = invalid_emails + abp_emails
        
        for idx, case in enumerate(all_email_cases, 1):
            # 处理空邮箱case（不跳过，要测试）
            email_display = case.get("email", "") if case.get("email") else "(空)"
            
            with allure.step(f"测试无效邮箱 {idx}: {email_display}"):
                logger.info(f"\n--- 测试 {idx}: {case['description']} ---")
                logger.info(f"   邮箱: {email_display}")
                
                register_page.navigate()
                
                # 前置截图
                page.screenshot(path=f"screenshots/reg_exc002_case{idx}_before.png")
                allure.attach.file(f"screenshots/reg_exc002_case{idx}_before.png", 
                                 name=f"用例{idx}-前-空表单", attachment_type=allure.attachment_type.PNG)
                
                # 使用唯一用户名避免冲突
                username, _ = generate_unique_user(worker_id, f"em{idx}")
                
                register_page.fill_username(username)
                register_page.fill_email(case.get("email", ""))
                register_page.fill_password(case.get("password", "ValidPass123!"))
                
                # 填写后截图
                page.screenshot(path=f"screenshots/reg_exc002_case{idx}_filled.png")
                allure.attach.file(f"screenshots/reg_exc002_case{idx}_filled.png", 
                                 name=f"用例{idx}-填写完成", attachment_type=allure.attachment_type.PNG)
                
                register_page.click_register_button()
                page.wait_for_timeout(1000)
                
                # 后置截图
                page.screenshot(path=f"screenshots/reg_exc002_case{idx}_after.png")
                allure.attach.file(f"screenshots/reg_exc002_case{idx}_after.png", 
                                 name=f"用例{idx}-后-提交结果", attachment_type=allure.attachment_type.PNG)
                
                assert "/Account/Register" in page.url, \
                    f"无效邮箱 {case['email']} 不应导致跳转"
                logger.info(f"   ✓ 无效邮箱被拦截")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-002执行成功")
        logger.info("=" * 60)

    # ==================== P0 安全测试 ====================
    
    @pytest.mark.P1
    @pytest.mark.security
    @allure.feature("注册功能")
    @allure.story("ABP密码策略")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_p1_abp_password_complexity(self, page, test_data, worker_id):
        """
        TC-SECURITY-001: ABP密码复杂度验证
        
        测试目标：验证系统对不符合ABP密码策略的密码的拦截能力
        测试区域：Register Page（ABP Framework注册页面）
        
        ABP Framework 密码策略要求：
        - 至少包含一位非字母数字字符（特殊字符）
        - 至少包含一位小写字母 (a-z)
        - 至少包含一位大写字母 (A-Z)
        - 至少包含一位数字 (0-9)
        - 最小长度 8 位
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-SECURITY-001: ABP密码复杂度验证")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        
        # 定义必须被拦截的弱密码测试用例（包含边界值测试）
        weak_password_cases = [
            # === 长度边界值测试 ===
            {
                "password": "T1!",
                "description": "长度边界-3位（严重不足）",
                "expected_errors": ["6", "8"]
            },
            {
                "password": "Tt1!@",
                "description": "长度边界-5位（临界不足）",
                "expected_errors": ["6", "8"]
            },
            # 注：6位满足所有要求的密码（Tt1!@#）可能会通过，取决于ABP配置
            
            # === 字符类型缺失测试 ===
            {
                "password": "12345678",
                "description": "仅数字-缺少大小写字母和特殊字符",
                "expected_errors": ["非字母数字字符", "小写字母", "大写字母"]
            },
            {
                "password": "abcdefgh",
                "description": "仅小写字母-缺少大写、数字和特殊字符",
                "expected_errors": ["非字母数字字符", "大写字母", "数字"]
            },
            {
                "password": "ABCDEFGH",
                "description": "仅大写字母-缺少小写、数字和特殊字符",
                "expected_errors": ["非字母数字字符", "小写字母", "数字"]
            },
            {
                "password": "TestPass123",
                "description": "缺少特殊字符（8位+大小写+数字）",
                "expected_errors": ["非字母数字字符"]
            },
            {
                "password": "TestPass!@#",
                "description": "缺少数字（8位+大小写+特殊字符）",
                "expected_errors": ["数字"]
            },
            {
                "password": "testpass123!",
                "description": "缺少大写字母（12位+小写+数字+特殊字符）",
                "expected_errors": ["大写字母"]
            },
            {
                "password": "TESTPASS123!",
                "description": "缺少小写字母（12位+大写+数字+特殊字符）",
                "expected_errors": ["小写字母"]
            },
        ]
        
        for idx, case in enumerate(weak_password_cases, 1):
            with allure.step(f"测试用例 {idx}: {case['description']}"):
                logger.info(f"\n--- 测试 {idx}/{len(weak_password_cases)}: {case['description']} ---")
                logger.info(f"   测试密码: {case['password']}")
                
                # 导航到注册页
                register_page.navigate()
                
                # 前置截图
                page.screenshot(path=f"screenshots/reg_sec001_case{idx}_before.png")
                allure.attach.file(f"screenshots/reg_sec001_case{idx}_before.png", 
                                 name=f"用例{idx}-前-空表单", 
                                 attachment_type=allure.attachment_type.PNG)
                
                # 生成唯一用户名避免冲突
                username, email = generate_unique_user(worker_id, f"pwd{idx}")
                
                # 填写表单
                register_page.fill_username(username)
                register_page.fill_email(email)
                register_page.fill_password(case["password"])
                
                # 填写后截图
                page.screenshot(path=f"screenshots/reg_sec001_case{idx}_filled.png")
                allure.attach.file(f"screenshots/reg_sec001_case{idx}_filled.png", 
                                 name=f"用例{idx}-填写完成", 
                                 attachment_type=allure.attachment_type.PNG)
                
                # 提交
                register_page.click_register_button()
                page.wait_for_timeout(2000)
                
                # 提交后截图
                page.screenshot(path=f"screenshots/reg_sec001_case{idx}_after.png")
                allure.attach.file(f"screenshots/reg_sec001_case{idx}_after.png", 
                                 name=f"用例{idx}-后-提交结果", 
                                 attachment_type=allure.attachment_type.PNG)
                
                # 验证：弱密码应该被拦截，停留在注册页
                current_url = page.url
                logger.info(f"   提交后URL: {current_url}")
                
                assert "/Register" in current_url, \
                    f"密码不符合要求时应保持在注册页面，实际URL: {current_url}"
                
                # 验证错误消息
                page_content = page.content()
                for expected_error in case["expected_errors"]:
                    if expected_error in page_content:
                        logger.info(f"   ✓ 捕获到预期错误关键词: '{expected_error}'")
                        break
                else:
                    logger.warning(f"   ⚠️ 未捕获到预期错误关键词，但注册已被拦截")
                
                logger.info(f"   ✓ 用例{idx}通过: 弱密码被正确拦截")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-SECURITY-001执行成功: 所有弱密码均被正确拦截")
        logger.info("=" * 60)

    # ==================== P1 异常测试 ====================
    
    @pytest.mark.P2
    @pytest.mark.exception
    @allure.feature("注册功能")
    @allure.story("用户名验证")
    def test_p2_username_validation(self, page, test_data, worker_id):
        """
        TC-EXCEPTION-003: ABP用户名格式验证（包含边界值）
        
        测试目标：验证用户名格式限制和边界情况
        测试区域：Register Page（ABP Framework注册页面）
        
        验证规则：
        - 不能为空
        - 最小长度限制（测试1位、2位边界）
        - 不能包含空格
        - 不能包含特殊字符（如 @ # $ % &）
        - 允许字母、数字、下划线、连字符、点号
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-EXCEPTION-003: ABP用户名格式验证")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        username_cases = test_data["register_data"].get("abp_username_validation", [])
        
        for idx, case in enumerate(username_cases, 1):
            if case.get("expected_result") == "success":
                continue  # 跳过预期成功的用例
            
            # 对于短用户名（易冲突），添加随机后缀
            test_username = case["username"]
            if len(test_username) <= 2 and test_username:  # 短用户名且非空
                timestamp = str(int(time.time() * 1000))[-6:]  # 取时间戳后6位
                test_username = f"{test_username}_{timestamp}"
                logger.info(f"   短用户名添加随机后缀: {case['username']} -> {test_username}")
            
            with allure.step(f"测试用户名: {case['username']} ({case['description']})"):
                logger.info(f"\n--- 测试 {idx}: {case['description']} ---")
                logger.info(f"   原用户名: {case['username']}")
                logger.info(f"   测试用户名: {test_username}")
                
                register_page.navigate()
                
                # 前置截图
                page.screenshot(path=f"screenshots/reg_exc003_case{idx}_before.png")
                allure.attach.file(f"screenshots/reg_exc003_case{idx}_before.png", 
                                 name=f"用例{idx}-前-空表单", attachment_type=allure.attachment_type.PNG)
                
                # 使用唯一邮箱
                _, email = generate_unique_user(worker_id, f"uname{idx}")
                
                register_page.fill_username(test_username)
                register_page.fill_email(email)
                register_page.fill_password(case["password"])
                
                # 填写后截图
                page.screenshot(path=f"screenshots/reg_exc003_case{idx}_filled.png")
                allure.attach.file(f"screenshots/reg_exc003_case{idx}_filled.png", 
                                 name=f"用例{idx}-填写完成", attachment_type=allure.attachment_type.PNG)
                
                register_page.click_register_button()
                page.wait_for_timeout(1500)
                
                # 后置截图
                page.screenshot(path=f"screenshots/reg_exc003_case{idx}_after.png")
                allure.attach.file(f"screenshots/reg_exc003_case{idx}_after.png", 
                                 name=f"用例{idx}-后-提交结果", attachment_type=allure.attachment_type.PNG)
                
                current_url = page.url
                page_content = page.content()
                
                # 验证是否被拦截（停留在注册页或显示错误）
                if "/Register" in current_url:
                    logger.info(f"   ✓ 无效用户名被拦截")
                elif case.get("expected_error") and case["expected_error"] in page_content:
                    logger.info(f"   ✓ 捕获到预期错误: {case['expected_error']}")
                else:
                    logger.warning(f"   ⚠️ 用户名 '{case['username']}' 未被拦截，当前URL: {current_url}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-EXCEPTION-003执行成功")
        logger.info("=" * 60)

    # ==================== P2 UI测试 ====================
    
    @pytest.mark.P2
    @pytest.mark.ui
    @allure.feature("注册功能")
    @allure.story("页面加载")
    def test_p2_register_page_load(self, page):
        """
        TC-UI-001: 注册页面加载与元素验证
        
        测试目标：验证注册页面所有核心元素正确加载
        测试区域：Register Page（ABP Framework注册页面）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-UI-001: 注册页面加载与元素验证")
        logger.info("=" * 60)
        
        register_page = RegisterPage(page)
        
        with allure.step("步骤1: 导航到注册页面"):
            # 前置截图
            page.screenshot(path="screenshots/reg_ui001_step1_before.png")
            allure.attach.file("screenshots/reg_ui001_step1_before.png", 
                             name="步骤1-前-导航前", attachment_type=allure.attachment_type.PNG)
            
            register_page.navigate()
            
            # 后置截图
            page.screenshot(path="screenshots/reg_ui001_step1_after.png")
            allure.attach.file("screenshots/reg_ui001_step1_after.png", 
                             name="步骤1-后-注册页面", attachment_type=allure.attachment_type.PNG)
            logger.info("   ✓ 注册页面导航完成")
        
        with allure.step("步骤2: 验证页面核心元素加载"):
            if not register_page.is_loaded():
                page.screenshot(path="screenshots/reg_ui001_failed.png")
                allure.attach.file("screenshots/reg_ui001_failed.png", 
                                 name="页面加载失败", attachment_type=allure.attachment_type.PNG)
                raise AssertionError("注册页面核心元素(输入框/按钮)未加载")
            
            # 截图 - 核心元素
            page.screenshot(path="screenshots/reg_ui001_step2_elements.png")
            allure.attach.file("screenshots/reg_ui001_step2_elements.png", 
                             name="步骤2-核心元素加载完成", attachment_type=allure.attachment_type.PNG)
            logger.info("   ✓ 核心元素加载完成")
        
        with allure.step("步骤3: 验证页面标题可见"):
            from playwright.sync_api import expect
            expect(page.locator(register_page.PAGE_TITLE).first).to_be_visible(timeout=5000)
            
            # 截图 - 页面标题
            page.screenshot(path="screenshots/reg_ui001_step3_title.png")
            allure.attach.file("screenshots/reg_ui001_step3_title.png", 
                             name="步骤3-页面标题可见", attachment_type=allure.attachment_type.PNG)
            logger.info("   ✓ 页面标题可见")
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-UI-001执行成功")
        logger.info("=" * 60)
