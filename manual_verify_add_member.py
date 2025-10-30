#!/usr/bin/env python3
"""
手动验证脚本：保持浏览器打开，让用户手动验证添加Member的流程
"""

import asyncio
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from tests.aevatar.test_daily_regression_project import perform_login, select_project

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)8s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "aevatarwh1@teml.net"
TEST_PASSWORD = "Test@1234"


async def manual_verify():
    """打开浏览器让用户手动验证"""
    
    async with async_playwright() as p:
        logger.info("=" * 80)
        logger.info("🔍 手动验证：Add Member流程")
        logger.info("=" * 80)
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            # 登录
            logger.info("\n1️⃣ 登录系统...")
            await perform_login(page, TEST_EMAIL, TEST_PASSWORD)
            logger.info("✅ 登录成功")
            
            # 选择Project
            logger.info("\n2️⃣ 选择Project...")
            await select_project(page)
            logger.info("✅ Project选择成功")
            
            # 打开Organisation Member页面
            logger.info("\n3️⃣ 打开Organisation Member页面...")
            await page.goto(f"{TEST_BASE_URL}/profile/organisations/member")
            await page.wait_for_timeout(5000)
            logger.info("✅ 请查看Organisation中有哪些成员")
            
            input("\n按Enter键继续到Project Member页面...")
            
            # 打开Project Member页面
            logger.info("\n4️⃣ 打开Project Member页面...")
            await page.goto(f"{TEST_BASE_URL}/profile/projects/member")
            await page.wait_for_timeout(5000)
            logger.info("✅ 请尝试手动添加member")
            
            logger.info("\n" + "=" * 80)
            logger.info("📝 请手动执行以下步骤:")
            logger.info("=" * 80)
            logger.info("1. 点击右上角 'Add new member' 按钮")
            logger.info("2. 在 'Add team members' 对话框中:")
            logger.info("   - 查看Email下拉框中有哪些选项")
            logger.info("   - 选择一个Email")
            logger.info("   - 选择Role为Reader")
            logger.info("   - 点击右下角 'Add' 按钮")
            logger.info("3. 观察:")
            logger.info("   - 是否有Toast提示？")
            logger.info("   - 是否有错误提示？")
            logger.info("   - Member列表是否增加了？")
            logger.info("=" * 80)
            
            input("\n完成手动测试后按Enter键关闭...")
            
        finally:
            await browser.close()
            logger.info("\n✅ 浏览器已关闭")


if __name__ == "__main__":
    logger.info("\n🎯 这个脚本将打开浏览器让你手动验证添加Member的流程")
    logger.info("   请观察实际的Add流程是否有任何错误提示\n")
    asyncio.run(manual_verify())

