#!/usr/bin/env python3
"""
验证 Aevatar 测试环境配置
确保所有测试都使用正确的环境URL
"""

import os
import sys
import yaml
from pathlib import Path

# 期望的环境URL
EXPECTED_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"

def check_yaml_config():
    """检查 YAML 配置文件"""
    print("📋 检查 YAML 配置文件...")
    yaml_path = Path("test-data/aevatar_test_data.yaml")
    
    if not yaml_path.exists():
        print(f"❌ YAML文件不存在: {yaml_path}")
        return False
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    env = data.get('environment', {})
    base_url = env.get('base_url', '')
    login_url = env.get('login_url', '')
    
    if EXPECTED_BASE_URL in base_url and EXPECTED_BASE_URL in login_url:
        print(f"✅ YAML配置正确: {base_url}")
        return True
    else:
        print(f"❌ YAML配置错误:")
        print(f"   期望: {EXPECTED_BASE_URL}")
        print(f"   实际: {base_url}")
        return False

def check_python_files():
    """检查Python测试文件中的URL配置"""
    print("\n📋 检查Python测试文件...")
    
    test_files = [
        "tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py",
        "tests/aevatar/test_daily_regression_project.py",
        "tests/aevatar/test_daily_regression_organisation.py",
        "tests/aevatar/test_daily_regression_dashboard.py",
    ]
    
    all_correct = True
    for file_path in test_files:
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if EXPECTED_BASE_URL in content:
            print(f"✅ {path.name}: 配置正确")
        else:
            print(f"❌ {path.name}: 未找到正确的URL")
            all_correct = False
    
    return all_correct

def check_old_urls():
    """检查是否还有旧的URL残留"""
    print("\n📋 检查旧URL残留...")
    
    old_urls = [
        "http://env-273db67a-ui.station-testing.aevatar.ai",
        "station-testing.aevatar.ai"
    ]
    
    test_dir = Path("tests/aevatar")
    found_old = False
    
    for py_file in test_dir.glob("test_*.py"):
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old_url in old_urls:
            if old_url in content:
                print(f"⚠️  {py_file.name}: 发现旧URL: {old_url}")
                found_old = True
    
    if not found_old:
        print("✅ 未发现旧URL残留")
    
    return not found_old

def main():
    """主函数"""
    print("="*80)
    print("🌐 Aevatar 测试环境配置验证")
    print("="*80)
    print()
    print(f"期望环境: {EXPECTED_BASE_URL}")
    print()
    
    # 检查各项配置
    yaml_ok = check_yaml_config()
    python_ok = check_python_files()
    no_old_urls = check_old_urls()
    
    # 总结
    print()
    print("="*80)
    print("📊 验证结果汇总")
    print("="*80)
    print(f"YAML配置:     {'✅ 通过' if yaml_ok else '❌ 失败'}")
    print(f"Python文件:   {'✅ 通过' if python_ok else '❌ 失败'}")
    print(f"无旧URL残留:  {'✅ 通过' if no_old_urls else '⚠️  警告'}")
    print()
    
    if yaml_ok and python_ok and no_old_urls:
        print("🎉 所有检查通过！环境配置正确！")
        print()
        print("💡 现在可以运行测试:")
        print("   pytest tests/aevatar/ -v -n auto")
        return 0
    else:
        print("❌ 部分检查失败，请修复配置后重试")
        print()
        print("💡 查看详细配置:")
        print("   cat TEST_ENVIRONMENT.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())

