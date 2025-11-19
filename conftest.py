import pytest
from pathlib import Path
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 使用pytest-playwright但每个测试使用独立browser
# 这样可以完全隔离测试，避免browser崩溃影响后续测试

@pytest.fixture(scope="function")
def browser(browser_type):
    """为每个测试函数创建独立的browser实例"""
    # 使用pytest-playwright的默认配置
    # 通过命令行参数 --headed --slowmo 500 来控制
    browser = browser_type.launch()
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    """自定义browser context参数"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture(autouse=True)
def test_info(request):
    """测试信息fixture - 打印测试执行信息"""
    test_name = request.node.name
    test_file = request.node.fspath.basename
    
    print(f"\n{'='*80}")
    print(f"▶️  开始测试: {test_file}::{test_name}")
    print(f"{'='*80}")
    
    # 标记测试开始
    pytest.current_test_failed = False
    
    def fin():
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            pytest.current_test_failed = True
            print(f"❌ 测试失败: {test_file}::{test_name}")
        elif hasattr(request.node, 'rep_call') and request.node.rep_call.passed:
            print(f"✅ 测试通过: {test_file}::{test_name}")
        elif hasattr(request.node, 'rep_setup') and request.node.rep_setup.failed:
            print(f"⚠️  测试Setup失败: {test_file}::{test_name}")
        print(f"{'='*80}\n")
    
    request.addfinalizer(fin)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告钩子"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境 - session级别，只运行一次"""
    # 创建必要的目录
    directories = [
        "reports",
        "reports/screenshots", 
        "reports/videos",
        "reports/allure-results",
        "reports/allure-results-p0",
        "test_data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("\n" + "="*80)
    print("🚀 测试环境初始化完成")
    print("="*80 + "\n")
    
    yield
    
    print("\n" + "="*80)
    print("🏁 测试环境清理完成")
    print("="*80 + "\n")
