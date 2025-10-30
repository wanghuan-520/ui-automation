#!/usr/bin/env python3
"""
Aevatar 登录回归测试
每日回归测试 - P0 核心登录功能
"""

import logging
import sys
import os
import pytest

logger = logging.getLogger(__name__)


# ========== 每日回归测试 - 简单直接的登录验证 ==========

@pytest.mark.asyncio
@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.p0
async def test_daily_regression_login():
    """
    每日回归测试 - 简单直接的登录验证
    不使用数据驱动，直接测试核心登录流程
    
    测试步骤:
        1. 打开登录页面
        2. 输入邮箱和密码
        3. 点击登录按钮
        4. 验证登录成功（URL跳转）
        5. 等待Workflow页面加载
    
    预期结果:
        - 成功跳转到dashboard页面
        - Workflow列表页面加载完成
    """
    from base_test import AevatarPytestTest
    
    logger.info("=" * 60)
    logger.info("🧪 每日回归测试: 简单登录验证")
    
    test_instance = AevatarPytestTest()
    
    try:
        await test_instance.setup_browser()
        
        # 导航到登录页面
        await test_instance.page.goto(test_instance.LOGIN_URL)
        await test_instance.take_screenshot("regression_login_page.png")
        logger.info("✅ 导航到登录页面")
        
        # 等待页面加载
        await test_instance.page.wait_for_timeout(3000)
        
        # 填写邮箱 - 尝试多种选择器
        email_input = None
        selectors = [
            'input[type="email"]',
            'input[name="email"]',
            'input[placeholder*="email" i]',
            'input[placeholder*="邮箱" i]',
            'input[placeholder*="Email" i]',
            'input[data-testid*="email" i]',
            'input[id*="email" i]'
        ]
        
        for selector in selectors:
            try:
                email_input = await test_instance.page.wait_for_selector(selector, timeout=3000)
                if email_input:
                    logger.info(f"✅ 找到邮箱输入框: {selector}")
                    break
            except:
                continue
        
        assert email_input, "未找到邮箱输入框"
        await email_input.fill(test_instance.EMAIL)
        logger.info(f"✅ 邮箱输入完成: {test_instance.EMAIL}")
        
        # 填写密码
        password_input = await test_instance.page.wait_for_selector('input[type="password"]', timeout=10000)
        await password_input.fill(test_instance.PASSWORD)
        logger.info("✅ 密码输入完成")
        
        await test_instance.take_screenshot("regression_form_filled.png")
        
        # 点击登录按钮
        login_button = await test_instance.page.wait_for_selector('button[type="submit"]', timeout=10000)
        await login_button.click()
        logger.info("✅ 登录按钮已点击")
        
        # 等待跳转到dashboard页面
        await test_instance.page.wait_for_timeout(3000)
        
        # 检查是否登录成功
        current_url = test_instance.page.url
        logger.info(f"📍 当前URL: {current_url}")
        
        assert "redirect" in current_url or "dashboard" in current_url, f"登录失败，当前URL: {current_url}"
        logger.info("✅ 登录成功，已跳转到dashboard")
        
        # 等待Workflow页面列表加载完成
        try:
            # 等待页面内容加载（等待主要内容区域）
            await test_instance.page.wait_for_selector(
                'main, [role="main"], .content, .workflow-list, table, [class*="table"], [class*="list"]',
                timeout=10000
            )
            logger.info("✅ 页面主要内容已加载")
            
            # 额外等待一下，确保列表数据渲染完成
            await test_instance.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.warning(f"⚠️ 等待列表元素超时，继续截图: {e}")
        
        # 截图：显示登录成功后的Workflow列表页面
        await test_instance.take_screenshot("regression_workflow_list_loaded.png")
        logger.info("📸 已截图Workflow列表页面")
        logger.info("🎉 每日回归登录测试完成!")
        
    finally:
        await test_instance.teardown_browser()


if __name__ == "__main__":
    import subprocess
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "-m", "p0"
    ]
    
    logger.info("🚀 运行Login回归测试（P0）...")
    result = subprocess.run(pytest_args)
    sys.exit(result.returncode)
