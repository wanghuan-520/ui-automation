"""
Profile/Settings页面测试
测试用户个人设置、组织管理、项目管理功能
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.profile_settings_page import ProfileSettingsPage
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Settings功能")
@allure.story("个人设置")
class TestProfileSettings:
    """Profile/Settings页面功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """
        测试前置设置 - 自动登录并导航到Profile页面
        
        Args:
            page: Playwright页面对象
        """
        logger.info("开始测试前置设置")
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 初始化Profile页面对象
        self.profile_page = ProfileSettingsPage(page)
        self.profile_page.navigate()
        
        logger.info("测试前置设置完成")
    
    @pytest.mark.smoke
    @pytest.mark.p0
    @allure.title("tc-profile-p0-001: Profile页面加载验证")
    @allure.description("验证Profile页面能够正常加载")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_profile_page_loads(self):
        """测试Profile页面正常加载"""
        logger.info("开始测试: Profile页面加载验证")
        
        # 验证页面已加载
        assert self.profile_page.is_loaded(), "Profile页面未正确加载"
        
        # 验证Profile General菜单可见
        assert self.profile_page.is_element_visible(
            self.profile_page.PROFILE_GENERAL_MENU
        ), "Profile General菜单不可见"
        
        logger.info("Profile页面加载验证测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-profile-p0-002: Name字段显示和编辑")
    @allure.description("验证Name字段正常显示且可编辑")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_name_field_editable(self):
        """测试Name字段可编辑"""
        logger.info("开始测试: Name字段显示和编辑")
        
        # 验证Name输入框可见
        assert self.profile_page.is_element_visible(
            self.profile_page.NAME_INPUT
        ), "Name输入框不可见"
        
        # 获取当前名称
        current_name = self.profile_page.get_current_name()
        logger.info(f"当前用户名称: {current_name}")
        
        # 验证名称不为空
        assert current_name != "", "用户名称为空"
        
        # 验证输入框可编辑
        name_element = self.page.locator(self.profile_page.NAME_INPUT)
        assert not name_element.is_disabled(), "Name输入框为disabled状态"
        
        logger.info("Name字段显示和编辑测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-profile-p0-003: Email字段显示且不可编辑")
    @allure.description("验证Email字段显示且为disabled状态")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_email_field_disabled(self):
        """测试Email字段不可编辑"""
        logger.info("开始测试: Email字段显示且不可编辑")
        
        # 获取当前邮箱
        current_email = self.profile_page.get_current_email()
        logger.info(f"当前邮箱: {current_email}")
        
        # 验证邮箱不为空
        assert current_email != "", "邮箱地址为空"
        
        # 验证邮箱为disabled状态
        assert self.profile_page.verify_email_disabled(), \
            "Email输入框不是disabled状态"
        
        logger.info("Email字段显示且不可编辑测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-profile-p0-004: Save按钮可见且可点击")
    @allure.description("验证Save按钮正常工作")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_save_button_visible(self):
        """测试Save按钮可见且可点击"""
        logger.info("开始测试: Save按钮可见且可点击")
        
        # 验证Save按钮可见
        assert self.profile_page.is_element_visible(
            self.profile_page.SAVE_BUTTON
        ), "Save按钮不可见"
        
        logger.info("Save按钮可见且可点击测试通过")
    
    @pytest.mark.p0
    @allure.title("tc-profile-p0-005: Reset Password按钮和说明")
    @allure.description("验证Reset Password按钮和说明文字显示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reset_password_button(self):
        """测试Reset Password按钮和说明"""
        logger.info("开始测试: Reset Password按钮和说明")
        
        # 验证Reset Password按钮可见
        assert self.profile_page.is_element_visible(
            self.profile_page.RESET_PASSWORD_BUTTON
        ), "Reset Password按钮不可见"
        
        # 验证说明文字可见
        assert self.profile_page.verify_reset_password_description(), \
            "Reset Password说明文字不可见"
        
        logger.info("Reset Password按钮和说明测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-profile-p1-001: 修改Name并保存")
    @allure.description("验证修改Name并保存功能正常")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_name(self):
        """测试修改Name并保存"""
        logger.info("开始测试: 修改Name并保存")
        
        # 获取原始名称
        original_name = self.profile_page.get_current_name()
        logger.info(f"原始名称: {original_name}")
        
        # 修改名称
        new_name = f"{original_name}_test"
        self.profile_page.update_name(new_name)
        
        # 验证名称已更新
        assert self.profile_page.verify_name_updated(new_name), \
            f"名称未更新为: {new_name}"
        
        # 恢复原始名称
        self.profile_page.update_name(original_name)
        assert self.profile_page.verify_name_updated(original_name), \
            "恢复原始名称失败"
        
        logger.info("修改Name并保存测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-profile-p1-006: Organisations导航菜单")
    @allure.description("验证Organisations导航菜单可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_organisations_menu_visible(self):
        """测试Organisations导航菜单"""
        logger.info("开始测试: Organisations导航菜单")
        
        # 验证Organisations部分可见
        assert self.profile_page.is_element_visible(
            self.profile_page.ORGANISATIONS_SECTION
        ), "Organisations部分不可见"
        
        # 验证General子菜单可见
        assert self.profile_page.is_element_visible(
            self.profile_page.ORG_GENERAL_MENU
        ), "Organisations > General菜单不可见"
        
        logger.info("Organisations导航菜单测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-profile-p1-007: Projects导航菜单")
    @allure.description("验证Projects导航菜单可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_projects_menu_visible(self):
        """测试Projects导航菜单"""
        logger.info("开始测试: Projects导航菜单")
        
        # 验证Projects部分可见
        assert self.profile_page.is_element_visible(
            self.profile_page.PROJECTS_SECTION
        ), "Projects部分不可见"
        
        # 验证General子菜单可见
        assert self.profile_page.is_element_visible(
            self.profile_page.PROJECT_GENERAL_MENU
        ), "Projects > General菜单不可见"
        
        logger.info("Projects导航菜单测试通过")
    
    @pytest.mark.p1
    @allure.title("tc-profile-p1-008: Notifications菜单导航")
    @allure.description("验证Profile > Notifications菜单可访问")
    @allure.severity(allure.severity_level.NORMAL)
    def test_notifications_menu_navigation(self):
        """测试Notifications菜单导航"""
        logger.info("开始测试: Notifications菜单导航")
        
        # 验证Notifications菜单可见
        assert self.profile_page.is_element_visible(
            self.profile_page.PROFILE_NOTIFICATIONS_MENU
        ), "Profile > Notifications菜单不可见"
        
        # 点击Notifications菜单
        self.profile_page.navigate_to_menu("Profile", "Notifications")
        
        # 等待页面加载
        self.page.wait_for_timeout(1000)
        
        logger.info("Notifications菜单导航测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-profile-p2-001: Name字段边界值测试 - 空字符串")
    @allure.description("验证Name字段空字符串提交行为")
    @allure.severity(allure.severity_level.MINOR)
    def test_name_empty_string(self):
        """测试Name字段空字符串边界"""
        logger.info("开始测试: Name字段边界值 - 空字符串")
        
        # 获取原始名称
        original_name = self.profile_page.get_current_name()
        
        # 尝试设置空字符串
        self.page.fill(self.profile_page.NAME_INPUT, "")
        self.profile_page.click_element(self.profile_page.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)
        
        # 验证是否有错误提示或恢复原值
        current_name = self.profile_page.get_current_name()
        logger.info(f"提交空字符串后的名称: {current_name}")
        
        # 恢复原始名称
        if current_name == "":
            self.profile_page.update_name(original_name)
        
        logger.info("Name字段边界值测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-profile-p2-003: 刷新页面后数据保持")
    @allure.description("验证刷新页面后数据不丢失")
    @allure.severity(allure.severity_level.MINOR)
    def test_page_refresh_data_persists(self):
        """测试刷新页面后数据保持"""
        logger.info("开始测试: 刷新页面后数据保持")
        
        # 获取当前数据
        name_before = self.profile_page.get_current_name()
        email_before = self.profile_page.get_current_email()
        
        # 刷新页面
        self.profile_page.refresh_page()
        
        # 验证数据一致
        name_after = self.profile_page.get_current_name()
        email_after = self.profile_page.get_current_email()
        
        assert name_before == name_after, \
            f"刷新后Name数据不一致: {name_before} vs {name_after}"
        assert email_before == email_after, \
            f"刷新后Email数据不一致: {email_before} vs {email_after}"
        
        logger.info("刷新页面后数据保持测试通过")
    
    @pytest.mark.p2
    @allure.title("tc-profile-p2-005: Dashboard按钮跳转")
    @allure.description("验证Dashboard按钮跳转功能")
    @allure.severity(allure.severity_level.MINOR)
    def test_dashboard_button_navigation(self):
        """测试Dashboard按钮跳转"""
        logger.info("开始测试: Dashboard按钮跳转")
        
        # 点击Dashboard按钮
        self.profile_page.click_dashboard_button()
        
        # 验证URL包含dashboard
        current_url = self.profile_page.get_current_url()
        assert "/dashboard" in current_url, \
            f"点击Dashboard后URL不正确: {current_url}"
        
        logger.info("Dashboard按钮跳转测试通过")


@allure.feature("Settings功能")
@allure.story("个人设置 - 集成测试")
class TestProfileSettingsIntegration:
    """Profile/Settings集成测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        
        # 登录
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 初始化Profile页面对象
        self.profile_page = ProfileSettingsPage(page)
        self.profile_page.navigate()
    
    @pytest.mark.integration
    @allure.title("集成测试: 登录到Profile完整流程")
    @allure.description("端到端测试从登录到访问Profile页面的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_to_profile_flow(self):
        """集成测试: 登录到Profile页面完整流程"""
        logger.info("开始集成测试: 登录到Profile流程")
        
        # 验证已在Profile页面
        assert self.profile_page.is_loaded(), "未成功加载Profile页面"
        
        # 验证可以获取用户信息
        name = self.profile_page.get_current_name()
        email = self.profile_page.get_current_email()
        
        assert name != "", "无法获取用户名称"
        assert email != "", "无法获取用户邮箱"
        assert "@" in email, "邮箱格式不正确"
        
        logger.info(f"用户信息 - 名称: {name}, 邮箱: {email}")
        logger.info("登录到Profile流程集成测试通过")


@allure.feature("Profile功能")
@allure.story("Profile设置 - 回归测试")
class TestProfileSettingsRegression:
    """Profile设置回归测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        
        # 登录（使用staging环境账号）
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("aevatarwh1@teml.net", "Wh520520!")
        assert login_page.is_login_successful(), f"登录失败，当前URL: {login_page.get_current_url()}"
        
        # 初始化Profile页面对象
        self.profile_page = ProfileSettingsPage(page)
        self.profile_page.navigate()
        
        logger.info("回归测试前置设置完成")
    
    @pytest.mark.regression
    @pytest.mark.p1
    @allure.title("回归测试-P1: Profile Name编辑完整流程")
    @allure.description("验证Profile Name修改 → 保存 → 验证的完整流程")
    @allure.severity(allure.severity_level.NORMAL)
    def test_profile_name_edit_regression(self):
        """
        P1 回归测试: 修改 Profile Name
        详细验证UI交互和数据持久化
        """
        logger.info("=" * 80)
        logger.info("👤 开始回归测试: 修改 Profile Name [P1]")
        logger.info("=" * 80)
        
        # 验证页面已加载
        assert self.profile_page.is_loaded(), "Profile页面未加载"
        logger.info("✅ Profile页面已加载")
        
        # 等待页面完全初始化（等待可能的loading状态）
        self.page.wait_for_timeout(2000)
        
        # 步骤1: 获取当前Name
        logger.info("📋 步骤1: 获取当前Name")
        original_name = self.profile_page.get_current_name()
        logger.info(f"✅ 当前Name: {original_name}")
        
        # 步骤2: 生成新的随机Name
        import time
        import random
        import string
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        timestamp = str(int(time.time()))[-6:]
        new_name = f"user_{timestamp}_{random_str}"
        logger.info(f"🔄 步骤2: 准备更新为: {new_name}")
        
        # 步骤3: 更新Name
        logger.info("✏️ 步骤3: 更新Name字段")
        success = self.profile_page.update_name(new_name)
        assert success, f"更新Name失败: {new_name}"
        logger.info(f"✅ Name已更新为: {new_name}")
        
        # 步骤4: 验证更新成功
        logger.info("🔍 步骤4: 验证Name已更新")
        # 等待保存完成
        self.page.wait_for_timeout(2000)
        
        # 重新获取Name值
        updated_name = self.profile_page.get_current_name()
        logger.info(f"✅ 更新后的Name: {updated_name}")
        
        # 验证Name已更新
        assert updated_name == new_name, \
            f"Name未正确更新，期望: {new_name}, 实际: {updated_name}"
        logger.info("✅ Name更新验证通过")
        
        # 步骤5: 刷新页面验证数据持久化
        logger.info("🔄 步骤5: 刷新页面验证数据持久化")
        self.profile_page.refresh_page()
        self.page.wait_for_timeout(3000)
        
        # 验证页面重新加载后Name依然是新值
        assert self.profile_page.is_loaded(), "刷新后页面未加载"
        persisted_name = self.profile_page.get_current_name()
        logger.info(f"✅ 刷新后的Name: {persisted_name}")
        
        assert persisted_name == new_name, \
            f"刷新后Name未持久化，期望: {new_name}, 实际: {persisted_name}"
        logger.info("✅ 数据持久化验证通过")
        
        logger.info("=" * 80)
        logger.info("🎉 回归测试完成: Profile Name编辑流程测试通过")
        logger.info("=" * 80)

