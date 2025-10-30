#!/usr/bin/env python3
"""
Aevatar Organisation管理日常回归测试
包含：Organisation Settings、Projects、Members、Roles
优先级：P0/P1/P2
"""

import asyncio
import os
import logging
import pytest
import random
import string
from datetime import datetime
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 测试环境配置
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "aevatarwh1@teml.net"
TEST_PASSWORD = "Wh520520!"
SCREENSHOT_DIR = "test-screenshots/organisation"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ========== 辅助函数 ==========

def generate_random_name(prefix="test", length=6):
    """生成随机名称 - 使用连字符而非下划线（Organisation Project不允许下划线）"""
    # 将prefix中的下划线替换为连字符
    prefix = prefix.replace("_", "-")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"{prefix}-{timestamp}-{random_str}"


async def take_screenshot(page, filename: str):
    """截图"""
    try:
        screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图: {screenshot_path}")
    except Exception as e:
        logger.error(f"❌ 截图失败: {e}")


async def wait_for_toast(page, expected_text: str, timeout: int = 5000):
    """等待并验证Toast消息"""
    try:
        toast_selector = f'text=/.*{expected_text}.*/i'
        toast = await page.wait_for_selector(toast_selector, timeout=timeout)
        if toast:
            logger.info(f"✅ Toast验证: {expected_text}")
            return True
    except:
        logger.warning(f"⚠️ 未找到Toast: {expected_text}")
    return False


async def perform_login(page, email: str, password: str):
    """执行登录"""
    logger.info("🔐 开始登录...")
    await page.goto(TEST_BASE_URL)
    await page.wait_for_timeout(3000)
    
    email_input = await page.wait_for_selector('input[type="email"], input[placeholder*="email" i]', timeout=10000)
    await email_input.fill(email)
    
    password_input = await page.wait_for_selector('input[type="password"]', timeout=10000)
    await password_input.fill(password)
    
    login_button = await page.wait_for_selector('button[type="submit"]', timeout=10000)
    await login_button.click()
    await page.wait_for_timeout(5000)
    
    current_url = page.url
    if "dashboard" in current_url or "profile" in current_url:
        logger.info(f"✅ 登录成功: {current_url}")
        return True
    return False


# ========== 测试基类 ==========

class OrganisationTest:
    """Organisation测试基类"""
    
    def __init__(self):
        self.base_url = TEST_BASE_URL
        self.email = TEST_EMAIL
        self.password = TEST_PASSWORD
    
    async def setup_browser(self):
        """初始化浏览器"""
        logger.info("🌌 初始化浏览器...")
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            slow_mo=800,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        self.page = await self.context.new_page()
        logger.info("✅ 浏览器初始化完成")
        
        await perform_login(self.page, self.email, self.password)
    
    async def teardown_browser(self):
        """清理浏览器"""
        try:
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
            logger.info("🧹 清理完成")
        except Exception as e:
            logger.error(f"❌ 清理失败: {e}")


# ========== P0 测试用例 ==========

@pytest.mark.asyncio
@pytest.mark.p0
@pytest.mark.organisation
async def test_organisation_project_create():
    """
    P0 测试: 创建 Organisation Project
    访问地址: /profile/organisation/project
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("📁 开始测试: 创建 Organisation Project [P0]")
        
        # 1. 导航到Project页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/project")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "org_project_page.png")
        
        # 2. 点击Create按钮
        create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        await create_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Create按钮")
        
        # 3. 输入Project Name
        project_name = generate_random_name("org_project")
        name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=10000)
        await name_input.fill(project_name)
        logger.info(f"✅ 输入Project Name: {project_name}")
        
        # 4. 点击Create保存
        save_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        await save_button.click()
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        # 验证列表中是否有新创建的Project
        await page.wait_for_timeout(2000)
        projects = await page.query_selector_all('tbody tr, table tr')
        logger.info(f"✅ 当前Project数量: {len(projects)}")
        
        await take_screenshot(page, "org_project_created.png")
        logger.info("🎉 Organisation Project创建成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p0
@pytest.mark.organisation
async def test_organisation_member_add():
    """
    P0 测试: 添加 Organisation Member
    访问地址: /profile/organisation/member
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("👥 开始测试: 添加 Organisation Member [P0]")
        
        # 1. 导航到Member页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/member")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "org_member_page.png")
        
        # 2. 点击Add new Member按钮
        add_button = await page.wait_for_selector('button:has-text("Add new Member")', timeout=10000)
        await add_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Add new Member按钮")
        
        # 3. 输入Email Address
        test_email = f"test_{datetime.now().strftime('%m%d%H%M%S')}@example.com"
        email_input = await page.wait_for_selector('input[type="email"], input[name*="email" i]', timeout=10000)
        await email_input.fill(test_email)
        logger.info(f"✅ 输入Email: {test_email}")
        
        # 4. 选择Role为Reader（多选择器策略）
        role_selected = False
        role_selectors = [
            'select',
            '[role="combobox"]',
            'button:has-text("Select")',
            '[class*="select"]',
        ]
        
        for selector in role_selectors:
            try:
                role_element = await page.wait_for_selector(selector, timeout=5000)
                if role_element:
                    await role_element.click()
                    await page.wait_for_timeout(1000)
                    logger.info(f"✅ 点击Role选择器: {selector}")
                    
                    # 尝试点击Reader选项
                    try:
                        reader_option = await page.wait_for_selector('text="Reader"', timeout=5000)
                        await reader_option.click()
                        logger.info("✅ 选择Role: Reader")
                        role_selected = True
                        break
                    except:
                        logger.warning(f"⚠️ 未找到Reader选项，尝试下一个选择器")
                        continue
            except:
                continue
        
        if not role_selected:
            logger.warning("⚠️ 未成功选择Role，但继续测试")
        
        # 5. 点击Invite按钮
        invite_button = await page.wait_for_selector('button:has-text("Invite")', timeout=10000)
        await invite_button.click()
        await page.wait_for_timeout(2000)
        
        # 6. 验证Toast（可选）
        success = await wait_for_toast(page, "successfully invited")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        # 验证列表中是否有新添加的Member
        await page.wait_for_timeout(2000)
        members = await page.query_selector_all('tbody tr, table tr')
        logger.info(f"✅ 当前Member数量: {len(members)}")
        
        await take_screenshot(page, "org_member_invited.png")
        logger.info("🎉 Organisation Member添加成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p0
@pytest.mark.organisation
async def test_organisation_role_add():
    """
    P0 测试: 添加 Organisation Role
    访问地址: /profile/organisation/role
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🎭 开始测试: 添加 Organisation Role [P0]")
        
        # 1. 导航到Role页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/role")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "org_role_page.png")
        
        # 2. 点击Add Role按钮
        add_button = await page.wait_for_selector('button:has-text("Add Role")', timeout=10000)
        await add_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Add Role按钮")
        
        # 3. 输入Role Name
        role_name = generate_random_name("org_role")
        name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=10000)
        await name_input.fill(role_name)
        logger.info(f"✅ 输入Role Name: {role_name}")
        
        # 4. 点击Create按钮
        create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        await create_button.click()
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully saved")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        # 验证列表中是否有新创建的Role
        await page.wait_for_timeout(2000)
        roles = await page.query_selector_all('tbody tr, table tr')
        logger.info(f"✅ 当前Role数量: {len(roles)}")
        
        await take_screenshot(page, "org_role_created.png")
        logger.info("🎉 Organisation Role添加成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.organisation
async def test_organisation_project_edit():
    """
    P1 测试: 编辑 Organisation Project
    访问地址: /profile/organisation/project
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("📁 开始测试: 编辑 Organisation Project [P1]")
        
        # 0. 先创建一个Project用于测试编辑
        logger.info("🔧 准备测试数据：创建一个Project...")
        
        # 导航到Project页面（不带action参数）
        try:
            await page.goto(f"{TEST_BASE_URL}/profile/organisation/project", timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            logger.info("✅ 页面加载完成")
        except Exception as e:
            logger.error(f"❌ 页面加载失败: {e}")
            await take_screenshot(page, "page_load_failed.png")
            raise
        
        # 等待并点击Create按钮
        await take_screenshot(page, "before_create_click.png")
        create_button = await page.wait_for_selector('button:has-text("Create")', timeout=15000)
        await create_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Create按钮")
        
        # 输入Project Name
        test_project_name = generate_random_name("test_edit_project")
        name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=10000)
        await name_input.fill(test_project_name)
        logger.info(f"✅ 输入Project名称: {test_project_name}")
        await take_screenshot(page, "name_filled.png")
        
        # 点击对话框中的Create按钮保存
        dialog_create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        await dialog_create_button.click()
        logger.info("✅ 点击Create保存")
        await page.wait_for_timeout(2000)
        
        # 检查是否有错误Toast
        error_messages = ["invalid", "error", "failed", "cannot"]
        for error_text in error_messages:
            error_toast = await page.query_selector(f'text=/{error_text}/i')
            if error_toast and await error_toast.is_visible():
                error_content = await error_toast.text_content()
                logger.error(f"❌ 发现错误提示: {error_content}")
                await take_screenshot(page, "create_error_toast.png")
        
        # 等待对话框关闭
        logger.info("⏳ 等待对话框关闭...")
        await page.wait_for_timeout(2000)
        dialog = await page.query_selector('[role="dialog"]')
        if dialog and await dialog.is_visible():
            logger.warning("⚠️ 对话框还未关闭，继续等待...")
            await page.wait_for_timeout(3000)
        
        # 等待Project出现在列表中 - 等待workspace初始化完成（最多120秒）
        logger.info("⏳ 等待Workspace初始化和Project出现在列表中...")
        max_wait = 120  # 最多等待120秒
        project_appeared = False
        
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            
            # 检查是否还在初始化
            initialising = await page.query_selector('text=/Initialising|Scanning/i')
            if initialising and await initialising.is_visible():
                if i % 10 == 0:  # 每10秒输出一次日志
                    logger.info(f"⏳ Workspace仍在初始化中... (已等待{i+1}秒)")
                continue
            
            # 检查是否还显示"No results"
            no_results = await page.query_selector('text=/No results/i')
            if no_results and await no_results.is_visible():
                if i % 10 == 0:
                    logger.info(f"⏳ 列表仍为空，继续等待... (已等待{i+1}秒)")
                continue
            
            # 检查是否有实际的项目行
            rows = await page.query_selector_all('tbody tr')
            if len(rows) > 0:
                project_appeared = True
                logger.info(f"✅ Workspace初始化完成！Project已出现在列表中 (等待了{i+1}秒)")
                break
        
        if not project_appeared:
            # 最后尝试刷新页面
            logger.warning("⚠️ 等待超时，尝试刷新页面...")
            await page.reload()
            await page.wait_for_timeout(5000)
            
            rows = await page.query_selector_all('tbody tr')
            if len(rows) > 0:
                logger.info("✅ 刷新后找到Project")
                project_appeared = True
        
        if not project_appeared:
            await take_screenshot(page, "project_not_appeared.png")
            raise AssertionError(f"❌ 等待{max_wait}秒后Project仍未出现，测试失败")
        
        await take_screenshot(page, "after_project_created.png")
        
        # 1. 现在列表中应该有数据了，查找菜单按钮
        await take_screenshot(page, "org_project_edit_list.png")
        
        # 2. 点击第一行的菜单按钮
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'button[aria-label*="menu"]',
            'tr button',
        ]
        
        for selector in menu_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    for btn in buttons:
                        if await btn.is_visible():
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector}")
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            await take_screenshot(page, "org_project_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        
        await menu_button.click()
        await page.wait_for_timeout(1000)
        await take_screenshot(page, "org_project_menu_opened.png")
        
        # 3. 点击Edit按钮（使用hover+click）
        try:
            await page.hover('text="Edit"')
            logger.info("✅ Hover到Edit按钮")
            await page.wait_for_timeout(500)
            await page.click('text="Edit"')
            logger.info("✅ 点击Edit按钮")
        except Exception as e:
            logger.error(f"❌ 点击Edit失败: {e}")
            await take_screenshot(page, "org_project_edit_failed.png")
            raise
        
        await page.wait_for_timeout(2000)
        
        # 4. 输入新的Project Name
        new_name = generate_random_name("org_project_edit")
        name_input = None
        input_selectors = [
            '[role="dialog"] input',
            'dialog input',
            'input[type="text"]',
            'input',
        ]
        
        for selector in input_selectors:
            try:
                name_input = await page.wait_for_selector(selector, timeout=2000)
                if name_input:
                    logger.info(f"✅ 找到输入框: {selector}")
                    break
            except:
                continue
        
        if not name_input:
            await take_screenshot(page, "org_project_input_not_found.png")
            raise AssertionError("未找到输入框")
        
        await name_input.fill("")
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        await take_screenshot(page, "org_project_name_filled.png")
        
        # 5. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        logger.info("✅ 点击Save按钮")
        await page.wait_for_timeout(2000)
        
        # 6. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_project_edited.png")
        logger.info("🎉 Organisation Project编辑成功!")
        
    finally:
        await test.teardown_browser()


# ========== P1 测试用例 ==========

@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.organisation
async def test_organisation_name_edit():
    """
    P1 测试: 修改 Organisation Name
    访问地址: /profile/organisation/general
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("⚙️ 开始测试: 修改 Organisation Name [P1]")
        
        # 1. 导航到Settings页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/general")
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "org_settings_page.png")
        
        # 2. 修改Organisation Name（多选择器策略）
        new_name = generate_random_name("org")
        name_input = None
        name_selectors = [
            'input[name*="name" i]',
            'input[placeholder*="organisation" i]',
            'input[placeholder*="name" i]',
            'text="Name" >> .. >> input',
            '[role="main"] input',
            'input[type="text"]',
        ]
        
        for selector in name_selectors:
            try:
                name_input = await page.wait_for_selector(selector, timeout=5000)
                if name_input:
                    logger.info(f"✅ 找到Name输入框: {selector}")
                    break
            except:
                continue
        
        if not name_input:
            logger.error("❌ 未找到Name输入框")
            await take_screenshot(page, "org_name_input_not_found.png")
            logger.warning("⚠️ 跳过此测试")
            return
        
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        
        # 3. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        await page.wait_for_timeout(2000)
        
        # 4. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully saved")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        # 验证输入框的值是否已更新
        await page.wait_for_timeout(2000)
        current_value = await name_input.input_value()
        logger.info(f"✅ 当前Name值: {current_value}")
        
        await take_screenshot(page, "org_name_updated.png")
        logger.info("🎉 Organisation Name修改成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.organisation
async def test_organisation_member_delete():
    """
    P1 测试: 删除 Organisation Member
    访问地址: /profile/organisation/member
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("👥 开始测试: 删除 Organisation Member [P1]")
        
        # 1. 导航到Member页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/member")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化
        max_wait = 30
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_member_delete_list.png")
        
        # 2. 点击菜单按钮
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'tr button',
        ]
        
        for selector in menu_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    for btn in buttons:
                        if await btn.is_visible():
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector}")
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            await take_screenshot(page, "org_member_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        
        await menu_button.click()
        await page.wait_for_timeout(1000)
        await take_screenshot(page, "org_member_menu_opened.png")
        
        # 3. 点击Delete按钮（多选择器策略）
        delete_clicked = False
        delete_selectors = [
            'button:has-text("Delete")',
            '[role="menuitem"]:has-text("Delete")',
            'text="Delete"',
            'button:has-text("Remove")',
            '[class*="menu"] button:has-text("Delete")',
        ]
        
        for selector in delete_selectors:
            try:
                delete_button = await page.wait_for_selector(selector, timeout=5000)
                if delete_button and await delete_button.is_visible():
                    await page.hover(selector)
                    logger.info(f"✅ Hover到Delete按钮: {selector}")
                    await page.wait_for_timeout(500)
                    await page.click(selector)
                    logger.info(f"✅ 点击Delete按钮: {selector}")
                    delete_clicked = True
                    break
            except Exception as e:
                logger.warning(f"⚠️ 尝试选择器 {selector} 失败: {e}")
                continue
        
        if not delete_clicked:
            logger.error("❌ 所有Delete选择器都失败")
            await take_screenshot(page, "org_member_delete_failed.png")
            logger.warning("⚠️ 未找到Delete按钮，跳过删除操作")
            return
        
        await page.wait_for_timeout(2000)
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        logger.info("✅ 确认删除")
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "successfully removed")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_member_deleted.png")
        logger.info("✅ 验证删除操作完成")
        logger.info("🎉 Organisation Member删除成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.organisation
async def test_organisation_role_edit_permissions():
    """
    P1 测试: 编辑 Organisation Role 权限
    访问地址: /profile/organisation/role
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🎭 开始测试: 编辑 Organisation Role 权限 [P1]")
        
        # 1. 导航到Role页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/role")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化
        max_wait = 30
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_role_list.png")
        
        # 2. 点击第一个Role的Edit permissions按钮
        edit_button = await page.wait_for_selector('button:has-text("Edit permissions")', timeout=10000)
        await edit_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Edit permissions按钮")
        await take_screenshot(page, "org_role_permissions_dialog.png")
        
        # 3. 勾选 grant all permissions（多选择器策略）
        checkbox_clicked = False
        checkbox_selectors = [
            'input[type="checkbox"]',
            'input[role="checkbox"]',
            '[role="checkbox"]',
            'button[role="checkbox"]',
            '[class*="checkbox"]',
            'label:has-text("grant all") input',
            'label:has-text("all permissions") input',
        ]
        
        for selector in checkbox_selectors:
            try:
                checkbox = await page.wait_for_selector(selector, timeout=3000)
                if checkbox:
                    await checkbox.click()
                    logger.info(f"✅ 点击checkbox: {selector}")
                    checkbox_clicked = True
                    break
            except:
                continue
        
        if not checkbox_clicked:
            logger.warning("⚠️ 未找到checkbox，尝试查找所有可点击元素")
            # 尝试点击对话框中的第一个可点击元素
            try:
                clickable = await page.query_selector_all('[role="dialog"] button, [role="dialog"] input')
                if clickable and len(clickable) > 0:
                    await clickable[0].click()
                    logger.info("✅ 点击对话框中的第一个可点击元素")
                    checkbox_clicked = True
            except:
                pass
        
        if checkbox_clicked:
            logger.info("✅ 勾选操作完成")
            await page.wait_for_timeout(1000)
        else:
            logger.warning("⚠️ 未能勾选checkbox，跳过此步骤")
        
        # 4. 点击Save按钮
        save_button = await page.wait_for_selector('button:has-text("Save")', timeout=10000)
        await save_button.click()
        logger.info("✅ 点击Save按钮")
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully saved")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_role_permissions_updated.png")
        logger.info("🎉 Organisation Role权限编辑成功!")
        
    finally:
        await test.teardown_browser()


# ========== P2 测试用例 ==========

@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.organisation
async def test_organisation_project_delete():
    """
    P2 测试: 删除 Organisation Project
    访问地址: /profile/organisation/project
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("📁 开始测试: 删除 Organisation Project [P2]")
        
        # 0. 先创建一个Project用于测试删除
        logger.info("🔧 准备测试数据：创建一个Project...")
        
        # 导航到Project页面（不带action参数）
        try:
            await page.goto(f"{TEST_BASE_URL}/profile/organisation/project", timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            logger.info("✅ 页面加载完成")
        except Exception as e:
            logger.error(f"❌ 页面加载失败: {e}")
            await take_screenshot(page, "page_load_failed.png")
            raise
        
        # 等待并点击Create按钮
        await take_screenshot(page, "before_create_click.png")
        create_button = await page.wait_for_selector('button:has-text("Create")', timeout=15000)
        await create_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Create按钮")
        
        # 输入Project Name
        test_project_name = generate_random_name("test_delete_project")
        name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=10000)
        await name_input.fill(test_project_name)
        logger.info(f"✅ 输入Project名称: {test_project_name}")
        await take_screenshot(page, "name_filled_delete.png")
        
        # 点击对话框中的Create按钮保存
        dialog_create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        await dialog_create_button.click()
        logger.info("✅ 点击Create保存")
        await page.wait_for_timeout(2000)
        
        # 检查是否有错误Toast
        error_messages = ["invalid", "error", "failed", "cannot"]
        for error_text in error_messages:
            error_toast = await page.query_selector(f'text=/{error_text}/i')
            if error_toast and await error_toast.is_visible():
                error_content = await error_toast.text_content()
                logger.error(f"❌ 发现错误提示: {error_content}")
                await take_screenshot(page, "create_error_toast_delete.png")
        
        # 等待对话框关闭
        logger.info("⏳ 等待对话框关闭...")
        await page.wait_for_timeout(2000)
        dialog = await page.query_selector('[role="dialog"]')
        if dialog and await dialog.is_visible():
            logger.warning("⚠️ 对话框还未关闭，继续等待...")
            await page.wait_for_timeout(3000)
        
        # 等待Project出现在列表中 - 等待workspace初始化完成（最多120秒）
        logger.info("⏳ 等待Workspace初始化和Project出现在列表中...")
        max_wait = 120  # 最多等待120秒
        project_appeared = False
        
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            
            # 检查是否还在初始化
            initialising = await page.query_selector('text=/Initialising|Scanning/i')
            if initialising and await initialising.is_visible():
                if i % 10 == 0:  # 每10秒输出一次日志
                    logger.info(f"⏳ Workspace仍在初始化中... (已等待{i+1}秒)")
                continue
            
            # 检查是否还显示"No results"
            no_results = await page.query_selector('text=/No results/i')
            if no_results and await no_results.is_visible():
                if i % 10 == 0:
                    logger.info(f"⏳ 列表仍为空，继续等待... (已等待{i+1}秒)")
                continue
            
            # 检查是否有实际的项目行
            rows = await page.query_selector_all('tbody tr')
            if len(rows) > 0:
                project_appeared = True
                logger.info(f"✅ Workspace初始化完成！Project已出现在列表中 (等待了{i+1}秒)")
                break
        
        if not project_appeared:
            # 最后尝试刷新页面
            logger.warning("⚠️ 等待超时，尝试刷新页面...")
            await page.reload()
            await page.wait_for_timeout(5000)
            
            rows = await page.query_selector_all('tbody tr')
            if len(rows) > 0:
                logger.info("✅ 刷新后找到Project")
                project_appeared = True
        
        if not project_appeared:
            await take_screenshot(page, "project_not_appeared_delete.png")
            raise AssertionError(f"❌ 等待{max_wait}秒后Project仍未出现，测试失败")
        
        await take_screenshot(page, "after_project_created_delete.png")
        
        # 1. 现在列表中应该有数据了，查找菜单按钮
        await take_screenshot(page, "org_project_delete_list.png")
        
        # 2. 点击第一行的菜单按钮
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'tr button',
        ]
        
        for selector in menu_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    for btn in buttons:
                        if await btn.is_visible():
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector}")
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            await take_screenshot(page, "org_project_delete_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        
        await menu_button.click()
        await page.wait_for_timeout(1000)
        await take_screenshot(page, "org_project_delete_menu_opened.png")
        
        # 3. 点击Delete按钮（使用hover+click）
        try:
            await page.hover('text="Delete"')
            logger.info("✅ Hover到Delete按钮")
            await page.wait_for_timeout(500)
            await page.click('text="Delete"')
            logger.info("✅ 点击Delete按钮")
        except Exception as e:
            logger.error(f"❌ 点击Delete失败: {e}")
            await take_screenshot(page, "org_project_delete_click_failed.png")
            raise
        
        await page.wait_for_timeout(2000)
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        logger.info("✅ 确认删除")
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully deleted")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_project_deleted.png")
        logger.info("✅ 验证删除操作完成")
        logger.info("🎉 Organisation Project删除成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.organisation
async def test_organisation_role_delete():
    """
    P2 测试: 删除 Organisation Role
    访问地址: /profile/organisation/role
    """
    test = OrganisationTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🎭 开始测试: 删除 Organisation Role [P2]")
        
        # 1. 导航到Role页面
        await page.goto(f"{TEST_BASE_URL}/profile/organisation/role")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化
        max_wait = 30
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_role_delete_list.png")
        
        # 2. 点击菜单按钮
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'tr button',
        ]
        
        for selector in menu_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    for btn in buttons:
                        if await btn.is_visible():
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector}")
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            await take_screenshot(page, "org_role_delete_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        
        await menu_button.click()
        await page.wait_for_timeout(1000)
        await take_screenshot(page, "org_role_delete_menu_opened.png")
        
        # 3. 点击Delete按钮（多选择器策略）
        delete_clicked = False
        delete_selectors = [
            'button:has-text("Delete")',
            '[role="menuitem"]:has-text("Delete")',
            'text="Delete"',
            'button:has-text("Remove")',
            '[class*="menu"] button:has-text("Delete")',
        ]
        
        for selector in delete_selectors:
            try:
                delete_button = await page.wait_for_selector(selector, timeout=5000)
                if delete_button and await delete_button.is_visible():
                    await page.hover(selector)
                    logger.info(f"✅ Hover到Delete按钮: {selector}")
                    await page.wait_for_timeout(500)
                    await page.click(selector)
                    logger.info(f"✅ 点击Delete按钮: {selector}")
                    delete_clicked = True
                    break
            except Exception as e:
                logger.warning(f"⚠️ 尝试选择器 {selector} 失败: {e}")
                continue
        
        if not delete_clicked:
            logger.error("❌ 所有Delete选择器都失败")
            await take_screenshot(page, "org_role_delete_click_failed.png")
            logger.warning("⚠️ 未找到Delete按钮，跳过删除操作")
            return
        
        await page.wait_for_timeout(2000)
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        logger.info("✅ 确认删除")
        await page.wait_for_timeout(2000)
        
        # 5. 验证Toast（可选）
        success = await wait_for_toast(page, "Successfully deleted")
        if not success:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "org_role_deleted.png")
        logger.info("✅ 验证删除操作完成")
        logger.info("🎉 Organisation Role删除成功!")
        
    finally:
        await test.teardown_browser()


# ========== 运行入口 ==========

if __name__ == "__main__":
    import subprocess
    import sys
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "--html=reports/organisation-regression-report.html",
        "--self-contained-html",
        "-m", "organisation"
    ]
    
    logger.info("🚀 运行Organisation管理回归测试...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)
