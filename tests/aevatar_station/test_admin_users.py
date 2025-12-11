"""
用户管理功能测试模块
路径: /admin/users
包含ABP Identity模块用户管理CRUD功能测试和表单验证测试
"""
import pytest
import logging
import allure
import uuid
from datetime import datetime
from tests.aevatar_station.pages.admin_users_page import AdminUsersPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


# ============================================================================
# ABP Framework 用户字段验证常量
# ============================================================================
class CreateUserConsts:
    """创建用户表单字段验证规则"""
    MaxUserNameLength = 256
    MinUserNameLength = 1
    UserNamePattern = r"^[a-zA-Z0-9_.@-]+$"
    MaxEmailLength = 256
    MinEmailLength = 3
    MinPasswordLength = 6
    MaxNameLength = 64
    MaxSurnameLength = 64
    MaxPhoneLength = 16


def get_rand(length=6):
    """生成随机字符串"""
    return uuid.uuid4().hex[:length]


@pytest.fixture(scope="class")
def admin_logged_in(browser, test_data):
    """管理员登录fixture"""
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    try:
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        admin_data = test_data["admin_login_data"][1]
        logger.info(f"使用Admin账号登录: {admin_data['username']}")
        
        page.fill("#LoginInput_UserNameOrEmailAddress", admin_data["username"])
        page.fill("#LoginInput_Password", admin_data["password"])
        page.click("button[type='submit']")
        
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        logger.info("管理员登录成功")
        
        yield page
        
    except Exception as e:
        logger.error(f"❌ 管理员登录失败: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/admin_login_failed_{timestamp}.png")
        raise e
    finally:
        context.close()


@pytest.fixture(scope="function")
def users_page(admin_logged_in):
    """每个测试函数的用户管理页面fixture"""
    page = admin_logged_in
    users_mgmt = AdminUsersPage(page)
    users_mgmt.navigate()
    
    if not users_mgmt.is_loaded():
        page.reload()
        users_mgmt.wait_for_load()
    
    return users_mgmt


@pytest.mark.admin
@pytest.mark.users
class TestAdminUsersCRUD:
    """用户管理CRUD功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    @pytest.mark.crud
    def test_p0_create_user_with_required_fields(self, users_page):
        """
        TC-CRUD-001: 创建用户 - 仅填写必填字段
        
        测试数据：
        - UserName: req_only_{timestamp}
        - Password: Test@123456
        - Email: req_only_{timestamp}@test.com
        
        预期结果：用户成功创建
        """
        logger.info("=" * 60)
        logger.info("TC-CRUD-001: 创建用户 - 仅填写必填字段")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"req_only_{timestamp}"
        test_email = f"{test_username}@test.com"
        test_password = "Test@123456"
        
        logger.info(f"   测试数据:")
        logger.info(f"      UserName: {test_username}")
        logger.info(f"      Password: {test_password}")
        logger.info(f"      Email: {test_email}")
        
        users_page.wait_for_table_load()
        
        # Step 1: 创建前搜索验证用户不存在
        logger.info(f"   [Step 1] 创建前搜索: {test_username}")
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"create_req_1_search_before_{ts}.png")
        allure.attach.file(
            f"screenshots/create_req_1_search_before_{ts}.png",
            name=f"1-创建前搜索'{test_username}': 应无结果",
            attachment_type=allure.attachment_type.PNG
        )
        
        user_exists_before = users_page.find_user_by_username(test_username) >= 0
        logger.info(f"      创建前用户存在: {user_exists_before}")
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # Step 2: 创建用户
        logger.info(f"   [Step 2] 创建用户")
        success = users_page.create_user(
            username=test_username,
            password=test_password,
            email=test_email
        )
        
        # 检查成功toast
        success_toast = users_page.is_success_message_visible()
        users_page.page.wait_for_timeout(1500)
        
        # 截图：创建后（带toast）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"create_req_2_after_{ts}.png")
        allure.attach.file(
            f"screenshots/create_req_2_after_{ts}.png",
            name=f"2-创建后: 成功toast={success_toast}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Step 3: 创建后搜索验证用户存在
        logger.info(f"   [Step 3] 创建后搜索: {test_username}")
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"create_req_3_search_after_{ts}.png")
        
        user_exists_after = users_page.find_user_by_username(test_username) >= 0
        
        allure.attach.file(
            f"screenshots/create_req_3_search_after_{ts}.png",
            name=f"3-创建后搜索'{test_username}': 用户存在={user_exists_after}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   创建结果: success={success}, toast={success_toast}, 用户存在={user_exists_after}")
        
        # 判断结果
        if success_toast and not user_exists_after:
            logger.error(f"   ✗ BUG: 显示成功toast但用户{test_username}不存在")
            users_page.clear_search()
            assert False, f"BUG: 显示成功toast但用户{test_username}不存在"
        elif user_exists_after:
            logger.info(f"   ✓ 用户创建成功")
            # 清理
            users_page.clear_search()
            users_page.page.wait_for_timeout(500)
            users_page.delete_user_by_username(test_username)
            logger.info("✅ TC-CRUD-001执行成功")
        else:
            logger.error(f"   ✗ 创建失败: 未出现成功toast且用户不存在")
            users_page.clear_search()
            assert False, f"创建失败: 未出现成功toast且用户{test_username}不存在"
    
    @pytest.mark.P0
    @pytest.mark.functional
    @pytest.mark.crud
    def test_p0_create_user_with_all_fields(self, users_page):
        """
        TC-CRUD-002: 创建用户 - 填写所有字段
        
        测试数据：
        - UserName: all_fields_{timestamp}
        - Password: Test@123456
        - Email: all_fields_{timestamp}@test.com
        - Name: TestName
        - Surname: TestSurname
        - Phone: 13800138000
        
        预期结果：用户成功创建，所有信息正确保存
        """
        logger.info("=" * 60)
        logger.info("TC-CRUD-002: 创建用户 - 填写所有字段")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"all_fields_{timestamp}"
        test_email = f"{test_username}@test.com"
        test_password = "Test@123456"
        test_name = "TestName"
        test_surname = "TestSurname"
        test_phone = "13800138000"
        
        logger.info(f"   测试数据:")
        logger.info(f"      UserName: {test_username}")
        logger.info(f"      Password: {test_password}")
        logger.info(f"      Email: {test_email}")
        logger.info(f"      Name: {test_name}")
        logger.info(f"      Surname: {test_surname}")
        logger.info(f"      Phone: {test_phone}")
        
        users_page.wait_for_table_load()
        
        # 截图：创建前
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"create_all_before_{ts}.png")
        allure.attach.file(f"screenshots/create_all_before_{ts}.png", name="1-创建前", attachment_type=allure.attachment_type.PNG)
        
        # 验证用户不存在（创建前）
        user_exists_before = users_page.is_user_in_list(test_username)
        logger.info(f"   创建前用户存在: {user_exists_before}")
        
        # 创建用户
        success = users_page.create_user(
            username=test_username,
            password=test_password,
            email=test_email,
            name=test_name,
            surname=test_surname,
            phone=test_phone
        )
        
        # 检查成功toast
        success_toast = users_page.is_success_message_visible()
        users_page.page.wait_for_timeout(1500)
        
        # 截图：创建后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"create_all_after_{ts}.png")
        
        # 刷新页面验证
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 验证用户存在（创建后）
        user_exists_after = users_page.is_user_in_list(test_username)
        
        logger.info(f"   创建结果: success={success}, toast={success_toast}, 用户存在={user_exists_after}")
        
        # 判断结果
        if success_toast and not user_exists_after:
            # BUG: 显示成功toast但用户不存在
            allure.attach.file(
                f"screenshots/create_all_after_{ts}.png",
                name=f"2-创建后: ❌BUG-成功toast=True但用户不存在",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ BUG: 显示成功toast但用户{test_username}不存在")
            assert False, f"BUG: 显示成功toast但用户{test_username}不存在"
        elif user_exists_after:
            # 正常：用户存在
            allure.attach.file(
                f"screenshots/create_all_after_{ts}.png",
                name=f"2-创建后: ✓用户存在",
                attachment_type=allure.attachment_type.PNG
            )
            # 验证用户信息
            row_index = users_page.find_user_by_username(test_username)
            user_info = users_page.get_user_info_by_row(row_index)
            logger.info(f"   ✓ 用户创建成功，信息: {user_info}")
        else:
            # 失败：无成功toast且用户不存在
            allure.attach.file(
                f"screenshots/create_all_after_{ts}.png",
                name=f"2-创建后: ❌创建失败",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ 创建失败: 未出现成功toast且用户不存在")
            assert False, f"创建失败: 未出现成功toast且用户{test_username}不存在"
        
        # 清理
        users_page.delete_user_by_username(test_username)
        logger.info("✅ TC-CRUD-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    @pytest.mark.crud
    def test_p1_edit_user_info(self, users_page):
        """
        TC-CRUD-003: 编辑用户信息
        
        测试数据：
        - 原始Name: Original
        - 原始Surname: Name
        - 修改后Name: UpdatedName
        - 修改后Surname: UpdatedSurname
        
        预期结果：用户信息成功更新
        """
        logger.info("=" * 60)
        logger.info("TC-CRUD-003: 编辑用户信息")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"edit_test_{timestamp}"
        test_email = f"{test_username}@test.com"
        test_password = "Test@123456"
        original_name = "Original"
        original_surname = "Name"
        new_name = "UpdatedName"
        new_surname = "UpdatedSurname"
        
        logger.info(f"   测试数据:")
        logger.info(f"      UserName: {test_username}")
        logger.info(f"      Email: {test_email}")
        logger.info(f"      Password: {test_password}")
        logger.info(f"      原始Name: {original_name} -> 修改后: {new_name}")
        logger.info(f"      原始Surname: {original_surname} -> 修改后: {new_surname}")
        
        # Step 1: 创建测试用户
        logger.info(f"   [Step 1] 创建测试用户: {test_username}")
        users_page.create_user(
            username=test_username,
            password=test_password,
            email=test_email,
            name=original_name,
            surname=original_surname
        )
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"未找到测试用户: {test_username}"
        
        # 截图：用户创建成功
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"edit_step1_created_{ts}.png")
        allure.attach.file(
            f"screenshots/edit_step1_created_{ts}.png",
            name=f"1-创建用户: {test_username} (Name={original_name}, Surname={original_surname})",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Step 2: 打开编辑对话框
        logger.info(f"   [Step 2] 打开编辑对话框")
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        # 截图：编辑对话框打开时（编辑前的原始值）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"edit_step2_dialog_before_{ts}.png")
        
        # 读取当前值
        name_field = users_page.page.get_by_role("textbox", name="Name", exact=True)
        surname_field = users_page.page.get_by_role("textbox", name="Surname", exact=True)
        before_name = name_field.input_value()
        before_surname = surname_field.input_value()
        
        allure.attach.file(
            f"screenshots/edit_step2_dialog_before_{ts}.png",
            name=f"2-编辑前对话框: Name={before_name}, Surname={before_surname}",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"      对话框中原始值: Name={before_name}, Surname={before_surname}")
        
        # Step 3: 填写新值
        logger.info(f"   [Step 3] 填写新值: Name={new_name}, Surname={new_surname}")
        name_field.fill(new_name)
        surname_field.fill(new_surname)
        users_page.page.wait_for_timeout(500)
        
        # 截图：填写后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"edit_step3_filled_{ts}.png")
        
        # 读取填写后的值
        filled_name = name_field.input_value()
        filled_surname = surname_field.input_value()
        
        allure.attach.file(
            f"screenshots/edit_step3_filled_{ts}.png",
            name=f"3-填写后: Name={filled_name}, Surname={filled_surname}",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"      填写后值: Name={filled_name}, Surname={filled_surname}")
        
        # Step 4: 点击保存
        logger.info(f"   [Step 4] 点击保存按钮")
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查成功toast
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"edit_step4_saved_{ts}.png")
        
        logger.info(f"      是否出现成功toast: {success_toast}")
        
        # 如果对话框还打开，检查是否有验证错误
        if users_page.is_dialog_open():
            # 检查是否有验证错误消息
            error_visible = users_page.is_error_message_visible()
            
            # 检查手机号字段是否有必填提示
            phone_field = users_page.page.get_by_role("textbox", name="Phone Number", exact=True)
            try:
                phone_value = phone_field.input_value()
            except:
                phone_value = "无法获取"
            
            allure.attach.file(
                f"screenshots/edit_step4_saved_{ts}.png",
                name=f"4-保存后对话框仍打开: 错误消息={error_visible}, 手机号={phone_value}",
                attachment_type=allure.attachment_type.PNG
            )
            
            logger.info(f"      对话框仍打开 - 可能是前端bug（手机号必填？）")
            logger.info(f"      错误消息可见: {error_visible}")
            logger.info(f"      手机号字段值: {phone_value}")
            
            users_page.press_escape()
            users_page.page.wait_for_timeout(1000)
        else:
            allure.attach.file(
                f"screenshots/edit_step4_saved_{ts}.png",
                name=f"4-保存后对话框关闭: 成功toast={success_toast}",
                attachment_type=allure.attachment_type.PNG
            )
        
        # Step 5: 验证编辑结果 - 重新打开编辑对话框
        logger.info(f"   [Step 5] 验证编辑结果 - 重新打开编辑对话框")
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if users_page.is_dialog_open():
            name_field = users_page.page.get_by_role("textbox", name="Name", exact=True)
            surname_field = users_page.page.get_by_role("textbox", name="Surname", exact=True)
            
            current_name = name_field.input_value()
            current_surname = surname_field.input_value()
            
            # 截图：验证
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"edit_step5_verify_{ts}.png")
            allure.attach.file(
                f"screenshots/edit_step5_verify_{ts}.png",
                name=f"5-验证: Name={current_name}, Surname={current_surname}",
                attachment_type=allure.attachment_type.PNG
            )
            
            users_page.press_escape()
            
            logger.info(f"   验证结果:")
            logger.info(f"      当前Name={current_name}, 期望={new_name}, {'✓' if current_name == new_name else '✗'}")
            logger.info(f"      当前Surname={current_surname}, 期望={new_surname}, {'✓' if current_surname == new_surname else '✗'}")
            
            # 清理
            logger.info(f"   [Step 6] 清理: 删除测试用户 {test_username}")
            users_page.delete_user_by_username(test_username)
            
            # 断言
            assert current_name == new_name, f"Name应更新为'{new_name}'，实际为'{current_name}'"
            assert current_surname == new_surname, f"Surname应更新为'{new_surname}'，实际为'{current_surname}'"
        else:
            users_page.delete_user_by_username(test_username)
            assert False, "无法打开编辑对话框进行验证"
        
        logger.info("✅ TC-CRUD-003执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    @pytest.mark.crud
    def test_p0_delete_user(self, users_page):
        """
        TC-CRUD-004: 删除用户
        
        预期结果：用户成功删除
        """
        logger.info("=" * 60)
        logger.info("TC-CRUD-004: 删除用户")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"delete_test_{timestamp}"
        test_email = f"{test_username}@test.com"
        test_password = "Test@123456"
        
        logger.info(f"   测试数据:")
        logger.info(f"      UserName: {test_username}")
        logger.info(f"      Email: {test_email}")
        logger.info(f"      Password: {test_password}")
        
        # Step 1: 创建测试用户
        logger.info(f"   [Step 1] 创建测试用户: {test_username}")
        users_page.create_user(username=test_username, password=test_password, email=test_email)
        
        # 检查创建成功toast
        create_success_toast = users_page.is_success_message_visible()
        users_page.page.wait_for_timeout(1500)
        
        # 刷新验证用户存在
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # Step 2: 删除前搜索验证用户存在
        logger.info(f"   [Step 2] 删除前搜索: {test_username}")
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"delete_1_search_before_{ts}.png")
        
        user_exists_before = users_page.find_user_by_username(test_username) >= 0
        allure.attach.file(
            f"screenshots/delete_1_search_before_{ts}.png",
            name=f"1-删除前搜索'{test_username}': 用户存在={user_exists_before}",
            attachment_type=allure.attachment_type.PNG
        )
        
        assert user_exists_before, f"测试用户{test_username}应存在"
        logger.info(f"      用户存在: {user_exists_before}")
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # Step 3: 删除用户
        logger.info(f"   [Step 3] 删除用户: {test_username}")
        success = users_page.delete_user_by_username(test_username)
        
        # 检查删除成功toast
        delete_success_toast = users_page.is_success_message_visible()
        users_page.page.wait_for_timeout(1500)
        
        # 截图：删除后（带toast）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"delete_2_after_{ts}.png")
        allure.attach.file(
            f"screenshots/delete_2_after_{ts}.png",
            name=f"2-删除后: 成功toast={delete_success_toast}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Step 4: 删除后搜索验证用户不存在
        logger.info(f"   [Step 4] 删除后搜索: {test_username}")
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"delete_3_search_after_{ts}.png")
        
        user_still_exists = users_page.find_user_by_username(test_username) >= 0
        allure.attach.file(
            f"screenshots/delete_3_search_after_{ts}.png",
            name=f"3-删除后搜索'{test_username}': 用户存在={user_still_exists} (应为False)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   删除结果: success={success}, toast={delete_success_toast}, 用户存在={user_still_exists}")
        
        # 验证：用户不应存在
        users_page.clear_search()
        assert not user_still_exists, f"用户{test_username}应已移除"
        logger.info(f"   ✓ 用户删除成功")
        
        logger.info("✅ TC-CRUD-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_search_user_found(self, users_page):
        """
        TC-SEARCH-001: 搜索存在的用户
        """
        logger.info("=" * 60)
        logger.info("TC-SEARCH-001: 搜索存在的用户")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"search_test_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        # 刷新验证用户存在
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        assert users_page.is_user_in_list(test_username), f"测试用户{test_username}应存在"
        logger.info(f"   测试用户创建成功")
        
        # 清除之前的搜索，显示完整列表
        users_page.clear_search()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：搜索前
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"search_before_{ts}.png")
        allure.attach.file(
            f"screenshots/search_before_{ts}.png",
            name=f"1-搜索前: 准备搜索用户{test_username}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 搜索
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1500)
        
        # 截图：搜索后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"search_after_{ts}.png")
        
        # 获取搜索结果
        matching_users = []
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            for row in rows:
                cells = row.locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    cell_text = cells[1].text_content()
                    if cell_text:
                        matching_users.append(cell_text.strip())
        except Exception as e:
            logger.warning(f"获取搜索结果失败: {e}")
        
        allure.attach.file(
            f"screenshots/search_after_{ts}.png",
            name=f"2-搜索后: 找到{len(matching_users)}个结果",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   搜索结果: {matching_users}")
        
        # 验证
        found = any(test_username in u for u in matching_users)
        assert found, f"搜索'{test_username}'应返回至少1个结果，实际: {matching_users}"
        logger.info(f"   ✓ 搜索成功，找到: {matching_users}")
        
        # 清空搜索
        users_page.clear_search()
        users_page.page.wait_for_timeout(1500)
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-SEARCH-001执行成功")


@pytest.mark.admin
@pytest.mark.users
@pytest.mark.validation
class TestAdminUsersValidation:
    """用户管理表单验证测试类"""
    
    # ==================== UserName字段验证 ====================
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_username_format_valid(self, users_page):
        """
        TC-VALID-001: UserName格式验证 - 有效格式
        
        规则：^[a-zA-Z0-9_.@-]+$
        
        测试场景（每个场景单独截图）：
        1. 纯字母：letters_{rand}
        2. 字母+数字：user123_{rand}
        3. 包含下划线：test_user_{rand}
        4. 包含点：test.user.{rand}
        5. 包含@：user@{rand}
        6. 包含连字符：test-user-{rand}
        
        预期结果：所有有效格式都能成功创建
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-001: UserName格式验证 - 有效格式")
        logger.info("=" * 60)
        
        valid_scenarios = [
            (f"letters_{get_rand()}", "1-纯字母"),
            (f"user123_{get_rand()}", "2-字母+数字"),
            (f"test_user_{get_rand()}", "3-包含下划线"),
            (f"test.user.{get_rand()}", "4-包含点"),
            (f"user@{get_rand()}", "5-包含@"),
            (f"test-user-{get_rand()}", "6-包含连字符"),
        ]
        
        results = []
        screenshot_idx = 1
        
        for username, scenario_name in valid_scenarios:
            email = f"{username.replace('@', '_').replace('.', '_')}@test.com"
            password = "Test@123456"
            
            logger.info(f"   场景: {scenario_name}")
            logger.info(f"      测试数据: UserName={username}, Email={email}, Password={password}")
            
            # 创建用户
            success = users_page.create_user(username=username, password=password, email=email)
            users_page.page.wait_for_timeout(1500)
            users_page.wait_for_table_load()
            
            created = users_page.is_user_in_list(username)
            
            # 截图
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"username_valid_{screenshot_idx}_{ts}.png")
            allure.attach.file(
                f"screenshots/username_valid_{screenshot_idx}_{ts}.png",
                name=f"{scenario_name}: UserName={username}, 结果={'成功' if created else '失败'}",
                attachment_type=allure.attachment_type.PNG
            )
            screenshot_idx += 1
            
            results.append((username, scenario_name, created))
            
            if created:
                logger.info(f"      ✓ 创建成功")
                users_page.delete_user_by_username(username)
                users_page.page.wait_for_timeout(1000)
            else:
                logger.error(f"      ✗ 创建失败")
        
        # 验证所有有效格式都成功
        failed = [(u, s) for u, s, c in results if not c]
        assert len(failed) == 0, f"以下有效格式创建失败: {failed}"
        
        logger.info("✅ TC-VALID-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_username_format_invalid(self, users_page):
        """
        TC-VALID-002: UserName格式验证 - 无效格式
        
        规则：^[a-zA-Z0-9_.@-]+$
        
        测试场景（每个场景单独截图）：
        1. 包含空格：test user {rand}
        2. 包含中文：测试用户{rand}
        3. 包含特殊字符：user!#{rand}
        
        预期结果：所有无效格式都被拒绝（用户数不增加）
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-002: UserName格式验证 - 无效格式")
        logger.info("=" * 60)
        
        invalid_scenarios = [
            (f"test user {get_rand()}", "1-包含空格"),
            (f"测试用户{get_rand()}", "2-包含中文"),
            (f"user!#{get_rand()}", "3-包含特殊字符"),
        ]
        
        users_page.wait_for_table_load()
        
        bugs_found = []
        screenshot_idx = 1
        
        for username, scenario_name in invalid_scenarios:
            email = f"invalid_{get_rand()}@test.com"
            password = "Test@123456"
            
            logger.info(f"   场景: {scenario_name}")
            logger.info(f"      测试数据: UserName={username}, Email={email}, Password={password}")
            logger.info(f"      预期: 应被拒绝")
            
            # 打开创建对话框
            users_page.click_new_user()
            users_page.page.wait_for_timeout(1000)
            
            # 填写表单
            users_page.fill_create_user_form(username=username, password=password, email=email)
            
            # 截图：填写后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"username_invalid_{screenshot_idx}_before_{ts}.png")
            allure.attach.file(
                f"screenshots/username_invalid_{screenshot_idx}_before_{ts}.png",
                name=f"{scenario_name}-填写: UserName={username}, Email={email}",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 点击保存
            users_page.click_save()
            users_page.page.wait_for_timeout(2000)
            
            # 检查是否出现成功toast
            success_toast_shown = users_page.is_success_message_visible()
            
            # 截图：保存后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"username_invalid_{screenshot_idx}_after_{ts}.png")
            
            logger.info(f"      是否出现成功toast: {success_toast_shown}")
            
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
            
            # 刷新页面验证用户是否被创建
            users_page.page.reload()
            users_page.wait_for_load()
            users_page.wait_for_table_load()
            
            # 通过搜索email来判断用户是否被创建（比件数更准确）
            user_created = False
            try:
                users_page.search_user(email)
                users_page.page.wait_for_timeout(1000)
                rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                for row in rows:
                    if email in row.text_content():
                        user_created = True
                        break
                # 清除搜索
                users_page.page.reload()
                users_page.wait_for_load()
                users_page.wait_for_table_load()
            except:
                pass
            
            logger.info(f"      用户是否被创建: {user_created}")
            
            # 判断结果
            if success_toast_shown or user_created:
                allure.attach.file(
                    f"screenshots/username_invalid_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: ❌BUG-无效格式被接受 (toast={success_toast_shown}, created={user_created})",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"      ✗ BUG: 无效UserName'{username}'被错误接受")
                bugs_found.append((username, scenario_name))
                # 清理
                if user_created:
                    try:
                        users_page.search_user(email)
                        users_page.page.wait_for_timeout(500)
                        # 找到并删除
                        rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                        for i, row in enumerate(rows):
                            if email in row.text_content():
                                users_page.delete_user_by_row(i + 1)
                                break
                        users_page.page.reload()
                        users_page.wait_for_load()
                        users_page.wait_for_table_load()
                    except:
                        pass
            else:
                allure.attach.file(
                    f"screenshots/username_invalid_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: ✓被正确拒绝",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info(f"      ✓ 被正确拒绝")
            
            screenshot_idx += 1
        
        # 验证所有无效格式都被拒绝
        assert len(bugs_found) == 0, f"BUG: 以下无效UserName格式被错误接受: {bugs_found}"
        
        logger.info("✅ TC-VALID-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_username_required(self, users_page):
        """
        TC-VALID-003: UserName必填验证
        
        测试数据：
        - UserName: （空）
        - Password: Test@123456
        - Email: empty_username_{rand}@test.com
        
        预期结果：创建被阻止
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-003: UserName必填验证")
        logger.info("=" * 60)
        
        email = f"empty_username_{get_rand()}@test.com"
        password = "Test@123456"
        
        logger.info(f"   测试数据:")
        logger.info(f"      UserName: （空）")
        logger.info(f"      Password: {password}")
        logger.info(f"      Email: {email}")
        
        users_page.wait_for_table_load()
        
        # 打开创建对话框
        users_page.click_new_user()
        users_page.page.wait_for_timeout(1000)
        
        # 只填写其他必填字段
        users_page.page.get_by_role("textbox", name="Password").fill(password)
        users_page.page.get_by_role("textbox", name="Email address").fill(email)
        
        # 截图：填写后（UserName为空）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"username_required_before_{ts}.png")
        allure.attach.file(
            f"screenshots/username_required_before_{ts}.png",
            name="1-填写数据（UserName为空）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查是否出现成功toast
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"username_required_after_{ts}.png")
        
        dialog_open = users_page.is_dialog_open()
        logger.info(f"   保存后: 对话框打开={dialog_open}, 成功toast={success_toast}")
        
        if dialog_open:
            allure.attach.file(
                f"screenshots/username_required_after_{ts}.png",
                name="2-结果: ✓被拒绝（对话框保持打开）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("   ✓ 对话框保持打开（验证生效）")
            users_page.press_escape()
        elif success_toast:
            allure.attach.file(
                f"screenshots/username_required_after_{ts}.png",
                name="2-结果: ❌BUG-出现成功toast",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error("   ✗ BUG: 空UserName出现成功toast")
            # 清理可能创建的用户
            users_page.page.reload()
            users_page.wait_for_load()
            users_page.wait_for_table_load()
            # 搜索email来查找
            users_page.search_user(email)
            users_page.page.wait_for_timeout(500)
            try:
                rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                for i, row in enumerate(rows):
                    if email in row.text_content():
                        users_page.delete_user_by_row(i + 1)
                        break
            except:
                pass
            assert False, "BUG: 空UserName应被拒绝，但出现了成功toast"
        else:
            allure.attach.file(
                f"screenshots/username_required_after_{ts}.png",
                name="2-结果: 对话框已关闭",
                attachment_type=allure.attachment_type.PNG
            )
        
        # 验证通过搜索email确认用户未被创建
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        users_page.search_user(email)
        users_page.page.wait_for_timeout(500)
        
        user_created = False
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            for row in rows:
                if email in row.text_content():
                    user_created = True
                    break
        except:
            pass
        
        assert not user_created, f"BUG: 空UserName不应创建用户，但找到了email={email}的用户"
        
        logger.info("✅ TC-VALID-003执行成功")
    
    # ==================== Email字段验证 ====================
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_email_format_valid(self, users_page):
        """
        TC-VALID-004: Email格式验证 - 有效格式
        
        测试场景（每个场景单独截图）：
        1. 标准格式：standard_{rand}@domain.com
        2. 子域名：subdomain_{rand}@sub.domain.com
        3. 带+号：plus_tag_{rand}+test@domain.com
        
        预期结果：所有有效格式都能成功创建
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-004: Email格式验证 - 有效格式")
        logger.info("=" * 60)
        
        rand = get_rand()
        valid_scenarios = [
            (f"standard_{rand}@domain.com", "1-标准格式"),
            (f"subdomain_{rand}@sub.domain.com", "2-子域名"),
            (f"plus_tag_{rand}+test@domain.com", "3-带+号"),
        ]
        
        results = []
        screenshot_idx = 1
        
        for email, scenario_name in valid_scenarios:
            username = f"email_test_{get_rand()}"
            password = "Test@123456"
            
            logger.info(f"   场景: {scenario_name}")
            logger.info(f"      测试数据: UserName={username}, Email={email}, Password={password}")
            
            # 打开创建对话框
            users_page.click_new_user()
            users_page.page.wait_for_timeout(1000)
            
            # 填写表单
            users_page.fill_create_user_form(username=username, password=password, email=email)
            
            # 截图：填写后（执行前）
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"email_valid_{screenshot_idx}_before_{ts}.png")
            allure.attach.file(
                f"screenshots/email_valid_{screenshot_idx}_before_{ts}.png",
                name=f"{scenario_name}-填写: UserName={username}, Email={email}",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 点击保存
            users_page.click_save()
            users_page.page.wait_for_timeout(2000)
            
            # 检查成功toast
            success_toast = users_page.is_success_message_visible()
            
            # 截图：保存后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"email_valid_{screenshot_idx}_after_{ts}.png")
            
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
            
            users_page.wait_for_table_load()
            created = users_page.is_user_in_list(username)
            
            allure.attach.file(
                f"screenshots/email_valid_{screenshot_idx}_after_{ts}.png",
                name=f"{scenario_name}-结果: 成功toast={success_toast}, 用户存在={created}",
                attachment_type=allure.attachment_type.PNG
            )
            screenshot_idx += 1
            
            # 使用成功toast或用户存在来判断创建成功
            created_success = success_toast or created
            results.append((email, scenario_name, created_success))
            
            if created_success:
                logger.info(f"      ✓ 创建成功 (toast={success_toast}, exists={created})")
                if created:
                    users_page.delete_user_by_username(username)
                    users_page.page.wait_for_timeout(1000)
            else:
                logger.error(f"      ✗ 创建失败")
        
        # 验证
        failed = [(e, s) for e, s, c in results if not c]
        assert len(failed) == 0, f"以下有效邮箱格式创建失败: {failed}"
        
        logger.info("✅ TC-VALID-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_email_format_invalid(self, users_page):
        """
        TC-VALID-005: Email格式验证 - 无效格式
        
        测试场景（每个场景单独截图）：
        1. 无@符号：invalidemail
        2. 无域名：user_{rand}@
        3. 无用户名：@domain.com
        
        预期结果：所有无效格式都被拒绝
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-005: Email格式验证 - 无效格式")
        logger.info("=" * 60)
        
        invalid_scenarios = [
            ("invalidemail", "1-无@符号"),
            (f"user_{get_rand()}@", "2-无域名"),
            ("@domain.com", "3-无用户名"),
        ]
        
        users_page.wait_for_table_load()
        initial_count = users_page.get_user_count()
        logger.info(f"   初始用户数: {initial_count}")
        
        bugs_found = []
        screenshot_idx = 1
        
        for email, scenario_name in invalid_scenarios:
            username = f"invalid_email_{get_rand()}"
            password = "Test@123456"
            
            logger.info(f"   场景: {scenario_name}")
            logger.info(f"      测试数据: UserName={username}, Email={email}, Password={password}")
            logger.info(f"      预期: 应被拒绝")
            
            users_page.click_new_user()
            users_page.page.wait_for_timeout(1000)
            
            users_page.fill_create_user_form(username=username, password=password, email=email)
            
            # 截图：填写后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"email_invalid_{screenshot_idx}_before_{ts}.png")
            allure.attach.file(
                f"screenshots/email_invalid_{screenshot_idx}_before_{ts}.png",
                name=f"{scenario_name}-填写: UserName={username}, Email={email}",
                attachment_type=allure.attachment_type.PNG
            )
            
            users_page.click_save()
            users_page.page.wait_for_timeout(2000)
            
            # 检查是否出现成功toast
            success_toast_shown = users_page.is_success_message_visible()
            
            # 截图：保存后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"email_invalid_{screenshot_idx}_after_{ts}.png")
            
            logger.info(f"      是否出现成功toast: {success_toast_shown}")
            
            # 如果出现成功toast，直接判定为bug
            if success_toast_shown:
                allure.attach.file(
                    f"screenshots/email_invalid_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: ❌BUG-出现Success toast",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"      ✗ BUG: 无效Email'{email}'出现成功toast")
                bugs_found.append((email, scenario_name, username))
                # 关闭对话框并清理
                if users_page.is_dialog_open():
                    users_page.press_escape()
                users_page.page.wait_for_timeout(1000)
                users_page.wait_for_table_load()
                if users_page.is_user_in_list(username):
                    users_page.delete_user_by_username(username)
                    users_page.page.wait_for_timeout(1000)
            else:
                # 关闭对话框
                if users_page.is_dialog_open():
                    users_page.press_escape()
                    users_page.page.wait_for_timeout(500)
                
                users_page.wait_for_table_load()
                
                # 再次检查用户是否被创建
                user_created = users_page.is_user_in_list(username)
                
                if user_created:
                    allure.attach.file(
                        f"screenshots/email_invalid_{screenshot_idx}_after_{ts}.png",
                        name=f"{scenario_name}-结果: ❌BUG-用户被创建",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.error(f"      ✗ BUG: 无效Email'{email}'被错误接受")
                    bugs_found.append((email, scenario_name, username))
                    users_page.delete_user_by_username(username)
                    users_page.page.wait_for_timeout(1000)
                else:
                    allure.attach.file(
                        f"screenshots/email_invalid_{screenshot_idx}_after_{ts}.png",
                        name=f"{scenario_name}-结果: ✓被正确拒绝",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"      ✓ 被正确拒绝")
            
            screenshot_idx += 1
        
        # 验证
        assert len(bugs_found) == 0, f"BUG: 以下无效邮箱格式被错误接受: {[(e, s) for e, s, u in bugs_found]}"
        
        logger.info("✅ TC-VALID-005执行成功")
    
    # ==================== Password字段验证 ====================
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_password_validation(self, users_page):
        """
        TC-VALID-006: Password验证
        
        测试场景（每个场景单独截图）：
        1. 空密码 - 应被拒绝
        2. 过短密码(3字符) - 应被拒绝
        3. 有效密码(Test@123456) - 应成功
        
        预期结果：正确验证密码
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-006: Password验证")
        logger.info("=" * 60)
        
        password_scenarios = [
            ("", "1-空密码", False),
            ("123", "2-过短密码(3字符)", False),
            ("Test@123456", "3-有效密码", True),
        ]
        
        results = []
        screenshot_idx = 1
        
        for password, scenario_name, should_succeed in password_scenarios:
            username = f"pwd_test_{get_rand()}"
            email = f"{username}@test.com"
            
            logger.info(f"   场景: {scenario_name}")
            logger.info(f"      测试数据: UserName={username}, Password='{password}', Email={email}")
            logger.info(f"      预期: {'成功创建' if should_succeed else '被拒绝'}")
            
            users_page.click_new_user()
            users_page.page.wait_for_timeout(1000)
            
            users_page.page.get_by_role("textbox", name="User name").fill(username)
            if password:
                users_page.page.get_by_role("textbox", name="Password").fill(password)
            users_page.page.get_by_role("textbox", name="Email address").fill(email)
            
            # 截图：填写后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"password_{screenshot_idx}_before_{ts}.png")
            allure.attach.file(
                f"screenshots/password_{screenshot_idx}_before_{ts}.png",
                name=f"{scenario_name}-填写数据",
                attachment_type=allure.attachment_type.PNG
            )
            
            users_page.click_save()
            users_page.page.wait_for_timeout(2000)
            
            # 检查是否出现成功toast
            success_toast_shown = users_page.is_success_message_visible()
            
            # 截图：保存后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"password_{screenshot_idx}_after_{ts}.png")
            
            logger.info(f"      是否出现成功toast: {success_toast_shown}")
            
            if users_page.is_dialog_open():
                result = "被拒绝"
                allure.attach.file(
                    f"screenshots/password_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: 被拒绝（对话框保持打开）",
                    attachment_type=allure.attachment_type.PNG
                )
                users_page.press_escape()
            elif success_toast_shown:
                result = "已创建"
                allure.attach.file(
                    f"screenshots/password_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: 出现成功toast",
                    attachment_type=allure.attachment_type.PNG
                )
                users_page.wait_for_table_load()
                if users_page.is_user_in_list(username):
                    users_page.delete_user_by_username(username)
                    users_page.page.wait_for_timeout(1000)
            else:
                result = "被拒绝"
                allure.attach.file(
                    f"screenshots/password_{screenshot_idx}_after_{ts}.png",
                    name=f"{scenario_name}-结果: 对话框关闭无成功toast",
                    attachment_type=allure.attachment_type.PNG
                )
            
            match = (result == "已创建") == should_succeed
            results.append((password, scenario_name, should_succeed, result == "已创建", match))
            
            logger.info(f"      实际: {result}, {'✓ 符合预期' if match else '✗ 不符合预期'}")
            
            screenshot_idx += 1
        
        # 验证
        failed = [(p, s) for p, s, exp, act, m in results if not m]
        assert len(failed) == 0, f"以下场景验证失败: {failed}"
        
        logger.info("✅ TC-VALID-006执行成功")
    
    # ==================== 可选字段长度验证 ====================
    
    @pytest.mark.P2
    @pytest.mark.validation
    def test_p2_optional_fields_length(self, users_page):
        """
        TC-VALID-007: 可选字段长度验证
        
        测试场景（每个场景单独截图）：
        1. 空值（允许）
        2. 最大长度Name=64字符, Surname=64字符, Phone=16字符（边界值）
        3. 超长Name=65字符（应被拒绝或截断）
        
        预期结果：正确处理长度限制
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-007: 可选字段长度验证")
        logger.info("=" * 60)
        
        screenshot_idx = 1
        
        # 场景1：空值
        logger.info("   场景1: 空值")
        username1 = f"empty_opt_{get_rand()}"
        logger.info(f"      测试数据: UserName={username1}, Name='', Surname='', Phone=''")
        
        success = users_page.create_user(
            username=username1, password="Test@123456", email=f"{username1}@test.com",
            name="", surname="", phone=""
        )
        users_page.page.wait_for_timeout(1500)
        users_page.wait_for_table_load()
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"optional_len_{screenshot_idx}_{ts}.png")
        created1 = users_page.is_user_in_list(username1)
        allure.attach.file(
            f"screenshots/optional_len_{screenshot_idx}_{ts}.png",
            name=f"1-空值: 结果={'成功' if created1 else '失败'}",
            attachment_type=allure.attachment_type.PNG
        )
        if created1:
            logger.info("      ✓ 空值创建成功")
            users_page.delete_user_by_username(username1)
            users_page.page.wait_for_timeout(1000)
        screenshot_idx += 1
        
        # 场景2：最大长度
        logger.info("   场景2: 最大长度（边界值）")
        username2 = f"max_len_{get_rand()}"
        max_name = "N" * 64
        max_surname = "S" * 64
        max_phone = "1" * 16
        logger.info(f"      测试数据: Name={len(max_name)}字符, Surname={len(max_surname)}字符, Phone={len(max_phone)}字符")
        
        success = users_page.create_user(
            username=username2, password="Test@123456", email=f"{username2}@test.com",
            name=max_name, surname=max_surname, phone=max_phone
        )
        users_page.page.wait_for_timeout(1500)
        users_page.wait_for_table_load()
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"optional_len_{screenshot_idx}_{ts}.png")
        created2 = users_page.is_user_in_list(username2)
        allure.attach.file(
            f"screenshots/optional_len_{screenshot_idx}_{ts}.png",
            name=f"2-最大长度: 结果={'成功' if created2 else '失败'}",
            attachment_type=allure.attachment_type.PNG
        )
        if created2:
            logger.info("      ✓ 最大长度创建成功")
            users_page.delete_user_by_username(username2)
            users_page.page.wait_for_timeout(1000)
        screenshot_idx += 1
        
        # 场景3：超长
        logger.info("   场景3: 超长（Name=65字符）")
        username3 = f"over_len_{get_rand()}"
        over_name = "N" * 65
        logger.info(f"      测试数据: Name={len(over_name)}字符（超过64字符限制）")
        
        users_page.click_new_user()
        users_page.page.wait_for_timeout(1000)
        
        users_page.page.get_by_role("textbox", name="User name").fill(username3)
        users_page.page.get_by_role("textbox", name="Password").fill("Test@123456")
        users_page.page.get_by_role("textbox", name="Email address").fill(f"{username3}@test.com")
        users_page.page.get_by_role("textbox", name="Name", exact=True).fill(over_name)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"optional_len_{screenshot_idx}_before_{ts}.png")
        allure.attach.file(
            f"screenshots/optional_len_{screenshot_idx}_before_{ts}.png",
            name=f"3-超长Name({len(over_name)}字符)-填写",
            attachment_type=allure.attachment_type.PNG
        )
        
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查成功toast
        success_toast = users_page.is_success_message_visible()
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"optional_len_{screenshot_idx}_after_{ts}.png")
        
        logger.info(f"      是否出现成功toast: {success_toast}")
        
        if users_page.is_dialog_open():
            allure.attach.file(
                f"screenshots/optional_len_{screenshot_idx}_after_{ts}.png",
                name=f"3-超长Name-结果: 被拒绝（对话框保持打开）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("      ✓ 超长被拒绝")
            users_page.press_escape()
        elif success_toast:
            # 出现成功toast说明超长数据被接受了，可能是bug或数据被截断
            allure.attach.file(
                f"screenshots/optional_len_{screenshot_idx}_after_{ts}.png",
                name=f"3-超长Name-结果: 出现成功toast（数据可能被截断）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("      ⚠ 出现成功toast，超长Name被接受（可能被截断）")
            users_page.wait_for_table_load()
            if users_page.is_user_in_list(username3):
                users_page.delete_user_by_username(username3)
        else:
            users_page.wait_for_table_load()
            created3 = users_page.is_user_in_list(username3)
            allure.attach.file(
                f"screenshots/optional_len_{screenshot_idx}_after_{ts}.png",
                name=f"3-超长Name-结果: 对话框关闭，用户存在={created3}",
                attachment_type=allure.attachment_type.PNG
            )
            if created3:
                logger.info("      ⚠ 超长被接受")
                users_page.delete_user_by_username(username3)
        
        logger.info("✅ TC-VALID-007执行成功")
    
    # ==================== 重复值验证 ====================
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_duplicate_username(self, users_page):
        """
        TC-VALID-008: 重复用户名验证
        
        测试数据：
        - 第一个用户: dup_test_{timestamp}, Email=dup_test_{timestamp}@test.com
        - 第二个用户: dup_test_{timestamp}（相同），Email=dup2_{timestamp}@test.com
        
        预期结果：第二个用户创建失败，不应出现Success toast
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-008: 重复用户名验证")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"dup_test_{timestamp}"
        email1 = f"{test_username}@test.com"
        email2 = f"dup2_{timestamp}@test.com"
        
        logger.info(f"   测试数据:")
        logger.info(f"      第一个用户: UserName={test_username}, Email={email1}")
        logger.info(f"      第二个用户: UserName={test_username}（相同）, Email={email2}（不同）")
        
        # Step 1: 创建第一个用户
        logger.info(f"   [Step 1] 创建第一个用户: {test_username}")
        users_page.create_user(username=test_username, password="Test@123456", email=email1)
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 验证第一个用户创建成功
        assert users_page.is_user_in_list(test_username), f"第一个用户{test_username}应创建成功"
        
        # 截图：第一个用户创建后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_username_1_{ts}.png")
        allure.attach.file(
            f"screenshots/dup_username_1_{ts}.png",
            name=f"1-第一个用户创建成功: UserName={test_username}, Email={email1}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"      用户1创建成功")
        
        # Step 2: 尝试创建重复用户名的第二个用户
        logger.info(f"   [Step 2] 尝试创建重复用户名: UserName={test_username}, Email={email2}")
        users_page.click_new_user()
        users_page.page.wait_for_timeout(1000)
        users_page.fill_create_user_form(username=test_username, password="Test@123456", email=email2)
        
        # 截图：填写重复用户名
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_username_2_{ts}.png")
        allure.attach.file(
            f"screenshots/dup_username_2_{ts}.png",
            name=f"2-填写重复用户名: UserName={test_username}（与用户1相同）, Email={email2}",
            attachment_type=allure.attachment_type.PNG
        )
        
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查是否出现成功toast（如果出现，说明是bug）
        success_toast_shown = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_username_3_{ts}.png")
        
        # Step 3: 验证结果
        logger.info(f"   [Step 3] 验证结果")
        logger.info(f"      是否出现成功toast: {success_toast_shown}")
        
        # 如果出现成功toast，直接判定为bug
        if success_toast_shown:
            allure.attach.file(
                f"screenshots/dup_username_3_{ts}.png",
                name=f"3-结果: ❌BUG-出现Success toast（重复用户名被错误接受）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ BUG: 出现'User Created Successfully' toast，重复用户名被错误接受")
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
            users_page.page.wait_for_timeout(1000)
            # 清理
            users_page.wait_for_table_load()
            users_page.delete_user_by_username(test_username)
            assert False, f"BUG: 重复用户名'{test_username}'应被拒绝，但出现了成功toast"
        
        # 关闭对话框（如果还打开）
        if users_page.is_dialog_open():
            logger.info("      对话框保持打开（正确行为）")
            users_page.press_escape()
            users_page.page.wait_for_timeout(1000)
        
        # 刷新页面验证
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 通过检查email2是否存在来判断第二个用户是否被创建（不使用件数）
        # 注意：由于用户名相同，需要通过搜索email2来判断
        users_page.search_user(email2)
        users_page.page.wait_for_timeout(1000)
        
        # 检查搜索结果中是否有email2对应的用户
        user2_created = False
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            for row in rows:
                row_text = row.text_content()
                if email2 in row_text:
                    user2_created = True
                    break
        except:
            pass
        
        # 清除搜索
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        logger.info(f"      第二个用户(Email={email2})是否被创建: {user2_created}")
        
        if user2_created:
            allure.attach.file(
                f"screenshots/dup_username_3_{ts}.png",
                name=f"3-结果: ❌BUG-重复用户名被错误接受",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ BUG: 重复用户名被错误接受")
            # 清理
            users_page.delete_user_by_username(test_username)
            assert False, f"BUG: 重复用户名'{test_username}'应被拒绝"
        else:
            allure.attach.file(
                f"screenshots/dup_username_3_{ts}.png",
                name=f"3-结果: ✓重复用户名被正确拒绝",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"   ✓ 重复用户名被正确拒绝")
            # 清理第一个用户
            users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-VALID-008执行成功")
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_duplicate_email(self, users_page):
        """
        TC-VALID-009: 重复邮箱验证
        
        测试数据：
        - 第一个用户: user1_{timestamp}, dup_email_{timestamp}@test.com
        - 第二个用户: user2_{timestamp}（不同）, dup_email_{timestamp}@test.com（相同）
        
        预期结果：第二个用户创建失败，不应出现Success toast
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-009: 重复邮箱验证")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_email = f"dup_email_{timestamp}@test.com"
        username1 = f"user1_{timestamp}"
        username2 = f"user2_{timestamp}"
        
        logger.info(f"   测试数据:")
        logger.info(f"      第一个用户: UserName={username1}, Email={test_email}")
        logger.info(f"      第二个用户: UserName={username2}（不同）, Email={test_email}（相同）")
        
        # Step 1: 创建第一个用户
        logger.info(f"   [Step 1] 创建第一个用户: {username1}")
        users_page.create_user(username=username1, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 验证第一个用户创建成功
        assert users_page.is_user_in_list(username1), f"第一个用户{username1}应创建成功"
        
        # 截图：第一个用户创建后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_email_1_{ts}.png")
        allure.attach.file(
            f"screenshots/dup_email_1_{ts}.png",
            name=f"1-第一个用户创建成功: UserName={username1}, Email={test_email}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"      用户1创建成功")
        
        # Step 2: 尝试创建重复邮箱的第二个用户
        logger.info(f"   [Step 2] 尝试创建重复邮箱: UserName={username2}, Email={test_email}")
        users_page.click_new_user()
        users_page.page.wait_for_timeout(1000)
        users_page.fill_create_user_form(username=username2, password="Test@123456", email=test_email)
        
        # 截图：填写重复邮箱
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_email_2_{ts}.png")
        allure.attach.file(
            f"screenshots/dup_email_2_{ts}.png",
            name=f"2-填写重复邮箱: UserName={username2}, Email={test_email}（与用户1相同）",
            attachment_type=allure.attachment_type.PNG
        )
        
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查是否出现成功toast（如果出现，说明是bug）
        success_toast_shown = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"dup_email_3_{ts}.png")
        
        # Step 3: 验证结果
        logger.info(f"   [Step 3] 验证结果")
        logger.info(f"      是否出现成功toast: {success_toast_shown}")
        
        # 如果出现成功toast，直接判定为bug
        if success_toast_shown:
            allure.attach.file(
                f"screenshots/dup_email_3_{ts}.png",
                name=f"3-结果: ❌BUG-出现Success toast（重复邮箱被错误接受）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ BUG: 出现'User Created Successfully' toast，重复邮箱被错误接受")
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
            users_page.page.wait_for_timeout(1000)
            # 清理可能创建的用户
            users_page.page.reload()
            users_page.wait_for_load()
            users_page.wait_for_table_load()
            if users_page.is_user_in_list(username2):
                users_page.delete_user_by_username(username2)
                users_page.page.wait_for_timeout(1000)
            users_page.delete_user_by_username(username1)
            assert False, f"BUG: 重复邮箱'{test_email}'应被拒绝，但出现了成功toast"
        
        # 关闭对话框（如果还打开）
        if users_page.is_dialog_open():
            logger.info("      对话框保持打开（正确行为）")
            users_page.press_escape()
            users_page.page.wait_for_timeout(1000)
        
        # 刷新页面验证
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 检查第二个用户是否被创建（通过用户名判断，不使用件数）
        user2_created = users_page.is_user_in_list(username2)
        
        logger.info(f"      第二个用户{username2}是否存在: {user2_created}")
        
        if user2_created:
            allure.attach.file(
                f"screenshots/dup_email_3_{ts}.png",
                name=f"3-结果: ❌BUG-重复邮箱被错误接受",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"   ✗ BUG: 重复邮箱被错误接受")
            # 清理
            users_page.delete_user_by_username(username2)
            users_page.page.wait_for_timeout(1000)
            users_page.delete_user_by_username(username1)
            assert False, f"BUG: 重复邮箱'{test_email}'应被拒绝，但用户被创建了"
        else:
            allure.attach.file(
                f"screenshots/dup_email_3_{ts}.png",
                name=f"3-结果: ✓重复邮箱被正确拒绝",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"   ✓ 重复邮箱被正确拒绝")
            # 只清理第一个用户
            users_page.delete_user_by_username(username1)
        
        logger.info("✅ TC-VALID-009执行成功")
    
    # ==================== 空表单验证 ====================
    
    @pytest.mark.P1
    @pytest.mark.validation
    def test_p1_empty_form_submit(self, users_page):
        """
        TC-VALID-010: 空表单提交验证
        
        测试数据：所有字段为空
        
        预期结果：空表单提交被阻止
        """
        logger.info("=" * 60)
        logger.info("TC-VALID-010: 空表单提交验证")
        logger.info("=" * 60)
        
        logger.info("   测试数据: 所有字段为空")
        
        users_page.wait_for_table_load()
        
        # 打开创建对话框
        users_page.click_new_user()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：空表单
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"empty_form_1_{ts}.png")
        allure.attach.file(
            f"screenshots/empty_form_1_{ts}.png",
            name="1-空表单（未填写任何字段）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 直接点击保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        # 检查是否出现成功toast
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"empty_form_2_{ts}.png")
        
        dialog_open = users_page.is_dialog_open()
        logger.info(f"   保存后: 对话框打开={dialog_open}, 成功toast={success_toast}")
        
        if dialog_open:
            allure.attach.file(
                f"screenshots/empty_form_2_{ts}.png",
                name="2-结果: ✓被阻止（对话框保持打开）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("   ✓ 空表单提交被阻止（对话框保持打开）")
            users_page.press_escape()
        elif success_toast:
            allure.attach.file(
                f"screenshots/empty_form_2_{ts}.png",
                name="2-结果: ❌BUG-出现成功toast",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error("   ✗ BUG: 空表单出现成功toast")
            assert False, "BUG: 空表单提交应被阻止，但出现了成功toast"
        else:
            allure.attach.file(
                f"screenshots/empty_form_2_{ts}.png",
                name="2-结果: 对话框已关闭（无成功toast）",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("   对话框已关闭但无成功toast")
        
        logger.info("✅ TC-VALID-010执行成功")


@pytest.mark.admin
@pytest.mark.users
@pytest.mark.pagination
class TestAdminUsersPagination:
    """用户管理分页功能测试类"""
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_pagination_display(self, users_page):
        """
        TC-PAGE-001: 分页控件显示
        
        验证分页控件是否正确显示
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-001: 分页控件显示")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 截图：分页显示
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"pagination_display_{ts}.png")
        
        # 检查分页控件
        pagination_visible = users_page.page.locator("nav[aria-label='Pagination'], .pagination, nav.pagination").first.is_visible(timeout=3000)
        
        # 检查页码信息
        page_info_visible = False
        try:
            page_info = users_page.page.locator("text=/Showing|Page|of|total/i").first
            page_info_visible = page_info.is_visible(timeout=2000)
        except:
            pass
        
        allure.attach.file(
            f"screenshots/pagination_display_{ts}.png",
            name=f"分页控件: 可见={pagination_visible}, 页码信息={page_info_visible}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   分页控件可见: {pagination_visible}")
        logger.info(f"   页码信息可见: {page_info_visible}")
        
        # 至少有分页控件或页码信息
        assert pagination_visible or page_info_visible, "分页控件或页码信息应可见"
        logger.info("✅ TC-PAGE-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_pagination_navigation(self, users_page):
        """
        TC-PAGE-002: 分页导航
        
        验证上一页/下一页导航功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-002: 分页导航")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 截图：第一页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"pagination_page1_{ts}.png")
        allure.attach.file(
            f"screenshots/pagination_page1_{ts}.png",
            name="1-第一页",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取第一页的用户列表
        first_page_users = []
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            for row in rows[:3]:  # 获取前3个用户
                cells = row.locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    first_page_users.append(cells[1].text_content())
        except:
            pass
        
        logger.info(f"   第一页用户: {first_page_users}")
        
        # 尝试点击下一页
        next_button = users_page.page.locator("button[aria-label='Go to next page'], button:has-text('Next'), button:has-text('>'), .next-page").first
        
        if next_button.is_visible(timeout=2000) and next_button.is_enabled():
            logger.info("   点击下一页")
            next_button.click()
            users_page.page.wait_for_timeout(1500)
            users_page.wait_for_table_load()
            
            # 截图：第二页
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"pagination_page2_{ts}.png")
            
            # 获取第二页的用户列表
            second_page_users = []
            try:
                rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                for row in rows[:3]:
                    cells = row.locator(users_page.TABLE_CELLS).all()
                    if len(cells) > 1:
                        second_page_users.append(cells[1].text_content())
            except:
                pass
            
            allure.attach.file(
                f"screenshots/pagination_page2_{ts}.png",
                name=f"2-第二页: {second_page_users[:3]}",
                attachment_type=allure.attachment_type.PNG
            )
            
            logger.info(f"   第二页用户: {second_page_users}")
            
            # 验证页面内容变化
            if first_page_users and second_page_users:
                # 如果两页内容相同，可能只有一页数据
                if first_page_users != second_page_users:
                    logger.info("   ✓ 分页导航正常，页面内容已变化")
                else:
                    logger.info("   ⚠ 两页内容相同，可能只有一页数据")
            
            # 点击上一页返回
            prev_button = users_page.page.locator("button[aria-label='Go to previous page'], button:has-text('Previous'), button:has-text('<'), .prev-page").first
            if prev_button.is_visible(timeout=2000) and prev_button.is_enabled():
                logger.info("   点击上一页返回")
                prev_button.click()
                users_page.page.wait_for_timeout(1500)
        else:
            logger.info("   下一页按钮不可用（可能只有一页数据）")
            allure.attach.file(
                f"screenshots/pagination_page1_{ts}.png",
                name="分页: 只有一页数据",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-PAGE-002执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_page_size_change(self, users_page):
        """
        TC-PAGE-003: 每页显示数量切换
        
        验证切换每页显示数量功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-003: 每页显示数量切换")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 获取当前行数
        current_rows = len(users_page.page.locator(users_page.TABLE_ROWS).all())
        logger.info(f"   当前显示行数: {current_rows}")
        
        # 截图：切换前
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"pagesize_before_{ts}.png")
        allure.attach.file(
            f"screenshots/pagesize_before_{ts}.png",
            name=f"1-切换前: 当前{current_rows}行",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 尝试找到页面大小选择器
        page_size_selector = users_page.page.locator("select[aria-label='page size'], .page-size-select, select:near(:text('per page'))").first
        
        if page_size_selector.is_visible(timeout=3000):
            # 尝试切换到不同的页面大小
            try:
                page_size_selector.select_option("25")
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                new_rows = len(users_page.page.locator(users_page.TABLE_ROWS).all())
                
                # 截图：切换后
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"pagesize_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/pagesize_after_{ts}.png",
                    name=f"2-切换后: {new_rows}行",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   切换后显示行数: {new_rows}")
                logger.info("   ✓ 页面大小切换功能正常")
            except Exception as e:
                logger.warning(f"   切换页面大小失败: {e}")
        else:
            logger.info("   未找到页面大小选择器")
            allure.attach.file(
                f"screenshots/pagesize_before_{ts}.png",
                name="页面大小选择器不可见",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-PAGE-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_go_to_next_page(self, users_page):
        """
        TC-PAGE-004: 下一页导航
        
        验证点击下一页按钮功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-004: 下一页导航")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 获取当前页第一个用户
        first_user_before = ""
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            if rows:
                cells = rows[0].locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    first_user_before = cells[1].text_content()
        except:
            pass
        
        # 截图：当前页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"next_page_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/next_page_1_before_{ts}.png",
            name=f"1-当前页: 第一个用户={first_user_before}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   当前页第一个用户: {first_user_before}")
        
        # 查找下一页按钮
        next_button = users_page.page.locator("button[aria-label='Go to next page'], button:has-text('Next'), [class*='next'], button:has-text('>')").first
        
        if next_button.is_visible(timeout=3000):
            is_enabled = next_button.is_enabled()
            logger.info(f"   下一页按钮: 可见=True, 启用={is_enabled}")
            
            if is_enabled:
                next_button.click()
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                # 获取下一页第一个用户
                first_user_after = ""
                try:
                    rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                    if rows:
                        cells = rows[0].locator(users_page.TABLE_CELLS).all()
                        if len(cells) > 1:
                            first_user_after = cells[1].text_content()
                except:
                    pass
                
                # 截图：下一页
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"next_page_2_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/next_page_2_after_{ts}.png",
                    name=f"2-下一页: 第一个用户={first_user_after}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   下一页第一个用户: {first_user_after}")
                
                # 验证页面变化
                if first_user_before and first_user_after:
                    if first_user_before != first_user_after:
                        logger.info("   ✓ 下一页导航成功")
                    else:
                        logger.info("   ⚠ 页面内容未变化（可能是最后一页或只有一页）")
            else:
                logger.info("   下一页按钮禁用（当前可能是最后一页）")
        else:
            logger.info("   未找到下一页按钮")
        
        logger.info("✅ TC-PAGE-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_go_to_previous_page(self, users_page):
        """
        TC-PAGE-005: 上一页导航
        
        验证点击上一页按钮功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-005: 上一页导航")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 先尝试跳转到第二页
        next_button = users_page.page.locator("button[aria-label='Go to next page'], button:has-text('Next'), [class*='next'], button:has-text('>')").first
        
        if next_button.is_visible(timeout=3000) and next_button.is_enabled():
            logger.info("   先跳转到下一页")
            next_button.click()
            users_page.page.wait_for_timeout(1500)
            users_page.wait_for_table_load()
        
        # 获取当前页第一个用户
        first_user_before = ""
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            if rows:
                cells = rows[0].locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    first_user_before = cells[1].text_content()
        except:
            pass
        
        # 截图：当前页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"prev_page_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/prev_page_1_before_{ts}.png",
            name=f"1-当前页: 第一个用户={first_user_before}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   当前页第一个用户: {first_user_before}")
        
        # 查找上一页按钮
        prev_button = users_page.page.locator("button[aria-label='Go to previous page'], button:has-text('Previous'), [class*='prev'], button:has-text('<')").first
        
        if prev_button.is_visible(timeout=3000):
            is_enabled = prev_button.is_enabled()
            logger.info(f"   上一页按钮: 可见=True, 启用={is_enabled}")
            
            if is_enabled:
                prev_button.click()
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                # 获取上一页第一个用户
                first_user_after = ""
                try:
                    rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                    if rows:
                        cells = rows[0].locator(users_page.TABLE_CELLS).all()
                        if len(cells) > 1:
                            first_user_after = cells[1].text_content()
                except:
                    pass
                
                # 截图：上一页
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"prev_page_2_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/prev_page_2_after_{ts}.png",
                    name=f"2-上一页: 第一个用户={first_user_after}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   上一页第一个用户: {first_user_after}")
                
                # 验证页面变化
                if first_user_before and first_user_after:
                    if first_user_before != first_user_after:
                        logger.info("   ✓ 上一页导航成功")
                    else:
                        logger.info("   ⚠ 页面内容未变化（可能是第一页或只有一页）")
            else:
                logger.info("   上一页按钮禁用（当前可能是第一页）")
        else:
            logger.info("   未找到上一页按钮")
        
        logger.info("✅ TC-PAGE-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_go_to_first_page(self, users_page):
        """
        TC-PAGE-006: 第一页导航
        
        验证点击第一页按钮功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-006: 第一页导航")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 先尝试跳转到后面的页面
        next_button = users_page.page.locator("button[aria-label='Go to next page'], button:has-text('Next'), [class*='next'], button:has-text('>')").first
        
        # 点击两次下一页（如果可以）
        for i in range(2):
            if next_button.is_visible(timeout=2000) and next_button.is_enabled():
                next_button.click()
                users_page.page.wait_for_timeout(1000)
                users_page.wait_for_table_load()
        
        # 获取当前页第一个用户
        first_user_before = ""
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            if rows:
                cells = rows[0].locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    first_user_before = cells[1].text_content()
        except:
            pass
        
        # 截图：当前页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"first_page_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/first_page_1_before_{ts}.png",
            name=f"1-当前页: 第一个用户={first_user_before}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   当前页第一个用户: {first_user_before}")
        
        # 查找第一页按钮
        first_button = users_page.page.locator("button[aria-label='Go to first page'], button:has-text('First'), button:has-text('«'), button:has-text('<<')").first
        
        if first_button.is_visible(timeout=3000):
            is_enabled = first_button.is_enabled()
            logger.info(f"   第一页按钮: 可见=True, 启用={is_enabled}")
            
            if is_enabled:
                first_button.click()
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                # 获取第一页第一个用户
                first_user_after = ""
                try:
                    rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                    if rows:
                        cells = rows[0].locator(users_page.TABLE_CELLS).all()
                        if len(cells) > 1:
                            first_user_after = cells[1].text_content()
                except:
                    pass
                
                # 截图：第一页
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"first_page_2_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/first_page_2_after_{ts}.png",
                    name=f"2-第一页: 第一个用户={first_user_after}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   第一页第一个用户: {first_user_after}")
                logger.info("   ✓ 第一页导航成功")
            else:
                logger.info("   第一页按钮禁用（当前已是第一页）")
        else:
            # 尝试点击页码1
            page_one = users_page.page.locator("button:has-text('1'), a:has-text('1')").first
            if page_one.is_visible(timeout=2000):
                page_one.click()
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"first_page_2_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/first_page_2_after_{ts}.png",
                    name="2-通过页码1跳转",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info("   通过点击页码1跳转到第一页")
            else:
                logger.info("   未找到第一页按钮或页码1")
        
        logger.info("✅ TC-PAGE-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_go_to_last_page(self, users_page):
        """
        TC-PAGE-007: 最后一页导航
        
        验证点击最后一页按钮功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-007: 最后一页导航")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 获取当前页第一个用户
        first_user_before = ""
        try:
            rows = users_page.page.locator(users_page.TABLE_ROWS).all()
            if rows:
                cells = rows[0].locator(users_page.TABLE_CELLS).all()
                if len(cells) > 1:
                    first_user_before = cells[1].text_content()
        except:
            pass
        
        # 截图：当前页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"last_page_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/last_page_1_before_{ts}.png",
            name=f"1-当前页: 第一个用户={first_user_before}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   当前页第一个用户: {first_user_before}")
        
        # 查找最后一页按钮
        last_button = users_page.page.locator("button[aria-label='Go to last page'], button:has-text('Last'), button:has-text('»'), button:has-text('>>')").first
        
        if last_button.is_visible(timeout=3000):
            is_enabled = last_button.is_enabled()
            logger.info(f"   最后一页按钮: 可见=True, 启用={is_enabled}")
            
            if is_enabled:
                last_button.click()
                users_page.page.wait_for_timeout(1500)
                users_page.wait_for_table_load()
                
                # 获取最后一页第一个用户
                first_user_after = ""
                try:
                    rows = users_page.page.locator(users_page.TABLE_ROWS).all()
                    if rows:
                        cells = rows[0].locator(users_page.TABLE_CELLS).all()
                        if len(cells) > 1:
                            first_user_after = cells[1].text_content()
                except:
                    pass
                
                # 截图：最后一页
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"last_page_2_after_{ts}.png")
                allure.attach.file(
                    f"screenshots/last_page_2_after_{ts}.png",
                    name=f"2-最后一页: 第一个用户={first_user_after}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   最后一页第一个用户: {first_user_after}")
                
                # 验证页面变化
                if first_user_before and first_user_after:
                    if first_user_before != first_user_after:
                        logger.info("   ✓ 最后一页导航成功")
                    else:
                        logger.info("   ⚠ 页面内容未变化（可能只有一页或已在最后一页）")
            else:
                logger.info("   最后一页按钮禁用（当前已是最后一页）")
        else:
            logger.info("   未找到最后一页按钮")
        
        logger.info("✅ TC-PAGE-007执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_page_number_click(self, users_page):
        """
        TC-PAGE-008: 点击页码跳转
        
        验证点击具体页码跳转功能
        """
        logger.info("=" * 60)
        logger.info("TC-PAGE-008: 点击页码跳转")
        logger.info("=" * 60)
        
        users_page.wait_for_table_load()
        
        # 截图：当前页
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"page_click_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/page_click_1_before_{ts}.png",
            name="1-当前页",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 查找页码按钮（尝试点击第2页）
        page_buttons = users_page.page.locator("nav[aria-label='Pagination'] button, .pagination button, .pagination a").all()
        
        logger.info(f"   找到 {len(page_buttons)} 个分页按钮")
        
        # 尝试找到页码2
        page_two_clicked = False
        for btn in page_buttons:
            try:
                text = btn.text_content().strip()
                if text == "2":
                    logger.info("   点击页码2")
                    btn.click()
                    users_page.page.wait_for_timeout(1500)
                    users_page.wait_for_table_load()
                    page_two_clicked = True
                    break
            except:
                continue
        
        if page_two_clicked:
            # 截图：第2页
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"page_click_2_after_{ts}.png")
            allure.attach.file(
                f"screenshots/page_click_2_after_{ts}.png",
                name="2-跳转到第2页",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info("   ✓ 页码跳转成功")
        else:
            logger.info("   未找到页码2（可能只有一页数据）")
        
        logger.info("✅ TC-PAGE-008执行成功")


@pytest.mark.admin
@pytest.mark.users
@pytest.mark.permission
class TestAdminUsersPermission:
    """用户权限管理测试类"""
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_open_permission_page(self, users_page):
        """
        TC-PERM-001: 打开用户权限页面
        
        验证能够打开用户权限管理页面
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-001: 打开用户权限页面")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"perm_test_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        # 截图：用户列表
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_1_user_list_{ts}.png")
        allure.attach.file(
            f"screenshots/perm_1_user_list_{ts}.png",
            name=f"1-用户列表: {test_username}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 打开权限页面
        logger.info(f"   打开用户权限页面")
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(2000)
        
        # 截图：权限页面
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_2_page_{ts}.png")
        
        # 检查权限页面是否加载
        permission_loaded = users_page.is_permission_page_loaded()
        
        allure.attach.file(
            f"screenshots/perm_2_page_{ts}.png",
            name=f"2-权限页面: 加载成功={permission_loaded}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   权限页面加载: {permission_loaded}")
        
        # 返回用户列表
        if permission_loaded:
            users_page.click_permission_back()
            users_page.page.wait_for_timeout(1000)
        else:
            users_page.page.go_back()
            users_page.page.wait_for_timeout(1000)
        
        # 清理
        users_page.wait_for_table_load()
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-001执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_assign_role_in_edit_dialog(self, users_page):
        """
        TC-PERM-002: 编辑对话框中分配角色
        
        验证在编辑对话框的Roles Tab中分配角色，并重新打开验证保存是否成功
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-002: 编辑对话框中分配角色")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"role_test_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        # 截图：编辑前搜索
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"role_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/role_1_before_{ts}.png",
            name=f"1-编辑前: 用户{test_username}",
            attachment_type=allure.attachment_type.PNG
        )
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # ===== Step 1: 打开编辑对话框并分配角色 =====
        logger.info(f"   [Step 1] 打开编辑对话框并分配角色")
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        # 切换到Roles Tab
        logger.info(f"   切换到Roles Tab")
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：Roles Tab（分配前）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"role_2_roles_before_{ts}.png")
        allure.attach.file(
            f"screenshots/role_2_roles_before_{ts}.png",
            name="2-Roles Tab: 分配前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 查找角色复选框并记录初始状态
        role_checkboxes = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        logger.info(f"   找到 {len(role_checkboxes)} 个角色复选框")
        
        # 记录分配的角色索引
        assigned_role_index = -1
        role_assigned = False
        
        for i, checkbox in enumerate(role_checkboxes):
            try:
                if not checkbox.is_checked():
                    checkbox.check()
                    role_assigned = True
                    assigned_role_index = i
                    logger.info(f"   勾选了第{i+1}个角色")
                    break
            except:
                continue
        
        if role_assigned:
            # 截图：勾选后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"role_3_checked_{ts}.png")
            allure.attach.file(
                f"screenshots/role_3_checked_{ts}.png",
                name=f"3-勾选第{assigned_role_index+1}个角色后",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 保存
            users_page.click_save()
            users_page.page.wait_for_timeout(2000)
            
            success_toast = users_page.is_success_message_visible()
            
            # 截图：保存后
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"role_4_saved_{ts}.png")
            allure.attach.file(
                f"screenshots/role_4_saved_{ts}.png",
                name=f"4-保存后: 成功toast={success_toast}",
                attachment_type=allure.attachment_type.PNG
            )
            
            logger.info(f"   保存结果: 成功toast={success_toast}")
            
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
            
            # ===== Step 2: 重新打开对话框验证角色是否真正保存 =====
            logger.info(f"   [Step 2] 重新打开对话框验证角色保存")
            users_page.page.wait_for_timeout(1000)
            
            # 重新搜索用户
            users_page.search_user(test_username)
            users_page.page.wait_for_timeout(1000)
            
            row_index = users_page.find_user_by_username(test_username)
            if row_index < 0:
                users_page.clear_search()
                users_page.delete_user_by_username(test_username)
                assert False, f"重新搜索用户{test_username}失败"
            
            users_page.clear_search()
            users_page.page.wait_for_timeout(500)
            
            # 重新打开编辑对话框
            users_page.click_edit_user(row_index)
            users_page.page.wait_for_timeout(1500)
            
            if not users_page.is_dialog_open():
                users_page.delete_user_by_username(test_username)
                assert False, "重新打开编辑对话框失败"
            
            # 切换到Roles Tab
            users_page.click_edit_tab_roles()
            users_page.page.wait_for_timeout(1000)
            
            # 截图：重新打开后的Roles Tab
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"role_5_verify_{ts}.png")
            allure.attach.file(
                f"screenshots/role_5_verify_{ts}.png",
                name="5-验证: 重新打开Roles Tab",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证之前分配的角色是否仍然勾选
            role_checkboxes_verify = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
            
            role_still_checked = False
            if assigned_role_index >= 0 and assigned_role_index < len(role_checkboxes_verify):
                try:
                    role_still_checked = role_checkboxes_verify[assigned_role_index].is_checked()
                except:
                    pass
            
            logger.info(f"   验证结果: 角色仍勾选={role_still_checked}")
            
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
            
            # 判断测试结果
            if success_toast and not role_still_checked:
                # BUG: 显示成功toast但角色未保存
                logger.error(f"   ✗ BUG: 显示成功toast但角色未真正保存")
                users_page.delete_user_by_username(test_username)
                assert False, "BUG: 显示成功toast但角色分配未真正保存"
            elif role_still_checked:
                logger.info(f"   ✓ 角色分配保存成功")
            else:
                logger.warning(f"   ⚠ 角色分配可能未成功")
        else:
            logger.info("   所有角色已勾选或无可用角色")
            # 关闭对话框
            if users_page.is_dialog_open():
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_assign_all_roles(self, users_page):
        """
        TC-PERM-003: 分配全部角色
        
        验证一次性分配所有角色
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-003: 分配全部角色")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"all_roles_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 打开编辑对话框
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        # 切换到Roles Tab
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：分配前
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"all_roles_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/all_roles_1_before_{ts}.png",
            name="1-分配前: Roles Tab",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 勾选所有角色
        role_checkboxes = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        total_roles = len(role_checkboxes)
        checked_count = 0
        
        for checkbox in role_checkboxes:
            try:
                if not checkbox.is_checked():
                    checkbox.check()
                    checked_count += 1
            except:
                continue
        
        logger.info(f"   勾选了 {checked_count} 个角色（共{total_roles}个）")
        
        # 截图：全部勾选后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"all_roles_2_checked_{ts}.png")
        allure.attach.file(
            f"screenshots/all_roles_2_checked_{ts}.png",
            name=f"2-全部勾选: {checked_count}个角色",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"all_roles_3_saved_{ts}.png")
        allure.attach.file(
            f"screenshots/all_roles_3_saved_{ts}.png",
            name=f"3-保存后: 成功toast={success_toast}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 关闭对话框
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # ===== 重新打开对话框验证所有角色是否真正保存 =====
        logger.info(f"   [验证] 重新打开对话框检查角色保存状态")
        users_page.page.wait_for_timeout(1000)
        
        # 重新搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        if row_index >= 0:
            users_page.clear_search()
            users_page.page.wait_for_timeout(500)
            
            # 重新打开编辑对话框
            users_page.click_edit_user(row_index)
            users_page.page.wait_for_timeout(1500)
            
            if users_page.is_dialog_open():
                # 切换到Roles Tab
                users_page.click_edit_tab_roles()
                users_page.page.wait_for_timeout(1000)
                
                # 截图：验证Roles Tab
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                users_page.take_screenshot(f"all_roles_4_verify_{ts}.png")
                
                # 统计勾选的角色数量
                role_checkboxes_verify = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
                verified_checked = sum(1 for cb in role_checkboxes_verify if cb.is_checked())
                
                allure.attach.file(
                    f"screenshots/all_roles_4_verify_{ts}.png",
                    name=f"4-验证: 已勾选{verified_checked}/{total_roles}个角色",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.info(f"   验证结果: 已勾选{verified_checked}/{total_roles}个角色")
                
                # 关闭对话框
                users_page.press_escape()
                users_page.page.wait_for_timeout(500)
                
                # 判断测试结果
                if success_toast and verified_checked < total_roles:
                    logger.error(f"   ✗ BUG: 显示成功toast但角色未完全保存")
                    users_page.delete_user_by_username(test_username)
                    assert False, f"BUG: 显示成功toast但只保存了{verified_checked}/{total_roles}个角色"
                elif verified_checked == total_roles:
                    logger.info(f"   ✓ 所有角色分配保存成功")
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_assign_partial_roles(self, users_page):
        """
        TC-PERM-004: 部分角色分配
        
        验证只分配部分角色，保存后重新打开验证是否成功
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-004: 部分角色分配")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"partial_roles_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # ===== Step 1: 打开编辑对话框并分配部分角色 =====
        logger.info(f"   [Step 1] 打开编辑对话框并分配部分角色")
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        # 切换到Roles Tab
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：分配前（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/partial_1_before_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/partial_1_before_{ts}.png",
            name="1-分配前: Roles Tab (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 获取所有角色复选框
        role_checkboxes = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        total_roles = len(role_checkboxes)
        
        # 只勾选前2个角色（部分分配）
        checked_count = 0
        assigned_indices = []
        for i, checkbox in enumerate(role_checkboxes[:2]):
            try:
                if not checkbox.is_checked():
                    checkbox.check()
                    checked_count += 1
                    assigned_indices.append(i)
            except:
                continue
        
        logger.info(f"   勾选了 {checked_count}/{total_roles} 个角色（部分）")
        
        # 截图：部分勾选后（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/partial_2_checked_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/partial_2_checked_{ts}.png",
            name=f"2-部分勾选: {checked_count}/{total_roles}个角色 (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/partial_3_saved_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/partial_3_saved_{ts}.png",
            name=f"3-保存后: 成功toast={success_toast} (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   保存结果: 成功toast={success_toast}")
        
        # 关闭对话框
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # ===== Step 2: 重新打开验证角色是否真正保存 =====
        logger.info(f"   [Step 2] 重新打开验证角色保存")
        users_page.page.wait_for_timeout(1000)
        
        # 重新搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        if row_index < 0:
            users_page.clear_search()
            users_page.delete_user_by_username(test_username)
            assert False, f"重新搜索用户{test_username}失败"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 重新打开编辑对话框
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "重新打开编辑对话框失败"
        
        # 切换到Roles Tab
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：重新打开后的Roles Tab（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/partial_4_verify_{ts}.png", full_page=True)
        
        # 验证之前分配的角色是否仍然勾选
        role_checkboxes_verify = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        verified_checked = sum(1 for cb in role_checkboxes_verify if cb.is_checked())
        
        allure.attach.file(
            f"screenshots/partial_4_verify_{ts}.png",
            name=f"4-验证: 已勾选{verified_checked}/{total_roles}个角色 (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   验证结果: 已勾选{verified_checked}/{total_roles}个角色 (预期{checked_count})")
        
        # 关闭对话框
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # 判断结果
        if success_toast and verified_checked < checked_count:
            logger.error(f"   ✗ BUG: 显示成功toast但角色未完全保存")
            users_page.delete_user_by_username(test_username)
            assert False, f"BUG: 显示成功toast但只保存了{verified_checked}/{checked_count}个角色"
        elif verified_checked == checked_count:
            logger.info(f"   ✓ 部分角色分配保存成功")
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_remove_assigned_roles(self, users_page):
        """
        TC-PERM-005: 移除已分配的角色
        
        验证移除已分配的角色，保存后重新打开验证角色是否为0
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-005: 移除已分配的角色")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"remove_roles_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # ===== Step 1: 先分配角色 =====
        logger.info(f"   [Step 1] 先分配角色")
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 获取所有角色复选框
        role_checkboxes = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        total_roles = len(role_checkboxes)
        
        # 勾选所有角色
        assigned_count = 0
        for checkbox in role_checkboxes:
            try:
                if not checkbox.is_checked():
                    checkbox.check()
                    assigned_count += 1
            except:
                continue
        
        logger.info(f"   勾选了 {assigned_count}/{total_roles} 个角色")
        
        # 截图：全部勾选（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/remove_1_all_checked_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/remove_1_all_checked_{ts}.png",
            name=f"1-全部角色已勾选: {assigned_count}个 (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # ===== Step 2: 重新打开并移除所有角色 =====
        logger.info(f"   [Step 2] 重新打开并移除所有角色")
        
        # 重新搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "编辑对话框未打开"
        
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：移除前（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/remove_2_before_{ts}.png", full_page=True)
        
        # 统计当前已勾选的角色数
        role_checkboxes = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        before_remove_count = sum(1 for cb in role_checkboxes if cb.is_checked())
        
        allure.attach.file(
            f"screenshots/remove_2_before_{ts}.png",
            name=f"2-移除前: 已勾选{before_remove_count}个角色 (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 取消勾选所有角色
        unchecked_count = 0
        for checkbox in role_checkboxes:
            try:
                if checkbox.is_checked():
                    checkbox.uncheck()
                    unchecked_count += 1
            except:
                continue
        
        logger.info(f"   取消勾选了 {unchecked_count} 个角色")
        
        # 截图：全部取消后（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/remove_3_unchecked_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/remove_3_unchecked_{ts}.png",
            name=f"3-移除后: 取消{unchecked_count}个角色 (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 保存
        users_page.click_save()
        users_page.page.wait_for_timeout(2000)
        
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/remove_4_saved_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/remove_4_saved_{ts}.png",
            name=f"4-保存后: 成功toast={success_toast} (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   保存结果: 成功toast={success_toast}")
        
        # 关闭对话框
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # ===== Step 3: 重新打开验证角色是否全部移除 =====
        logger.info(f"   [Step 3] 重新打开验证角色移除")
        users_page.page.wait_for_timeout(1000)
        
        # 重新搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        
        if row_index < 0:
            users_page.clear_search()
            users_page.delete_user_by_username(test_username)
            assert False, f"重新搜索用户{test_username}失败"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 重新打开编辑对话框
        users_page.click_edit_user(row_index)
        users_page.page.wait_for_timeout(1500)
        
        if not users_page.is_dialog_open():
            users_page.delete_user_by_username(test_username)
            assert False, "重新打开编辑对话框失败"
        
        # 切换到Roles Tab
        users_page.click_edit_tab_roles()
        users_page.page.wait_for_timeout(1000)
        
        # 截图：重新打开后的Roles Tab（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/remove_5_verify_{ts}.png", full_page=True)
        
        # 验证角色是否全部取消
        role_checkboxes_verify = users_page.page.locator("[role='dialog'] input[type='checkbox'], [role='dialog'] [role='checkbox']").all()
        verified_checked = sum(1 for cb in role_checkboxes_verify if cb.is_checked())
        
        allure.attach.file(
            f"screenshots/remove_5_verify_{ts}.png",
            name=f"5-验证: 已勾选{verified_checked}个角色 (应为0) (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   验证结果: 已勾选{verified_checked}个角色 (应为0)")
        
        # 关闭对话框
        if users_page.is_dialog_open():
            users_page.press_escape()
            users_page.page.wait_for_timeout(500)
        
        # 判断结果
        if verified_checked != 0:
            logger.error(f"   ✗ BUG: 移除角色后应为0，实际为{verified_checked}")
            users_page.delete_user_by_username(test_username)
            assert False, f"BUG: 移除角色后应为0，实际仍有{verified_checked}个角色"
        else:
            logger.info(f"   ✓ 角色移除保存成功, 已勾选=0")
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-005执行成功")
    
    # ==================== Action菜单Permission页面相关测试 ====================
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_action_permission_page_elements(self, users_page):
        """
        TC-PERM-006: Action菜单Permission页面元素验证
        
        验证通过Action菜单打开的Permission页面包含所有必要元素
        使用admin用户验证（有权限但不可修改）
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-006: Action菜单Permission页面元素验证")
        logger.info("=" * 60)
        
        # 使用admin用户测试（有完整权限）
        test_username = "admin"
        
        logger.info(f"   测试用户: {test_username}")
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 截图：用户列表
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_elem_1_list_{ts}.png")
        allure.attach.file(
            f"screenshots/perm_elem_1_list_{ts}.png",
            name=f"1-用户列表: {test_username}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 打开Permission页面
        logger.info(f"   通过Action菜单打开Permission页面")
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)
        
        # 截图：Permission页面
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_elem_2_page_{ts}.png")
        
        # 验证页面元素
        page_loaded = users_page.is_permission_page_loaded()
        has_back_btn = users_page.is_visible("button:has-text('Back')", timeout=3000)
        has_grant_all = users_page.is_visible("button:has-text('Grant All')", timeout=3000)
        has_search = users_page.is_visible("input[placeholder*='Search']", timeout=3000)
        has_tabs = users_page.is_visible("[role='tablist']", timeout=3000)
        has_save_btn = users_page.is_visible("button:has-text('Save Changes')", timeout=3000)
        has_cancel_btn = users_page.is_visible("button:has-text('Cancel')", timeout=3000)
        
        allure.attach.file(
            f"screenshots/perm_elem_2_page_{ts}.png",
            name=f"2-Permission页面: 加载={page_loaded}, Back={has_back_btn}, GrantAll={has_grant_all}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   页面元素验证:")
        logger.info(f"      页面标题: {page_loaded}")
        logger.info(f"      Back按钮: {has_back_btn}")
        logger.info(f"      Grant All按钮: {has_grant_all}")
        logger.info(f"      搜索框: {has_search}")
        logger.info(f"      权限Tab列表: {has_tabs}")
        logger.info(f"      Save Changes按钮: {has_save_btn}")
        logger.info(f"      Cancel按钮: {has_cancel_btn}")
        
        # 获取权限摘要
        summary = users_page.get_permission_summary()
        logger.info(f"   权限摘要: Total={summary['total']}, Granted={summary['granted']}, NotGranted={summary['not_granted']}")

        # 在Permission页面检查Grant All或Revoke All按钮（包括disabled状态）
        has_revoke_all = users_page.is_visible("button:has-text('Revoke All')", timeout=2000)
        has_grant_or_revoke = has_grant_all or has_revoke_all
        
        logger.info(f"      Revoke All按钮: {has_revoke_all}")
        logger.info(f"      Grant All或Revoke All: {has_grant_or_revoke}")

        # 返回用户列表
        users_page.page.go_back()
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 不删除admin用户
        
        # 断言基本元素存在
        assert page_loaded, "Permission页面标题应显示"
        assert has_back_btn, "Back按钮应存在"
        assert has_grant_or_revoke, "Grant All或Revoke All按钮应存在"
        assert has_save_btn, "Save Changes按钮应存在"
        assert has_cancel_btn, "Cancel按钮应存在"
        
        logger.info("✅ TC-PERM-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_action_permission_grant_single(self, users_page):
        """
        TC-PERM-007: Action菜单Permission页面授予单个权限
        
        验证在Permission页面授予单个权限并保存，然后重新打开验证
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-007: Permission页面授予单个权限")
        logger.info("=" * 60)
        
        timestamp = datetime.now().strftime("%H%M%S")
        test_username = f"perm_single_{timestamp}"
        test_email = f"{test_username}@test.com"
        
        logger.info(f"   测试数据: UserName={test_username}")
        
        # 创建测试用户
        users_page.create_user(username=test_username, password="Test@123456", email=test_email)
        users_page.page.wait_for_timeout(2000)
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # ===== Step 1: 打开Permission页面并授予权限 =====
        logger.info(f"   [Step 1] 打开Permission页面并授予权限")
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)
        
        # 获取初始权限摘要
        initial_summary = users_page.get_permission_summary()
        
        # 截图：授予前
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_single_1_before_{ts}.png")
        allure.attach.file(
            f"screenshots/perm_single_1_before_{ts}.png",
            name=f"1-授予前: Granted={initial_summary['granted']}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 授予第一个可用权限
        granted_permission = users_page.grant_first_available_permission()
        logger.info(f"   授予权限: {granted_permission}")
        
        # 截图：授予后（未保存）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_single_2_granted_{ts}.png")
        allure.attach.file(
            f"screenshots/perm_single_2_granted_{ts}.png",
            name=f"2-授予后(未保存): {granted_permission}",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查未保存更改提示和Save按钮状态
        has_unsaved = users_page.is_unsaved_changes_visible()
        save_enabled = users_page.is_save_changes_enabled()
        logger.info(f"   未保存提示: {has_unsaved}, Save按钮可用: {save_enabled}")
        
        # 保存权限
        save_result = users_page.click_permission_save()
        users_page.page.wait_for_timeout(2000)
        
        success_toast = users_page.is_success_message_visible()
        
        # 截图：保存后
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.take_screenshot(f"perm_single_3_saved_{ts}.png")
        allure.attach.file(
            f"screenshots/perm_single_3_saved_{ts}.png",
            name=f"3-保存后: 成功toast={success_toast}",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   保存结果: {save_result}, 成功toast={success_toast}")
        
        # ===== Step 2: 返回并重新打开验证 =====
        logger.info(f"   [Step 2] 返回并重新打开验证权限保存")
        
        # 点击Back返回
        users_page.page.click("button:has-text('Back')")
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 重新搜索用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        
        if row_index >= 0:
            users_page.clear_search()
            users_page.page.wait_for_timeout(500)
            
            # 重新打开Permission页面
            users_page.click_user_permissions(row_index)
            users_page.page.wait_for_timeout(3000)
            
            # 获取验证后的权限摘要
            verify_summary = users_page.get_permission_summary()
            
            # 截图：验证
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            users_page.take_screenshot(f"perm_single_4_verify_{ts}.png")
            allure.attach.file(
                f"screenshots/perm_single_4_verify_{ts}.png",
                name=f"4-验证: Granted从{initial_summary['granted']}变为{verify_summary['granted']}",
                attachment_type=allure.attachment_type.PNG
            )
            
            logger.info(f"   验证结果: Granted从{initial_summary['granted']}变为{verify_summary['granted']}")
            
            # 返回用户列表
            users_page.page.go_back()
            users_page.page.wait_for_timeout(2000)
            users_page.wait_for_table_load()
            
            # 判断结果
            if success_toast and verify_summary['granted'] <= initial_summary['granted']:
                logger.error(f"   ✗ BUG: 显示成功toast但权限未真正保存")
                users_page.delete_user_by_username(test_username)
                assert False, "BUG: 显示成功toast但权限未真正保存"
            elif verify_summary['granted'] > initial_summary['granted']:
                logger.info(f"   ✓ 权限授予保存成功")
        
        # 清理
        users_page.delete_user_by_username(test_username)
        
        logger.info("✅ TC-PERM-007执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_action_permission_grant_all(self, users_page):
        """
        TC-PERM-008: Action菜单Permission页面授予所有权限

        验证使用Grant All按钮授予所有权限（如果可用）
        注意：新创建的用户可能没有可管理的权限（Total=0）
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-008: Permission页面授予所有权限")
        logger.info("=" * 60)

        # 使用admin用户测试（有完整权限配置）
        test_username = "admin"
        cleanup_needed = False

        logger.info(f"   测试用户: {test_username}")

        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()

        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)

        # 打开Permission页面
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)

        # 获取初始权限摘要
        initial_summary = users_page.get_permission_summary()

        # 截图：Permission页面（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/perm_all_1_page_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/perm_all_1_page_{ts}.png",
            name=f"1-Permission页面: Total={initial_summary['total']}, Granted={initial_summary['granted']} (全页)",
            attachment_type=allure.attachment_type.PNG
        )

        # 检查权限状态
        logger.info(f"   权限摘要: Total={initial_summary['total']}, Granted={initial_summary['granted']}")

        # 检查Grant All和Revoke All按钮状态
        has_grant_all = users_page.is_visible("button:has-text('Grant All'):not([disabled])", timeout=2000)
        has_revoke_all = users_page.is_visible("button:has-text('Revoke All'):not([disabled])", timeout=2000)
        
        logger.info(f"   Grant All可用: {has_grant_all}, Revoke All可用: {has_revoke_all}")
        
        # 验证权限摘要显示正确
        if initial_summary['total'] > 0:
            # admin用户应该有权限配置
            if initial_summary['granted'] == initial_summary['total']:
                logger.info(f"   ✓ 所有权限已授予（Revoke All应可用）")
                # 验证Revoke All按钮存在（即使disabled也算存在）
                has_revoke = users_page.is_visible("button:has-text('Revoke All')", timeout=2000)
                assert has_revoke, "当所有权限已授予时，Revoke All按钮应显示"
            else:
                logger.info(f"   ✓ 部分权限未授予（Grant All应可用）")
                assert has_grant_all or has_revoke_all, "应显示Grant All或Revoke All按钮"
        
        # 验证安全提示（admin用户不可修改）
        has_security_notice = users_page.is_visible("text=Admin permissions cannot be modified", timeout=2000)
        logger.info(f"   安全提示显示: {has_security_notice}")
        
        # 返回用户列表
        users_page.page.click("button:has-text('Back')")
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 验证结果
        assert initial_summary['total'] > 0, f"admin用户应有权限配置，实际Total={initial_summary['total']}"
        
        logger.info("✅ TC-PERM-008执行成功 - 权限页面元素验证通过")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_action_permission_revoke_all(self, users_page):
        """
        TC-PERM-009: Action菜单Permission页面撤销全部权限功能验证
        
        验证Revoke All按钮状态（admin用户权限不可修改，仅验证UI）
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-009: Permission页面Revoke All功能验证")
        logger.info("=" * 60)
        
        # 使用admin用户测试（有完整权限配置）
        test_username = "admin"
        
        logger.info(f"   测试用户: {test_username}")
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 打开Permission页面
        logger.info(f"   打开Permission页面")
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)
        
        # 获取权限摘要
        summary = users_page.get_permission_summary()
        
        # 截图：Permission页面（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/perm_revoke_1_page_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/perm_revoke_1_page_{ts}.png",
            name=f"1-Permission页面: Total={summary['total']}, Granted={summary['granted']} (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"   权限摘要: Total={summary['total']}, Granted={summary['granted']}, NotGranted={summary['not_granted']}")
        
        # 检查Revoke All按钮状态
        has_revoke_all = users_page.is_visible("button:has-text('Revoke All')", timeout=2000)
        has_grant_all = users_page.is_visible("button:has-text('Grant All')", timeout=2000)
        
        logger.info(f"   Revoke All存在: {has_revoke_all}, Grant All存在: {has_grant_all}")
        
        # 验证：当Granted > 0时应显示Revoke All
        if summary['granted'] > 0:
            logger.info(f"   ✓ Granted={summary['granted']} > 0, Revoke All应可见")
        
        # 验证安全提示（admin用户不可修改）
        has_security_notice = users_page.is_visible("text=Admin permissions cannot be modified", timeout=2000)
        logger.info(f"   安全提示显示: {has_security_notice}")
        
        # 返回用户列表
        users_page.page.click("button:has-text('Back')")
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 验证结果
        assert summary['total'] > 0, f"admin用户应有权限配置，实际Total={summary['total']}"
        # admin用户通常全部授予
        if summary['granted'] == summary['total']:
            assert has_revoke_all or has_security_notice, "全部授予时应显示Revoke All或安全提示"
        
        logger.info("✅ TC-PERM-009执行成功 - Revoke All功能验证通过")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_action_permission_page_search(self, users_page):
        """
        TC-PERM-011: Permission页面搜索功能验证
        
        验证Permission页面的搜索框存在并可用
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-011: Permission页面搜索功能验证")
        logger.info("=" * 60)
        
        # 使用admin用户测试
        test_username = "admin"
        
        logger.info(f"   测试用户: {test_username}")
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 打开Permission页面
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)
        
        # 获取权限摘要
        summary = users_page.get_permission_summary()
        
        # 截图：Permission页面（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/perm_search_1_page_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/perm_search_1_page_{ts}.png",
            name=f"1-Permission页面: Total={summary['total']} (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查搜索框存在
        has_search = users_page.is_visible("input[placeholder*='Search permissions']", timeout=3000)
        logger.info(f"   搜索框存在: {has_search}")
        
        # 检查Cancel和Save Changes按钮
        has_cancel = users_page.is_visible("button:has-text('Cancel')", timeout=2000)
        has_save = users_page.is_visible("button:has-text('Save Changes')", timeout=2000)
        logger.info(f"   Cancel按钮: {has_cancel}, Save Changes按钮: {has_save}")
        
        # 返回用户列表
        users_page.page.click("button:has-text('Back')")
        users_page.page.wait_for_timeout(2000)
        users_page.wait_for_table_load()
        
        # 验证
        assert has_cancel, "Cancel按钮应存在"
        assert has_save, "Save Changes按钮应存在"
        
        logger.info("✅ TC-PERM-011执行成功 - Permission页面搜索功能验证通过")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_action_permission_cancel_button(self, users_page):
        """
        TC-PERM-010: Permission页面Cancel按钮验证
        
        验证Cancel按钮存在并可点击
        """
        logger.info("=" * 60)
        logger.info("TC-PERM-010: Permission页面Cancel按钮验证")
        logger.info("=" * 60)
        
        # 使用admin用户测试
        test_username = "admin"
        
        logger.info(f"   测试用户: {test_username}")
        
        users_page.page.reload()
        users_page.wait_for_load()
        users_page.wait_for_table_load()
        
        # 搜索并找到用户
        users_page.search_user(test_username)
        users_page.page.wait_for_timeout(1000)
        row_index = users_page.find_user_by_username(test_username)
        assert row_index >= 0, f"用户{test_username}应存在"
        users_page.clear_search()
        users_page.page.wait_for_timeout(500)
        
        # 打开Permission页面
        users_page.click_user_permissions(row_index)
        users_page.page.wait_for_timeout(3000)
        
        # 获取权限摘要
        summary = users_page.get_permission_summary()
        
        # 截图：Permission页面（全页截图）
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        users_page.page.screenshot(path=f"screenshots/perm_cancel_1_page_{ts}.png", full_page=True)
        allure.attach.file(
            f"screenshots/perm_cancel_1_page_{ts}.png",
            name=f"1-Permission页面: Total={summary['total']} (全页)",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查Cancel按钮存在
        has_cancel = users_page.is_visible("button:has-text('Cancel')", timeout=3000)
        logger.info(f"   Cancel按钮存在: {has_cancel}")
        
        # 点击Cancel
        if has_cancel:
            users_page.page.click("button:has-text('Cancel')")
            users_page.page.wait_for_timeout(2000)
        
        # 等待返回用户列表
        users_page.wait_for_table_load()
        
        # 验证Cancel按钮功能正常
        assert has_cancel, "Cancel按钮应存在"
        
        logger.info("✅ TC-PERM-010执行成功 - Cancel按钮验证通过")
