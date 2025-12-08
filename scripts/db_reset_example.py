#!/usr/bin/env python3
"""
数据库重置密码脚本使用示例
"""
import os
import sys
from pathlib import Path

# 设置数据库连接信息（示例）
os.environ["DB_TYPE"] = "sqlserver"  # 或 "postgresql", "mysql"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "1433"  # SQL Server默认1433
os.environ["DB_NAME"] = "AevatarStation"
os.environ["DB_USER"] = "sa"
os.environ["DB_PASSWORD"] = "your_password"

# 导入重置函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.db_reset_passwords import reset_all_passwords, reset_single_password

if __name__ == "__main__":
    # 示例1: 重置所有账号
    print("=" * 50)
    print("示例1: 重置所有账号")
    print("=" * 50)
    reset_all_passwords()
    
    # 示例2: 重置单个账号
    print("\n" + "=" * 50)
    print("示例2: 重置单个账号")
    print("=" * 50)
    success = reset_single_password("qatest_v3__001")
    if success:
        print("✅ 单个账号重置成功")
    else:
        print("❌ 单个账号重置失败")

