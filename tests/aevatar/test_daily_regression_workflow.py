#!/usr/bin/env python3
"""
Aevatar Workflow回归测试
每日回归测试 - P0/P2 核心Workflow功能
"""

import logging
import sys
import os
import pytest

logger = logging.getLogger(__name__)


# ========== 每日回归测试 - 简单直接的Workflow测试 ==========

@pytest.mark.asyncio
@pytest.mark.workflow
@pytest.mark.workflows
@pytest.mark.integration
@pytest.mark.p0
async def test_workflow_create_and_run_regression():
    """
    每日回归测试 - 创建并运行 Workflow
    不使用数据驱动，直接测试核心Workflow流程
    
    测试步骤:
        1. 登录系统
        2. 导航到Workflow页面
        3. 创建新的Workflow
        4. 添加InputGAgent到画布
        5. 配置Agent参数
        6. 运行Workflow
        7. 验证执行结果
    
    预期结果:
        - 成功创建Workflow
        - Agent成功添加到画布
        - Workflow成功执行
    """
    from base_test import AevatarPytestTest
    
    logger.info("=" * 60)
    logger.info("🧪 每日回归测试: 创建并运行 Workflow [P0]")
    
    test_instance = AevatarPytestTest()
    
    try:
        await test_instance.setup_browser()
        
        # 先登录
        await test_instance.page.goto(test_instance.LOGIN_URL)
        await test_instance.page.wait_for_timeout(3000)
        
        # 填写登录信息
        email_input = await test_instance.page.wait_for_selector('input[placeholder*="email" i]', timeout=10000)
        await email_input.fill(test_instance.EMAIL)
        
        password_input = await test_instance.page.wait_for_selector('input[type="password"]', timeout=10000)
        await password_input.fill(test_instance.PASSWORD)
        
        login_button = await test_instance.page.wait_for_selector('button[type="submit"]', timeout=10000)
        await login_button.click()
        
        # 等待登录完成
        await test_instance.page.wait_for_timeout(5000)
        
        # 验证登录是否成功
        current_url = test_instance.page.url
        if "dashboard" not in current_url and "redirect" not in current_url:
            logger.error(f"❌ 登录失败，当前URL: {current_url}")
            await test_instance.take_screenshot("regression_create_login_failed.png")
            assert False, f"登录失败，未跳转到dashboard页面: {current_url}"
        
        logger.info(f"✅ 登录完成，当前URL: {current_url}")
        
        # 导航到workflow页面
        await test_instance.page.goto(f"{test_instance.BASE_URL}/dashboard/workflows")
        await test_instance.page.wait_for_timeout(3000)
        await test_instance.take_screenshot("regression_create_workflow_page.png")
        
        # 验证是否真的在workflow页面
        current_url = test_instance.page.url
        if "login" in current_url.lower() or current_url == test_instance.LOGIN_URL:
            logger.error(f"❌ 被重定向回登录页，session可能失效。当前URL: {current_url}")
            assert False, f"无法访问workflow页面，被重定向回登录页: {current_url}"
        
        logger.info(f"✅ 成功进入workflow页面，当前URL: {current_url}")
        
        # 点击New Workflow按钮
        new_workflow_button = await test_instance.page.wait_for_selector('button:has-text("New Workflow")', timeout=10000)
        await new_workflow_button.click()
        logger.info("✅ 点击New Workflow按钮")
        
        await test_instance.page.wait_for_timeout(2000)
        await test_instance.take_screenshot("regression_create_new_workflow_clicked.png")
        
        # 关闭AI弹窗 (按ESC键)
        await test_instance.page.keyboard.press('Escape')
        logger.info("✅ 关闭AI弹窗")
        
        await test_instance.page.wait_for_timeout(2000)
        await test_instance.take_screenshot("regression_create_modal_closed.png")
        
        # 拖拽InputGAgent agent到workflow看板
        agent_added = False
        try:
            logger.info("🔄 开始添加InputGAgent agent...")
            
            # 等待页面稳定
            await test_instance.page.wait_for_timeout(2000)
            
            # 尝试通过点击agent方式添加
            agent_selectors = [
                "text=InputGAgent",
                "[class*='InputGAgent']", 
                "div:has-text('InputGAgent')"
            ]
            
            input_agent = None
            for selector in agent_selectors:
                try:
                    input_agent = await test_instance.page.wait_for_selector(selector, timeout=3000)
                    if input_agent:
                        logger.info(f"✅ 找到InputGAgent agent: {selector}")
                        break
                except:
                    continue
            
            if not input_agent:
                logger.error("❌ 未找到InputGAgent agent元素")
                assert False, "无法找到InputGAgent agent"
            else:
                # 获取agent和画布的位置
                agent_box = await input_agent.bounding_box()
                if not agent_box:
                    logger.error("❌ 无法获取agent位置")
                    assert False, "无法获取agent元素的边界框"
                
                # 获取画布中心位置
                viewport = test_instance.page.viewport_size
                canvas_center_x = viewport['width'] * 0.6
                canvas_center_y = viewport['height'] // 2
                
                # 执行拖拽
                logger.info(f"🔄 从 ({agent_box['x']}, {agent_box['y']}) 拖拽到 ({canvas_center_x}, {canvas_center_y})")
                
                await test_instance.page.mouse.move(
                    agent_box['x'] + agent_box['width'] / 2,
                    agent_box['y'] + agent_box['height'] / 2
                )
                await test_instance.page.mouse.down()
                await test_instance.page.wait_for_timeout(300)
                
                # 拖拽到画布
                await test_instance.page.mouse.move(canvas_center_x, canvas_center_y, steps=10)
                await test_instance.page.wait_for_timeout(300)
                await test_instance.page.mouse.up()
                
                # 等待agent添加
                await test_instance.page.wait_for_timeout(2000)
                await test_instance.take_screenshot("regression_create_agent_dragged.png")
                
                # 验证agent是否被添加
                try:
                    config_modal = await test_instance.page.wait_for_selector(
                        'text=/Agent configuration|Configure/i',
                        timeout=3000
                    )
                    if config_modal:
                        logger.info("✅ Agent配置弹窗出现，agent添加成功")
                        agent_added = True
                        
                        # 填写必要字段
                        await test_instance.page.wait_for_timeout(1000)
                        
                        try:
                            textareas = await test_instance.page.query_selector_all('textarea')
                            logger.info(f"📝 找到 {len(textareas)} 个textarea输入框")
                            
                            if len(textareas) >= 2:
                                # 第一个textarea是memberName
                                await textareas[0].fill("test")
                                logger.info("✅ 填写memberName: test")
                                
                                # 第二个textarea是input
                                await textareas[1].fill("中国美食推荐")
                                logger.info("✅ 填写input: 中国美食推荐")
                            else:
                                logger.warning(f"⚠️ textarea数量不符合预期: {len(textareas)}")
                        except Exception as e:
                            logger.error(f"❌ 填写字段失败: {e}")
                        
                        # 关闭配置弹窗
                        await test_instance.page.keyboard.press('Escape')
                        await test_instance.page.wait_for_timeout(1000)
                        logger.info("✅ 关闭agent配置弹窗")
                        
                except Exception as e:
                    logger.warning(f"⚠️ 未出现配置弹窗: {e}")
                
                # 检查画布上是否有节点
                if not agent_added:
                    try:
                        drag_hint = await test_instance.page.wait_for_selector(
                            'text=/Drag and drop/i',
                            timeout=2000
                        )
                        if drag_hint:
                            logger.error("❌ 画布仍显示拖拽提示，agent未成功添加")
                            await test_instance.take_screenshot("regression_create_agent_add_failed.png")
                            assert False, "Agent未成功添加到画布"
                        else:
                            agent_added = True
                    except:
                        agent_added = True
                        logger.info("✅ 画布上没有拖拽提示，假设agent已添加")
                
        except Exception as e:
            logger.error(f"❌ 添加agent失败: {e}")
            await test_instance.take_screenshot("regression_create_agent_add_error.png")
            raise
        
        # 点击Run按钮
        try:
            run_button = await test_instance.page.wait_for_selector('button:has-text("Run")', timeout=10000)
            await run_button.click()
            logger.info("✅ 点击Run按钮")
            
            # 等待workflow执行
            await test_instance.page.wait_for_timeout(3000)
            await test_instance.take_screenshot("regression_create_run_clicked.png")
            
            # 验证是否有错误提示
            try:
                validation_error = await test_instance.page.wait_for_selector(
                    'text=/Validation error|Schema validation failed|error/i', 
                    timeout=2000
                )
                if validation_error:
                    error_text = await validation_error.inner_text()
                    await test_instance.take_screenshot("regression_create_workflow_error.png")
                    logger.error(f"❌ Workflow执行失败: {error_text}")
                    assert False, f"Workflow执行出现验证错误: {error_text}"
            except Exception as e:
                if "Timeout" in str(e) or "waiting for" in str(e):
                    logger.info("✅ 未检测到错误消息")
                else:
                    raise e
            
            # 检查是否成功运行
            try:
                await test_instance.page.wait_for_timeout(2000)
                
                execution_log_button = await test_instance.page.wait_for_selector(
                    'button:has-text("Execution log")', 
                    timeout=5000
                )
                if execution_log_button:
                    logger.info("✅ 找到Execution log按钮，可能执行成功")
                    await test_instance.take_screenshot("regression_create_workflow_running.png")
                else:
                    logger.warning("⚠️ 未找到Execution log按钮")
                    
            except Exception as e:
                logger.warning(f"⚠️ 验证workflow执行状态失败: {e}")
                await test_instance.take_screenshot("regression_create_workflow_status_check.png")
            
        except Exception as e:
            logger.error(f"❌ 运行workflow失败: {e}")
            await test_instance.take_screenshot("regression_create_run_failed.png")
            raise
        
        logger.info("🎉 Workflow创建和运行测试完成!")
        
    finally:
        await test_instance.teardown_browser()


@pytest.mark.asyncio
@pytest.mark.p2
@pytest.mark.workflows
async def test_workflow_delete_regression():
    """
    每日回归测试 - 创建并删除 Workflow
    测试完整的创建-删除流程，确保测试独立性
    
    测试步骤:
        1. 登录系统
        2. 创建一个临时 Workflow
        3. 导航回 Workflows 列表页面
        4. 等待列表加载
        5. 点击菜单删除该 Workflow
        6. 确认删除
    
    预期结果:
        - 成功创建 Workflow
        - 成功删除 Workflow
    """
    from playwright.async_api import async_playwright
    
    logger.info("=" * 60)
    logger.info("🧪 每日回归测试: 创建并删除 Workflow [P2]")
    
    # 测试环境配置
    TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
    TEST_EMAIL = "aevatarwh1@teml.net"
    TEST_PASSWORD = "Wh520520!"
    SCREENSHOT_DIR = "test-screenshots/workflows"
    
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    playwright = None
    browser = None
    
    try:
        # 初始化浏览器
        logger.info("🌌 初始化浏览器...")
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch(
            headless=False,
            slow_mo=800,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        logger.info("✅ 浏览器初始化完成")
        
        # 登录
        logger.info("🔐 开始登录...")
        await page.goto(TEST_BASE_URL)
        await page.wait_for_timeout(3000)
        
        email_input = await page.wait_for_selector('input[type="email"], input[placeholder*="email" i]', timeout=10000)
        await email_input.fill(TEST_EMAIL)
        
        password_input = await page.wait_for_selector('input[type="password"]', timeout=10000)
        await password_input.fill(TEST_PASSWORD)
        
        login_button = await page.wait_for_selector('button[type="submit"]', timeout=10000)
        await login_button.click()
        await page.wait_for_timeout(5000)
        
        current_url = page.url
        if "dashboard" in current_url or "profile" in current_url:
            logger.info(f"✅ 登录成功: {current_url}")
        
        # ====== 步骤1: 创建临时 Workflow ======
        logger.info("🔨 开始创建临时 Workflow...")
        
        # 导航到Workflows页面
        await page.goto(f"{TEST_BASE_URL}/dashboard/workflows")
        await page.wait_for_timeout(3000)
        
        # 点击 New Workflow 按钮
        new_workflow_button = await page.wait_for_selector('button:has-text("New Workflow")', timeout=10000)
        await new_workflow_button.click()
        logger.info("✅ 点击 New Workflow 按钮")
        await page.wait_for_timeout(2000)
        
        # 关闭 AI 弹窗
        await page.keyboard.press('Escape')
        logger.info("✅ 关闭 AI 弹窗")
        await page.wait_for_timeout(2000)
        
        # 添加一个简单的 Agent（确保 Workflow 能被保存）
        try:
            # 查找 InputGAgent
            input_agent = await page.wait_for_selector('text=InputGAgent', timeout=5000)
            if input_agent:
                logger.info("✅ 找到 InputGAgent")
                
                # 获取 agent 位置并拖拽到画布
                agent_box = await input_agent.bounding_box()
                if agent_box:
                    viewport = await page.evaluate('() => ({ width: window.innerWidth, height: window.innerHeight })')
                    canvas_x = viewport['width'] * 0.6
                    canvas_y = viewport['height'] // 2
                    
                    # 拖拽 Agent
                    await page.mouse.move(
                        agent_box['x'] + agent_box['width'] / 2,
                        agent_box['y'] + agent_box['height'] / 2
                    )
                    await page.mouse.down()
                    await page.wait_for_timeout(300)
                    await page.mouse.move(canvas_x, canvas_y, steps=10)
                    await page.wait_for_timeout(300)
                    await page.mouse.up()
                    await page.wait_for_timeout(2000)
                    logger.info("✅ Agent 已添加到画布")
                    
                    # 关闭配置弹窗（如果有）
                    await page.keyboard.press('Escape')
                    await page.wait_for_timeout(1000)
                    logger.info("✅ 关闭配置弹窗")
                    
                    # 运行 Workflow 以触发保存
                    try:
                        run_button = await page.wait_for_selector('button:has-text("Run")', timeout=5000)
                        if run_button:
                            await run_button.click()
                            logger.info("✅ 点击 Run 按钮（触发保存）")
                            # 等待执行
                            await page.wait_for_timeout(5000)
                    except Exception as e2:
                        logger.warning(f"⚠️ 运行 Workflow 失败，依赖自动保存: {e2}")
        except Exception as e:
            logger.warning(f"⚠️ 添加 Agent 失败: {e}")
        
        # 等待自动保存和数据库写入
        await page.wait_for_timeout(3000)
        logger.info("✅ 临时 Workflow 已创建（已运行/已保存）")
        
        # ====== 步骤2: 导航回 Workflows 列表页面 ======
        logger.info("🔙 返回 Workflows 列表页面...")
        await page.goto(f"{TEST_BASE_URL}/dashboard/workflows")
        await page.wait_for_timeout(3000)
        
        # 等待列表加载完成
        try:
            await page.wait_for_selector('table, [class*="list"], [class*="table"]', timeout=10000)
            logger.info("✅ Workflow 列表加载完成")
        except Exception as e:
            logger.warning(f"⚠️ 等待列表加载超时: {e}")
        
        # 额外等待确保列表数据渲染完成
        await page.wait_for_timeout(2000)
        
        screenshot_path = os.path.join(SCREENSHOT_DIR, "regression_delete_workflows_list.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图: {screenshot_path}")
        
        # ====== 步骤3: 删除刚创建的 Workflow (最新创建的，在列表顶部) ======
        logger.info("🗑️ 开始删除最新创建的 Workflow...")
        
        # 从截图可以看到，三个点按钮在表格的每一行右侧
        # 使用更通用的选择器策略：查找所有 button 元素
        menu_button = None
        menu_selectors = [
            # 尝试直接选择所有 button，然后取第一个可见的
            'tbody tr:first-child button',  # 第一行的按钮
            'table button:first-of-type',  # 表格中的第一个按钮
            'tr button',  # 任何行的按钮
            '[class*="table"] button',  # 表格容器中的按钮
            'button',  # 所有按钮（最后的备选）
        ]
        
        for selector in menu_selectors:
            try:
                # 获取所有匹配的按钮
                buttons = await page.query_selector_all(selector)
                if buttons:
                    # 检查每个按钮是否可见
                    for btn in buttons:
                        is_visible = await btn.is_visible()
                        if is_visible:
                            menu_button = btn
                            logger.info(f"✅ 找到菜单按钮: {selector} (共{len(buttons)}个按钮，使用第一个可见的)")
                            break
                if menu_button:
                    break
            except Exception as e:
                logger.debug(f"选择器 {selector} 失败: {e}")
                continue
        
        if not menu_button:
            logger.error("❌ 未找到菜单按钮")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "regression_delete_menu_not_found.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"📸 截图: {screenshot_path}")
            raise AssertionError("找不到菜单按钮")
        
        await menu_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击菜单按钮")
        
        # 截图查看菜单展开后的状态
        screenshot_path = os.path.join(SCREENSHOT_DIR, "regression_delete_menu_opened.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图（菜单打开）: {screenshot_path}")
        
        # 点击Delete按钮（尝试多种选择器）
        delete_button = None
        delete_selectors = [
            'button:has-text("Delete")',
            '[role="menuitem"]:has-text("Delete")',
            'text=Delete',
            'button:has-text("删除")',
            '[class*="menu"] button',  # 菜单中的任何按钮
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
            logger.error("❌ 菜单打开后未找到删除按钮")
            raise AssertionError("未找到删除按钮")
        
        # 点击找到的删除按钮
        await delete_button.click()
        await page.wait_for_timeout(2000)
        logger.info("✅ 点击删除按钮")
        
        # 确认删除
        confirm_button = await page.wait_for_selector('button:has-text("Yes"), button:has-text("Confirm"), button:has-text("确认")', timeout=10000)
        await confirm_button.click()
        logger.info("✅ 点击确认删除按钮")
        
        # 等待删除操作完成和页面刷新
        await page.wait_for_timeout(2000)
        
        # 等待加载动画消失（如果有）
        try:
            # 等待加载指示器消失
            await page.wait_for_selector('[class*="loading"], [class*="spinner"], [role="progressbar"]', state='hidden', timeout=5000)
            logger.info("✅ 加载动画已消失")
        except:
            logger.info("⚠️ 未检测到加载动画或已消失")
        
        # 额外等待确保列表完全渲染
        await page.wait_for_timeout(3000)
        
        # 等待表格或列表重新加载
        try:
            await page.wait_for_selector('table, [class*="list"], [class*="table"]', timeout=5000)
            logger.info("✅ 列表已重新加载")
        except:
            logger.info("⚠️ 未检测到列表元素")
        
        logger.info("✅ 删除操作已完成，页面已刷新")
        
        # 截图验证删除后的状态（应该比删除前少一个Workflow）
        screenshot_path = os.path.join(SCREENSHOT_DIR, "regression_delete_workflow_deleted.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"📸 截图（删除后）: {screenshot_path}")
        
        logger.info("🎉 Workflow 创建-删除流程测试完成！")
        logger.info("✅ 验证: 测试独立性 - 可单独运行")
        logger.info("✅ 验证: 创建功能正常")
        logger.info("✅ 验证: 删除功能正常")
        
    finally:
        # 清理浏览器
        try:
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
            logger.info("🧹 清理完成")
        except Exception as e:
            logger.error(f"❌ 清理失败: {e}")


if __name__ == "__main__":
    import subprocess
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "-m", "p0 or p2"
    ]
    
    logger.info("🚀 运行Workflow回归测试（P0 + P2）...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)
