#!/usr/bin/env python3
"""
顺序运行所有测试 - 避免资源耗尽
每次只运行一个测试模块，模块之间有延迟
"""

import subprocess
import time
import os
import shutil
from pathlib import Path

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

print_header("🌌 Aevatar 每日回归测试 - 顺序执行模式")

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

# 统计
total = len(test_files)
passed = 0
failed = 0
results = []

print(f"\n📊 将运行 {total} 个测试模块\n")

# 逐个运行测试
for index, test_file in enumerate(test_files, 1):
    module_name = Path(test_file).stem
    
    print_header(f"[{index}/{total}] 🧪 {module_name}")
    
    # 构建pytest命令 - 使用相对简单的参数
    cmd = [
        "python3", "-m", "pytest",
        test_file,
        "-v",
        "--tb=line",  # 简化错误输出
        f"--alluredir={allure_results}",
        "--maxfail=5",  # 失败5个就停止该模块
    ]
    
    try:
        # 运行测试，捕获输出
        result = subprocess.run(
            cmd,
            capture_output=False,  # 直接显示输出
            timeout=600  # 10分钟超时
        )
        
        if result.returncode == 0:
            print_success(f"{module_name}: 全部通过")
            passed += 1
            results.append((module_name, "✅ 通过"))
        else:
            print_error(f"{module_name}: 部分失败或错误")
            failed += 1
            results.append((module_name, "❌ 失败"))
            
    except subprocess.TimeoutExpired:
        print_error(f"{module_name}: 超时（>10分钟）")
        failed += 1
        results.append((module_name, "⏱️ 超时"))
    except Exception as e:
        print_error(f"{module_name}: 异常 - {e}")
        failed += 1
        results.append((module_name, f"💥 异常: {e}"))
    
    # 等待释放资源
    if index < total:
        print_info("等待10秒释放资源...")
        time.sleep(10)
        print()

# 打印总结
print_header("📊 测试执行总结")

print("模块执行结果：")
print("-" * 60)
for module, status in results:
    print(f"  {status:<10} {module}")
print("-" * 60)
print(f"  ✅ 通过: {passed}/{total}")
print(f"  ❌ 失败: {failed}/{total}")
print()

# 生成Allure报告
print_header("📊 生成Allure报告")

if not list(allure_results.glob("*.json")):
    print_error("未找到测试结果，无法生成报告")
else:
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
            print("🌐 查看方式：")
            print(f"   方式1: open {allure_report}/index.html")
            print(f"   方式2: allure open {allure_report}")
            print(f"   方式3: allure serve {allure_results}")
        else:
            print_error("Allure报告生成失败")
            print(result.stderr)
    except Exception as e:
        print_error(f"生成报告时出错: {e}")

print_header("🎉 完成！")

# 返回退出码
exit(0 if failed == 0 else 1)

