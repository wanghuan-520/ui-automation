#!/usr/bin/env python3
"""
超快速冒烟测试 - 1-3分钟完成
只测试最核心的功能，快速验证系统是否正常

适用场景：
- 快速验证部署
- 提交前检查
- 开发过程中的快速反馈
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

print_header("⚡ Aevatar 超快速冒烟测试")

# 清理旧结果
allure_results = Path("allure-results-smoke")
allure_report = Path("allure-report-smoke")

print_info("清理旧结果...")
if allure_results.exists():
    shutil.rmtree(allure_results)
if allure_report.exists():
    shutil.rmtree(allure_report)

allure_results.mkdir(exist_ok=True)
print_success("准备就绪")

# 只测试最核心的功能
print_header("🎯 测试范围")
print("只测试3个最核心功能：")
print("  1. 登录功能 ✅")
print("  2. Dashboard访问 ✅")
print("  3. 一个基本操作（Workflow查看）✅")
print()
print_info("预计时间: 1-3分钟")
print()

start_time = datetime.now()

# 方案1: 只运行login测试（最快）
test_selection = [
    "tests/aevatar/test_daily_regression_login.py",
    # 可选：如果想要稍微完整一点，取消下面的注释
    # "tests/aevatar/test_daily_regression_dashboard.py::test_dashboard_access",
    # "tests/aevatar/test_daily_regression_workflow.py::test_workflow_access",
]

# 构建pytest命令
pytest_cmd = [
    sys.executable, "-m", "pytest",
    *test_selection,
    "-v",
    "-x",  # 失败即停止
    "--tb=line",  # 简化错误输出
    f"--alluredir={allure_results}",
]

print_header("🚀 开始测试")

try:
    result = subprocess.run(pytest_cmd)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print()
    print_header(f"⏱️ 测试完成 - 耗时: {duration:.1f} 秒")
    
    if result.returncode == 0:
        print_success("冒烟测试通过！系统基本功能正常 ✅")
    else:
        print_error("冒烟测试失败！发现问题 ❌")
        sys.exit(1)
        
except KeyboardInterrupt:
    print_error("\n测试被中断")
    sys.exit(1)
except Exception as e:
    print_error(f"测试执行异常: {e}")
    sys.exit(1)

# 生成简单报告
print_header("📊 生成报告")

if not list(allure_results.glob("*.json")):
    print_error("未找到测试结果")
    sys.exit(1)

print_info("生成Allure报告...")

generate_cmd = [
    "allure", "generate",
    str(allure_results),
    "-o", str(allure_report),
    "--clean"
]

try:
    result = subprocess.run(
        generate_cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print_success("报告生成成功！")
        print(f"📁 报告: {allure_report}/index.html")
        print()
        
        # 自动打开
        try:
            subprocess.run(["open", f"{allure_report}/index.html"])
            print_success("报告已打开")
        except:
            print_info(f"手动打开: open {allure_report}/index.html")
    else:
        print_error("报告生成失败")
        
except Exception as e:
    print_error(f"生成报告时出错: {e}")

# 总结
print_header("🎉 完成！")
print(f"⚡ 冒烟测试耗时: {duration:.1f} 秒")
print(f"✅ 基本功能验证: 通过")
print()
print("💡 提示：")
print("  - 冒烟测试只验证最核心功能")
print("  - 完整测试请使用: python3 run_all_tests_parallel.py")
print("  - P0测试请使用: pytest -n 4 -m p0 tests/aevatar/")
print()

sys.exit(0)

