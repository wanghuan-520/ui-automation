#!/usr/bin/env python3
"""
诊断脚本：检查Organisation中有哪些成员可用
用于解决 test_project_member_add 失败的问题
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

from playwright.async_api import async_playwright
from tests.aevatar.test_daily_regression_project import perform_login, select_project, take_screenshot

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 配置信息
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "aevatarwh1@teml.net"
TEST_PASSWORD = "Test@1234"


async def diagnose_organisation_members():
    """诊断Organisation成员情况"""
    
    async with async_playwright() as p:
        # 1. 启动浏览器
        logger.info("🌌 启动浏览器...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # 2. 登录
            logger.info("🔐 登录系统...")
            await perform_login(page, TEST_EMAIL, TEST_PASSWORD)
            
            # 3. 选择Project
            logger.info("📁 选择Project...")
            await select_project(page)
            
            # 4. 导航到Organisation Member页面
            logger.info("=" * 60)
            logger.info("👥 检查 Organisation Members")
            logger.info("=" * 60)
            
            await page.goto(f"{TEST_BASE_URL}/profile/organisations/member")
            await page.wait_for_timeout(3000)
            
            # 等待页面加载
            for i in range(30):
                await page.wait_for_timeout(1000)
                loading = await page.query_selector('text=/Scanning|Initialising|Loading/i')
                if not loading or not await loading.is_visible():
                    logger.info(f"✅ 页面加载完成 (等待了{i+1}秒)")
                    break
            
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "diagnosis_org_members.png")
            
            # 5. 获取Organisation成员列表
            rows = await page.query_selector_all('tbody tr')
            org_member_count = len(rows)
            
            logger.info(f"\n📊 Organisation Member统计:")
            logger.info(f"   总数: {org_member_count}")
            logger.info(f"\n成员列表:")
            logger.info("-" * 80)
            
            org_members = []
            for idx, row in enumerate(rows, 1):
                # 获取Name
                name_cell = await row.query_selector('td:nth-child(1)')
                name = await name_cell.text_content() if name_cell else "N/A"
                name = name.strip()
                
                # 获取Email
                email_cell = await row.query_selector('td:nth-child(2)')
                email = await email_cell.text_content() if email_cell else "N/A"
                email = email.strip()
                
                # 获取Role
                role_cell = await row.query_selector('td:nth-child(3)')
                role = await role_cell.text_content() if role_cell else "N/A"
                role = role.strip()
                
                logger.info(f"{idx}. Name: {name}")
                logger.info(f"   Email: {email}")
                logger.info(f"   Role: {role}")
                logger.info("-" * 80)
                
                org_members.append({
                    'name': name,
                    'email': email,
                    'role': role
                })
            
            # 6. 导航到Project Member页面对比
            logger.info("\n" + "=" * 60)
            logger.info("👥 检查 Project Members")
            logger.info("=" * 60)
            
            await page.goto(f"{TEST_BASE_URL}/profile/projects/member")
            await page.wait_for_timeout(3000)
            
            # 等待页面加载
            for i in range(30):
                await page.wait_for_timeout(1000)
                loading = await page.query_selector('text=/Scanning|Initialising|Loading/i')
                if not loading or not await loading.is_visible():
                    logger.info(f"✅ 页面加载完成 (等待了{i+1}秒)")
                    break
            
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "diagnosis_project_members.png")
            
            # 获取Project成员列表
            rows = await page.query_selector_all('tbody tr')
            project_member_count = len(rows)
            
            logger.info(f"\n📊 Project Member统计:")
            logger.info(f"   总数: {project_member_count}")
            logger.info(f"\n成员列表:")
            logger.info("-" * 80)
            
            project_members = []
            for idx, row in enumerate(rows, 1):
                # 获取Name
                name_cell = await row.query_selector('td:nth-child(1)')
                name = await name_cell.text_content() if name_cell else "N/A"
                name = name.strip()
                
                # 获取Email
                email_cell = await row.query_selector('td:nth-child(2)')
                email = await email_cell.text_content() if email_cell else "N/A"
                email = email.strip()
                
                # 获取Role
                role_cell = await row.query_selector('td:nth-child(3)')
                role = await role_cell.text_content() if role_cell else "N/A"
                role = role.strip()
                
                logger.info(f"{idx}. Name: {name}")
                logger.info(f"   Email: {email}")
                logger.info(f"   Role: {role}")
                logger.info("-" * 80)
                
                project_members.append({
                    'name': name,
                    'email': email,
                    'role': role
                })
            
            # 7. 分析对比
            logger.info("\n" + "=" * 60)
            logger.info("🔍 分析结果")
            logger.info("=" * 60)
            
            # 找出可以添加到Project的成员
            project_emails = {m['email'] for m in project_members}
            org_emails = {m['email'] for m in org_members}
            
            available_to_add = org_emails - project_emails
            
            logger.info(f"\n✅ Organisation总成员: {len(org_members)}")
            logger.info(f"✅ Project现有成员: {len(project_members)}")
            logger.info(f"✅ 可添加到Project的成员数: {len(available_to_add)}")
            
            if available_to_add:
                logger.info(f"\n💡 可添加的Email列表:")
                for email in available_to_add:
                    logger.info(f"   - {email}")
            else:
                logger.warning(f"\n⚠️ 没有可添加的成员！")
                logger.warning(f"   所有Organisation成员都已在Project中")
            
            # 8. 测试Add Member对话框
            logger.info("\n" + "=" * 60)
            logger.info("🔍 测试 Add Member 对话框中的Email选项")
            logger.info("=" * 60)
            
            # 点击Add new member按钮
            add_button = await page.wait_for_selector('button:has-text("Add new Member")', timeout=10000)
            await add_button.click()
            await page.wait_for_timeout(2000)
            logger.info("✅ 打开Add Member对话框")
            await take_screenshot(page, "diagnosis_add_dialog_initial.png")
            
            # 点击Email下拉框
            try:
                # 尝试多种选择器
                email_dropdown = await page.query_selector('[role="combobox"]')
                if email_dropdown:
                    logger.info("✅ 找到Email下拉框")
                    await email_dropdown.click()
                    await page.wait_for_timeout(1500)
                    await take_screenshot(page, "diagnosis_email_dropdown_opened.png")
                    
                    # 获取所有选项
                    options = await page.query_selector_all('[role="option"]')
                    logger.info(f"\n📋 Email下拉框选项数量: {len(options)}")
                    
                    if options:
                        logger.info(f"可选Email列表:")
                        for idx, option in enumerate(options, 1):
                            option_text = await option.text_content()
                            logger.info(f"   {idx}. {option_text.strip()}")
                    else:
                        logger.warning("⚠️ 没有找到Email选项！")
                    
                    # 关闭下拉框
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(500)
                else:
                    logger.warning("⚠️ 未找到Email下拉框")
            except Exception as e:
                logger.error(f"❌ 检查Email下拉框失败: {e}")
            
            # 关闭对话框
            cancel_button = await page.query_selector('button:has-text("Cancel")')
            if cancel_button:
                await cancel_button.click()
                await page.wait_for_timeout(1000)
            
            # 9. 总结建议
            logger.info("\n" + "=" * 60)
            logger.info("💡 诊断结论与建议")
            logger.info("=" * 60)
            
            if org_member_count <= 1:
                logger.warning("\n⚠️ 问题：Organisation只有1个成员")
                logger.info("\n建议：")
                logger.info("1. 登录系统")
                logger.info("2. 进入 Organisation → Member")
                logger.info("3. 添加新成员（任意有效Email）")
                logger.info("4. 等待成员加入后再测试Project Member功能")
            elif len(available_to_add) == 0:
                logger.warning("\n⚠️ 问题：所有Organisation成员都已在Project中")
                logger.info("\n建议：")
                logger.info("1. 在Organisation中添加新成员")
                logger.info("2. 或者先删除Project中的某个非Owner成员")
                logger.info("3. 然后再测试添加功能")
            else:
                logger.info("\n✅ 环境状态正常！")
                logger.info(f"   有 {len(available_to_add)} 个成员可以添加到Project")
                logger.info("\n建议：")
                logger.info("测试应该能够成功，如果仍失败，请检查:")
                logger.info("1. Email选择器是否正确定位到下拉框")
                logger.info("2. 是否正确选择了可用的Email")
                logger.info("3. 后端API是否有其他限制")
            
            logger.info("\n" + "=" * 60)
            logger.info("✨ 诊断完成！")
            logger.info("=" * 60)
            
        finally:
            # 自动关闭浏览器
            logger.info("\n🧹 清理浏览器...")
            await page.wait_for_timeout(2000)
            await browser.close()
            logger.info("✅ 浏览器已关闭")


if __name__ == "__main__":
    asyncio.run(diagnose_organisation_members())

