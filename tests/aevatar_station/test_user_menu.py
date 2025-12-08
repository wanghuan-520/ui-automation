"""
用户菜单功能测试模块
包含用户菜单展开、登出等功能测试
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.landing_page import LandingPage
from tests.aevatar_station.pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def logged_in_page(page, test_data):
    """
    登录页面fixture - 为每个测试提供已登录的页面
    """
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    try:
        landing_page.navigate()
        landing_page.click_sign_in()
        login_page.wait_for_load()
        
        valid_data = test_data["valid_login_data"][0]
        logger.info(f"使用账号登录: {valid_data['username']}")
        
        page.fill("#LoginInput_UserNameOrEmailAddress", valid_data["username"])
        page.fill("#LoginInput_Password", valid_data["password"])
        page.click("button[type='submit']")
        
        # 等待登录完成
        page.wait_for_function(
            "() => !window.location.href.includes('/Account/Login')",
            timeout=30000
        )
        
        landing_page.handle_ssl_warning()
        page.wait_for_timeout(2000)
        
        return page
    except Exception as e:
        logger.error(f"❌ 登录失败: {e}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"screenshots/login_failed_menu_{timestamp}.png")
        raise e


@pytest.mark.user_menu
class TestUserMenu:
    """用户菜单功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_user_menu_display(self, logged_in_page):
        """
        TC-FUNC-009: 用户菜单展开和选项显示测试
        
        测试目标：验证已登录用户的菜单按钮可以正常展开并显示菜单选项
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FUNC-009: 用户菜单展开和选项显示测试")
        logger.info("=" * 60)
        
        page = logged_in_page
        landing_page = LandingPage(page)
        
        # 验证登录成功
        assert landing_page.is_user_menu_visible(), "登录后用户菜单按钮应该可见"
        logger.info("   ✓ 用户菜单按钮已显示")
        
        # 截图：登录后的首页状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"user_menu_logged_in_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-登录后的首页状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击用户菜单
        logger.info("步骤1: 点击用户菜单按钮")
        landing_page.click_element(landing_page.USER_MENU_BUTTON)
        page.wait_for_timeout(1000)
        
        # 截图：菜单展开后
        screenshot_path = f"user_menu_expanded_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-用户菜单展开状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证菜单展开
        logger.info("步骤2: 验证菜单项")
        menu_items = {
            "Profile": page.locator("text=Profile, [role='menuitem']:has-text('Profile')"),
            "Settings": page.locator("text=Settings, [role='menuitem']:has-text('Settings')"),
            "Logout": page.locator("text=Logout, text=Sign out, [role='menuitem']:has-text('Logout')")
        }
        
        found_count = 0
        for item_name, locator in menu_items.items():
            if locator.first.is_visible(timeout=2000):
                logger.info(f"   ✓ 菜单项'{item_name}'可见")
                found_count += 1
            else:
                logger.warning(f"   ⚠️ 菜单项'{item_name}'未找到")
        
        assert found_count > 0, "至少应该显示一个菜单项"
        logger.info(f"   ✓ 成功找到 {found_count} 个菜单项")
        
        logger.info("✅ TC-FUNC-009执行成功")
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_user_logout(self, logged_in_page):
        """
        TC-FUNC-010: 用户登出功能测试
        
        测试目标：验证已登录用户可以通过用户菜单成功登出系统
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-FUNC-010: 用户登出功能测试")
        logger.info("=" * 60)
        
        page = logged_in_page
        landing_page = LandingPage(page)
        
        # 截图：登录后状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"logout_before_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-登出前的登录状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 点击用户菜单
        logger.info("步骤1: 点击用户菜单按钮")
        landing_page.click_element(landing_page.USER_MENU_BUTTON)
        page.wait_for_timeout(1000)
        
        # 点击Logout
        logger.info("步骤2: 点击Logout选项")
        logout_selectors = [
            "button:has-text('Logout')",
            "button:has-text('Sign out')",
            "[role='menuitem']:has-text('Logout')",
            "text=Logout"
        ]
        
        logout_clicked = False
        for selector in logout_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible(timeout=2000):
                    btn.click()
                    logger.info(f"   ✓ 已点击Logout (selector: {selector})")
                    logout_clicked = True
                    break
            except:
                continue
        
        if not logout_clicked:
            logger.error("   ❌ 未找到Logout按钮")
            # 尝试通过截图辅助调试
            screenshot_path = f"logout_button_not_found_{timestamp}.png"
            landing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="Logout按钮未找到",
                attachment_type=allure.attachment_type.PNG
            )
            pytest.fail("无法找到Logout按钮")
            
        # 验证登出成功
        logger.info("步骤3: 验证登出状态")
        page.wait_for_timeout(3000)  # 等待跳转和状态更新
        
        # 截图：登出后状态
        screenshot_path = f"logout_after_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="3-登出后的页面状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        current_url = landing_page.get_current_url()
        logger.info(f"   登出后URL: {current_url}")
        
        # 检查登出标志
        sign_in_visible = landing_page.is_visible(landing_page.SIGN_IN_BUTTON)
        user_menu_hidden = not landing_page.is_user_menu_visible()
        url_has_login = "Account/Login" in current_url
        
        is_signed_out = sign_in_visible or user_menu_hidden or url_has_login
        
        if is_signed_out:
            logger.info("   ✓ 登出验证通过")
            if sign_in_visible: logger.info("     - Sign In按钮可见")
            if user_menu_hidden: logger.info("     - 用户菜单已隐藏")
            if url_has_login: logger.info("     - URL包含登录页路径")
        else:
            logger.error("   ❌ 登出验证失败")
            
        assert is_signed_out, "登出后应该显示Sign In按钮或用户菜单消失"
        
        logger.info("✅ TC-FUNC-010执行成功")
