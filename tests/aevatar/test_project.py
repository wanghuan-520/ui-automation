import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.project_page import ProjectPage
from pages.aevatar.organisation_page import OrganisationPage
from utils.logger import get_logger
from utils.page_utils import PageUtils
from tests.aevatar.test_helpers import generate_random_name, generate_random_email

logger = get_logger(__name__)

@allure.feature("Project管理功能")
class TestProjectFeatures:
    """Project功能测试类 (Sync)"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, shared_page: Page):
        """类级别的设置，所有测试共享一次登录"""
        logger.info("=" * 60)
        logger.info("🚀 开始 Project 测试类 - Class级别Setup")
        logger.info("=" * 60)
        
        self.page = shared_page
        self.page_utils = PageUtils(shared_page)
        
        # 登录一次
        logger.info("📍 执行登录（Class级别，所有测试共享）")
        login_page = LocalhostEmailLoginPage(shared_page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), "登录失败"
        self.page_utils.screenshot_step("setup_class_login_success")
        
        # 初始化Project页面
        self.project_page = ProjectPage(shared_page)
        
        logger.info("✅ Class Setup 完成")
        yield
        logger.info("🔚 Project 测试类结束")
    
    @pytest.fixture(autouse=True)
    def setup_method(self, shared_page: Page):
        """方法级别的设置，每个测试前执行"""
        logger.info("-" * 60)
        logger.info("📌 测试方法Setup - 导航到Project页面")
        
        # 每个测试前导航到Project页面
        self.page = shared_page
        self.page_utils = PageUtils(shared_page)
        self.project_page = ProjectPage(shared_page)
        self.project_page.navigate()
        
        if not self.project_page.is_loaded():
            logger.warning("未直接进入Project页面，尝试截图")
            self.page_utils.screenshot_step("project_navigation_failed")
        
        self.page_utils.screenshot_step("setup_method_ready")
        logger.info("✅ 测试方法Setup完成")
        yield
        logger.info("🔚 测试方法结束")

    @pytest.mark.p0
    @pytest.mark.p1
    @allure.title("Lifecycle: Project Member完整生命周期")
    @allure.description("验证Project Member的完整生命周期：添加(P0) -> 删除(P1)")
    def test_proj_member_lifecycle(self):
        """
        Project Member 完整生命周期测试
        1. 添加成员 [P0]
        2. 删除成员 [P1]
        """
        logger.info("=" * 60)
        logger.info("👥 开始测试: Project Member 完整生命周期 [P0 -> P1]")
        
        member_email = "haylee1@test.com"
        logger.info(f"测试目标成员: {member_email}")
        
        # --- Pre-condition 1: 确保成员在 Organisation 中 ---
        logger.info("📍 Pre-check: 验证成员是否在 Organisation 中")
        org_page = OrganisationPage(self.page)
        org_page.navigate()
        
        if not org_page.verify_member_exists(member_email):
            logger.info(f"⚠️ 成员 {member_email} 不在 Organisation 中，执行邀请")
            org_page.invite_member(member_email)
            self.page.wait_for_timeout(2000)
        else:
            logger.info(f"✅ 成员 {member_email} 已在 Organisation 中")
            
        # --- Pre-condition 2: 确保 Project 中无此成员 (环境清理) ---
        logger.info("📍 Pre-check: 清理 Project 中的目标成员")
        self.project_page.navigate()
        
        # delete_member 返回 True 如果成员不存在或删除成功
        clean_success = self.project_page.delete_member(member_email)
        assert clean_success, "环境清理失败: 无法确保成员不在 Project 中"
        self.page_utils.screenshot_step("lifecycle_proj_member_pre_clean")
        
        # --- Step 1: 添加成员 (P0) ---
        logger.info(f"📍 步骤1: 添加项目成员: {member_email}")
        
        self.page_utils.screenshot_step("lifecycle_proj_member_1_before_add")
        add_success = self.project_page.add_member(member_email)
        self.page_utils.screenshot_step("lifecycle_proj_member_1_after_add")
        
        assert add_success, f"步骤1失败: 添加项目成员失败 {member_email}"
        logger.info(f"✅ 步骤1成功: 项目成员已添加")
        
        # --- Step 2: 删除成员 (P1) ---
        logger.info(f"📍 步骤2: 删除项目成员: {member_email}")
        
        self.page_utils.screenshot_step("lifecycle_proj_member_2_before_delete")
        delete_success = self.project_page.delete_member(member_email)
        self.page_utils.screenshot_step("lifecycle_proj_member_2_after_delete")
        
        assert delete_success, f"步骤2失败: 删除项目成员失败 {member_email}"
        logger.info(f"✅ 步骤2成功: 项目成员已删除")
        
        logger.info("🎉 Project Member 完整生命周期测试通过!")

    @pytest.mark.p0
    @pytest.mark.p1
    @pytest.mark.p2
    @allure.title("Lifecycle: Project Role完整生命周期")
    @allure.description("验证Project Role的完整生命周期：创建(P0) -> 编辑权限(P1) -> 删除(P2)")
    def test_proj_role_lifecycle(self):
        """
        Project Role 完整生命周期测试
        1. 创建角色 [P0]
        2. 编辑角色权限 [P1]
        3. 删除角色 [P2]
        """
        logger.info("=" * 60)
        logger.info("🛡️ 开始测试: Project Role 完整生命周期 [P0 -> P1 -> P2]")
        
        role_name = generate_random_name("proj-role-life")
        logger.info(f"测试目标角色: {role_name}")
        
        # --- Step 1: 创建角色 (P0) ---
        logger.info(f"📍 步骤1: 创建角色: {role_name}")
        
        self.page_utils.screenshot_step("lifecycle_proj_role_1_before_create")
        create_success = self.project_page.add_role(role_name)
        self.page_utils.screenshot_step("lifecycle_proj_role_1_after_create")
        
        assert create_success, f"步骤1失败: 创建角色失败 {role_name}"
        logger.info(f"✅ 步骤1成功: 角色已创建")
        
        # --- Step 2: 编辑角色权限 (P1) ---
        logger.info(f"📍 步骤2: 编辑角色权限: {role_name}")
        
        self.page_utils.screenshot_step("lifecycle_proj_role_2_before_edit")
        edit_success = self.project_page.edit_role_permissions(role_name)
        self.page_utils.screenshot_step("lifecycle_proj_role_2_after_edit")
        
        assert edit_success, f"步骤2失败: 编辑角色权限失败 {role_name}"
        logger.info(f"✅ 步骤2成功: 角色权限已编辑")
        
        # --- Step 3: 删除角色 (P2) ---
        logger.info(f"📍 步骤3: 删除角色: {role_name}")
        
        self.page_utils.screenshot_step("lifecycle_proj_role_3_before_delete")
        delete_success = self.project_page.delete_role(role_name)
        self.page_utils.screenshot_step("lifecycle_proj_role_3_after_delete")
        
        assert delete_success, f"步骤3失败: 删除角色失败 {role_name}"
        logger.info(f"✅ 步骤3成功: 角色已删除")
        
        logger.info("🎉 Project Role 完整生命周期测试通过!")

    @pytest.mark.p1
    @allure.title("P1: 编辑Project Name")
    def test_proj_name_edit_p1(self):
        """P1测试: 编辑Project Name"""
        logger.info("=" * 60)
        logger.info("⚙️ 开始测试: 编辑 Project Name [P1]")
        
        new_name = generate_random_name("proj-edit")
        success = self.project_page.edit_project_name(new_name)
        
        self.page_utils.screenshot_step("after_edit_project_name")
        assert success, f"编辑项目名称失败: {new_name}"
        logger.info(f"✅ 项目名称编辑成功: {new_name}")
