#!/usr/bin/env python3
"""
Aevatar 日常回归测试主运行脚本
执行所有26个回归测试用例
"""

import subprocess
import sys
import os
from datetime import datetime
import argparse

# 测试文件列表
TEST_FILES = [
    "tests/aevatar/test_daily_regression_dashboard.py",
    "tests/aevatar/test_daily_regression_organisation.py",
    "tests/aevatar/test_daily_regression_project.py"
]


def run_tests(priority=None, module=None, verbose=False):
    """
    运行回归测试
    
    Args:
        priority: 优先级过滤 (p0, p1, p2)
        module: 模块过滤 (login, apikeys, workflows, etc.)
        verbose: 是否显示详细输出
    """
    # 生成时间戳用于报告命名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/daily_regression_report_{timestamp}.html"
    
    # 构建pytest命令
    pytest_args = [
        sys.executable, "-m", "pytest"
    ]
    
    # 添加测试文件
    if module:
        # 如果指定了模块，只运行相关的测试文件
        if module in ["login", "apikeys", "workflows", "configuration"]:
            pytest_args.append("tests/aevatar/test_daily_regression_dashboard.py")
        elif module in ["profile", "organisation"]:
            pytest_args.append("tests/aevatar/test_daily_regression_organisation.py")
        elif module == "project":
            pytest_args.append("tests/aevatar/test_daily_regression_project.py")
        else:
            pytest_args.extend(TEST_FILES)
    else:
        pytest_args.extend(TEST_FILES)
    
    # 添加标记过滤
    if priority:
        pytest_args.extend(["-m", priority])
    
    if module and not priority:
        pytest_args.extend(["-m", module])
    
    # 添加报告选项
    pytest_args.extend([
        "-v" if verbose else "-q",
        "--tb=short",
        f"--html={report_name}",
        "--self-contained-html",
        "--durations=10",
        "--capture=no" if verbose else "--capture=sys",
        "--log-cli-level=INFO" if verbose else "--log-cli-level=WARNING",
        "--log-cli-format=%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        "--log-cli-date-format=%Y-%m-%d %H:%M:%S",
        "--color=yes"
    ])
    
    print("=" * 80)
    print("🌌 Aevatar 日常回归测试")
    print("=" * 80)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if priority:
        print(f"🎯 优先级过滤: {priority.upper()}")
    if module:
        print(f"📦 模块过滤: {module}")
    
    print(f"📊 报告路径: {report_name}")
    print("=" * 80)
    print()
    
    # 执行测试
    result = subprocess.run(pytest_args)
    
    print()
    print("=" * 80)
    if result.returncode == 0:
        print("✅ 所有测试通过!")
    else:
        print(f"❌ 测试失败 (退出码: {result.returncode})")
    print(f"📊 详细报告: {report_name}")
    print("=" * 80)
    
    return result.returncode


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Aevatar 日常回归测试运行器")
    
    parser.add_argument(
        "-p", "--priority",
        choices=["p0", "p1", "p2"],
        help="按优先级过滤测试 (p0=核心功能, p1=重要功能, p2=一般功能)"
    )
    
    parser.add_argument(
        "-m", "--module",
        choices=[
            "login", "apikeys", "workflows", "configuration",
            "profile", "organisation", "project"
        ],
        help="按模块过滤测试"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细输出"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有测试用例"
    )
    
    args = parser.parse_args()
    
    # 如果是列出测试用例
    if args.list:
        list_args = [
            sys.executable, "-m", "pytest",
            *TEST_FILES,
            "--collect-only",
            "-q"
        ]
        subprocess.run(list_args)
        return 0
    
    # 运行测试
    return run_tests(
        priority=args.priority,
        module=args.module,
        verbose=args.verbose
    )


if __name__ == "__main__":
    sys.exit(main())

