import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.organisation_page import OrganisationPage
from utils.logger import get_logger
from utils.page_utils import PageUtils
from tests.aevatar.test_helpers import generate_random_name, generate_random_email

logger = get_logger(__name__)

@allure.feature("Organisation管理功能")
class TestOrganisationFeatures:
    """Organisation功能测试类 (Sync)"""
    
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
        
        # 初始化Organisation页面并导航
        self.org_page = OrganisationPage(page)
        self.org_page.navigate()
        
        # 验证是否在Organisation页面
        if not self.org_page.is_loaded():
            logger.warning("未直接进入Organisation页面，尝试截图")
            self.page_utils.screenshot_step("org_navigation_failed")
            # 尝试再次点击Settings -> Organisation (如果页面结构特殊)
            # 这里假设 navigate() 已经尽力了
            pass

    @pytest.mark.p0
    @allure.title("P0: 创建Organisation Project")
    @allure.description("验证创建Organisation Project的核心流程")
    def test_org_project_create_p0(self):
        """
        P0测试: 创建Organisation Project
        """
        logger.info("=" * 60)
        logger.info("📁 开始测试: 创建 Organisation Project [P0]")
        
        # 生成随机项目名称
        project_name = generate_random_name("org-proj")
        logger.info(f"准备创建项目: {project_name}")
        
        # 执行创建
        success = self.org_page.create_project(project_name, "Auto-generated description")
        
        # 验证
        self.page_utils.screenshot_step("after_create_project")
        assert success, f"创建项目失败: {project_name}"
        logger.info(f"✅ 项目创建成功: {project_name}")

    @pytest.mark.p0
    @allure.title("P0: 添加Organisation Member")
    @allure.description("验证邀请Organisation Member的核心流程")
    def test_org_member_add_p0(self):
        """
        P0测试: 添加Organisation Member
        """
        logger.info("=" * 60)
        logger.info("👥 开始测试: 添加 Organisation Member [P0]")
        
        # 生成随机邮箱
        member_email = generate_random_email()
        logger.info(f"准备邀请成员: {member_email}")
        
        # 执行邀请
        success = self.org_page.invite_member(member_email)
        
        # 验证
        self.page_utils.screenshot_step("after_invite_member")
        assert success, f"邀请成员失败: {member_email}"
        logger.info(f"✅ 成员邀请成功: {member_email}")

    @pytest.mark.p0
    @allure.title("P0: 添加Organisation Role")
    @allure.description("验证创建Organisation Role的核心流程")
    def test_org_role_add_p0(self):
        """
        P0测试: 添加Organisation Role
        """
        logger.info("=" * 60)
        logger.info("🛡️ 开始测试: 添加 Organisation Role [P0]")
        
        # 生成随机角色名称
        role_name = generate_random_name("org-role")
        logger.info(f"准备创建角色: {role_name}")
        
        # 执行创建
        success = self.org_page.create_role(role_name)
        
        # 验证
        self.page_utils.screenshot_step("after_create_role")
        assert success, f"创建角色失败: {role_name}"
        logger.info(f"✅ 角色创建成功: {role_name}")

