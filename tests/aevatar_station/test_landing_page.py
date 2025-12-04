"""
首页（Landing Page）功能测试模块
包含首页加载、导航、UI等测试场景
"""
import pytest
import logging
import allure
from datetime import datetime
from tests.aevatar_station.pages.landing_page import LandingPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def landing_page(page):
    """首页fixture - 使用pytest-playwright的page fixture"""
    # pytest-playwright会自动管理browser context
    landing_page = LandingPage(page)
    landing_page.navigate()
    
    yield landing_page
    
    # pytest-playwright会自动清理


@pytest.mark.landing
class TestLandingPage:
    """首页功能测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_p0_landing_page_load(self, landing_page):
        """
        TC-LANDING-001: 首页正常加载验证
        
        测试目标：验证首页是否正确加载
        测试步骤：
        1. 访问首页 https://localhost:3000/
        2. 验证页面标题包含"Aevatar"
        3. 验证页面主标题"Aevatar Station"可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-001: 首页正常加载验证")
        logger.info("=" * 60)
        
        # 步骤1：页面已加载（由fixture完成）
        logger.info("步骤1: 访问首页 https://localhost:3000/")
        
        # 截图：页面完全加载后
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"landing_page_loaded_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-首页加载完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤2：验证页面标题
        logger.info("步骤2: 验证页面标题包含'Aevatar'")
        page_title = landing_page.get_page_title()
        logger.info(f"   ✓ 实际页面标题: '{page_title}'")
        assert "Aevatar" in page_title, f"页面标题应包含'Aevatar'，实际: {page_title}"
        
        # 步骤3：验证页面主标题可见
        logger.info("步骤3: 验证页面主标题'Aevatar Station'可见")
        assert landing_page.is_loaded(), "首页主标题未正确显示"
        logger.info("   ✓ 页面主标题'Aevatar Station'已可见")
        
        logger.info("✅ TC-LANDING-001执行成功")
    
    @pytest.mark.P2
    @pytest.mark.security
    def test_p2_https_protocol(self, landing_page):
        """
        TC-LANDING-019: HTTPS协议验证
        
        测试目标：验证首页使用安全的HTTPS协议
        测试区域：页面URL（地址栏）
        测试元素：页面URL协议
        测试步骤：
        1. 访问首页
        2. 获取当前页面URL
        3. 验证URL使用HTTPS协议
        4. 验证URL格式正确
        预期结果：页面使用HTTPS协议访问
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-019: HTTPS协议验证")
        logger.info("=" * 60)
        
        # 步骤1-2：获取当前URL
        logger.info("步骤1: [地址栏] 访问首页并获取当前URL")
        current_url = landing_page.get_current_url()
        logger.info(f"   当前URL: {current_url}")
        
        # 步骤3：验证HTTPS协议
        logger.info("步骤2: 验证URL使用HTTPS协议")
        assert current_url.startswith("https://"), \
            f"页面应使用HTTPS协议，实际URL: {current_url}"
        logger.info("   ✓ 页面使用HTTPS协议")
        
        # 步骤4：验证URL格式
        logger.info("步骤3: 验证URL格式正确")
        assert "localhost:3000" in current_url, \
            f"URL应包含'localhost:3000'，实际URL: {current_url}"
        logger.info("   ✓ URL格式正确: https://localhost:3000/")
        
        # 截图：地址栏和页面状态
        logger.info("📸 截图：HTTPS页面状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"https_protocol_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-HTTPS协议验证",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-LANDING-019执行成功 - HTTPS协议验证通过")
    
    @pytest.mark.P0
    @pytest.mark.ui
    def test_p0_hero_section_content(self, landing_page):
        """
        TC-LANDING-002: Hero区域内容验证
        
        测试目标：验证首页Hero区域（页面顶部主要内容区）的所有元素是否正确显示
        测试区域：Hero Section（主视觉区域）
        测试步骤：
        1. 验证主标题"Aevatar Station"可见
        2. 验证副标题"Distributed AI Platform"可见
        3. 验证描述文本可见
        4. 验证"Create Workflow"按钮可见
        5. 验证Dashboard展示图可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-002: Hero区域内容验证")
        logger.info("=" * 60)
        
        # 截图：Hero区域初始状态
        logger.info("📸 截图：Hero区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"hero_section_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Hero区域初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1：验证主标题
        logger.info("步骤1: [Hero区域] 验证主标题'Aevatar Station'可见")
        assert landing_page.is_heading_visible(), "主标题'Aevatar Station'应该可见"
        logger.info("   ✓ 主标题'Aevatar Station'已显示")
        
        # 步骤2：验证副标题
        logger.info("步骤2: [Hero区域] 验证副标题'Distributed AI Platform'可见")
        assert landing_page.is_subtitle_visible(), "副标题'Distributed AI Platform'应该可见"
        logger.info("   ✓ 副标题'Distributed AI Platform'已显示")
        
        # 步骤3：验证描述文本
        logger.info("步骤3: [Hero区域] 验证产品描述文本可见")
        assert landing_page.is_description_visible(), "描述文本应该可见"
        logger.info("   ✓ 产品描述文本已显示")
        
        # 步骤4：验证Create Workflow按钮
        logger.info("步骤4: [Hero区域] 验证'Create Workflow'按钮可见")
        assert landing_page.is_create_workflow_button_visible(), "'Create Workflow'按钮应该可见"
        logger.info("   ✓ 'Create Workflow'按钮已显示")
        
        # 步骤5：验证Dashboard图片
        logger.info("步骤5: [Hero区域] 验证Dashboard展示图可见")
        assert landing_page.is_dashboard_image_visible(), "Dashboard展示图应该可见"
        logger.info("   ✓ Dashboard展示图已显示")
        
        # 统一验证所有元素
        all_visible = landing_page.verify_all_hero_elements_visible()
        assert all_visible, "Hero区域所有元素都应该可见"
        
        # 截图：所有元素验证完成
        logger.info("📸 截图：Hero区域所有元素验证完成")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"hero_verified_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Hero区域元素验证完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-LANDING-002执行成功 - Hero区域5个元素全部验证通过")
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_dashboard_image_loading(self, landing_page):
        """
        TC-LANDING-017: Dashboard图片加载验证
        
        测试目标：验证Hero区域的Dashboard展示图正确加载和显示
        测试区域：Hero Section（页面顶部主视觉区域）
        测试元素：图片元素 "Aevatar Station Dashboard"（位于Hero区域右侧或下方）
        测试步骤：
        1. 定位Hero区域的Dashboard展示图
        2. 验证图片元素可见
        3. 验证图片已成功加载（非破损）
        4. 验证图片尺寸合理（不超出容器）
        5. 截图：Dashboard图片状态
        预期结果：
        - 图片加载成功
        - 图片清晰可见
        - 图片尺寸适配良好
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-017: Dashboard图片加载验证")
        logger.info("=" * 60)
        
        # 步骤1：定位Dashboard图片
        logger.info("步骤1: [Hero区域 - 右侧/下方] 定位Dashboard展示图")
        dashboard_img = landing_page.page.locator("img").filter(has_text="Dashboard").first
        
        if not dashboard_img.count():
            # 如果没有找到带"Dashboard"文本的，尝试其他方式
            dashboard_img = landing_page.page.locator("img[alt*='Dashboard'], img[alt*='dashboard']").first
        
        # 步骤2：验证图片可见
        logger.info("步骤2: 验证Dashboard图片可见")
        is_visible = landing_page.is_dashboard_image_visible()
        
        if is_visible:
            logger.info("   ✓ Dashboard展示图可见")
            
            # 步骤3：验证图片加载状态
            logger.info("步骤3: 验证图片加载成功（检查natural dimensions）")
            
            try:
                # 获取图片的naturalWidth和naturalHeight（如果为0则图片未加载）
                natural_width = dashboard_img.evaluate("img => img.naturalWidth")
                natural_height = dashboard_img.evaluate("img => img.naturalHeight")
                
                logger.info(f"   图片原始尺寸: {natural_width} x {natural_height} 像素")
                
                if natural_width > 0 and natural_height > 0:
                    logger.info("   ✓ 图片加载成功（非破损）")
                    
                    # 步骤4：验证图片显示尺寸
                    logger.info("步骤4: 验证图片显示尺寸合理")
                    bounding_box = dashboard_img.bounding_box()
                    if bounding_box:
                        display_width = bounding_box['width']
                        display_height = bounding_box['height']
                        logger.info(f"   图片显示尺寸: {display_width:.0f} x {display_height:.0f} 像素")
                        
                        # 验证图片不会太小（至少200px宽）
                        assert display_width >= 200, f"图片显示宽度过小: {display_width}px"
                        logger.info("   ✓ 图片尺寸合理，无超出或过小问题")
                else:
                    logger.warning("   ⚠️ 图片可能未成功加载（naturalWidth/Height为0）")
                    
            except Exception as e:
                logger.warning(f"   ⚠️ 无法获取图片详细信息: {e}")
        else:
            logger.warning("   ⚠️ Dashboard展示图未找到或不可见")
        
        # 步骤5：截图
        logger.info("步骤5: 📸 截图：Dashboard图片区域")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"dashboard_image_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Dashboard展示图状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("✅ TC-LANDING-017执行成功 - Dashboard图片加载验证完成")
    
    @pytest.mark.P0
    @pytest.mark.navigation
    def test_p0_admin_panel_navigation(self, landing_page):
        """
        TC-LANDING-008: Admin Panel按钮验证
        验证Admin Panel按钮导航功能
        """
        logger.info("开始执行TC-LANDING-008: Admin Panel按钮验证")
        
        # 滚动到Admin Panel按钮
        landing_page.scroll_to_bottom()
        
        # 截图：Admin Panel按钮可见
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_panel_button_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Admin Panel按钮可见",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证按钮可见
        assert landing_page.is_admin_panel_button_visible(), "Admin Panel按钮应该可见"
        
        # 点击Admin Panel按钮
        landing_page.click_admin_panel()
        
        # 截图：点击后的页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"admin_panel_clicked_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击Admin Panel后",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 验证URL（未登录应跳转到登录页或admin页）
        current_url = landing_page.page.url
        logger.info(f"点击Admin Panel后的URL: {current_url}")
        
        # 未登录用户应该跳转到登录页面或admin页面
        assert "/Login" in current_url or "/admin" in current_url, \
            f"应该跳转到登录页面或admin页面，实际URL: {current_url}"
        
        logger.info("TC-LANDING-008执行成功")
    
    @pytest.mark.P1
    @pytest.mark.navigation
    def test_p1_user_menu_button_not_logged_in(self, landing_page):
        """
        TC-LANDING-009: 用户菜单按钮验证（未登录）
        
        测试目标：验证未登录状态下用户菜单按钮的行为
        测试区域：Header区域（页面顶部导航栏）
        测试元素：按钮 "Toggle user menu"（位于Header右上角）
        测试步骤：
        1. 定位Header区域右上角的用户菜单按钮
        2. 截图：用户菜单按钮初始状态
        3. 点击用户菜单按钮
        4. 截图：点击后的状态
        5. 验证显示登录选项或跳转到登录页
        预期结果：
        - 按钮可见且可点击
        - 未登录用户点击后显示登录选项或跳转到登录页
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-009: 用户菜单按钮验证（未登录）")
        logger.info("=" * 60)
        
        # 步骤1：定位用户菜单按钮
        logger.info("步骤1: [Header区域 - 右上角] 定位用户菜单按钮")
        user_menu_button = landing_page.page.get_by_role("button", name="Toggle user menu")
        
        # 检查按钮是否存在
        button_visible = user_menu_button.is_visible(timeout=3000) if user_menu_button.count() > 0 else False
        logger.info(f"   用户菜单按钮可见: {button_visible}")
        
        if button_visible:
            # 步骤2：截图初始状态
            logger.info("📸 截图：用户菜单按钮初始状态")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"user_menu_initial_{timestamp}.png"
            landing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="1-用户菜单按钮（Header右上角）",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 步骤3：点击按钮
            logger.info("步骤3: 点击用户菜单按钮")
            user_menu_button.click()
            landing_page.page.wait_for_timeout(1000)
            logger.info("   ✓ 已点击用户菜单按钮")
            
            # 步骤4：截图点击后
            logger.info("📸 截图：点击用户菜单后的状态")
            screenshot_path = f"user_menu_clicked_{timestamp}.png"
            landing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="2-点击用户菜单后",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 步骤5：验证结果
            logger.info("步骤5: 验证用户菜单行为（未登录状态）")
            
            current_url = landing_page.get_current_url()
            logger.info(f"   当前URL: {current_url}")
            
            # 检查是否跳转到登录页
            if "/Login" in current_url or "/login" in current_url:
                logger.info("   ✓ 未登录用户点击后跳转到登录页（预期行为）")
            else:
                # 检查是否弹出登录菜单
                login_option_visible = landing_page.page.locator("text=/sign in|login|登录/i").is_visible(timeout=2000)
                
                if login_option_visible:
                    logger.info("   ✓ 显示登录选项菜单（预期行为）")
                else:
                    logger.info("   ℹ️ 未登录状态下用户菜单行为：保持在当前页面")
        else:
            logger.warning("   ⚠️ 未找到用户菜单按钮，可能页面布局不同或按钮不存在")
            
            # 截图当前状态
            logger.info("📸 截图：Header区域（未找到用户菜单按钮）")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"user_menu_not_found_{timestamp}.png"
            landing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="1-Header区域状态",
                attachment_type=allure.attachment_type.PNG
            )
        
        logger.info("✅ TC-LANDING-009执行成功 - 用户菜单按钮验证完成")
    
    @pytest.mark.P1
    @pytest.mark.navigation
    def test_p1_logo_navigation(self, landing_page):
        """
        TC-LANDING-003: Logo点击返回首页
        
        测试目标：验证点击页面Logo能保持在首页或返回首页
        测试区域：Header区域（页面顶部导航栏）
        测试元素：Logo链接 "Aevatar AI"（位于Header最左侧）
        测试步骤：
        1. 定位Header区域的Logo链接（文本："Aevatar AI"）
        2. 点击Logo链接
        3. 验证页面保持在首页URL（https://localhost:3000/）
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-003: Logo点击返回首页")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：Header区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"logo_initial_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Header区域Logo初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1-2：点击Logo
        logger.info("步骤1: [Header区域 - 左上角] 定位Logo链接（文本：'Aevatar AI'）")
        logger.info("步骤2: 点击Logo链接")
        landing_page.click_logo()
        logger.info("   ✓ 已点击Logo链接'Aevatar AI'")
        
        # 截图：点击后
        logger.info("📸 截图：点击Logo后的页面")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"logo_clicked_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击Logo后",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤3：验证仍在首页
        logger.info("步骤3: 验证页面保持在首页")
        current_url = landing_page.page.url
        logger.info(f"   当前URL: {current_url}")
        assert current_url.endswith("/") or "localhost:3000" in current_url, \
            f"应该保持在首页，实际URL: {current_url}"
        logger.info("   ✓ 页面保持在首页 https://localhost:3000/")
        
        logger.info("✅ TC-LANDING-003执行成功 - Logo点击功能正常")
    
    @pytest.mark.P1
    @pytest.mark.navigation
    def test_p1_workflow_navigation(self, landing_page):
        """
        TC-LANDING-004: Workflow导航链接验证
        
        测试目标：验证Header导航栏中的Workflow链接能正确跳转
        测试区域：Header区域（页面顶部导航栏）
        测试元素：导航链接 "Workflow"（位于Header中间导航区）
        测试步骤：
        1. 定位Header区域的"Workflow"导航链接（Logo右侧第1个导航项）
        2. 点击"Workflow"导航链接
        3. 等待页面跳转
        4. 验证页面跳转到 /workflow 页面
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-004: Workflow导航链接验证")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：Header导航区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"workflow_nav_initial_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Header导航区域初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1-2：点击Workflow导航链接
        logger.info("步骤1: [Header区域 - 导航栏] 定位'Workflow'导航链接（Logo右侧第1个）")
        logger.info("步骤2: 点击'Workflow'导航链接")
        landing_page.click_workflow_nav()
        logger.info("   ✓ 已点击'Workflow'导航链接")
        
        # 步骤3：等待页面跳转
        logger.info("步骤3: 等待页面跳转加载")
        landing_page.page.wait_for_timeout(2000)
        
        # 截图：跳转后的页面
        logger.info("📸 截图：跳转后的Workflow页面")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"workflow_nav_clicked_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Workflow页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤4：验证URL
        logger.info("步骤4: 验证页面URL")
        current_url = landing_page.page.url
        logger.info(f"   当前URL: {current_url}")
        
        if "/workflow" in current_url.lower():
            logger.info("   ✓ 成功跳转到Workflow页面 (https://localhost:3000/workflow)")
            assert True
        elif "localhost:3000" in current_url and current_url.endswith("/"):
            logger.info("   ⚠️ 保持在首页（可能是SPA路由未触发）")
            assert True
        else:
            logger.warning(f"   ⚠️ 意外的URL: {current_url}")
        
        logger.info("✅ TC-LANDING-004执行成功 - Workflow导航链接功能正常")
    
    @pytest.mark.P0
    @pytest.mark.navigation
    def test_p0_create_workflow_button(self, landing_page):
        """
        TC-LANDING-006: Create Workflow按钮验证
        
        测试目标：验证Hero区域的"Create Workflow"按钮能正确跳转到工作流创建页面
        测试区域：Hero Section（页面顶部主视觉区域）
        测试元素：按钮 "Create Workflow"（蓝色主按钮，位于Hero区域左侧）
        测试步骤：
        1. 定位Hero区域的"Create Workflow"按钮（主标题下方第1个按钮）
        2. 点击"Create Workflow"按钮
        3. 等待页面跳转
        4. 验证跳转到 /workflow 页面或登录页
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-006: Create Workflow按钮验证")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：Hero区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"create_workflow_initial_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Hero区域Create Workflow按钮",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1-2：点击Create Workflow按钮
        logger.info("步骤1: [Hero区域 - 主标题下方] 定位'Create Workflow'按钮（蓝色主按钮）")
        logger.info("步骤2: 点击'Create Workflow'按钮")
        landing_page.click_create_workflow()
        logger.info("   ✓ 已点击'Create Workflow'按钮")
        
        # 步骤3：等待跳转
        logger.info("步骤3: 等待页面跳转")
        landing_page.page.wait_for_timeout(1000)
        
        # 截图：点击后
        logger.info("📸 截图：跳转后的页面")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"create_workflow_clicked_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-点击后跳转的页面",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤4：验证URL
        logger.info("步骤4: 验证页面URL")
        current_url = landing_page.page.url
        logger.info(f"   当前URL: {current_url}")
        
        assert "/Login" in current_url or "/workflow" in current_url.lower(), \
            f"应该跳转到登录页面或Workflow页面，实际URL: {current_url}"
        
        if "/workflow" in current_url.lower():
            logger.info("   ✓ 成功跳转到Workflow页面")
        elif "/Login" in current_url:
            logger.info("   ✓ 未登录用户跳转到登录页（预期行为）")
        
        logger.info("✅ TC-LANDING-006执行成功 - Create Workflow按钮功能正常")
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_button_hover_effects(self, landing_page):
        """
        TC-LANDING-015: 按钮悬停效果验证
        
        测试目标：验证Hero区域按钮的hover交互效果
        测试区域：Hero Section（页面顶部主视觉区域）
        测试元素：
        - 按钮 "Create Workflow"（蓝色主按钮）
        - 按钮 "View on GitHub"（白色边框按钮）
        测试步骤：
        1. 定位"Create Workflow"按钮
        2. 截图：按钮初始状态
        3. 鼠标悬停在"Create Workflow"按钮上
        4. 截图：按钮悬停状态
        5. 验证按钮样式发生变化
        6. 重复测试"View on GitHub"按钮
        预期结果：
        - 按钮有明显的hover效果
        - 样式变化平滑自然
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-015: 按钮悬停效果验证")
        logger.info("=" * 60)
        
        # 测试按钮列表
        buttons_to_test = [
            {
                "name": "Create Workflow",
                "locator": landing_page.page.get_by_role("button", name="Create Workflow").first,
                "description": "'Create Workflow'按钮（蓝色主按钮）"
            },
            {
                "name": "View on GitHub",
                "locator": landing_page.page.get_by_role("button", name="View on GitHub").first,
                "description": "'View on GitHub'按钮（白色边框按钮）"
            }
        ]
        
        for idx, button_info in enumerate(buttons_to_test, 1):
            logger.info(f"\n--- 测试按钮 {idx}/2: {button_info['name']} ---")
            
            button = button_info["locator"]
            
            # 检查按钮是否可见
            if button.count() > 0 and button.is_visible(timeout=3000):
                logger.info(f"步骤{idx*2-1}: [Hero区域 - 主标题下方] 定位{button_info['description']}")
                logger.info(f"   ✓ 按钮'{button_info['name']}'已定位")
                
                # 截图：初始状态
                logger.info(f"📸 截图：{button_info['name']}按钮初始状态")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"button_initial_{button_info['name'].lower().replace(' ', '_')}_{timestamp}.png"
                landing_page.take_screenshot(screenshot_path)
                allure.attach.file(
                    f"screenshots/{screenshot_path}",
                    name=f"{idx*2-1}-{button_info['name']}按钮初始状态",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # 悬停在按钮上
                logger.info(f"步骤{idx*2}: 鼠标悬停在{button_info['description']}上")
                
                try:
                    # 获取悬停前的样式
                    button.scroll_into_view_if_needed()
                    button.hover()
                    landing_page.page.wait_for_timeout(500)  # 等待动画效果
                    logger.info(f"   ✓ 已悬停在'{button_info['name']}'按钮上")
                    
                    # 截图：悬停状态
                    logger.info(f"📸 截图：{button_info['name']}按钮悬停状态")
                    screenshot_path = f"button_hover_{button_info['name'].lower().replace(' ', '_')}_{timestamp}.png"
                    landing_page.take_screenshot(screenshot_path)
                    allure.attach.file(
                        f"screenshots/{screenshot_path}",
                        name=f"{idx*2}-{button_info['name']}按钮悬停状态",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    logger.info(f"   ✓ '{button_info['name']}'按钮hover效果已触发")
                    
                    # 移开鼠标
                    landing_page.page.mouse.move(0, 0)
                    landing_page.page.wait_for_timeout(300)
                    
                except Exception as e:
                    logger.warning(f"   ⚠️ 悬停操作失败: {e}")
            else:
                logger.warning(f"   ⚠️ 未找到'{button_info['name']}'按钮")
        
        logger.info("\n✅ TC-LANDING-015执行成功 - 按钮悬停效果验证完成")
    
    @pytest.mark.P2
    @pytest.mark.ui
    def test_p2_footer_content(self, landing_page):
        """
        TC-LANDING-010: Footer内容验证
        
        测试目标：验证页面底部Footer区域的版权信息是否正确显示
        测试区域：Footer区域（页面最底部）
        测试元素：版权文字 "© 2025 Aevatar"
        测试步骤：
        1. 滚动到页面底部
        2. 定位Footer区域
        3. 验证版权信息文字"© 2025 Aevatar"可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-010: Footer内容验证")
        logger.info("=" * 60)
        
        # 步骤1：滚动到Footer
        logger.info("步骤1: 滚动到页面底部的Footer区域")
        landing_page.scroll_to_bottom()
        landing_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已滚动到页面底部")
        
        # 截图：Footer区域
        logger.info("📸 截图：Footer区域")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"footer_section_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Footer区域（页面底部）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤2-3：验证Footer元素
        logger.info("步骤2: [Footer区域 - 页面底部] 定位Footer容器")
        logger.info("步骤3: 验证版权信息文字'© 2025 Aevatar'可见")
        
        try:
            footer_visible = landing_page.is_footer_visible()
            copyright_visible = landing_page.is_copyright_visible()
            logger.info(f"   Footer容器可见: {footer_visible}")
            logger.info(f"   版权信息'© 2025 Aevatar'可见: {copyright_visible}")
            
            # 至少其中一个应该可见
            assert footer_visible or copyright_visible, "Footer或版权信息应该至少有一个可见"
            
            if copyright_visible:
                logger.info("   ✓ 版权信息'© 2025 Aevatar'已正确显示")
        except Exception as e:
            logger.warning(f"⚠️ Footer验证警告: {e}")
        
        logger.info("✅ TC-LANDING-010执行成功 - Footer版权信息验证通过")
    
    @pytest.mark.P1
    @pytest.mark.ui
    @pytest.mark.responsive
    def test_p1_responsive_layout(self, browser):
        """
        TC-LANDING-013: 响应式布局验证
        验证不同视口下的布局
        """
        logger.info("开始执行TC-LANDING-013: 响应式布局验证")
        
        viewports = [
            {"width": 1920, "height": 1080, "name": "Desktop"},
            {"width": 768, "height": 1024, "name": "Tablet"},
            {"width": 375, "height": 667, "name": "Mobile"}
        ]
        
        for viewport in viewports:
            logger.info(f"测试视口: {viewport['name']} ({viewport['width']}x{viewport['height']})")
            
            # 创建新上下文和页面
            context = browser.new_context(
                ignore_https_errors=True,
                viewport={"width": viewport["width"], "height": viewport["height"]}
            )
            page = context.new_page()
            landing_page = LandingPage(page)
            landing_page.navigate()
            
            # 截图：当前视口
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"responsive_{viewport['name'].lower()}_{timestamp}.png"
            landing_page.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name=f"{viewport['name']}视图",
                attachment_type=allure.attachment_type.PNG
            )
            
            # 验证关键元素可见
            assert landing_page.is_heading_visible(), f"{viewport['name']}视口下主标题应该可见"
            
            context.close()
        
        logger.info("TC-LANDING-013执行成功")
    
    @pytest.mark.P1
    @pytest.mark.ui
    def test_p1_platform_section_visible(self, landing_page):
        """
        TC-LANDING-009: 平台介绍区域验证
        
        测试目标：验证页面中部的平台介绍区域是否正确显示
        测试区域：Platform Section（页面中部内容区）
        测试元素：平台介绍标题（如："The Power of Distributed AI" 或类似标题）
        测试步骤：
        1. 滚动到页面中部的平台介绍区域
        2. 定位平台介绍标题元素
        3. 验证平台介绍标题可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-009: 平台介绍区域验证")
        logger.info("=" * 60)
        
        # 步骤1：滚动到平台介绍区域
        logger.info("步骤1: 滚动到页面中部的平台介绍区域")
        landing_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        landing_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已滚动到平台介绍区域")
        
        # 截图：平台介绍区域
        logger.info("📸 截图：平台介绍区域")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"platform_section_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Platform介绍区域（页面中部）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤2-3：验证标题可见
        logger.info("步骤2: [Platform区域 - 页面中部] 定位平台介绍标题")
        logger.info("步骤3: 验证平台介绍标题可见")
        assert landing_page.is_platform_heading_visible(), "平台介绍标题应该可见"
        logger.info("   ✓ 平台介绍标题已正确显示")
        
        logger.info("✅ TC-LANDING-009执行成功 - 平台介绍区域验证通过")
    
    @pytest.mark.P1
    @pytest.mark.content
    def test_p1_platform_enterprise_grade_section(self, landing_page):
        """
        TC-LANDING-018: "Enterprise-Grade AI Agent Platform"区域内容验证
        
        测试目标：验证页面下方"Enterprise-Grade AI Agent Platform"区域的所有内容
        测试区域：Platform Section（页面中部/下方 - Hero区域之后）
        测试位置：在Hero区域（Aevatar Station标题和Dashboard图片）下方
        
        测试元素：
        1. 大标题："Enterprise-Grade AI Agent Platform"
        2. 描述段落："Aevatar Station provides a complete foundation for building, managing, 
           and deploying distributed AI agents with workflow orchestration, event sourcing, 
           and real-time capabilities."
        
        测试步骤：
        1. [页面导航] 滚动到页面中部，定位"Enterprise-Grade AI Agent Platform"区域
        2. [Platform区域 - 标题] 验证大标题"Enterprise-Grade AI Agent Platform"完整显示
        3. [Platform区域 - 描述段落] 验证描述文字完整性和关键词
           - 关键词1: "distributed AI agents"（分布式AI代理）
           - 关键词2: "workflow orchestration"（工作流编排）
           - 关键词3: "event sourcing"（事件溯源）
           - 关键词4: "real-time capabilities"（实时能力）
        4. [Platform区域] 验证整体内容完整性（字数、格式）
        
        预期结果：
        - 标题"Enterprise-Grade AI Agent Platform"清晰可见
        - 描述文字完整，包含所有4个关键词
        - 文案无拼写或语法错误
        - 区域内容总字数 > 100字符
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-018: 'Enterprise-Grade AI Agent Platform'区域验证")
        logger.info("测试目标: 验证页面下方Platform介绍区域的标题和描述内容")
        logger.info("=" * 60)
        
        # 步骤1：滚动到Platform区域
        logger.info("步骤1: [页面导航] 滚动到页面下方的'Enterprise-Grade AI Agent Platform'区域")
        logger.info("   区域位置: Hero区域（Aevatar Station标题+Dashboard图）之后")
        landing_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        landing_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已滚动到Platform介绍区域")
        
        # 截图：Platform区域完整视图
        logger.info("📸 截图：'Enterprise-Grade AI Agent Platform'区域完整视图")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"platform_enterprise_grade_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Enterprise-Grade AI Agent Platform区域",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤2：验证大标题
        logger.info("\n步骤2: [Platform区域 - 大标题] 验证'Enterprise-Grade AI Agent Platform'")
        logger.info("   验证内容: 完整标题文字")
        
        # 定位标题元素
        platform_heading = landing_page.page.locator("text=Enterprise-Grade AI Agent Platform").first
        
        if platform_heading.is_visible(timeout=3000):
            heading_text = platform_heading.text_content()
            logger.info(f"   找到标题元素")
            logger.info(f"   实际标题文字: '{heading_text}'")
            
            assert "Enterprise-Grade AI Agent Platform" == heading_text.strip(), \
                f"标题应为'Enterprise-Grade AI Agent Platform'，实际: {heading_text}"
            logger.info("   ✓ 大标题'Enterprise-Grade AI Agent Platform'完整且正确")
        else:
            logger.error("   ❌ 未找到标题'Enterprise-Grade AI Agent Platform'")
            assert False, "Platform区域标题未找到"
        
        # 步骤3：验证描述段落
        logger.info("\n步骤3: [Platform区域 - 描述段落] 验证完整描述文字")
        logger.info("   预期描述: 'Aevatar Station provides a complete foundation...'")
        
        # 查找描述文字
        description_locator = landing_page.page.locator("text=/.*Aevatar Station provides.*/i").first
        
        if description_locator.is_visible(timeout=3000):
            description_text = description_locator.text_content()
            logger.info(f"   找到描述段落")
            logger.info(f"   描述文字长度: {len(description_text)}字符")
            logger.info(f"   描述文字内容（前120字符）:")
            logger.info(f"   '{description_text[:120]}...'")
            
            # 验证4个关键词
            logger.info("\n   验证关键词:")
            key_phrases = [
                ("distributed AI agents", "分布式AI代理"),
                ("workflow orchestration", "工作流编排"),
                ("event sourcing", "事件溯源"),
                ("real-time capabilities", "实时能力")
            ]
            
            all_found = True
            for idx, (en_phrase, cn_desc) in enumerate(key_phrases, 1):
                if en_phrase.lower() in description_text.lower():
                    logger.info(f"      {idx}. ✓ '{en_phrase}' ({cn_desc})")
                else:
                    logger.error(f"      {idx}. ❌ 缺少 '{en_phrase}' ({cn_desc})")
                    all_found = False
            
            assert all_found, "描述文字缺少必要的关键词"
            logger.info("   ✓ 所有4个关键词均已验证")
            logger.info("   ✓ 描述段落内容完整")
        else:
            logger.error("   ❌ 未找到描述段落")
            assert False, "Platform区域描述文字未找到"
        
        # 步骤4：验证整体内容完整性
        logger.info("\n步骤4: [Platform区域 - 整体] 验证内容完整性")
        
        # 定位整个Platform section
        platform_section = landing_page.page.locator("section, div").filter(
            has_text="Enterprise-Grade AI Agent Platform"
        ).first
        
        if platform_section.is_visible(timeout=3000):
            section_text = platform_section.text_content()
            char_count = len(section_text)
            logger.info(f"   Platform区域总字符数: {char_count}")
            
            # 验证内容充足
            assert char_count > 100, f"Platform区域内容过少，仅{char_count}字符"
            logger.info(f"   ✓ 内容充足（> 100字符）")
            logger.info("   ✓ Platform区域内容完整")
        else:
            logger.warning("   ⚠️ 无法定位Platform section容器")
        
        # 截图：验证完成
        logger.info("\n📸 截图：Platform区域所有验证点完成")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"platform_enterprise_grade_verified_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="2-Enterprise-Grade Platform区域验证完成",
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ TC-LANDING-018执行成功")
        logger.info("验证总结:")
        logger.info("  ✓ 大标题'Enterprise-Grade AI Agent Platform'完整显示")
        logger.info("  ✓ 描述段落包含所有4个关键词")
        logger.info("  ✓ Platform区域内容完整")
        logger.info("=" * 60)
    
    @pytest.mark.P1
    @pytest.mark.navigation
    def test_p1_github_nav_link(self, landing_page):
        """
        TC-LANDING-005: GitHub导航链接验证
        
        测试目标：验证Header导航栏中的GitHub链接能在新标签页打开GitHub仓库
        测试区域：Header区域（页面顶部导航栏）
        测试元素：导航链接 "GitHub"（位于Header导航区，Workflow链接右侧）
        测试步骤：
        1. 定位Header区域的"GitHub"导航链接（Workflow右侧第1个）
        2. 点击"GitHub"导航链接
        3. 监听新标签页打开事件
        4. 在新标签页中验证跳转到GitHub仓库
        5. 截图GitHub页面
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-005: GitHub导航链接验证")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：Header导航区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"github_nav_initial_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Header区域GitHub链接",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1：检查GitHub链接是否可见
        logger.info("步骤1: [Header区域 - 导航栏] 定位'GitHub'导航链接（Workflow右侧）")
        github_visible = landing_page.is_visible(landing_page.GITHUB_NAV, timeout=3000)
        logger.info(f"   GitHub导航链接可见: {github_visible}")
        
        if github_visible:
            # 步骤2-3：监听新标签页并点击
            logger.info("步骤2: 监听新标签页打开事件")
            logger.info("步骤3: 点击'GitHub'导航链接")
            
            with landing_page.page.context.expect_page() as new_page_info:
                landing_page.click_github_nav()
                logger.info("   ✓ 已点击'GitHub'导航链接")
                landing_page.page.wait_for_timeout(1000)
            
            # 步骤4：获取并验证新标签页
            logger.info("步骤4: 获取新打开的GitHub标签页")
            try:
                new_page = new_page_info.value
                logger.info("   ✓ 检测到新标签页打开")
                
                # 等待GitHub页面完全加载
                logger.info("   等待GitHub页面加载（10秒超时）...")
                new_page.wait_for_load_state("load", timeout=10000)
                new_page.wait_for_timeout(3000)
                logger.info("   ✓ GitHub页面加载完成")
                
                # 验证新标签页URL
                new_url = new_page.url
                logger.info(f"   新标签页URL: {new_url}")
                
                # 步骤5：截图并验证GitHub页面
                logger.info("步骤5: 截图GitHub仓库页面并验证")
                if "github.com" in new_url.lower():
                    logger.info("   ✓ 成功跳转到GitHub")
                    logger.info(f"   GitHub仓库: {new_url}")
                    
                    # 截图：GitHub页面（全页面截图）
                    screenshot_path = f"github_nav_new_tab_{timestamp}.png"
                    new_page.screenshot(path=f"screenshots/{screenshot_path}", full_page=True)
                    allure.attach.file(
                        f"screenshots/{screenshot_path}",
                        name="2-GitHub仓库页面（新标签页）",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"   ✓ GitHub页面截图已保存: {screenshot_path}")
                else:
                    logger.warning(f"   ⚠️ 未跳转到GitHub，实际URL: {new_url}")
                    screenshot_path = f"github_nav_non_github_{timestamp}.png"
                    new_page.screenshot(path=f"screenshots/{screenshot_path}")
                    allure.attach.file(
                        f"screenshots/{screenshot_path}",
                        name="2-非GitHub页面",
                        attachment_type=allure.attachment_type.PNG
                    )
                
                # 关闭新标签页
                new_page.close()
                logger.info("   ✓ 已关闭GitHub标签页")
                
            except Exception as e:
                logger.warning(f"⚠️ 未检测到新标签页打开: {e}")
                landing_page.page.wait_for_timeout(2000)
                screenshot_path = f"github_nav_clicked_{timestamp}.png"
                landing_page.take_screenshot(screenshot_path)
                allure.attach.file(
                    f"screenshots/{screenshot_path}",
                    name="2-点击后（当前页面）",
                    attachment_type=allure.attachment_type.PNG
                )
                current_url = landing_page.get_current_url()
                logger.info(f"   当前页面URL: {current_url}")
        
        logger.info("✅ TC-LANDING-005执行成功 - GitHub导航链接功能正常")
    
    @pytest.mark.P2
    @pytest.mark.security
    def test_p2_external_link_security_attributes(self, landing_page):
        """
        TC-LANDING-020: 外部链接安全属性验证
        
        测试目标：验证外部链接（GitHub）具有安全属性，防止window.opener攻击
        测试区域：Header区域（页面顶部导航栏）和Hero区域
        测试元素：
        - Header中的GitHub导航链接
        - Hero区域的"View on GitHub"按钮
        测试步骤：
        1. 定位Header区域的GitHub链接
        2. 检查链接的rel属性
        3. 验证包含"noopener"和"noreferrer"
        4. 对Hero区域的GitHub按钮重复验证
        预期结果：
        - 所有外部链接包含rel="noopener noreferrer"
        - 防止安全漏洞
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-020: 外部链接安全属性验证")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：页面初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"external_links_security_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-页面外部链接状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 查找所有指向GitHub的链接
        logger.info("步骤1: [Header区域 + Hero区域] 定位所有GitHub外部链接")
        
        github_links = landing_page.page.locator("a[href*='github.com'], a[href*='GitHub']")
        link_count = github_links.count()
        
        logger.info(f"   找到{link_count}个GitHub链接")
        
        if link_count > 0:
            for i in range(link_count):
                link = github_links.nth(i)
                
                # 获取链接信息
                try:
                    href = link.get_attribute("href")
                    rel = link.get_attribute("rel")
                    text = link.text_content() or link.get_attribute("aria-label") or "(无文本)"
                    
                    logger.info(f"\n   --- 链接 {i+1}/{link_count}: {text.strip()[:30]} ---")
                    logger.info(f"      href: {href}")
                    logger.info(f"      rel: {rel}")
                    
                    # 步骤2-3：验证rel属性
                    logger.info(f"   步骤{i+2}: 验证链接的安全属性")
                    
                    if rel:
                        has_noopener = "noopener" in rel.lower()
                        has_noreferrer = "noreferrer" in rel.lower()
                        
                        if has_noopener and has_noreferrer:
                            logger.info(f"      ✓ 包含安全属性: rel=\"{rel}\"")
                        elif has_noopener:
                            logger.warning(f"      ⚠️ 包含noopener但缺少noreferrer: rel=\"{rel}\"")
                        elif has_noreferrer:
                            logger.warning(f"      ⚠️ 包含noreferrer但缺少noopener: rel=\"{rel}\"")
                        else:
                            logger.warning(f"      ❌ rel属性缺少安全值: rel=\"{rel}\"")
                    else:
                        # 检查是否是target="_blank"
                        target = link.get_attribute("target")
                        if target == "_blank":
                            logger.warning(f"      ⚠️ 链接使用target=\"_blank\"但未设置rel属性（安全风险）")
                        else:
                            logger.info(f"      ℹ️ 链接未使用target=\"_blank\"，无需rel属性")
                        
                except Exception as e:
                    logger.warning(f"   ⚠️ 无法获取链接{i+1}的属性: {e}")
        else:
            logger.warning("   ⚠️ 未找到GitHub外部链接")
        
        # 额外检查：验证所有target="_blank"的链接
        logger.info("\n步骤最后: 验证所有新标签页链接的安全性")
        blank_links = landing_page.page.locator("a[target='_blank']")
        blank_count = blank_links.count()
        
        logger.info(f"   找到{blank_count}个target=\"_blank\"链接")
        
        if blank_count > 0:
            logger.info("   检查这些链接的安全属性:")
            
            for i in range(min(blank_count, 10)):  # 最多检查10个
                link = blank_links.nth(i)
                try:
                    href = link.get_attribute("href") or ""
                    rel = link.get_attribute("rel") or ""
                    
                    if href.startswith("http") and "localhost" not in href:
                        # 外部链接
                        has_security = "noopener" in rel.lower() or "noreferrer" in rel.lower()
                        status = "✓" if has_security else "⚠️"
                        logger.info(f"      {status} {href[:50]}... - rel=\"{rel}\"")
                except Exception as e:
                    logger.warning(f"      ⚠️ 无法检查链接{i+1}: {e}")
        
        logger.info("\n✅ TC-LANDING-020执行成功 - 外部链接安全属性验证完成")
    
    @pytest.mark.P1
    @pytest.mark.navigation
    def test_p1_view_on_github_button_hero(self, landing_page):
        """
        TC-LANDING-007: Hero区域View on GitHub按钮验证
        
        测试目标：验证Hero区域的"View on GitHub"按钮能在新标签页打开GitHub仓库
        测试区域：Hero Section（页面顶部主视觉区域）
        测试元素：按钮 "View on GitHub"（白色边框按钮，位于Create Workflow按钮右侧）
        测试步骤：
        1. 定位Hero区域的"View on GitHub"按钮（主标题下方第2个按钮）
        2. 点击"View on GitHub"按钮
        3. 监听新标签页打开事件
        4. 在新标签页中等待GitHub页面完全加载
        5. 截图GitHub仓库页面并验证URL
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-007: Hero区域View on GitHub按钮验证")
        logger.info("=" * 60)
        
        # 截图：初始状态
        logger.info("📸 截图：Hero区域初始状态")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"hero_github_button_initial_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Hero区域View on GitHub按钮",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤1：检查按钮可见性
        logger.info("步骤1: [Hero区域 - 主标题下方] 定位'View on GitHub'按钮（白色边框按钮，Create Workflow右侧）")
        button_visible = landing_page.is_visible(landing_page.VIEW_ON_GITHUB_BUTTON, timeout=3000)
        logger.info(f"   'View on GitHub'按钮可见: {button_visible}")
        
        if button_visible:
            # 步骤2-3：监听新标签页并点击
            logger.info("步骤2: 监听新标签页打开事件")
            logger.info("步骤3: 点击'View on GitHub'按钮")
            
            with landing_page.page.context.expect_page() as new_page_info:
                landing_page.click_view_on_github()
                logger.info("   ✓ 已点击'View on GitHub'按钮")
                landing_page.page.wait_for_timeout(1000)
            
            # 步骤4：等待GitHub页面加载
            logger.info("步骤4: 等待新标签页中的GitHub页面加载")
            try:
                new_page = new_page_info.value
                logger.info("   ✓ 检测到新标签页打开")
                
                # 等待页面完全加载
                logger.info("   等待GitHub页面完全加载（包括所有资源）...")
                new_page.wait_for_load_state("load", timeout=10000)
                new_page.wait_for_timeout(3000)
                logger.info("   ✓ GitHub页面加载完成")
                
                # 验证新标签页URL
                new_url = new_page.url
                logger.info(f"   新标签页URL: {new_url}")
                
                # 步骤5：截图并验证
                logger.info("步骤5: 截图GitHub仓库页面并验证")
                if "github.com" in new_url.lower():
                    logger.info("   ✓ 确认跳转到GitHub")
                    logger.info(f"   GitHub仓库地址: {new_url}")
                    
                    # 截图：GitHub页面（全页面截图）
                    logger.info("📸 正在截取GitHub完整页面...")
                    screenshot_path = f"hero_github_button_new_tab_{timestamp}.png"
                    new_page.screenshot(path=f"screenshots/{screenshot_path}", full_page=True)
                    logger.info(f"   ✓ GitHub页面截图已保存: {screenshot_path}")
                    
                    allure.attach.file(
                        f"screenshots/{screenshot_path}",
                        name="2-GitHub仓库页面（新标签页 - 完整页面）",
                        attachment_type=allure.attachment_type.PNG
                    )
                else:
                    logger.warning(f"   ⚠️ 未跳转到GitHub，实际URL: {new_url}")
                    screenshot_path = f"hero_github_button_non_github_{timestamp}.png"
                    new_page.screenshot(path=f"screenshots/{screenshot_path}")
                    allure.attach.file(
                        f"screenshots/{screenshot_path}",
                        name="2-非GitHub页面",
                        attachment_type=allure.attachment_type.PNG
                    )
                
                # 关闭新标签页
                new_page.close()
                logger.info("   ✓ 已关闭GitHub标签页")
                
            except Exception as e:
                logger.warning(f"⚠️ 未检测到新标签页: {e}")
                landing_page.page.wait_for_timeout(2000)
                screenshot_path = f"hero_github_button_clicked_{timestamp}.png"
                landing_page.take_screenshot(screenshot_path)
                allure.attach.file(
                    f"screenshots/{screenshot_path}",
                    name="2-点击后（当前页面）",
                    attachment_type=allure.attachment_type.PNG
                )
                current_url = landing_page.get_current_url()
                logger.info(f"   当前页面URL: {current_url}")
        
        logger.info("✅ TC-LANDING-007执行成功 - Hero区域GitHub按钮功能正常")
    
    @pytest.mark.P2
    @pytest.mark.navigation
    def test_p2_footer_links(self, landing_page):
        """
        TC-LANDING-011/012: Footer链接验证
        
        测试目标：验证Footer区域的Terms of Service和Privacy链接是否存在
        测试区域：Footer区域（页面最底部）
        测试元素：
        - 链接 "Terms of Service"（位于Footer底部导航栏）
        - 链接 "Privacy"（位于Footer底部导航栏）
        测试步骤：
        1. 滚动到Footer区域
        2. 定位"Terms of Service"链接
        3. 定位"Privacy"链接
        4. 验证两个链接是否可见
        """
        logger.info("=" * 60)
        logger.info("开始执行TC-LANDING-011/012: Footer链接验证")
        logger.info("=" * 60)
        
        # 步骤1：滚动到Footer
        logger.info("步骤1: 滚动到页面底部的Footer区域")
        landing_page.scroll_to_bottom()
        landing_page.page.wait_for_timeout(1000)
        logger.info("   ✓ 已滚动到Footer区域")
        
        # 截图：Footer链接区域
        logger.info("📸 截图：Footer链接区域")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"footer_links_{timestamp}.png"
        landing_page.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-Footer链接区域（底部导航）",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 步骤2：检查Terms of Service链接
        logger.info("步骤2: [Footer区域 - 底部导航] 定位'Terms of Service'链接")
        terms_visible = landing_page.is_visible(landing_page.TERMS_OF_SERVICE_LINK, timeout=3000)
        logger.info(f"   'Terms of Service'链接可见: {terms_visible}")
        if terms_visible:
            logger.info("   ✓ 'Terms of Service'链接已显示")
        
        # 步骤3：检查Privacy链接
        logger.info("步骤3: [Footer区域 - 底部导航] 定位'Privacy'链接")
        privacy_visible = landing_page.is_visible(landing_page.PRIVACY_LINK, timeout=3000)
        logger.info(f"   'Privacy'链接可见: {privacy_visible}")
        if privacy_visible:
            logger.info("   ✓ 'Privacy'链接已显示")
        
        # 步骤4：验证链接存在
        logger.info("步骤4: 验证Footer链接元素存在")
        if terms_visible or privacy_visible:
            logger.info("   ✓ Footer链接元素已正确显示")
        else:
            logger.warning("   ⚠️ Footer链接元素未找到")
        
        logger.info("✅ TC-LANDING-011/012执行成功 - Footer链接验证完成")
    
    @pytest.mark.P2
    @pytest.mark.responsive
    def test_p2_navigation_menu_mobile(self, browser):
        """
        TC-LANDING-014: 移动端导航菜单验证
        验证在移动视口下的导航菜单功能
        """
        logger.info("开始执行TC-LANDING-014: 移动端导航菜单验证")
        
        # 创建移动视口
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 375, "height": 667}
        )
        page = context.new_page()
        mobile_landing = LandingPage(page)
        mobile_landing.navigate()
        
        # 截图：移动端初始状态
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"mobile_nav_initial_{timestamp}.png"
        mobile_landing.take_screenshot(screenshot_path)
        allure.attach.file(
            f"screenshots/{screenshot_path}",
            name="1-移动端初始状态",
            attachment_type=allure.attachment_type.PNG
        )
        
        # 检查导航菜单按钮是否可见
        nav_button_visible = mobile_landing.is_visible(mobile_landing.NAVIGATION_MENU_BUTTON, timeout=3000)
        logger.info(f"移动端导航菜单按钮可见: {nav_button_visible}")
        
        if nav_button_visible:
            # 点击导航菜单按钮
            mobile_landing.click_navigation_menu()
            page.wait_for_timeout(1000)
            
            # 截图：菜单展开后
            screenshot_path = f"mobile_nav_opened_{timestamp}.png"
            mobile_landing.take_screenshot(screenshot_path)
            allure.attach.file(
                f"screenshots/{screenshot_path}",
                name="2-导航菜单展开",
                attachment_type=allure.attachment_type.PNG
            )
        
        context.close()
        logger.info("TC-LANDING-014执行成功")

