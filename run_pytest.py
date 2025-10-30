#!/usr/bin/env python3
"""
Aevatar 有头模式 pytest 测试运行器
使用pytest-html框架生成专业测试报告
"""

import subprocess
import os
from datetime import datetime
import sys
import webbrowser

def run_pytest_tests():
    """运行有头模式pytest测试"""
    project_root = os.path.abspath(os.path.dirname(__file__))
    reports_dir = os.path.join(project_root, "reports")
    logs_dir = os.path.join(project_root, "logs")
    screenshots_dir = os.path.join(project_root, "test-screenshots")

    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🌌 Aevatar 有头模式pytest测试")
    print(f"============================================================")
    print(f"测试时间: {current_time}")
    print(f"测试框架: pytest + pytest-html")
    print(f"浏览器: 有头模式")
    print(f"============================================================")
    print(f"📁 创建目录: {reports_dir.split('/')[-1]}")
    print(f"📁 创建目录: {logs_dir.split('/')[-1]}")
    print(f"📁 创建目录: {screenshots_dir.split('/')[-1]}")

    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_root)

    pytest_args = [
        "python3", "-m", "pytest",
        "tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py",
        "-v",  # 详细输出
        "--tb=short",  # 简短的traceback
        "--html=reports/pytest-report.html",  # HTML报告
        "--self-contained-html",  # 自包含HTML
        "--durations=10",  # 显示最慢的10个测试
        "--junitxml=reports/pytest-junit.xml",  # JUnit XML报告
        "--json-report",  # JSON报告
        "--json-report-file=reports/pytest-report.json",  # JSON报告文件
        "--capture=no",  # 显示print输出
        "--log-cli-level=INFO",  # 日志级别
        "--log-cli-format=%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        "--log-cli-date-format=%Y-%m-%d %H:%M:%S",
        "--log-file=logs/pytest.log",  # 日志文件
        "--log-file-level=DEBUG",  # 日志文件级别
        "-p", "no:xonsh", # 禁用xonsh插件
        "--maxfail=2", # 最多允许2个失败
        "--color=yes"
    ]

    print(f"🔧 执行命令: {' '.join(pytest_args)}")
    print("=" * 60)

    try:
        result = subprocess.run(pytest_args, cwd=project_root, capture_output=True, text=True, check=False, env=env)
        print(result.stdout)
        print(result.stderr)

        html_report_path = os.path.join(reports_dir, "pytest-report.html")
        json_report_path = os.path.join(reports_dir, "pytest-report.json")
        junit_report_path = os.path.join(reports_dir, "pytest-junit.xml")
        log_file_path = os.path.join(logs_dir, "pytest.log")

        print("============================================================")
        if result.returncode == 0:
            print("✅ 所有有头模式测试通过!")
        else:
            print(f"❌ 测试失败 (退出码: {result.returncode})")

        print("\n📊 生成的报告文件:")
        for report_file, original_name in [
            (html_report_path, "pytest-report.html"),
            (json_report_path, "pytest-report.json"),
            (junit_report_path, "pytest-junit.xml"),
            (log_file_path, "pytest.log")
        ]:
            if os.path.exists(report_file):
                file_size = os.path.getsize(report_file)
                print(f"  ✅ {original_name} -> {report_file} ({file_size} bytes)")
                if original_name == "pytest-report.html":
                    print(f"🌐 已在浏览器中打开: {original_name}")
                    open_report_in_browser(report_file)
            else:
                print(f"  ❌ {original_name} (文件不存在)")

        # 解析测试统计
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        skipped_tests = 0
        total_duration = 0.0

        if "collected" in result.stdout:
            try:
                collected_line = [line for line in result.stdout.splitlines() if "collected" in line][-1]
                total_tests = int(collected_line.split("collected ")[1].split(" items")[0])
            except:
                pass

        if "passed" in result.stdout:
            passed_tests = len([line for line in result.stdout.splitlines() if "PASSED" in line])
        if "failed" in result.stdout:
            failed_tests = len([line for line in result.stdout.splitlines() if "FAILED" in line])
        if "skipped" in result.stdout:
            skipped_tests = len([line for line in result.stdout.splitlines() if "SKIPPED" in line])

        import re
        duration_match = re.search(r"in (\d+\.\d+)s", result.stdout)
        if duration_match:
            total_duration = float(duration_match.group(1))
        else:
            duration_match = re.search(r"in (\d+:\d+)", result.stdout)
            if duration_match:
                minutes, seconds = map(int, duration_match.group(1).split(':'))
                total_duration = minutes * 60 + seconds

        print("\n📈 测试统计:")
        print(f"  📊 总测试数: {total_tests}")
        print(f"  ✅ 通过: {passed_tests}")
        print(f"  ❌ 失败: {failed_tests}")
        print(f"  ⏭️ 跳过: {skipped_tests}")
        print(f"  ⏱️ 总耗时: {total_duration:.2f}秒")

        print("\n============================================================")
        if result.returncode == 0:
            print("🎉 有头模式pytest测试执行完成! 请查看生成的报告文件")
        else:
            print("❌ 有头模式pytest测试执行失败! 请查看日志和报告文件")
        print(f"📄 HTML报告: {os.path.relpath(html_report_path, project_root)}")
        print(f"📄 JSON报告: {os.path.relpath(json_report_path, project_root)}")
        print(f"📄 JUnit报告: {os.path.relpath(junit_report_path, project_root)}")
        print(f"📄 日志文件: {os.path.relpath(log_file_path, project_root)}")
        print("============================================================")

        return result.returncode
    except FileNotFoundError:
        print("❌ 错误: python3 命令未找到。请确保Python已正确安装并配置到PATH中。")
        return 1
    except Exception as e:
        print(f"❌ 执行pytest时发生未知错误: {e}")
        return 1

def open_report_in_browser(report_path: str):
    """在浏览器中打开测试报告"""
    try:
        abs_path = os.path.abspath(report_path)
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.run(['open', abs_path])
        elif sys.platform.startswith('win'):  # Windows
            os.startfile(abs_path)
        elif sys.platform.startswith('linux'):  # Linux
            subprocess.run(['xdg-open', abs_path])
        else:
            webbrowser.open(f'file://{abs_path}')
    except Exception as e:
        print(f"❌ 无法打开浏览器: {e}")
        print(f"请手动打开文件: {abs_path}")

if __name__ == "__main__":
    sys.exit(run_pytest_tests())
