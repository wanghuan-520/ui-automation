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
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.page_utils = PageUtils(page)
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), "登录失败"
        
        # 初始化Project页面并导航
        self.project_page = ProjectPage(page)
        self.project_page.navigate()
        
        if not self.project_page.is_loaded():
            logger.warning("未直接进入Project页面，尝试截图")
            self.page_utils.screenshot_step("project_navigation_failed")

    @pytest.mark.p0
    @allure.title("P0: 添加Project Member")
    @allure.description("验证添加Project Member的核心流程")
    def test_proj_member_add_p0(self):
        """P0测试: 添加Project Member"""
        logger.info("=" * 60)
        logger.info("👥 开始测试: 添加 Project Member [P0]")
        
        # 1. 先在Organisation中添加成员 (依赖条件)
        member_email = generate_random_email()
        logger.info(f"步骤1: 在Organisation中邀请成员: {member_email}")
        
        org_page = OrganisationPage(self.page)
        org_page.navigate()
        assert org_page.invite_member(member_email), f"在Organisation中邀请成员失败: {member_email}"
        logger.info(f"✅ Organisation成员邀请成功")
        
        # 2. 导航回Project页面
        logger.info("步骤2: 导航回Project页面添加成员")
        self.project_page.navigate()
        
        # 3. 在Project中添加该成员
        success = self.project_page.add_member(member_email)
        
        self.page_utils.screenshot_step("after_add_project_member")
        assert success, f"添加项目成员失败: {member_email}"
        logger.info(f"✅ 项目成员添加成功: {member_email}")

    @pytest.mark.p0
    @allure.title("P0: 添加Project Role")
    @allure.description("验证添加Project Role的核心流程")
    def test_proj_role_add_p0(self):
        """P0测试: 添加Project Role"""
        logger.info("=" * 60)
        logger.info("🛡️ 开始测试: 添加 Project Role [P0]")
        
        role_name = generate_random_name("proj-role")
        success = self.project_page.add_role(role_name)
        
        self.page_utils.screenshot_step("after_add_project_role")
        assert success, f"添加角色失败: {role_name}"
        logger.info(f"✅ 角色添加成功: {role_name}")

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

    @pytest.mark.p1
    @allure.title("P1: 删除Project Member")
    def test_proj_member_delete_p1(self):
        """P1测试: 删除Project Member"""
        logger.info("=" * 60)
        logger.info("👥 开始测试: 删除 Project Member [P1]")
        
        # 1. 准备数据：在Org和Project中添加成员
        member_email = generate_random_email()
        
        # 1.1 添加到Organisation
        org_page = OrganisationPage(self.page)
        org_page.navigate()
        assert org_page.invite_member(member_email), "Org成员邀请失败"
        
        # 1.2 添加到Project
        self.project_page.navigate()
        assert self.project_page.add_member(member_email), "Project成员添加失败"
        
        # 2. 删除成员
        success = self.project_page.delete_member(member_email)
        self.page_utils.screenshot_step("after_delete_project_member")
        assert success, f"删除成员失败: {member_email}"
        logger.info(f"✅ 成员删除成功: {member_email}")

    @pytest.mark.p1
    @allure.title("P1: 编辑Project Role权限")
    def test_proj_role_edit_permissions_p1(self):
        """P1测试: 编辑Project Role权限"""
        logger.info("=" * 60)
        logger.info("🛡️ 开始测试: 编辑 Project Role 权限 [P1]")
        
        # 1. 添加角色
        role_name = generate_random_name("proj-role-perm")
        self.project_page.add_role(role_name)
        
        # 2. 编辑权限
        success = self.project_page.edit_role_permissions(role_name)
        self.page_utils.screenshot_step("after_edit_project_role_perm")
        assert success, f"编辑角色权限失败: {role_name}"
        logger.info(f"✅ 角色权限编辑成功: {role_name}")

    @pytest.mark.p2
    @allure.title("P2: 删除Project Role")
    def test_proj_role_delete_p2(self):
        """P2测试: 删除Project Role"""
        logger.info("=" * 60)
        logger.info("🛡️ 开始测试: 删除 Project Role [P2]")
        
        # 1. 添加角色
        role_name = generate_random_name("proj-role-del")
        self.project_page.add_role(role_name)
        
        # 2. 删除角色
        success = self.project_page.delete_role(role_name)
        self.page_utils.screenshot_step("after_delete_project_role")
        assert success, f"删除角色失败: {role_name}"
        logger.info(f"✅ 角色删除成功: {role_name}")
