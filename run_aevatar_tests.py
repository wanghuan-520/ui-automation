#!/usr/bin/env python3
"""
Aevatar 测试运行脚本
提供便捷的测试执行入口
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(args):
    """运行测试"""
    
    # 基础pytest命令
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/aevatar/",
        "-v",
        "--tb=short",
        "--capture=no",
        "--log-cli-level=INFO",
        "--log-cli-format=%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        "--log-cli-date-format=%Y-%m-%d %H:%M:%S",
        "--color=yes"
    ]
    
    # 添加HTML报告
    if args.html:
        pytest_args.extend([
            "--html=reports/aevatar-report.html",
            "--self-contained-html"
        ])
    
    # 添加JSON报告
    if args.json:
        pytest_args.extend([
            "--json-report",
            "--json-report-file=reports/aevatar-report.json"
        ])
    
    # 添加标记过滤
    if args.marker:
        pytest_args.extend(["-m", args.marker])
    
    # 添加并行执行
    if args.parallel:
        pytest_args.extend(["-n", "auto"])
    
    # 添加失败重试
    if args.reruns:
        pytest_args.extend(["--reruns", str(args.reruns)])
    
    # 只运行特定测试文件
    if args.test_file:
        pytest_args[2] = f"tests/aevatar/{args.test_file}"
    
    # 显示执行的命令
    print("🚀 执行命令:")
    print(" ".join(pytest_args))
    print("\n" + "="*80 + "\n")
    
    # 运行pytest
    result = subprocess.run(pytest_args)
    return result.returncode


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Aevatar 测试运行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行所有测试
  python run_aevatar_tests.py
  
  # 运行登录测试并生成HTML报告
  python run_aevatar_tests.py --test-file test_login.py --html
  
  # 只运行冒烟测试
  python run_aevatar_tests.py -m smoke
  
  # 并行运行所有测试
  python run_aevatar_tests.py --parallel
  
  # 失败重试2次
  python run_aevatar_tests.py --reruns 2
        """
    )
    
    parser.add_argument(
        "--test-file",
        choices=["test_login.py", "test_workflow.py"],
        help="只运行指定的测试文件"
    )
    
    parser.add_argument(
        "-m", "--marker",
        choices=["smoke", "positive", "negative", "login", "workflow", "integration"],
        help="按标记过滤测试"
    )
    
    parser.add_argument(
        "--html",
        action="store_true",
        help="生成HTML测试报告"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="生成JSON测试报告"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="并行执行测试（使用所有CPU核心）"
    )
    
    parser.add_argument(
        "--reruns",
        type=int,
        metavar="N",
        help="失败重试次数"
    )
    
    args = parser.parse_args()
    
    # 打印欢迎信息
    print("\n" + "="*80)
    print("🌌 Aevatar 数据驱动测试框架")
    print("="*80 + "\n")
    
    # 运行测试
    exit_code = run_tests(args)
    
    # 打印结束信息
    print("\n" + "="*80)
    if exit_code == 0:
        print("✅ 测试执行完成")
    else:
        print("❌ 测试执行失败")
    print("="*80 + "\n")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

