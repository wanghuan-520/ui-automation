import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.project_page import ProjectPage
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
        
        member_email = generate_random_email()
        success = self.project_page.add_member(member_email)
        
        self.page_utils.screenshot_step("after_add_project_member")
        assert success, f"添加成员失败: {member_email}"
        logger.info(f"✅ 成员添加成功: {member_email}")

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

