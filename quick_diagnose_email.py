#!/usr/bin/env python3
"""
快速诊断：检查Add Member对话框中的Email选项
专注于解决test_project_member_add的Email选择问题
"""

import asyncio
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from tests.aevatar.test_daily_regression_project import perform_login, select_project, take_screenshot

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 配置信息
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "aevatarwh1@teml.net"
TEST_PASSWORD = "Test@1234"


async def quick_diagnose():
    """快速诊断Email选择问题"""
    
    async with async_playwright() as p:
        logger.info("=" * 70)
        logger.info("🔍 快速诊断：Add Member对话框Email选项")
        logger.info("=" * 70)
        
        # 启动浏览器（headless模式避免资源问题）
        logger.info("\n1️⃣ 启动浏览器...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # 登录
            logger.info("2️⃣ 登录系统...")
            await perform_login(page, TEST_EMAIL, TEST_PASSWORD)
            
            # 选择Project
            logger.info("3️⃣ 选择Project...")
            await select_project(page)
            
            # 导航到Project Member页面
            logger.info("4️⃣ 导航到Project Member页面...")
            await page.goto(f"{TEST_BASE_URL}/profile/projects/member")
            await page.wait_for_timeout(3000)
            
            # 等待页面加载
            for i in range(30):
                await page.wait_for_timeout(1000)
                loading = await page.query_selector('text=/Scanning|Initialising|Loading/i')
                if not loading or not await loading.is_visible():
                    logger.info(f"   ✅ 页面加载完成 (等待了{i+1}秒)")
                    break
            
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "quick_diag_member_list.png")
            
            # 获取当前Member数量
            rows = await page.query_selector_all('tbody tr')
            logger.info(f"   📊 当前Member数量: {len(rows)}")
            
            # 打开Add Member对话框
            logger.info("\n5️⃣ 打开Add Member对话框...")
            add_button = await page.wait_for_selector('button:has-text("Add new Member")', timeout=10000)
            await add_button.click()
            await page.wait_for_timeout(2000)
            logger.info("   ✅ 对话框已打开")
            await take_screenshot(page, "quick_diag_dialog_opened.png")
            
            # 核心诊断：检查Email下拉框
            logger.info("\n6️⃣ 诊断Email下拉框...")
            logger.info("-" * 70)
            
            # 尝试方案1：找第一个combobox
            logger.info("   方案1: 查找第一个 [role='combobox']")
            email_dropdown = await page.query_selector('[role="combobox"]')
            if email_dropdown:
                logger.info("   ✅ 找到下拉框")
                
                # 获取当前显示的值
                current_text = await email_dropdown.text_content() or ""
                logger.info(f"   📝 当前显示: '{current_text.strip()}'")
                
                # 点击打开下拉框
                logger.info("   🖱️ 点击打开下拉框...")
                await email_dropdown.click()
                await page.wait_for_timeout(1500)
                await take_screenshot(page, "quick_diag_dropdown_opened.png")
                
                # 获取所有选项
                options = await page.query_selector_all('[role="option"]')
                logger.info(f"   📋 选项数量: {len(options)}")
                
                if options:
                    logger.info("   可选Email列表:")
                    for idx, option in enumerate(options, 1):
                        option_text = await option.text_content() or ""
                        logger.info(f"      {idx}. {option_text.strip()}")
                    
                    # 检查目标Email
                    logger.info("\n   🎯 检查目标Email: aevatarwh2@teml.net")
                    found_target = False
                    for idx, option in enumerate(options):
                        option_text = await option.text_content() or ""
                        if "aevatarwh2" in option_text:
                            logger.info(f"      ✅ 找到目标Email在选项{idx+1}")
                            found_target = True
                            break
                    
                    if not found_target:
                        logger.warning("      ⚠️ 未找到aevatarwh2@teml.net")
                        logger.info("      这意味着该Email可能不在Organisation中")
                    
                    # 关闭下拉框
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(500)
                else:
                    logger.warning("   ⚠️ 没有找到任何选项！")
                    logger.info("   这说明Email下拉框为空")
            else:
                logger.error("   ❌ 未找到Email下拉框")
            
            logger.info("-" * 70)
            
            # 尝试方案2：检查所有combobox
            logger.info("\n   方案2: 检查所有 combobox")
            all_comboboxes = await page.query_selector_all('[role="combobox"]')
            logger.info(f"   共找到 {len(all_comboboxes)} 个下拉框")
            
            for idx, combo in enumerate(all_comboboxes, 1):
                combo_text = await combo.text_content() or ""
                logger.info(f"   {idx}. {combo_text.strip()}")
            
            # 检查对话框的HTML结构
            logger.info("\n7️⃣ 检查对话框HTML结构...")
            dialog = await page.query_selector('text="Add team members"')
            if dialog:
                dialog_parent = await dialog.evaluate('el => el.closest("[role=\\"dialog\\"]") || el.closest(".modal") || el.parentElement.parentElement.parentElement')
                if dialog_parent:
                    # 获取对话框内的所有input
                    inputs = await page.query_selector_all('[role="dialog"] input, .modal input')
                    logger.info(f"   找到 {len(inputs)} 个input元素")
                    
                    for idx, inp in enumerate(inputs[:5], 1):  # 只看前5个
                        inp_type = await inp.get_attribute('type') or 'text'
                        inp_placeholder = await inp.get_attribute('placeholder') or ''
                        inp_name = await inp.get_attribute('name') or ''
                        logger.info(f"   {idx}. type={inp_type}, name={inp_name}, placeholder={inp_placeholder}")
            
            # 关闭对话框
            logger.info("\n8️⃣ 关闭对话框...")
            cancel_button = await page.query_selector('button:has-text("Cancel")')
            if cancel_button:
                await cancel_button.click()
                await page.wait_for_timeout(1000)
                logger.info("   ✅ 对话框已关闭")
            
            # 总结
            logger.info("\n" + "=" * 70)
            logger.info("📊 诊断总结")
            logger.info("=" * 70)
            
            if email_dropdown and options and len(options) > 0:
                logger.info("✅ Email下拉框工作正常")
                logger.info(f"✅ 找到 {len(options)} 个可选Email")
                
                # 检查是否有aevatarwh2
                target_found = any("aevatarwh2" in (await opt.text_content() or "") for opt in options)
                if target_found:
                    logger.info("✅ aevatarwh2@teml.net 在可选列表中")
                    logger.info("\n💡 建议：测试代码应该能够选择该Email")
                    logger.info("   问题可能在于：")
                    logger.info("   1. 选择器定位不准确")
                    logger.info("   2. 选项点击失败")
                    logger.info("   3. 后端API拒绝添加")
                else:
                    logger.warning("⚠️ aevatarwh2@teml.net 不在可选列表中")
                    logger.info("\n💡 解决方案：")
                    logger.info("   1. 在Organisation中添加 aevatarwh2@teml.net")
                    logger.info("   2. 或者使用可选列表中的其他Email")
            else:
                logger.error("❌ Email下拉框异常")
                logger.info("\n💡 问题：")
                logger.info("   1. 下拉框定位失败")
                logger.info("   2. 或者没有可选Email（Organisation中只有Owner）")
            
            logger.info("=" * 70)
            
        finally:
            # 关闭浏览器
            logger.info("\n🧹 清理...")
            await page.wait_for_timeout(2000)
            await browser.close()
            logger.info("✅ 完成！")


if __name__ == "__main__":
    asyncio.run(quick_diagnose())

