#!/usr/bin/env python3
"""
并行运行所有测试 - 显著缩短测试时间
使用pytest-xdist实现多进程并行执行

预计时间：20-30分钟（vs 顺序执行60-90分钟）
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
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

print_header("🚀 Aevatar 每日回归测试 - 并行执行模式")

# 检查pytest-xdist是否安装
print_info("检查pytest-xdist插件...")
try:
    import xdist
    print_success("pytest-xdist 已安装")
except ImportError:
    print_warning("pytest-xdist 未安装，正在安装...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest-xdist", "-q"])
    print_success("pytest-xdist 安装完成")

# 清理旧结果
allure_results = Path("allure-results")
allure_report = Path("allure-report")

print_info("清理旧结果...")
if allure_results.exists():
    shutil.rmtree(allure_results)
if allure_report.exists():
    shutil.rmtree(allure_report)

allure_results.mkdir(exist_ok=True)
print_success("准备就绪")

# 测试文件列表
test_files = [
    "tests/aevatar/test_daily_regression_login.py",
    "tests/aevatar/test_daily_regression_dashboard.py",
    "tests/aevatar/test_daily_regression_apikeys.py",
    "tests/aevatar/test_daily_regression_workflow.py",
    "tests/aevatar/test_daily_regression_configuration.py",
    "tests/aevatar/test_daily_regression_profile.py",
    "tests/aevatar/test_daily_regression_organisation.py",
    "tests/aevatar/test_daily_regression_project.py"
]

# 并行配置
PARALLEL_WORKERS = 4  # 推荐4个并行worker，平衡速度和资源

print_header("⚙️ 并行测试配置")
print(f"📊 测试模块数: {len(test_files)}")
print(f"🔄 并行Worker数: {PARALLEL_WORKERS}")
print(f"⚡ 预计加速: {60//PARALLEL_WORKERS}分钟 (vs 顺序60-90分钟)")
print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

print_info("提示：并行测试会同时打开多个浏览器窗口，这是正常的")
print_warning("建议关闭不必要的应用程序以确保足够的系统资源")
print()

input("按 Enter 键开始测试（或 Ctrl+C 取消）...")

# 构建pytest命令
pytest_cmd = [
    sys.executable, "-m", "pytest",
    *test_files,  # 所有测试文件
    "-v",  # 详细输出
    "-n", str(PARALLEL_WORKERS),  # 并行worker数
    "--dist", "loadfile",  # 按文件分发（每个文件作为一个整体）
    "--tb=short",  # 简化错误输出
    f"--alluredir={allure_results}",
    "--maxfail=10",  # 最多失败10个就停止
    "--durations=20",  # 显示最慢的20个测试
]

print_header("🚀 开始并行测试")
print(f"💡 命令: {' '.join(pytest_cmd)}")
print()

# 运行测试
start_time = datetime.now()

try:
    result = subprocess.run(
        pytest_cmd,
        timeout=1800  # 30分钟超时
    )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60
    
    print()
    print_header(f"⏱️ 测试执行完成 - 耗时: {duration:.1f} 分钟")
    
    if result.returncode == 0:
        print_success("所有测试通过！")
    else:
        print_warning("部分测试失败，请查看报告")
        
except subprocess.TimeoutExpired:
    print_error("测试超时（>30分钟）")
    sys.exit(1)
except KeyboardInterrupt:
    print_warning("\n测试被用户中断")
    sys.exit(1)
except Exception as e:
    print_error(f"测试执行异常: {e}")
    sys.exit(1)

# 生成Allure报告
print_header("📊 生成Allure报告")

if not list(allure_results.glob("*.json")):
    print_error("未找到测试结果，无法生成报告")
    sys.exit(1)

print_info("正在生成HTML报告...")

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
        timeout=60
    )
    
    if result.returncode == 0:
        print_success("Allure报告生成成功！")
        print()
        print(f"📁 报告位置: {allure_report}/index.html")
        print(f"📁 结果位置: {allure_results}/")
        print()
        
        # 自动打开报告
        print_info("正在打开报告...")
        try:
            # macOS
            subprocess.run(["open", f"{allure_report}/index.html"])
            print_success("报告已在浏览器中打开")
        except:
            print_info("请手动打开: open allure-report/index.html")
    else:
        print_error("Allure报告生成失败")
        print(result.stderr)
        
except Exception as e:
    print_error(f"生成报告时出错: {e}")

# 总结
print_header("🎉 完成！")
print(f"⏱️ 总耗时: {duration:.1f} 分钟")
print(f"📊 测试模块: {len(test_files)}")
print(f"🔄 并行数: {PARALLEL_WORKERS}")
print()
print("🌐 查看报告的其他方式：")
print(f"   方式1: open {allure_report}/index.html")
print(f"   方式2: allure open {allure_report}")
print(f"   方式3: allure serve {allure_results}")
print()

sys.exit(result.returncode if result.returncode != 0 else 0)

