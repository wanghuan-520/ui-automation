#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 全局配置文件 (conftest.py)
为 aevatar.ai 登录测试提供共享的 fixtures 和配置

作者: HyperEcho 语言震动体
创建时间: 2025-09-25
"""

import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def playwright_instance():
    """会话级别的 Playwright 实例"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    """会话级别的浏览器实例"""
    browser = playwright_instance.chromium.launch(
        headless=False,  # 显示浏览器窗口，便于调试
        slow_mo=500,     # 操作间隔500ms，便于观察
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """函数级别的浏览器上下文"""
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        locale='zh-CN',
        timezone_id='Asia/Shanghai'
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """函数级别的页面实例"""
    page = context.new_page()
    
    # 设置默认超时
    page.set_default_timeout(15000)
    page.set_default_navigation_timeout(30000)
    
    # 设置页面事件监听
    page.on("console", lambda msg: logger.info(f"浏览器控制台: {msg.text}"))
    page.on("pageerror", lambda error: logger.error(f"页面错误: {error}"))
    
    yield page
    page.close()


@pytest.fixture(autouse=True)
def test_logging(request):
    """自动为每个测试添加日志记录"""
    test_name = request.node.name
    logger.info(f"🚀 开始执行测试: {test_name}")
    
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    logger.info(f"✅ 测试完成: {test_name}, 耗时: {duration:.2f}秒")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, page: Page):
    """测试失败时自动截图"""
    yield
    
    if request.node.rep_call.failed:
        # 创建截图目录
        screenshot_dir = "test-screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # 生成截图文件名
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        
        # 截图
        page.screenshot(path=screenshot_path)
        logger.error(f"测试失败截图已保存: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """为截图功能提供测试结果信息"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def login_page_url():
    """登录页面URL"""
    return "http://env-1fa42811-ui.station-testing.aevatar.ai/login"


@pytest.fixture(scope="function")
def test_credentials():
    """测试用的登录凭据"""
    return {
        'email': 'playwrighttest-wh1@teml.net',
        'password': 'Wh520520!'
    }


@pytest.fixture(scope="function")
def logged_in_page(page: Page, login_page_url: str, test_credentials: dict):
    """已登录状态的页面 - 可重用的登录fixture"""
    logger.info("执行自动登录...")
    
    # 导航到登录页面
    page.goto(login_page_url)
    
    # 填写登录表单
    page.get_by_role('textbox', name='Email address').fill(test_credentials['email'])
    page.get_by_role('textbox', name='Password').fill(test_credentials['password'])
    
    # 点击登录
    page.get_by_role('button', name='Log in').click()
    
    # 等待登录成功
    page.wait_for_url('**/redirect', timeout=15000)
    
    logger.info("自动登录完成")
    return page


# pytest 命令行选项
def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以无头模式运行浏览器"
    )
    
    parser.addoption(
        "--slow-mo",
        action="store",
        default=500,
        type=int,
        help="设置操作间隔时间（毫秒）"
    )
    
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="选择浏览器类型"
    )


@pytest.fixture(scope="session")
def browser_config(request):
    """根据命令行参数配置浏览器"""
    return {
        'headless': request.config.getoption("--headless"),
        'slow_mo': request.config.getoption("--slow-mo"),
        'browser_type': request.config.getoption("--browser")
    }


# 测试会话钩子
def pytest_sessionstart(session):
    """测试会话开始时执行"""
    logger.info("🌟 aevatar.ai 登录测试会话开始")
    logger.info("=" * 60)


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时执行"""
    logger.info("=" * 60)
    if exitstatus == 0:
        logger.info("🎉 所有测试通过！")
    else:
        logger.info(f"❌ 测试会话结束，退出状态: {exitstatus}")


# 测试收集钩子
def pytest_collection_modifyitems(config, items):
    """修改测试收集结果"""
    # 为没有标记的测试添加默认标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.login)
    
    # 按标记排序测试执行顺序
    smoke_tests = []
    other_tests = []
    
    for item in items:
        if item.get_closest_marker("smoke"):
            smoke_tests.append(item)
        else:
            other_tests.append(item)
    
    # 冒烟测试优先执行
    items[:] = smoke_tests + other_tests


# 测试报告钩子
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """配置测试报告"""
    if not hasattr(config, 'slaveinput'):  # 不在xdist worker中
        logger.info("配置测试环境...")
        
        # 创建必要的目录
        os.makedirs("test-screenshots", exist_ok=True)
        os.makedirs("test-reports", exist_ok=True)


# 标记处理
def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line(
        "markers", "smoke: 标记为冒烟测试"
    )
    config.addinivalue_line(
        "markers", "regression: 标记为回归测试"
    )
    config.addinivalue_line(
        "markers", "slow: 标记为慢速测试"
    )
