"""
Pytest配置文件
定义fixtures和测试配置
"""
import pytest
import json
import logging
from pathlib import Path
from playwright.sync_api import Browser, Page, BrowserContext

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    配置浏览器上下文参数
    忽略HTTPS错误（用于localhost自签名证书）
    """
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    配置浏览器启动参数
    添加参数以解决 SSL 证书和浏览器崩溃问题
    """
    return {
        **browser_type_launch_args,
        "headless": True,
        "args": [
            "--disable-web-security",  # 禁用 Web 安全策略
            "--ignore-certificate-errors",  # 忽略证书错误
            "--allow-insecure-localhost",  # 允许不安全的 localhost
            "--disable-gpu",  # 禁用 GPU（避免某些崩溃）
            "--disable-dev-shm-usage",  # 避免共享内存问题
            "--no-sandbox",  # 禁用沙箱（已在默认参数中）
            "--disable-setuid-sandbox",  # 禁用 setuid 沙箱
        ],
    }


# 注释掉自定义page fixture，使用pytest-playwright提供的默认page fixture
# @pytest.fixture(scope="function")
# def page(context: BrowserContext) -> Page:
#     """
#     为每个测试函数创建新的页面
#     """
#     page = context.new_page()
#     logger.info(f"创建新页面: {page}")
#     
#     yield page
#     
#     # 清理：关闭页面
#     logger.info(f"关闭页面: {page}")
#     page.close()


@pytest.fixture(scope="session")
def test_data():
    """
    加载所有测试数据
    """
    data_dir = Path(__file__).parent / "test-data"
    
    test_data = {}
    
    # 加载登录数据
    with open(data_dir / "login_data.json", "r", encoding="utf-8") as f:
        login_data = json.load(f)
        test_data.update(login_data)
    
    # 加载个人信息数据
    with open(data_dir / "profile_data.json", "r", encoding="utf-8") as f:
        profile_data = json.load(f)
        test_data.update(profile_data)
    
    # 加载设置数据
    with open(data_dir / "settings_data.json", "r", encoding="utf-8") as f:
        settings_data = json.load(f)
        test_data.update(settings_data)
    
    # 加载邮件配置数据
    try:
        with open(data_dir / "email_config_data.json", "r", encoding="utf-8") as f:
            email_config_data = json.load(f)
            test_data.update(email_config_data)
    except FileNotFoundError:
        logger.warning("未找到email_config_data.json，跳过加载")
    
    # 加载注册测试数据
    try:
        with open(data_dir / "register_data.json", "r", encoding="utf-8") as f:
            register_data = json.load(f)
            test_data["register_data"] = register_data
    except FileNotFoundError:
        logger.warning("未找到register_data.json，跳过加载")
    
    logger.info(f"测试数据加载完成，包含 {len(test_data)} 个数据集")
    
    return test_data


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    自动记录测试信息
    """
    logger.info(f"开始测试: {request.node.nodeid}")
    
    yield
    
    logger.info(f"结束测试: {request.node.nodeid}")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, page: Page):
    """
    测试失败时自动截图
    """
    yield
    
    if request.node.rep_call.failed:
        screenshot_dir = Path(__file__).parent.parent.parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        
        test_name = request.node.nodeid.replace("/", "_").replace("::", "_")
        screenshot_path = screenshot_dir / f"{test_name}_failure.png"
        
        try:
            page.screenshot(path=str(screenshot_path))
            logger.info(f"失败截图已保存: {screenshot_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook用于在fixture中访问测试结果
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# Pytest标记定义
def pytest_configure(config):
    """
    注册自定义标记
    """
    config.addinivalue_line("markers", "landing: 首页相关测试")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "register: 注册相关测试")
    config.addinivalue_line("markers", "forgot_password: 忘记密码相关测试")
    config.addinivalue_line("markers", "navigation: 导航测试")
    config.addinivalue_line("markers", "responsive: 响应式测试")
    config.addinivalue_line("markers", "abp_validation: ABP框架验证测试")
    config.addinivalue_line("markers", "content: 内容测试")
    config.addinivalue_line("markers", "workflow: 工作流相关测试")
    config.addinivalue_line("markers", "profile: 个人信息相关测试")
    config.addinivalue_line("markers", "password: 密码管理相关测试")
    config.addinivalue_line("markers", "user_menu: 用户菜单相关测试")
    config.addinivalue_line("markers", "dashboard: Dashboard页面测试")
    config.addinivalue_line("markers", "settings: Settings页面测试")
    config.addinivalue_line("markers", "feature_management: Feature Management测试")
    config.addinivalue_line("markers", "security: 安全性测试")
    config.addinivalue_line("markers", "performance: 性能测试")
    config.addinivalue_line("markers", "compatibility: 兼容性测试")
    config.addinivalue_line("markers", "ux: 用户体验测试")
    config.addinivalue_line("markers", "functional: 功能测试")
    config.addinivalue_line("markers", "boundary: 边界测试")
    config.addinivalue_line("markers", "validation: 数据验证测试")
    config.addinivalue_line("markers", "exception: 异常测试")
    config.addinivalue_line("markers", "data: 数据一致性测试")
    config.addinivalue_line("markers", "ui: UI测试")
    config.addinivalue_line("markers", "usability: 可用性测试")
    config.addinivalue_line("markers", "P0: 优先级P0")
    config.addinivalue_line("markers", "P1: 优先级P1")
    config.addinivalue_line("markers", "P2: 优先级P2")


@pytest.fixture(scope="function")
def logged_in_profile_page(page, test_data):
    """登录后的个人设置页面fixture - 每个测试独立实例"""
    from tests.aevatar_station.pages.landing_page import LandingPage
    from tests.aevatar_station.pages.login_page import LoginPage
    from tests.aevatar_station.pages.profile_settings_page import ProfileSettingsPage
    
    logger.info("=== 开始登录流程 ===")
    
    # 先登录
    landing_page = LandingPage(page)
    login_page = LoginPage(page)
    
    landing_page.navigate()
    landing_page.click_sign_in()
    login_page.wait_for_load()
    
    valid_data = test_data["valid_login_data"][0]
    login_page.login(
        username=valid_data["username"],
        password=valid_data["password"]
    )
    
    # 登录方法内部已经等待完成，这里再处理一次SSL
    landing_page.handle_ssl_warning()
    
    # 验证登录成功：检查当前URL
    current_url = page.url
    logger.info(f"登录后URL: {current_url}")
    
    if "/Account/Login" in current_url or "authorize" in current_url:
        logger.error("登录后仍在登录/授权页面，会话可能未建立")
        raise Exception(f"登录失败，当前URL: {current_url}")
    
    # 导航到profile页面
    profile_page = ProfileSettingsPage(page)
    profile_page.navigate()
    
    logger.info("=== Profile 页面准备完成 ===")
    return profile_page

