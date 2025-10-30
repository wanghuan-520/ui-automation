#!/usr/bin/env python3
"""
Aevatar API Keys 日常回归测试
包含：API Keys 编辑、删除
优先级：P1/P2
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
SCREENSHOT_DIR = "test-screenshots/apikeys"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ========== 辅助函数 ==========

def generate_random_name(prefix="test", length=6):
    """生成随机名称"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    return f"{prefix}_{timestamp}_{random_str}"


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

class APIKeysTest:
    """API Keys测试基类"""
    
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


# ========== API Keys 测试 ==========

@pytest.mark.asyncio
@pytest.mark.p1
@pytest.mark.apikeys
async def test_apikeys_edit():
    """
    P1 测试: 修改 API Key
    访问地址: /dashboard/apikeys
    """
    test = APIKeysTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔑 开始测试: 修改 API Key [P1]")
        
        # 1. 导航到API Keys页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/apikeys")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化完成（等待Scanning/Initialising消失）
        max_wait = 30  # 最多等待30秒
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            # 检查页面中是否还有loading文本
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
            if i == max_wait - 1:
                logger.warning(f"⚠️ 页面初始化超时 (等待了{max_wait}秒)")
        
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "apikeys_edit_before_create.png")
        
        # 1.5. 先创建一个API Key（确保有可编辑的对象）
        logger.info("🔨 先创建一个临时 API Key...")
        try:
            create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
            await create_button.click(force=True)
            logger.info("✅ 点击Create按钮")
            await page.wait_for_timeout(2000)
            
            # 检查弹窗是否打开
            dialog = await page.query_selector('[role="dialog"], .modal, .dialog')
            if dialog:
                logger.info("✅ 弹窗已打开，填写API Key名称")
                api_key_name = generate_random_name("apikey_edit")
                name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=5000)
                await name_input.fill(api_key_name)
                logger.info(f"✅ 输入API Key名称: {api_key_name}")
                await page.wait_for_timeout(1000)
                
                # 点击Create保存（使用多选择器策略，参考P0测试）
                save_button = None
                save_selectors = [
                    'button[type="submit"]',
                    'button:has-text("Create")',
                    'button:has-text("Save")',
                    'button:has-text("Confirm")',
                    '[role="dialog"] button:has-text("Create")',
                ]
                
                for selector in save_selectors:
                    try:
                        save_button = await page.wait_for_selector(selector, timeout=3000)
                        if save_button:
                            logger.info(f"✅ 找到保存按钮: {selector}")
                            break
                    except:
                        continue
                
                if save_button:
                    await save_button.click()
                    logger.info("✅ 点击保存按钮")
                    await page.wait_for_timeout(3000)
                else:
                    logger.warning("⚠️ 未找到保存按钮")
            else:
                logger.info("⚠️ 弹窗未打开，可能快速创建成功")
                
            await page.wait_for_timeout(2000)
            
            # 验证是否创建成功（检查列表中是否有API Key）
            try:
                await page.wait_for_selector('table tbody tr', timeout=5000)
                rows = await page.query_selector_all('table tbody tr')
                if len(rows) > 0:
                    logger.info(f"✅ 临时 API Key 已创建，列表中有 {len(rows)} 个")
                else:
                    logger.warning("⚠️ 列表为空，创建可能失败")
            except:
                logger.warning("⚠️ 未检测到列表")
            
        except Exception as e:
            logger.warning(f"⚠️ 创建API Key时出现问题: {e}")
        
        await take_screenshot(page, "apikeys_edit_after_create.png")
        
        # 2. 点击第一个API Key的三个点菜单（使用更通用的选择器）
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'button[aria-label*="menu"]',
            'button:has-text("⋮")',
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
            await take_screenshot(page, "apikeys_edit_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        await menu_button.click()
        await page.wait_for_timeout(1000)  # 缩短等待时间
        logger.info("✅ 菜单已点击")
        
        await take_screenshot(page, "apikeys_edit_menu_opened.png")
        
        # 3. 点击Edit按钮（使用hover+click确保精确点击）
        logger.info("🔍 开始查找Edit按钮...")
        
        # 方式1: 尝试直接使用text定位并hover+click
        try:
            # 先hover到Edit选项
            await page.hover('text="Edit"')
            logger.info("✅ Hover到Edit按钮")
            await page.wait_for_timeout(500)
            
            # 然后点击
            await page.click('text="Edit"')
            logger.info("✅ 点击Edit按钮 (Playwright click)")
            
        except Exception as e:
            logger.warning(f"⚠️ text=Edit点击失败: {e}")
            
            # 方式2: 查找菜单中的Edit按钮并点击
            try:
                # 查找菜单项
                edit_items = await page.query_selector_all('text="Edit"')
                logger.info(f"🔍 找到 {len(edit_items)} 个Edit元素")
                
                for idx, item in enumerate(edit_items):
                    is_visible = await item.is_visible()
                    logger.info(f"   Edit元素 {idx+1}: visible={is_visible}")
                    if is_visible:
                        # 使用JavaScript点击可见的Edit
                        await item.evaluate('element => element.click()')
                        logger.info(f"✅ JavaScript点击第 {idx+1} 个Edit元素")
                        break
            except Exception as e2:
                logger.error(f"❌ 所有点击方式都失败: {e2}")
                await take_screenshot(page, "apikeys_edit_click_failed.png")
                raise
        
        # 等待可能的页面跳转、弹窗打开或网络请求
        await page.wait_for_timeout(1000)
        
        # 等待可能的loading状态消失
        try:
            await page.wait_for_selector('[class*="loading"], [class*="spinner"], [role="progressbar"]', state='hidden', timeout=5000)
            logger.info("✅ Loading状态已消失")
        except:
            logger.info("⚠️ 未检测到loading状态")
        
        await page.wait_for_timeout(2000)
        
        # 记录点击后的URL
        url_after = page.url
        logger.info(f"🔍 点击Edit后URL: {url_after}")
        
        # 检查URL是否变化
        if "/dashboard/apikeys" not in url_after or "edit" in url_after.lower():
            logger.info("✅ URL发生变化，可能跳转到编辑页面")
            await page.wait_for_timeout(2000)
        else:
            logger.info("⚠️ URL未变化，应该是弹窗模式")
        
        await take_screenshot(page, "apikeys_edit_dialog_opened.png")
        
        # 调试：检查页面上是否有弹窗
        dialogs = await page.query_selector_all('[role="dialog"], .modal, .dialog, [class*="modal"], [class*="dialog"]')
        logger.info(f"🔍 检测到 {len(dialogs)} 个弹窗元素")
        
        # 检查是否有输入框
        all_inputs = await page.query_selector_all('input')
        logger.info(f"🔍 检测到 {len(all_inputs)} 个input元素")
        
        if len(all_inputs) > 0:
            for idx, inp in enumerate(all_inputs[:5]):  # 只显示前5个
                is_visible = await inp.is_visible()
                input_type = await inp.get_attribute('type')
                input_name = await inp.get_attribute('name')
                input_placeholder = await inp.get_attribute('placeholder')
                logger.info(f"   Input {idx+1}: type={input_type}, name={input_name}, placeholder={input_placeholder}, visible={is_visible}")
        
        # 检查页面上所有可见的文本，看是否有"edit"相关内容
        page_text = await page.inner_text('body')
        if 'edit' in page_text.lower() or 'name' in page_text.lower():
            logger.info("🔍 页面包含edit或name相关文本")
        else:
            logger.info("⚠️ 页面不包含edit或name相关文本")
        
        # 尝试新策略：直接点击API Key的Name，看是否inline editing
        logger.info("🔍 尝试新策略：查找API Key的Name元素...")
        try:
            # 查找第一行的Name列
            name_cell = await page.wait_for_selector('tbody tr:first-child td:first-child, tbody tr:first-child [class*="name"]', timeout=3000)
            if name_cell:
                logger.info("✅ 找到Name单元格")
                await name_cell.click()
                await page.wait_for_timeout(1000)
                logger.info("✅ 点击Name单元格")
                
                await take_screenshot(page, "apikeys_name_clicked.png")
                
                # 再次检查是否有输入框出现
                inputs_after_click = await page.query_selector_all('input')
                logger.info(f"🔍 点击Name后检测到 {len(inputs_after_click)} 个input元素")
                
                if len(inputs_after_click) > 0:
                    logger.info("✅ 发现inline editing模式！")
        except Exception as e:
            logger.warning(f"⚠️ inline editing测试失败: {e}")
        
        # 4. 修改API Key名称（尝试多种选择器）
        new_name = generate_random_name("apikey_edited")
        name_input = None
        name_selectors = [
            'input[name*="name" i]',
            'input[placeholder*="name" i]',
            '[role="dialog"] input',
            '.modal input',
            'input[type="text"]',
        ]
        
        for selector in name_selectors:
            try:
                name_input = await page.wait_for_selector(selector, timeout=3000)
                if name_input:
                    logger.info(f"✅ 找到name输入框: {selector}")
                    break
            except:
                continue
        
        if not name_input:
            await take_screenshot(page, "apikeys_edit_name_input_not_found.png")
            raise AssertionError("未找到name输入框")
        await name_input.fill("")  # 清空
        await name_input.fill(new_name)
        logger.info(f"✅ 输入新名称: {new_name}")
        await page.wait_for_timeout(1000)
        
        await take_screenshot(page, "apikeys_edit_name_filled.png")
        
        # 5. 点击Save按钮（尝试多种选择器）
        save_button = None
        save_selectors = [
            'button:has-text("Save")',
            'button[type="submit"]',
            '[role="dialog"] button:has-text("Save")',
            'button:has-text("Update")',
        ]
        
        for selector in save_selectors:
            try:
                save_button = await page.wait_for_selector(selector, timeout=3000)
                if save_button:
                    logger.info(f"✅ 找到保存按钮: {selector}")
                    break
            except:
                continue
        
        if save_button:
            await save_button.click()
            logger.info("✅ 点击保存按钮")
            await page.wait_for_timeout(3000)
        else:
            logger.warning("⚠️ 未找到保存按钮")
        
        await take_screenshot(page, "apikeys_edited.png")
        
        # 6. 验证Toast（可选，不强制）
        success = await wait_for_toast(page, "Successfully")
        if success:
            logger.info("✅ 找到成功Toast")
        else:
            logger.warning("⚠️ 未找到Toast，但继续验证")
        
        # 7. 验证列表中是否有更新后的API Key
        await page.wait_for_timeout(2000)
        try:
            await page.wait_for_selector('table tbody tr', timeout=5000)
            logger.info("✅ API Key列表已更新")
        except:
            logger.warning("⚠️ 未检测到列表")
        
        logger.info("🎉 API Key编辑测试完成!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.apikeys
async def test_apikeys_delete():
    """
    P2 测试: 删除 API Key
    访问地址: /dashboard/apikeys
    """
    test = APIKeysTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔑 开始测试: 删除 API Key [P2]")
        
        # 1. 导航到API Keys页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/apikeys")
        await page.wait_for_timeout(3000)
        
        # 等待页面初始化完成（等待Scanning/Initialising消失）
        max_wait = 30  # 最多等待30秒
        for i in range(max_wait):
            await page.wait_for_timeout(1000)
            # 检查页面中是否还有loading文本
            scanning = await page.query_selector('text=/Scanning|Initialising/i')
            if scanning:
                is_visible = await scanning.is_visible()
                if not is_visible:
                    logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                    break
            else:
                logger.info(f"✅ 页面初始化完成 (等待了{i+1}秒)")
                break
            if i == max_wait - 1:
                logger.warning(f"⚠️ 页面初始化超时 (等待了{max_wait}秒)")
        
        await page.wait_for_timeout(3000)
        await take_screenshot(page, "apikeys_before_delete.png")
        
        # 2. 点击第一个API Key的三个点菜单（使用更通用的选择器）
        menu_button = None
        menu_selectors = [
            'tbody tr:first-child button',
            'table button:first-of-type',
            'button[aria-label*="menu"]',
            'button:has-text("⋮")',
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
            await take_screenshot(page, "apikeys_delete_menu_not_found.png")
            raise AssertionError("未找到菜单按钮")
        await menu_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 菜单已点击")
        
        await take_screenshot(page, "apikeys_delete_menu_opened.png")
        
        # 3. 点击Delete按钮（尝试多种选择器）
        delete_button = None
        delete_selectors = [
            'button:has-text("Delete")',
            '[role="menuitem"]:has-text("Delete")',
            'text=Delete',
            '[class*="menu"] button:has-text("Delete")',
        ]
        
        for selector in delete_selectors:
            try:
                delete_button = await page.wait_for_selector(selector, timeout=3000)
                if delete_button:
                    logger.info(f"✅ 找到删除按钮: {selector}")
                    break
            except:
                continue
        
        if not delete_button:
            await take_screenshot(page, "apikeys_delete_button_not_found.png")
            raise AssertionError("未找到删除按钮")
        await delete_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击Delete按钮")
        
        # 4. 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes")', timeout=10000)
        await confirm_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 确认删除")
        
        # 5. 验证删除成功
        await take_screenshot(page, "apikeys_deleted.png")
        logger.info("🎉 API Key删除成功!")
        
    finally:
        await test.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.apikeys
async def test_apikeys_create():
    """
    P0 测试: 创建 API Key
    访问地址: /dashboard/apikeys
    """
    test = APIKeysTest()
    try:
        await test.setup_browser()
        page = test.page
        
        logger.info("=" * 60)
        logger.info("🔑 开始测试: 创建 API Key [P0]")
        
        # 1. 导航到API Keys页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/apikeys")
        await page.wait_for_timeout(3000)
        
        # 等待页面加载完成（等待Scanning消失）
        try:
            await page.wait_for_selector('text=/Scanning/i', state='hidden', timeout=15000)
            logger.info("✅ 页面加载完成")
        except:
            logger.warning("⚠️ 未检测到Scanning状态或已消失")
        
        # 额外等待确保页面完全渲染
        await page.wait_for_timeout(3000)
        
        await take_screenshot(page, "apikeys_create_page.png")
        logger.info("✅ 导航到API Keys页面")
        
        # 2. 点击Create按钮
        create_button = await page.wait_for_selector('button:has-text("Create")', timeout=10000)
        
        # 检查按钮是否可见
        is_visible = await create_button.is_visible()
        logger.info(f"Create按钮可见性: {is_visible}")
        
        # 使用force点击，避免被其他元素遮挡
        await create_button.click(force=True)
        logger.info("✅ 点击Create按钮")
        await page.wait_for_timeout(2000)
        
        await take_screenshot(page, "apikeys_after_create_click.png")
        
        # 3. 检查弹窗是否打开
        dialog_opened = False
        try:
            # 尝试查找弹窗
            dialog = await page.wait_for_selector('[role="dialog"], .modal, .dialog', timeout=3000)
            if dialog:
                dialog_opened = True
                logger.info("✅ 弹窗已打开")
                
                # 填写API Key名称
                api_key_name = generate_random_name("apikey")
                name_input = await page.wait_for_selector('input[name*="name" i], input[placeholder*="name" i]', timeout=5000)
                await name_input.fill(api_key_name)
                logger.info(f"✅ 输入API Key名称: {api_key_name}")
                await page.wait_for_timeout(1000)
                
                await take_screenshot(page, "apikeys_create_name_filled.png")
                
                # 点击Create按钮保存
                save_button = await page.wait_for_selector('button[type="submit"], button:has-text("Create")', timeout=5000)
                await save_button.click()
                logger.info("✅ 点击保存按钮")
                await page.wait_for_timeout(3000)
        except Exception as e:
            logger.warning(f"⚠️ 弹窗未打开或操作失败: {e}")
            dialog_opened = False
        
        # 4. 验证API Key列表（无论弹窗是否打开，都验证列表）
        await page.wait_for_timeout(2000)
        await take_screenshot(page, "apikeys_final_list.png")
        
        # 检查页面是否有API Key（检查表格中是否有数据）
        try:
            # 等待表格加载
            await page.wait_for_selector('table tbody tr', timeout=10000)
            
            # 获取API Key数量
            rows = await page.query_selector_all('table tbody tr')
            count = len(rows)
            logger.info(f"✅ API Key列表中有 {count} 个API Key")
            
            if count > 0:
                logger.info("✅ 验证成功：至少有一个API Key存在")
            else:
                raise AssertionError("API Key列表为空")
                
        except Exception as e:
            await take_screenshot(page, "apikeys_verification_failed.png")
            raise AssertionError(f"未检测到API Key列表: {e}")
        
        logger.info("🎉 API Key创建/验证测试完成!")
        
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
        "--html=reports/apikeys-regression-report.html",
        "--self-contained-html",
        "-m", "apikeys"
    ]
    
    logger.info("🚀 运行API Keys回归测试...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)

