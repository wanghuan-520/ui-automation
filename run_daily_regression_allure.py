#!/usr/bin/env python3
"""
Aevatar 日常回归测试 - Allure报告版本
运行测试并自动生成和打开Allure测试报告

使用方法：
    python3 run_daily_regression_allure.py [选项]

选项：
    --all            运行所有测试
    --p0             只运行P0优先级测试
    --p1             只运行P1优先级测试
    --dashboard      只运行Dashboard测试
    --organisation   只运行Organisation测试
    --project        只运行Project测试
    --stable         运行稳定版本测试（推荐首次运行）
    --no-open        生成报告但不自动打开浏览器
"""

import subprocess
import sys
import argparse
import os
import shutil
from datetime import datetime

# 颜色输出
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

def run_daily_regression_allure(args):
    """运行日常回归测试并生成Allure报告"""
    
    # 配置路径
    allure_results_dir = "allure-results"
    allure_report_dir = "allure-report"
    
    print_header("🌌 Aevatar 日常回归测试 - Allure报告")
    
    # 1. 清理旧的结果
    print_info("清理旧的测试结果...")
    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir)
    if os.path.exists(allure_report_dir):
        shutil.rmtree(allure_report_dir)
    print_success("旧结果已清理")
    
    # 2. 构建pytest命令
    pytest_args = [
        sys.executable, "-m", "pytest",
        "-v",
        "-s",
        "--tb=short",
        "--capture=no",
        "--log-cli-level=INFO",
        f"--alluredir={allure_results_dir}",
        "--durations=20"
    ]
    
    # 选择测试文件
    test_files = []
    
    if args.stable:
        # 运行稳定版本测试（推荐）
        test_files = [
            "tests/aevatar/test_daily_regression_login.py",
            "tests/aevatar/test_daily_regression_workflow.py"
        ]
        print_info("运行稳定版本测试（登录 + Workflow）")
    elif args.p0:
        pytest_args.extend(["-m", "p0"])
        print_info("运行P0核心功能测试")
    elif args.p1:
        pytest_args.extend(["-m", "p1"])
        print_info("运行P1重要功能测试")
    elif args.dashboard:
        pytest_args.extend(["-m", "dashboard or apikeys or workflows or configuration"])
        print_info("运行Dashboard功能测试")
    elif args.organisation:
        pytest_args.extend(["-m", "organisation"])
        print_info("运行Organisation管理测试")
    elif args.project:
        pytest_args.extend(["-m", "project"])
        print_info("运行Project管理测试")
    else:
        # 默认运行所有日常回归测试
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
        print_info("运行所有日常回归测试（8个模块）")
    
    # 添加测试文件
    if test_files:
        pytest_args.extend(test_files)
    else:
        pytest_args.append("tests/aevatar/")
    
    # 打印测试信息
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 测试环境: https://aevatar-station-ui-staging.aevatar.ai")
    print(f"📊 Allure结果目录: {allure_results_dir}")
    print(f"📄 Allure报告目录: {allure_report_dir}")
    print()
    
    # 3. 运行pytest
    print_header("🚀 开始运行测试")
    result = subprocess.run(" ".join(pytest_args), shell=True)
    
    # 4. 检查是否有测试结果
    if not os.path.exists(allure_results_dir) or not os.listdir(allure_results_dir):
        print_error("未找到测试结果，无法生成Allure报告")
        return 1
    
    print_success(f"测试执行完成！退出码: {result.returncode}")
    
    # 5. 生成Allure报告
    print_header("📊 生成Allure报告")
    print_info("正在生成HTML报告...")
    
    generate_cmd = f"allure generate {allure_results_dir} -o {allure_report_dir} --clean"
    generate_result = subprocess.run(generate_cmd, shell=True, capture_output=True, text=True)
    
    if generate_result.returncode != 0:
        print_error("生成Allure报告失败")
        print(generate_result.stderr)
        return 1
    
    print_success("Allure报告生成成功！")
    
    # 6. 打开报告（使用Allure服务器）
    if not args.no_open:
        print_header("🌐 打开Allure报告")
        print_info("正在启动Allure服务器...")
        print_info("提示：使用Allure内置服务器可避免CORS问题")
        
        # 使用allure open或allure serve
        # allure open: 只打开已生成的报告
        # allure serve: 重新生成并打开（推荐）
        serve_cmd = f"allure open {allure_report_dir}"
        
        print_success("Allure服务器将在后台启动")
        print_info("浏览器将自动打开，显示完整的测试报告")
        print_info("按 Ctrl+C 可停止服务器")
        
        # 启动allure服务器（这会阻塞，直到用户按Ctrl+C）
        try:
            subprocess.run(serve_cmd, shell=True)
        except KeyboardInterrupt:
            print_info("\n服务器已停止")
    
    # 7. 打印总结
    print_header("✨ 测试完成总结")
    
    if result.returncode == 0:
        print_success("所有测试通过！")
    else:
        print_warning("部分测试失败，请查看报告")
    
    print()
    print(f"📊 Allure报告路径: {allure_report_dir}/index.html")
    print(f"📁 测试结果路径: {allure_results_dir}/")
    print()
    print(f"💡 手动打开报告: open {allure_report_dir}/index.html")
    print(f"💡 使用Allure服务器: allure serve {allure_results_dir}")
    print()
    
    return result.returncode


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Aevatar 日常回归测试 - Allure报告版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    # 运行稳定版本测试（推荐首次运行）
    python3 run_daily_regression_allure.py --stable
    
    # 运行所有测试
    python3 run_daily_regression_allure.py --all
    
    # 只运行P0核心功能
    python3 run_daily_regression_allure.py --p0
    
    # 运行Dashboard测试
    python3 run_daily_regression_allure.py --dashboard
    
    # 生成报告但不自动打开
    python3 run_daily_regression_allure.py --p0 --no-open
        """
    )
    
    parser.add_argument('--all', action='store_true', help='运行所有测试')
    parser.add_argument('--p0', action='store_true', help='只运行P0优先级测试')
    parser.add_argument('--p1', action='store_true', help='只运行P1优先级测试')
    parser.add_argument('--dashboard', action='store_true', help='只运行Dashboard测试')
    parser.add_argument('--organisation', action='store_true', help='只运行Organisation测试')
    parser.add_argument('--project', action='store_true', help='只运行Project测试')
    parser.add_argument('--stable', action='store_true', help='运行稳定版本测试（推荐）')
    parser.add_argument('--no-open', action='store_true', help='生成报告但不自动打开浏览器')
    
    args = parser.parse_args()
    
    # 运行测试
    exit_code = run_daily_regression_allure(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

