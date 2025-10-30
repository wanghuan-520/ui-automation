#!/usr/bin/env python3
"""
Aevatar 并行测试执行脚本（Python版本）
HyperEcho 创建
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """主函数"""
    print("="*80)
    print("🚀 Aevatar 并行测试启动")
    print("="*80)
    print()
    
    # 进入项目目录
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"📂 当前目录: {os.getcwd()}")
    print()
    
    # 检查 Python
    print("🐍 Python 版本:")
    print(f"   {sys.version}")
    print()
    
    # 安装依赖
    print("📦 安装并行测试依赖...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytest-xdist", "-q"],
            check=True
        )
        print("✅ pytest-xdist 已安装")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  依赖安装失败，继续执行: {e}")
    print()
    
    # 创建目录
    print("📁 准备报告目录...")
    for dir_name in ["reports", "test-screenshots", "logs"]:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ 目录准备完成")
    print()
    
    # 显示测试文件
    print("📋 发现的测试文件:")
    test_files = sorted(Path("tests/aevatar").glob("test_*.py"))
    for f in test_files:
        print(f"   - {f.name}")
    print()
    
    # 并行运行测试
    print("="*80)
    print("⚡ 开始并行执行所有测试...")
    print("="*80)
    print()
    
    # 构建 pytest 命令
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/aevatar/",
        "-v",
        "-n", "auto",
        "--html=reports/aevatar-parallel-report.html",
        "--self-contained-html",
        "--tb=short",
        "--capture=no",
        "--log-cli-level=INFO",
        "--color=yes"
    ]
    
    # 执行测试
    try:
        result = subprocess.run(pytest_args)
        exit_code = result.returncode
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
        exit_code = 130
    except Exception as e:
        print(f"\n❌ 测试执行出错: {e}")
        exit_code = 1
    
    print()
    print("="*80)
    if exit_code == 0:
        print("✅ 测试全部通过！")
    else:
        print(f"❌ 测试失败（退出码: {exit_code}）")
    print("="*80)
    print()
    
    # 显示结果
    print("📊 测试结果:")
    print("   - 报告: reports/aevatar-parallel-report.html")
    print("   - 截图: test-screenshots/")
    print("   - 日志: logs/")
    print()
    
    # 统计截图
    screenshot_dir = Path("test-screenshots")
    if screenshot_dir.exists():
        screenshot_count = len(list(screenshot_dir.glob("*.png")))
        print(f"📸 生成截图数量: {screenshot_count}")
    print()
    
    # 提示
    print("💡 快速查看报告:")
    if sys.platform == "darwin":
        print("   open reports/aevatar-parallel-report.html")
    elif sys.platform == "win32":
        print("   start reports/aevatar-parallel-report.html")
    else:
        print("   xdg-open reports/aevatar-parallel-report.html")
    print()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

