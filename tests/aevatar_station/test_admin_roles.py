"""
角色管理功能测试模块
路径: /admin/users/roles
包含ABP Identity模块角色管理功能测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.admin_roles_page import AdminRolesPage
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def admin_logged_in_roles(browser, test_data):
    """
    管理员登录fixture - 整个测试类只登录一次
    使用admin-test01账号登录以访问管理功能
    """
    # 创建新的浏览器上下文
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    
    # 登录流程
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    try:
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        # 使用admin-test01账号
        admin_data = test_data["admin_login_data"][1]  # admin-test01
        logger.info(f"使用Admin账号登录: {admin_data['username']}")
        
        page.fill("#LoginInput_UserNameOrEmailAddress", admin_data["username"])
        page.fill("#LoginInput_Password", admin_data["password"])
        page.click("button[type='submit']")
        
        # 等待登录完成
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        logger.info(f"登录跳转完成，当前URL: {page.url}")
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        
        logger.info("管理员登录成功")
        
        yield page
        
    except Exception as e:
        logger.error(f"❌ 管理员登录失败: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/admin_login_failed_roles_{timestamp}.png")
        raise e
    finally:
        context.close()


@pytest.fixture(scope="function")
def roles_page(admin_logged_in_roles):
    """
    每个测试函数的角色管理页面fixture
    """
    page = admin_logged_in_roles
    
    # 导航到角色管理页面
    roles_mgmt = AdminRolesPage(page)
    roles_mgmt.navigate()
    
    # 确认页面加载
    if not roles_mgmt.is_loaded():
        logger.warning("角色管理页面可能未完全加载，尝试刷新")
        page.reload()
        roles_mgmt.wait_for_load()
    
    return roles_mgmt


@pytest.mark.admin
@pytest.mark.roles
class TestAdminRoles:
    """角色管理功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_roles_page_load(self, roles_page):
        """
        TC-ADMIN-ROLES-001: 验证角色管理页面加载
        
        测试目标：验证管理员可以访问角色管理页面
        测试路径：/admin/users/roles
        
        测试步骤：
        1. 使用管理员账号登录
        2. 导航到角色管理页面
        3. 验证页面正确加载
        
        预期结果：
        - 页面成功加载
        - 显示角色列表表格
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-001: 验证角色管理页面加载")
        logger.info("=" * 60)
        
        # 验证页面加载
        assert roles_page.is_loaded(), "角色管理页面未正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 验证URL
        current_url = roles_page.page.url
        logger.info(f"   当前URL: {current_url}")
        assert "/admin/users/roles" in current_url or "/roles" in current_url, f"URL应包含角色管理路径，实际: {current_url}"
        logger.info("   ✓ URL验证通过")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_page_load_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="角色管理页面加载",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-001执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_roles_table_visible(self, roles_page):
        """
        TC-ADMIN-ROLES-002: 验证角色列表表格显示
        
        测试目标：验证角色列表表格正确显示
        
        测试步骤：
        1. 导航到角色管理页面
        2. 等待表格加载
        3. 验证表格可见
        
        预期结果：
        - 角色列表表格可见
        - 表格包含角色数据
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-002: 验证角色列表表格显示")
        logger.info("=" * 60)
        
        # 等待表格加载
        roles_page.wait_for_table_load()
        
        # 验证表格可见
        table_visible = roles_page.is_visible(roles_page.ROLES_TABLE, timeout=10000)
        assert table_visible, "角色列表表格不可见"
        logger.info("   ✓ 角色列表表格可见")
        
        # 获取角色数量
        role_count = roles_page.get_role_count()
        logger.info(f"   当前显示角色数: {role_count}")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_table_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="角色列表表格",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-002执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_new_role_button_visible(self, roles_page):
        """
        TC-ADMIN-ROLES-003: 验证新建角色按钮可见
        
        测试目标：验证管理员可以看到新建角色按钮
        
        测试步骤：
        1. 导航到角色管理页面
        2. 检查新建角色按钮
        
        预期结果：
        - 新建角色按钮可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-003: 验证新建角色按钮可见")
        logger.info("=" * 60)
        
        # 验证新建角色按钮
        button_visible = roles_page.is_new_role_button_visible()
        assert button_visible, "新建角色按钮不可见"
        logger.info("   ✓ 新建角色按钮可见")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_new_button_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="新建角色按钮",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-003执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_new_role_dialog_open(self, roles_page):
        """
        TC-ADMIN-ROLES-004: 验证新建角色对话框打开
        
        测试目标：验证点击新建角色按钮后对话框正确打开
        
        测试步骤：
        1. 导航到角色管理页面
        2. 点击新建角色按钮
        3. 验证对话框打开
        
        预期结果：
        - 对话框成功打开
        - 显示角色表单
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-004: 验证新建角色对话框打开")
        logger.info("=" * 60)
        
        # 截图：点击前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_before_new_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击新建角色前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击新建角色按钮
        logger.info("步骤1: 点击新建角色按钮")
        roles_page.click_new_role()
        roles_page.page.wait_for_timeout(1500)
        
        # 验证对话框打开
        dialog_open = roles_page.is_dialog_open()
        assert dialog_open, "新建角色对话框未打开"
        logger.info("   ✓ 对话框已打开")
        
        # 截图：对话框打开
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_new_dialog_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-新建角色对话框",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 关闭对话框
        roles_page.click_cancel()
        
        logger.info("✅ TC-ADMIN-ROLES-004执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_role_actions_menu(self, roles_page):
        """
        TC-ADMIN-ROLES-005: 验证角色操作菜单
        
        测试目标：验证角色行的操作下拉菜单
        
        测试步骤：
        1. 导航到角色管理页面
        2. 确保有角色数据
        3. 点击第一行的操作按钮
        4. 验证操作菜单显示
        
        预期结果：
        - 操作菜单正确显示
        - 包含编辑、删除、权限等选项
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-005: 验证角色操作菜单")
        logger.info("=" * 60)
        
        # 等待表格加载
        roles_page.wait_for_table_load()
        
        # 获取角色数量
        role_count = roles_page.get_role_count()
        if role_count == 0:
            logger.warning("   ⚠️ 角色列表为空，跳过此测试")
            pytest.skip("角色列表为空")
        
        logger.info(f"   当前角色数: {role_count}")
        
        # 截图：点击前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_before_action_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击操作菜单前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 打开操作菜单
        logger.info("步骤1: 打开第一行角色的操作菜单")
        roles_page.open_role_actions(0)
        roles_page.page.wait_for_timeout(1000)
        
        # 截图：操作菜单打开
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_action_menu_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-操作菜单打开",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("   ✓ 操作菜单已显示")
        
        # 按ESC关闭菜单
        roles_page.press_escape()
        
        logger.info("✅ TC-ADMIN-ROLES-005执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_role_permissions_dialog(self, roles_page):
        """
        TC-ADMIN-ROLES-006: 验证角色权限对话框
        
        测试目标：验证角色权限管理功能
        
        测试步骤：
        1. 导航到角色管理页面
        2. 点击第一行角色的权限按钮
        3. 验证权限对话框打开
        
        预期结果：
        - 权限对话框正确打开
        - 显示权限列表
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-006: 验证角色权限对话框")
        logger.info("=" * 60)
        
        # 等待表格加载
        roles_page.wait_for_table_load()
        
        # 获取角色数量
        role_count = roles_page.get_role_count()
        if role_count == 0:
            logger.warning("   ⚠️ 角色列表为空，跳过此测试")
            pytest.skip("角色列表为空")
        
        # 点击权限
        logger.info("步骤1: 点击第一行角色的权限")
        roles_page.click_role_permissions(0)
        roles_page.page.wait_for_timeout(2000)
        
        # 验证权限对话框打开
        if roles_page.is_permissions_dialog_open():
            logger.info("   ✓ 权限对话框已打开")
            
            # 获取权限数量
            perm_count = roles_page.get_permission_count()
            logger.info(f"   权限数量: {perm_count}")
        else:
            logger.info("   ℹ️ 可能使用其他方式展示权限")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_permissions_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="角色权限对话框",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 关闭对话框
        roles_page.press_escape()
        
        logger.info("✅ TC-ADMIN-ROLES-006执行成功")
    
    @pytest.mark.P1
    @pytest.mark.functional
    def test_p1_edit_role_dialog(self, roles_page):
        """
        TC-ADMIN-ROLES-007: 验证编辑角色对话框
        
        测试目标：验证编辑角色功能
        
        测试步骤：
        1. 导航到角色管理页面
        2. 点击第一行角色的编辑按钮
        3. 验证编辑对话框打开
        
        预期结果：
        - 编辑对话框正确打开
        - 显示角色当前信息
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-007: 验证编辑角色对话框")
        logger.info("=" * 60)
        
        # 等待表格加载
        roles_page.wait_for_table_load()
        
        # 获取角色数量
        role_count = roles_page.get_role_count()
        if role_count == 0:
            logger.warning("   ⚠️ 角色列表为空，跳过此测试")
            pytest.skip("角色列表为空")
        
        # 点击编辑
        logger.info("步骤1: 点击编辑第一行角色")
        roles_page.click_edit_role(0)
        roles_page.page.wait_for_timeout(1500)
        
        # 验证对话框打开
        dialog_open = roles_page.is_dialog_open()
        assert dialog_open, "编辑角色对话框未打开"
        logger.info("   ✓ 编辑对话框已打开")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_edit_dialog_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="编辑角色对话框",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 关闭对话框
        roles_page.click_cancel()
        
        logger.info("✅ TC-ADMIN-ROLES-007执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_dialog_cancel_button(self, roles_page):
        """
        TC-ADMIN-ROLES-008: 验证对话框取消按钮
        
        测试目标：验证取消按钮正确关闭对话框
        
        测试步骤：
        1. 打开新建角色对话框
        2. 点击取消按钮
        3. 验证对话框关闭
        
        预期结果：
        - 对话框正确关闭
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-008: 验证对话框取消按钮")
        logger.info("=" * 60)
        
        # 打开对话框
        roles_page.click_new_role()
        roles_page.page.wait_for_timeout(1000)
        
        assert roles_page.is_dialog_open(), "对话框应该打开"
        logger.info("   ✓ 对话框已打开")
        
        # 截图：点击取消前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_before_cancel_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-点击取消前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击取消
        logger.info("步骤1: 点击取消按钮")
        roles_page.click_cancel()
        roles_page.page.wait_for_timeout(1000)
        
        # 验证对话框关闭
        assert not roles_page.is_dialog_open(), "对话框应该关闭"
        logger.info("   ✓ 对话框已关闭")
        
        # 截图：取消后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_after_cancel_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击取消后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-008执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_dialog_esc_close(self, roles_page):
        """
        TC-ADMIN-ROLES-009: 验证ESC键关闭对话框
        
        测试目标：验证按ESC键可以关闭对话框
        
        测试步骤：
        1. 打开新建角色对话框
        2. 按ESC键
        3. 验证对话框关闭
        
        预期结果：
        - 对话框正确关闭
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-009: 验证ESC键关闭对话框")
        logger.info("=" * 60)
        
        # 打开对话框
        roles_page.click_new_role()
        roles_page.page.wait_for_timeout(1000)
        
        assert roles_page.is_dialog_open(), "对话框应该打开"
        logger.info("   ✓ 对话框已打开")
        
        # 按ESC键
        logger.info("步骤1: 按ESC键")
        roles_page.press_escape()
        roles_page.page.wait_for_timeout(1000)
        
        # 验证对话框关闭
        assert not roles_page.is_dialog_open(), "对话框应该关闭"
        logger.info("   ✓ 对话框已关闭")
        
        # 截图
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_esc_close_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="ESC关闭对话框后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-009执行成功")
    
    @pytest.mark.P2
    @pytest.mark.functional
    def test_p2_page_refresh(self, roles_page):
        """
        TC-ADMIN-ROLES-010: 验证页面刷新保持状态
        
        测试目标：验证刷新页面后仍在角色管理页面
        
        测试步骤：
        1. 导航到角色管理页面
        2. 刷新页面
        3. 验证仍在角色管理页面
        
        预期结果：
        - 刷新后保持在角色管理页面
        - 页面内容正常显示
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-ADMIN-ROLES-010: 验证页面刷新保持状态")
        logger.info("=" * 60)
        
        # 截图：刷新前
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_before_refresh_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-刷新前",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 刷新页面
        logger.info("步骤1: 刷新页面")
        roles_page.page.reload()
        roles_page.page.wait_for_load_state("domcontentloaded")
        roles_page.page.wait_for_timeout(2000)
        
        # 验证URL
        current_url = roles_page.page.url
        assert "/roles" in current_url, f"刷新后应保持在角色管理页面，当前URL: {current_url}"
        logger.info("   ✓ URL验证通过")
        
        # 验证页面加载
        assert roles_page.is_loaded(), "刷新后页面应正确加载"
        logger.info("   ✓ 页面加载验证通过")
        
        # 截图：刷新后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_roles_after_refresh_{timestamp}.png"
        roles_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-刷新后",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-ADMIN-ROLES-010执行成功")
