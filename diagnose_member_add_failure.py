#!/usr/bin/env python3
"""
深度诊断：为什么 aevatarwh2@teml.net 无法添加到Project
对比Organisation和Project的成员列表，找出根本原因
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


async def diagnose_member_issue():
    """深度诊断成员添加失败的原因"""
    
    async with async_playwright() as p:
        logger.info("=" * 80)
        logger.info("🔍 深度诊断：Member添加失败根因分析")
        logger.info("=" * 80)
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # 登录
            logger.info("\n1️⃣ 登录系统...")
            await perform_login(page, TEST_EMAIL, TEST_PASSWORD)
            
            # 选择Project
            logger.info("2️⃣ 选择Project...")
            await select_project(page)
            
            # ========== 步骤1: 检查Organisation Members ==========
            logger.info("\n" + "=" * 80)
            logger.info("📋 步骤1: 检查 Organisation Members")
            logger.info("=" * 80)
            
            await page.goto(f"{TEST_BASE_URL}/profile/organisations/member")
            await page.wait_for_timeout(3000)
            
            # 等待加载
            for i in range(30):
                await page.wait_for_timeout(1000)
                loading = await page.query_selector('text=/Scanning|Initialising|Loading/i')
                if not loading or not await loading.is_visible():
                    logger.info(f"✅ Organisation Member页面加载完成 (等待了{i+1}秒)")
                    break
            
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "diag_org_members.png")
            
            # 获取Organisation成员列表
            org_rows = await page.query_selector_all('tbody tr')
            logger.info(f"\n📊 Organisation Member总数: {len(org_rows)}")
            
            org_members = []
            for idx, row in enumerate(org_rows, 1):
                try:
                    cells = await row.query_selector_all('td')
                    if len(cells) >= 3:
                        name = await cells[0].text_content() or ""
                        email = await cells[1].text_content() or ""
                        role = await cells[2].text_content() or ""
                        
                        name = name.strip()
                        email = email.strip()
                        role = role.strip()
                        
                        org_members.append({
                            'name': name,
                            'email': email,
                            'role': role
                        })
                        
                        logger.info(f"{idx}. {email} ({role})")
                except Exception as e:
                    logger.warning(f"⚠️ 解析第{idx}行失败: {e}")
            
            # ========== 步骤2: 检查Project Members ==========
            logger.info("\n" + "=" * 80)
            logger.info("📋 步骤2: 检查 Project Members")
            logger.info("=" * 80)
            
            await page.goto(f"{TEST_BASE_URL}/profile/projects/member")
            await page.wait_for_timeout(3000)
            
            # 等待加载
            for i in range(30):
                await page.wait_for_timeout(1000)
                loading = await page.query_selector('text=/Scanning|Initialising|Loading/i')
                if not loading or not await loading.is_visible():
                    logger.info(f"✅ Project Member页面加载完成 (等待了{i+1}秒)")
                    break
            
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "diag_project_members.png")
            
            # 获取Project成员列表
            project_rows = await page.query_selector_all('tbody tr')
            logger.info(f"\n📊 Project Member总数: {len(project_rows)}")
            
            project_members = []
            for idx, row in enumerate(project_rows, 1):
                try:
                    cells = await row.query_selector_all('td')
                    if len(cells) >= 3:
                        name = await cells[0].text_content() or ""
                        email = await cells[1].text_content() or ""
                        role = await cells[2].text_content() or ""
                        
                        name = name.strip()
                        email = email.strip()
                        role = role.strip()
                        
                        project_members.append({
                            'name': name,
                            'email': email,
                            'role': role
                        })
                        
                        logger.info(f"{idx}. {email} ({role})")
                except Exception as e:
                    logger.warning(f"⚠️ 解析第{idx}行失败: {e}")
            
            # ========== 步骤3: 对比分析 ==========
            logger.info("\n" + "=" * 80)
            logger.info("🔍 步骤3: 对比分析")
            logger.info("=" * 80)
            
            org_emails = {m['email'] for m in org_members}
            project_emails = {m['email'] for m in project_members}
            
            # 可以添加的Email
            available_emails = org_emails - project_emails
            
            logger.info(f"\n✅ Organisation成员: {len(org_emails)}")
            for email in sorted(org_emails):
                logger.info(f"   - {email}")
            
            logger.info(f"\n✅ Project成员: {len(project_emails)}")
            for email in sorted(project_emails):
                logger.info(f"   - {email}")
            
            logger.info(f"\n💡 可添加到Project的Email: {len(available_emails)}")
            if available_emails:
                for email in sorted(available_emails):
                    logger.info(f"   ✅ {email}")
            else:
                logger.warning("   ⚠️ 没有可添加的Email（所有Organisation成员都已在Project中）")
            
            # 检查目标Email
            target_email = "aevatarwh2@teml.net"
            logger.info(f"\n🎯 检查目标Email: {target_email}")
            
            if target_email in org_emails:
                logger.info(f"   ✅ 在Organisation中")
            else:
                logger.error(f"   ❌ 不在Organisation中！")
            
            if target_email in project_emails:
                logger.warning(f"   ⚠️ 已经在Project中！")
                # 找到该member的详细信息
                for m in project_members:
                    if m['email'] == target_email:
                        logger.info(f"      Name: {m['name']}")
                        logger.info(f"      Role: {m['role']}")
            else:
                logger.info(f"   ✅ 不在Project中（可以添加）")
            
            # ========== 步骤4: 实际测试添加流程 ==========
            logger.info("\n" + "=" * 80)
            logger.info("🧪 步骤4: 实际测试添加流程")
            logger.info("=" * 80)
            
            # 打开Add Member对话框
            logger.info("\n4.1 打开Add Member对话框...")
            add_button = await page.wait_for_selector('button:has-text("Add new Member")', timeout=10000)
            await add_button.click()
            await page.wait_for_timeout(2000)
            await take_screenshot(page, "diag_dialog_opened.png")
            logger.info("   ✅ 对话框已打开")
            
            # 检查Email下拉框
            logger.info("\n4.2 检查Email下拉框...")
            email_dropdown = await page.query_selector('[role="combobox"]')
            if email_dropdown:
                logger.info("   ✅ 找到Email下拉框")
                
                current_text = await email_dropdown.text_content() or ""
                logger.info(f"   当前显示: {current_text.strip()}")
                
                # 打开下拉框
                await email_dropdown.click()
                await page.wait_for_timeout(1500)
                await take_screenshot(page, "diag_dropdown_opened.png")
                
                # 获取选项
                options = await page.query_selector_all('[role="option"]')
                logger.info(f"   📋 选项数量: {len(options)}")
                
                dialog_emails = []
                for idx, option in enumerate(options, 1):
                    option_text = await option.text_content() or ""
                    option_text = option_text.strip()
                    dialog_emails.append(option_text)
                    
                    is_target = "✅" if target_email in option_text else "  "
                    logger.info(f"   {is_target} {idx}. {option_text}")
                
                # 检查目标Email是否在选项中
                target_in_dialog = any(target_email in email for email in dialog_emails)
                
                if target_in_dialog:
                    logger.info(f"\n   ✅ {target_email} 在可选列表中")
                else:
                    logger.error(f"\n   ❌ {target_email} 不在可选列表中！")
                    logger.error("   这说明该Email虽然在Organisation中，但不能添加到Project")
                
                # 关闭下拉框
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)
            else:
                logger.error("   ❌ 未找到Email下拉框")
            
            # 关闭对话框
            cancel_button = await page.query_selector('button:has-text("Cancel")')
            if cancel_button:
                await cancel_button.click()
                await page.wait_for_timeout(1000)
            
            # ========== 步骤5: 结论与建议 ==========
            logger.info("\n" + "=" * 80)
            logger.info("📊 步骤5: 诊断结论")
            logger.info("=" * 80)
            
            logger.info(f"\n数据汇总:")
            logger.info(f"  Organisation成员: {len(org_members)}")
            logger.info(f"  Project成员: {len(project_members)}")
            logger.info(f"  理论可添加: {len(available_emails)}")
            
            # 判断根本原因
            if target_email not in org_emails:
                logger.error(f"\n❌ 根本原因: {target_email} 不在Organisation中")
                logger.info("\n💡 解决方案:")
                logger.info("  1. 在Organisation中添加该Email")
                logger.info("  2. 或使用其他已在Organisation中的Email测试")
            
            elif target_email in project_emails:
                logger.warning(f"\n⚠️ 根本原因: {target_email} 已经是Project member")
                logger.info("\n💡 解决方案:")
                logger.info("  1. 先删除该member")
                logger.info("  2. 然后再测试添加功能")
                logger.info("  3. 或使用其他Email测试")
            
            elif len(available_emails) == 0:
                logger.warning(f"\n⚠️ 根本原因: 所有Organisation成员都已在Project中")
                logger.info("\n💡 解决方案:")
                logger.info("  1. 在Organisation中添加新成员")
                logger.info("  2. 然后测试将新成员添加到Project")
            
            elif target_email in dialog_emails:
                logger.info(f"\n✅ {target_email} 应该可以添加")
                logger.warning("但实际测试中添加失败，可能原因:")
                logger.info("  1. 需要特殊权限或配置")
                logger.info("  2. 后端有其他业务规则限制")
                logger.info("  3. 需要先发送邀请而不是直接添加")
                logger.info("\n💡 建议:")
                logger.info("  手动测试一次，观察是否有错误提示或特殊流程")
            
            else:
                logger.error(f"\n❌ {target_email} 在Organisation中但不在对话框选项中")
                logger.info("这说明存在某种过滤规则，可能:")
                logger.info("  1. Email状态不对（pending/inactive）")
                logger.info("  2. 权限不足")
                logger.info("  3. 其他业务规则")
            
            logger.info("\n" + "=" * 80)
            logger.info("✨ 诊断完成！")
            logger.info("=" * 80)
            
        finally:
            logger.info("\n🧹 清理...")
            await page.wait_for_timeout(2000)
            await browser.close()
            logger.info("✅ 浏览器已关闭")


if __name__ == "__main__":
    asyncio.run(diagnose_member_issue())

