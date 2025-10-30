#!/usr/bin/env python3
"""
Aevatar 日常回归测试 - 主运行脚本
基于 daily_regression_test_mindmap.md

测试模块：
1. Dashboard功能（API Keys、Workflows、Configuration）
2. Profile配置
3. Organisation管理（Settings、Projects、Members、Roles）
4. Project管理（Settings、Members、Roles）

使用方法：
    python3 run_daily_regression.py [选项]

选项：
    --all            运行所有测试
    --p0             只运行P0优先级测试
    --p1             只运行P1优先级测试
    --dashboard      只运行Dashboard测试
    --organisation   只运行Organisation测试
    --project        只运行Project测试
    --profile        只运行Profile测试
    --parallel       并行运行（使用pytest-xdist）
"""

import subprocess
import sys
import argparse
from datetime import datetime

def run_daily_regression(args):
    """运行日常回归测试"""
    
    # 基础pytest参数
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/aevatar/",
        "-v",
        "-s",
        "--tb=short",
        "--html=reports/daily-regression-report.html",
        "--self-contained-html",
        "--capture=no",
        "--log-cli-level=INFO",
        "--durations=20"
    ]
    
    # 根据参数选择测试
    if args.p0:
        pytest_args.extend(["-m", "p0"])
        print("🔴 运行P0核心功能测试...")
    elif args.p1:
        pytest_args.extend(["-m", "p1"])
        print("🟡 运行P1重要功能测试...")
    elif args.dashboard:
        pytest_args.extend(["-m", "dashboard or apikeys or workflows or configuration"])
        print("📊 运行Dashboard功能测试...")
    elif args.organisation:
        pytest_args.extend(["-m", "organisation"])
        print("🏢 运行Organisation管理测试...")
    elif args.project:
        pytest_args.extend(["-m", "project"])
        print("📂 运行Project管理测试...")
    elif args.profile:
        pytest_args.extend(["-m", "profile"])
        print("👤 运行Profile配置测试...")
    else:
        # 默认运行所有测试
        print("🚀 运行所有日常回归测试...")
    
    # 并行执行
    if args.parallel:
        try:
            import xdist
            pytest_args.extend(["-n", "auto"])
            print("⚡ 启用并行执行模式")
        except ImportError:
            print("⚠️  pytest-xdist未安装，使用顺序执行")
            print("💡 安装方法：pip3 install pytest-xdist")
    
    # 指定测试文件
    test_files = []
    if args.dashboard or args.all or (not any([args.p0, args.p1, args.organisation, args.project, args.profile])):
        test_files.append("tests/aevatar/test_daily_regression_dashboard.py")
    
    if args.organisation or args.all or (not any([args.p0, args.p1, args.dashboard, args.project, args.profile])):
        test_files.append("tests/aevatar/test_daily_regression_organisation.py")
    
    if args.project or args.all or (not any([args.p0, args.p1, args.dashboard, args.organisation, args.profile])):
        test_files.append("tests/aevatar/test_daily_regression_project.py")
    
    # 如果没有指定具体文件，添加完整测试
    if not test_files:
        test_files = ["tests/aevatar/test_daily_regression_*.py"]
    
    # 替换测试路径
    pytest_args[2] = " ".join(test_files)
    
    print("=" * 80)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 测试环境: https://aevatar-station-ui-staging.aevatar.ai")
    print("=" * 80)
    
    # 执行测试
    result = subprocess.run(" ".join(pytest_args), shell=True)
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("✅ 测试全部通过!")
    else:
        print("❌ 部分测试失败，请查看报告")
    print(f"📊 详细报告: reports/daily-regression-report.html")
    print("=" * 80)
    
    return result.returncode


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Aevatar 日常回归测试运行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    # 运行所有测试
    python3 run_daily_regression.py --all
    
    # 只运行P0核心功能
    python3 run_daily_regression.py --p0
    
    # 运行Dashboard测试
    python3 run_daily_regression.py --dashboard
    
    # 并行运行Organisation测试
    python3 run_daily_regression.py --organisation --parallel
        """
    )
    
    parser.add_argument('--all', action='store_true', help='运行所有测试')
    parser.add_argument('--p0', action='store_true', help='只运行P0优先级测试')
    parser.add_argument('--p1', action='store_true', help='只运行P1优先级测试')
    parser.add_argument('--dashboard', action='store_true', help='只运行Dashboard测试')
    parser.add_argument('--organisation', action='store_true', help='只运行Organisation测试')
    parser.add_argument('--project', action='store_true', help='只运行Project测试')
    parser.add_argument('--profile', action='store_true', help='只运行Profile测试')
    parser.add_argument('--parallel', action='store_true', help='并行运行测试')
    
    args = parser.parse_args()
    
    # 运行测试
    exit_code = run_daily_regression(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

