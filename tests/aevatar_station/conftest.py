"""
Pytest配置文件
定义fixtures和测试配置
"""
import pytest
import json
import logging
from pathlib import Path
from playwright.sync_api import Browser, Page, BrowserContext

def pytest_sessionstart(session):
    """
    【HyperEcho 守护】
    在所有测试开始前运行一次。
    功能：检查账号池，剔除被污染的账号，补充新账号，保证有20个健康账号
    """
    # 仅在主进程执行（避免 xdist worker 进程重复执行）
    if not hasattr(session.config, 'workerinput'):
        import subprocess
        import sys
        
        # 定位脚本路径：tests/aevatar_station/conftest.py -> aevatar_station -> tests -> root
        root_dir = Path(__file__).parent.parent.parent
        script_path = root_dir / "scripts" / "clean_and_refill_account_pool.py"
        
        if script_path.exists():
            try:
                subprocess.run([sys.executable, str(script_path)], check=True)
            except Exception as e:
                print(f"⚠️ [HyperEcho] 账号池清洗失败: {e}")
        else:
            print(f"⚠️ [HyperEcho] 未找到清洗脚本: {script_path}")

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
    ⚡ 性能优化：减小viewport尺寸以提升性能
    ⚡ 并行执行优化：添加超时和重试配置
    """
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1280, "height": 720},  # ⚡ 性能优化：减小分辨率（1920x1080 → 1280x720）
        "screen": {"width": 1280, "height": 720},  # ⚡ 性能优化：同步屏幕尺寸
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    配置浏览器启动参数
    添加参数以解决 SSL 证书和浏览器崩溃问题
    ⚡ 性能优化：已启用headless模式和性能优化参数
    ⚡ 并行执行优化：添加稳定性参数，减少浏览器崩溃
    """
    return {
        **browser_type_launch_args,
        "headless": True,  # ⚡ 性能优化：启用headless模式
        "timeout": 60000,  # ⚡ 并行执行优化：增加浏览器启动超时（60秒）
        "args": [
            "--disable-web-security",  # 禁用 Web 安全策略
            "--ignore-certificate-errors",  # 忽略证书错误
            "--allow-insecure-localhost",  # 允许不安全的 localhost
            "--disable-gpu",  # 禁用 GPU（避免某些崩溃）
            "--disable-dev-shm-usage",  # 避免共享内存问题
            "--no-sandbox",  # 禁用沙箱
            "--disable-setuid-sandbox",  # 禁用 setuid 沙箱
            # ⚡ 并行执行优化：添加稳定性参数
            "--disable-background-networking",  # 禁用后台网络请求
            "--disable-background-timer-throttling",  # 禁用后台定时器节流
            "--disable-renderer-backgrounding",  # 禁用渲染器后台化
            "--disable-backgrounding-occluded-windows",  # 禁用被遮挡窗口的后台化
            "--disable-ipc-flooding-protection",  # 禁用IPC洪水保护
            "--disable-popup-blocking", # 禁用弹窗拦截
            "--disable-notifications", # 禁用通知
            "--disable-infobars", # 禁用信息栏
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    处理测试报告，捕获浏览器关闭错误
    ⚡ 并行执行优化：优雅处理TargetClosedError
    Hook用于在fixture中访问测试结果
    """
    outcome = yield
    rep = outcome.get_result()
    
    # 存储测试结果到item，供fixture使用
    setattr(item, f"rep_{rep.when}", rep)
    
    # 如果是setup阶段出错且是TargetClosedError，记录警告
    if rep.when == "setup" and rep.failed:
        error_str = str(rep.longrepr) if rep.longrepr else ""
        if "TargetClosedError" in error_str or "Target page, context or browser has been closed" in error_str:
            logger.warning(f"⚠️ 测试 {item.nodeid} 在setup阶段遇到浏览器关闭错误，可能是并行执行冲突")
            logger.warning(f"   错误详情: {error_str[:200]}")
            # 不修改报告状态，让pytest正常处理


@pytest.fixture(scope="function")
def screenshot_on_failure(request, page: Page):
    """
    测试失败时自动截图
    """
    yield
    
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_dir = Path(__file__).parent.parent.parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        
        test_name = request.node.nodeid.replace("/", "_").replace("::", "_")
        screenshot_path = screenshot_dir / f"{test_name}_failure.png"
        
        try:
            page.screenshot(path=str(screenshot_path))
            logger.info(f"失败截图已保存: {screenshot_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")


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


def get_test_account_from_pool(worker_id=None):
    """
    ⚡ 阶段2优化：从测试账号池获取账号（避免每次注册产生脏数据）
    ⚡ 并发安全：使用文件锁防止并发访问冲突
    
    Args:
        worker_id: pytest-xdist的worker ID（用于并行执行时分配不同账号）
    
    Returns:
        tuple: (username, email, password) 或 None（如果池中无可用账号）
    """
    import json
    import os
    import time
    from pathlib import Path
    from datetime import datetime
    
    # 尝试导入文件锁模块（Unix系统使用fcntl，Windows使用msvcrt）
    try:
        import fcntl
        use_lock = True
    except ImportError:
        try:
            import msvcrt
            use_lock = True
        except ImportError:
            use_lock = False
            logger.warning("  无法导入文件锁模块，并发访问可能不安全")
    
    pool_file = Path(__file__).parent / "test-data" / "test_account_pool.json"
    
    # 如果账号池文件不存在，返回None（回退到自动注册）
    if not pool_file.exists():
        logger.warning("  测试账号池文件不存在，将使用自动注册")
        return None
    
    max_retries = 5
    retry_delay = 0.1  # 100ms
    
    for attempt in range(max_retries):
        try:
            # 使用文件锁打开文件（读写模式）
            with open(pool_file, "r+", encoding="utf-8") as f:
                # 尝试获取排他锁（非阻塞）
                if use_lock:
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except (IOError, OSError):
                        # 如果无法获取锁，等待后重试
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                        else:
                            logger.warning(f"  无法获取文件锁（尝试 {attempt + 1}/{max_retries}），将使用自动注册")
                            return None
                
                # 读取文件内容
                f.seek(0)  # 确保从文件开头读取
                pool_data = json.load(f)
        
                accounts = pool_data.get("test_account_pool", [])
                config = pool_data.get("pool_config", {})
        
                # ⚡ 改进：寻找第一个可用且未锁定的账号
                # 而不是基于worker_id固定分配（避免账号锁定导致测试失败）
                account = None
                account_idx = -1
                
                # 优先策略：找到第一个未使用且未锁定的账号
                for idx, acc in enumerate(accounts):
                    is_locked = acc.get("is_locked", False)
                    in_use = acc.get("in_use", False)
                    
                    if not is_locked and not in_use:
                        account = acc
                        account_idx = idx
                        logger.info(f"  ✅ 找到可用账号: {acc['username']} (索引: {idx}, 未锁定, 未使用)")
                        break
                
                # 如果没有未使用的账号，尝试复用最早使用的账号（但必须未锁定）
                if not account:
                    logger.warning("  ⚠️ 所有账号都在使用中，尝试复用未锁定的账号...")
                    for idx, acc in enumerate(accounts):
                        is_locked = acc.get("is_locked", False)
                        if not is_locked:
                            account = acc
                            account_idx = idx
                            logger.info(f"  ⚡ 复用账号: {acc['username']} (索引: {idx}, 未锁定)")
                            break
                
                # 如果仍然没有账号（所有账号都被锁定），返回None触发自动注册
                if not account:
                    logger.warning("  ❌ 所有账号都被锁定，将使用自动注册")
                    return None
        
                # 更新使用状态
                account["in_use"] = True
                account["last_used"] = datetime.now().isoformat()
        
                # 写入更新后的池数据
                f.seek(0)  # 回到文件开头
                f.truncate()  # 清空文件内容
                json.dump(pool_data, f, indent=2, ensure_ascii=False)
                f.flush()  # 确保数据写入磁盘
                
                # 释放锁（文件关闭时自动释放）
        
            logger.info(f"  ✅ 从账号池获取账号: {account['username']} (索引: {account_idx})")
            return (account["username"], account["email"], account["password"])
        
        except json.JSONDecodeError as e:
            # JSON解析错误，可能是文件正在被写入
            if attempt < max_retries - 1:
                logger.warning(f"  JSON解析失败（尝试 {attempt + 1}/{max_retries}）: {e}，重试...")
                time.sleep(retry_delay * (attempt + 1))
                continue
            else:
                logger.warning(f"  从账号池获取账号失败（JSON解析错误）: {e}，将使用自动注册")
                return None
        except Exception as e:
            logger.warning(f"  从账号池获取账号失败: {e}，将使用自动注册")
            return None
    
    return None


def mark_account_as_locked(username, reason=None):
    """
    ⚡ 账号锁定管理：标记账号为已锁定状态
    ⚡ 并发安全：使用文件锁防止并发访问冲突
    
    Args:
        username: 要标记为锁定的账号用户名
        reason: 锁定原因（可选）
    """
    import json
    import time
    from pathlib import Path
    
    # 尝试导入文件锁模块
    try:
        import fcntl
        use_lock = True
    except ImportError:
        try:
            import msvcrt
            use_lock = True
        except ImportError:
            use_lock = False
            logger.warning("  无法导入文件锁模块，并发访问可能不安全")
    
    pool_file = Path(__file__).parent / "test-data" / "test_account_pool.json"
    
    if not pool_file.exists():
        logger.warning(f"  测试账号池文件不存在，无法标记账号 {username} 为锁定")
        return
    
    max_retries = 5
    retry_delay = 0.1  # 100ms
    
    for attempt in range(max_retries):
        try:
            with open(pool_file, "r+", encoding="utf-8") as f:
                # 尝试获取排他锁（非阻塞）
                if use_lock:
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except (IOError, OSError):
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                        else:
                            logger.warning(f"  无法获取文件锁（尝试 {attempt + 1}/{max_retries}），无法标记账号 {username} 为锁定")
                            return
                
                # 读取文件内容
                f.seek(0)
                pool_data = json.load(f)
                
                accounts = pool_data.get("test_account_pool", [])
                
                # 查找并标记账号
                account_found = False
                for account in accounts:
                    if account["username"] == username:
                        account["is_locked"] = True
                        account["in_use"] = False  # 同时释放使用状态
                        if reason:
                            account["locked_reason"] = reason
                        account_found = True
                        logger.info(f"  ✅ 已标记账号 {username} 为锁定状态" + (f"（原因：{reason}）" if reason else ""))
                        break
                
                if not account_found:
                    logger.warning(f"  未在账号池中找到账号 {username}")
                    return
                
                # 写入更新后的池数据
                f.seek(0)
                f.truncate()
                json.dump(pool_data, f, indent=2, ensure_ascii=False)
                f.flush()
                
                return
                
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                logger.warning(f"  JSON解析失败（尝试 {attempt + 1}/{max_retries}）: {e}，重试...")
                time.sleep(retry_delay * (attempt + 1))
                continue
            else:
                logger.warning(f"  标记账号 {username} 为锁定失败（JSON解析错误）: {e}")
                return
        except Exception as e:
            logger.warning(f"  标记账号 {username} 为锁定失败: {e}")
            return


def release_test_account_to_pool(username):
    """
    ⚡ 阶段2优化：释放账号回池（标记为可用）
    ⚡ 并发安全：使用文件锁防止并发访问冲突
    
    Args:
        username: 要释放的账号用户名
    """
    import json
    import time
    from pathlib import Path
    
    # 尝试导入文件锁模块
    try:
        import fcntl
        use_lock = True
    except ImportError:
        try:
            import msvcrt
            use_lock = True
        except ImportError:
            use_lock = False
    
    pool_file = Path(__file__).parent / "test-data" / "test_account_pool.json"
    
    if not pool_file.exists():
        return
    
    max_retries = 5
    retry_delay = 0.1  # 100ms
    
    for attempt in range(max_retries):
        try:
            # 使用文件锁打开文件（读写模式）
            with open(pool_file, "r+", encoding="utf-8") as f:
                # 尝试获取排他锁（非阻塞）
                if use_lock:
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except (IOError, OSError):
                        # 如果无法获取锁，等待后重试
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                        else:
                            logger.warning(f"  无法获取文件锁（尝试 {attempt + 1}/{max_retries}），跳过释放账号")
                            return
                
                # 读取文件内容
                f.seek(0)  # 确保从文件开头读取
                pool_data = json.load(f)
        
                accounts = pool_data.get("test_account_pool", [])
        
                # 找到对应的账号并标记为可用
                for account in accounts:
                    if account["username"] == username:
                        account["in_use"] = False
                        logger.info(f"  ✅ 账号已释放回池: {username}")
                        break
        
                # 写入更新后的池数据
                f.seek(0)  # 回到文件开头
                f.truncate()  # 清空文件内容
                json.dump(pool_data, f, indent=2, ensure_ascii=False)
                f.flush()  # 确保数据写入磁盘
                
                # 释放锁（文件关闭时自动释放）
                return
                
        except json.JSONDecodeError as e:
            # JSON解析错误，可能是文件正在被写入
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                continue
            else:
                logger.warning(f"  释放账号回池失败（JSON解析错误）: {e}")
                return
        except Exception as e:
            logger.warning(f"  释放账号回池失败: {e}")
            return


def auto_register_and_login(page, request):
    """
    ⚡ 阶段2优化：智能账号管理（避免数据库脏数据）
    
    策略：
    1. 串行执行：使用预设账号（无数据冲突，无需注册）
    2. 并行执行：优先使用账号池（复用已有账号，避免脏数据）
    3. 账号池不足：才自动注册新账号（作为最后备选）
    
    可通过环境变量控制：
    - AUTO_REGISTER=true/false: 是否启用自动注册（默认：仅在并行时启用）
    - USE_ACCOUNT_POOL=true/false: 是否使用账号池（默认：true）
    
    Args:
        page: Playwright Page对象
        request: pytest request对象（用于获取测试函数名和worker_id）
    
    Returns:
        tuple: (username, email, password) 账号信息
    """
    from tests.aevatar_station.pages.landing_page import LandingPage
    from tests.aevatar_station.pages.register_page import RegisterPage
    from tests.aevatar_station.pages.login_page import LoginPage
    from datetime import datetime
    import hashlib
    import os
    
    logger.info("=" * 80)
    logger.info("⚡ 智能账号管理（避免数据库脏数据）")
    logger.info("=" * 80)
    
    # 获取worker_id（pytest-xdist并行执行时）
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", None) or os.environ.get("PYTEST_CURRENT_TEST", "").split("::")[0] if os.environ.get("PYTEST_CURRENT_TEST") else None
    
    # 判断是否并行执行
    is_parallel = worker_id and worker_id != "master"
    
    # 读取环境变量配置
    use_account_pool = os.environ.get("USE_ACCOUNT_POOL", "true").lower() == "true"
    auto_register_enabled = os.environ.get("AUTO_REGISTER", "auto").lower()
    if auto_register_enabled == "auto":
        # 自动模式：并行时启用，串行时禁用
        auto_register_enabled = is_parallel
    else:
        auto_register_enabled = auto_register_enabled == "true"
    
    logger.info(f"  执行模式: {'并行' if is_parallel else '串行'}")
    logger.info(f"  使用账号池: {use_account_pool}")
    logger.info(f"  自动注册: {auto_register_enabled}")
    
    # 策略1：串行执行时，直接使用预设账号（无数据冲突，无需注册）
    if not is_parallel:
        logger.info("  💡 串行执行：使用预设账号（无数据冲突，避免脏数据）")
        raise Exception("串行执行使用预设账号")  # 触发回退逻辑
    
    # 策略2：并行执行时，优先使用账号池（添加自动换号重试机制）
    if use_account_pool:
        max_retries = 3
        last_error = None
        
        for retry_attempt in range(max_retries):
            pool_account = get_test_account_from_pool(worker_id)
            
            if not pool_account:
                logger.warning(f"  ⚠️ 第{retry_attempt+1}次尝试：账号池无可用账号")
                if retry_attempt == max_retries - 1:
                    logger.warning(f"  ⚠️ 已尝试{max_retries}次，账号池无可用账号")
                    break  # 跳出循环，进入自动注册逻辑
                continue
            
            username, email, password = pool_account
            logger.info(f"  🔄 第{retry_attempt+1}次尝试：使用账号池账号 {username}")
            
            try:
                # 使用账号池账号登录
                landing_page = LandingPage(page)
                login_page = LoginPage(page)
            
                # ⚡ 并行执行优化：捕获浏览器崩溃（TargetClosedError），自动重试
                try:
                    landing_page.navigate()
                    landing_page.page.wait_for_timeout(500)
                except Exception as nav_error:
                    if "Target page, context or browser has been closed" in str(nav_error):
                        logger.error(f"  ❌ 浏览器崩溃（TargetClosedError），尝试换下一个账号...")
                        # 标记账号，继续尝试下一个
                        if retry_attempt < max_retries - 1:
                            continue
                        else:
                            logger.error(f"  ❌ 已尝试{max_retries}个账号，全部崩溃")
                            raise Exception("浏览器持续崩溃，无法登录")
                    else:
                        raise
                
                # 检查是否已登录
                try:
                    user_menu_visible = page.is_visible("button:has-text('Toggle user menu')", timeout=2000)
                    if user_menu_visible:
                        logger.info("  检测到已登录，跳过登录流程")
                        logger.info("=" * 80)
                        logger.info("")
                        logger.info("📋 使用的账号信息：")
                        logger.info(f"   用户名: {username}")
                        logger.info(f"   邮箱: {email}")
                        logger.info(f"   密码: {password}")
                        logger.info("")
                        return (username, email, password)
                except:
                    pass
                
                # 执行登录（添加账号锁定和密码错误检测）
                try:
                    landing_page.click_sign_in()
                    # 简单等待登录页面出现，不使用复杂的load_state检查
                    login_page.page.wait_for_timeout(2000)
                    
                    login_page.login(username=username, password=password)
                    login_page.page.wait_for_timeout(2000)  # 增加等待时间
                
                    landing_page.handle_ssl_warning()
                except Exception as click_error:
                    if "Target page, context or browser has been closed" in str(click_error):
                        logger.error(f"  ❌ 点击登录时浏览器崩溃，尝试换下一个账号...")
                        if retry_attempt < max_retries - 1:
                            continue
                        else:
                            logger.error(f"  ❌ 已尝试{max_retries}个账号，全部崩溃")
                            raise Exception("浏览器持续崩溃，无法登录")
                    else:
                        raise
                
                # 验证登录成功
                current_url = page.url
                if "/Account/Login" in current_url or "authorize" in current_url:
                    logger.error("  登录失败，仍在登录/授权页面")
                    raise Exception(f"账号池账号登录失败，当前URL: {current_url}")
                
                logger.info("  ✅ 账号池账号登录成功")
                logger.info("=" * 80)
                logger.info("")
                logger.info("📋 使用的账号信息：")
                logger.info(f"   用户名: {username}")
                logger.info(f"   邮箱: {email}")
                logger.info(f"   密码: {password}")
                logger.info("")
                
                return (username, email, password)
                    
            except Exception as login_error:
                last_error = login_error
                error_msg = str(login_error).lower()
                
                # 检测密码错误（账号被污染）
                is_password_wrong = any(keyword in error_msg for keyword in [
                    "invalid username or password",
                    "invalid login",
                    "incorrect password",
                    "invalid password"
                ])
                
                if is_password_wrong:
                    logger.error(f"  ❌ 账号 {username} 密码错误（可能被测试污染）")
                    logger.error(f"  错误信息: {login_error}")
                    
                    # 标记账号为已锁定（密码被污染）
                    mark_account_as_locked(username, reason="密码被污染，无法登录")
                    logger.warning(f"  已标记账号 {username} 为锁定状态")
                    logger.info(f"  🔄 自动换下一个账号...")
                    
                    # 继续尝试下一个账号
                    if retry_attempt < max_retries - 1:
                        continue
                    else:
                        logger.error(f"  ❌ 已尝试{max_retries}个账号，全部密码错误")
                        break
                
                # 检测账号锁定错误
                is_account_locked = any(keyword in error_msg for keyword in [
                    "locked out",
                    "locked",
                    "lockout",
                    "too many attempts",
                    "account has been locked"
                ])
                
                if is_account_locked:
                    logger.error(f"  ❌ 账号 {username} 已被锁定！")
                    logger.error(f"  错误信息: {login_error}")
                    
                    # 标记账号为已锁定
                    mark_account_as_locked(username, reason="账号被锁定")
                    logger.warning(f"  已标记账号 {username} 为锁定状态")
                    logger.info(f"  🔄 自动换下一个账号...")
                    
                    # 继续尝试下一个账号
                    if retry_attempt < max_retries - 1:
                        continue
                    else:
                        logger.error(f"  ❌ 已尝试{max_retries}个账号，全部被锁定")
                        break
                
                # 其他登录错误，直接抛出
                logger.error(f"  ❌ 登录时发生未知错误: {login_error}")
                raise
        
        # 所有重试都失败，记录错误并进入自动注册逻辑
        if last_error:
            logger.warning(f"  ⚠️ 账号池尝试{max_retries}次后都失败，将尝试自动注册")
            logger.warning(f"  最后一次错误: {last_error}")
    
    # 策略3：账号池无可用账号时，根据配置决定是否自动注册
    if not auto_register_enabled:
        logger.warning("  ⚠️ 账号池无可用账号，且自动注册已禁用，将回退到预设账号")
        raise Exception("账号池无可用账号且自动注册已禁用")
    
    # 策略4：最后备选 - 自动注册新账号（仅在并行执行且账号池不足时）
    logger.warning("  ⚠️ 账号池无可用账号，自动注册新账号（会产生脏数据）")
    logger.info("=" * 80)
    logger.info("⚡ 自动注册新账号（确保测试隔离）")
    logger.info("=" * 80)
    
    # 生成唯一的用户名和邮箱
    test_name = request.node.name if request else "test"
    test_name_clean = "".join(c if c.isalnum() or c == "_" else "_" for c in test_name)[:30]
    worker_suffix = f"w{worker_id}" if worker_id and worker_id != "master" else ""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    unique_str = f"{test_name_clean}_{worker_suffix}_{timestamp}"
    short_hash = hashlib.md5(unique_str.encode()).hexdigest()[:8]
    
    username = f"autotest_{short_hash}"
    email = f"autotest_{short_hash}@test.com"
    password = "TestPass123!"
    
    logger.info(f"  测试函数: {test_name}")
    logger.info(f"  Worker ID: {worker_id if worker_id else 'master'}")
    logger.info(f"  生成用户名: {username}")
    logger.info(f"  生成邮箱: {email}")
    
    # 导航到注册页面
    landing_page = LandingPage(page)
    register_page = RegisterPage(page)
    
    landing_page.navigate()
    landing_page.page.wait_for_timeout(500)
    
    # 检查是否已登录
    try:
        user_menu_visible = page.is_visible("button:has-text('Toggle user menu')", timeout=2000)
        if user_menu_visible:
            logger.info("  检测到已登录，跳过注册流程")
            return (username, email, password)
    except:
        pass
    
    # 导航到注册页面
    register_page.navigate()
    register_page.page.wait_for_timeout(500)
    
    # 执行注册
    logger.info("  开始注册新账号...")
    try:
        register_page.register(username, email, password)
    except Exception as e:
        logger.warning(f"  注册过程出现异常: {e}，继续等待响应...")
    
    # 等待注册完成
    register_page.page.wait_for_timeout(3000)
    
    # 检查注册结果
    current_url = page.url
    logger.info(f"  注册后URL: {current_url}")
    
    if "/Register" in current_url:
        error_msg = register_page.get_error_message()
        if error_msg:
            logger.warning(f"  注册可能失败: {error_msg}")
            if "already" in error_msg.lower() or "exists" in error_msg.lower() or "taken" in error_msg.lower():
                timestamp2 = datetime.now().strftime("%H%M%S%f")
                username = f"autotest_{short_hash}_{timestamp2[-6:]}"
                email = f"autotest_{short_hash}_{timestamp2[-6:]}@test.com"
                logger.info(f"  用户名已存在，重新生成: {username}")
                register_page.fill_username(username)
                register_page.fill_email(email)
                register_page.click_register_button()
                register_page.page.wait_for_timeout(2000)
                current_url = page.url
    
    # 导航到登录页面（如果注册后没有自动登录）
    login_page = LoginPage(page)
    if "/Account/Login" not in current_url and "/Register" in current_url:
        logger.info("  注册成功，导航到登录页面...")
        login_page.navigate()
        login_page.wait_for_load()
        login_page.page.wait_for_timeout(500)
    
    # 执行登录（如果还没有自动登录）
    current_url = page.url
    if "/Account/Login" in current_url or "authorize" in current_url:
        logger.info("  使用新注册的账号登录...")
        login_page.login(username=username, password=password)
        login_page.page.wait_for_timeout(1000)
    
    # 处理SSL警告
    landing_page.handle_ssl_warning()
    
    # 验证登录成功
    current_url = page.url
    logger.info(f"  登录后URL: {current_url}")
    
    if "/Account/Login" in current_url or "authorize" in current_url:
        logger.error("  登录失败，仍在登录/授权页面")
        raise Exception(f"自动注册登录失败，当前URL: {current_url}")
    
    page.wait_for_timeout(1000)
    
    logger.info("  ✅ 自动注册并登录成功")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📋 注册的账号信息（可用于手动登录检查）：")
    logger.info(f"   用户名: {username}")
    logger.info(f"   邮箱: {email}")
    logger.info(f"   密码: {password}")
    logger.info("")
    logger.info("  ⚠️ 注意：此账号为自动注册，建议使用账号池机制避免脏数据")
    logger.info("")
    
    return (username, email, password)


@pytest.fixture(scope="function")
def logged_in_profile_page(page, test_data, request):
    """
    登录后的个人设置页面fixture - 每个测试独立实例
    ⚡ 阶段2优化：支持并行执行，每个测试用例自动注册独立账号
    
    工作流程：
    1. 自动注册新账号（用户名和邮箱基于测试函数名+时间戳+hash生成）
    2. 使用新注册的账号自动登录
    3. 导航到Profile页面
    4. 如果注册失败，回退到使用预设账号
    """
    from tests.aevatar_station.pages.landing_page import LandingPage
    from tests.aevatar_station.pages.login_page import LoginPage
    from tests.aevatar_station.pages.profile_settings_page import ProfileSettingsPage
    
    logger.info("=== 开始登录流程 ===")
    
    # ⚡ 阶段2优化：自动注册新账号并登录（确保每个测试用例完全独立）
    try:
        username, email, password = auto_register_and_login(page, request)
        logger.info(f"✅ 使用自动注册的账号: {username}")
    except Exception as e:
        logger.warning(f"⚠️ 自动注册失败: {e}，回退到使用预设账号")
        logger.exception("自动注册异常详情:")
        # 回退到使用预设账号
        landing_page = LandingPage(page)
        login_page = LoginPage(page)
        
        landing_page.navigate()
        landing_page.page.wait_for_timeout(500)
        
        # 检查是否已登录
        try:
            user_menu_visible = page.is_visible("button:has-text('Toggle user menu')", timeout=2000)
            if user_menu_visible:
                logger.info("  检测到已登录，跳过登录流程")
            else:
                landing_page.click_sign_in()
                login_page.wait_for_load()
                
                valid_data = test_data["valid_login_data"][0]
                login_page.login(
                    username=valid_data["username"],
                    password=valid_data["password"]
                )
                
                landing_page.handle_ssl_warning()
        except Exception as e2:
            logger.error(f"回退登录也失败: {e2}")
            raise
    
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

