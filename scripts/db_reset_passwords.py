#!/usr/bin/env python3
"""
数据库直接重置密码脚本
功能：直接操作数据库，将账号池中所有账号的密码重置为初始密码
优势：绕过API限制，更快、更可靠
"""
import json
import os
import hashlib
from pathlib import Path
from typing import Optional, List, Dict

# 数据库连接配置（从环境变量读取）
DB_TYPE = os.getenv("DB_TYPE", "sqlserver")  # sqlserver, postgresql, mysql
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")  # SQL Server默认1433, PostgreSQL默认5432, MySQL默认3306
DB_NAME = os.getenv("DB_NAME", "AevatarStation")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"
TARGET_PASSWORD = "TestPass123!"


def get_db_connection():
    """
    根据DB_TYPE创建数据库连接
    """
    if DB_TYPE.lower() == "sqlserver":
        try:
            import pyodbc
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={DB_HOST},{DB_PORT};"
                f"DATABASE={DB_NAME};"
                f"UID={DB_USER};"
                f"PWD={DB_PASSWORD};"
                f"TrustServerCertificate=yes;"
            )
            return pyodbc.connect(conn_str)
        except ImportError:
            print("❌ 错误: 需要安装 pyodbc: pip install pyodbc")
            return None
        except Exception as e:
            print(f"❌ SQL Server连接失败: {e}")
            return None
    
    elif DB_TYPE.lower() == "postgresql":
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except ImportError:
            print("❌ 错误: 需要安装 psycopg2: pip install psycopg2-binary")
            return None
        except Exception as e:
            print(f"❌ PostgreSQL连接失败: {e}")
            return None
    
    elif DB_TYPE.lower() == "mysql":
        try:
            import pymysql
            conn = pymysql.connect(
                host=DB_HOST,
                port=int(DB_PORT),
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except ImportError:
            print("❌ 错误: 需要安装 pymysql: pip install pymysql")
            return None
        except Exception as e:
            print(f"❌ MySQL连接失败: {e}")
            return None
    
    else:
        print(f"❌ 不支持的数据库类型: {DB_TYPE}")
        return None


def get_password_hash_from_reference(conn, reference_username: str) -> Optional[str]:
    """
    从参考账号（已知密码正确的账号）获取密码哈希
    这是最可靠的方法，因为直接复制ABP生成的哈希值
    """
    cursor = conn.cursor()
    
    try:
        # 尝试不同的表名和字段名
        table_names = ["AspNetUsers", "AbpUsers", "Users"]
        username_fields = ["UserName", "user_name", "username"]
        password_fields = ["PasswordHash", "password_hash", "Password"]
        
        for table in table_names:
            for username_field in username_fields:
                for password_field in password_fields:
                    try:
                        if DB_TYPE.lower() == "sqlserver":
                            sql = f"""
                                SELECT {password_field}
                                FROM {table}
                                WHERE {username_field} = ?
                            """
                            cursor.execute(sql, (reference_username,))
                        elif DB_TYPE.lower() == "postgresql":
                            sql = f"""
                                SELECT {password_field}
                                FROM {table}
                                WHERE {username_field} = %s
                            """
                            cursor.execute(sql, (reference_username,))
                        elif DB_TYPE.lower() == "mysql":
                            sql = f"""
                                SELECT {password_field}
                                FROM {table}
                                WHERE {username_field} = %s
                            """
                            cursor.execute(sql, (reference_username,))
                        
                        result = cursor.fetchone()
                        if result and result[0]:
                            return result[0]
                    except:
                        continue
        
        return None
    except Exception as e:
        print(f"  ⚠️ 获取参考哈希失败: {e}")
        return None
    finally:
        cursor.close()


def reset_account_fields_in_db(
    conn, 
    current_username: str, 
    fields_to_reset: Dict[str, str],
    reference_username: Optional[str] = None
) -> bool:
    """
    在数据库中重置账号的字段（username, email, password等）
    
    Args:
        conn: 数据库连接
        current_username: 当前用户名（用于查找账号）
        fields_to_reset: 要重置的字段字典，例如：
            - {"password": "hash_value"} - 重置密码
            - {"username": "new_username", "email": "new_email"} - 重置用户名和邮箱
            - {"username": "new_username"} - 只重置用户名
        reference_username: 参考账号（用于获取密码哈希，如果重置密码）
    
    Returns:
        bool: 是否成功
    """
    cursor = conn.cursor()
    
    try:
        # 尝试不同的表名（根据ABP版本）
        table_names = [
            "AspNetUsers",      # ASP.NET Core Identity标准表名
            "AbpUsers",          # ABP框架可能使用的表名
            "Users",             # 简化表名
        ]
        
        # 字段名映射
        field_mappings = {
            "username": ["UserName", "user_name", "username"],
            "email": ["Email", "email", "EmailAddress"],
            "password": ["PasswordHash", "password_hash", "Password"],
        }
        
        # 如果重置密码，需要从参考账号获取哈希
        if "password" in fields_to_reset and reference_username:
            password_hash = get_password_hash_from_reference(conn, reference_username)
            if password_hash:
                fields_to_reset["password"] = password_hash
            else:
                print(f"  ⚠️ 无法获取参考账号 {reference_username} 的密码哈希")
                return False
        
        # 尝试查找并更新
        for table in table_names:
            for username_field in field_mappings["username"]:
                try:
                    # 检查表是否存在
                    if DB_TYPE.lower() == "sqlserver":
                        check_table = f"""
                            SELECT COUNT(*) 
                            FROM INFORMATION_SCHEMA.TABLES 
                            WHERE TABLE_NAME = '{table}'
                        """
                        cursor.execute(check_table)
                        if cursor.fetchone()[0] == 0:
                            continue
                        
                        # 构建UPDATE语句
                        set_clauses = []
                        params = []
                        
                        for field_name, field_value in fields_to_reset.items():
                            if field_name == "password":
                                # 密码字段
                                for password_field in field_mappings["password"]:
                                    set_clauses.append(f"{password_field} = ?")
                                    params.append(field_value)
                                    break  # 只使用第一个匹配的字段名
                            elif field_name == "username":
                                # 用户名字段（注意：如果更新username，WHERE条件也需要用旧username）
                                for username_field_update in field_mappings["username"]:
                                    set_clauses.append(f"{username_field_update} = ?")
                                    params.append(field_value)
                                    break
                            elif field_name == "email":
                                # 邮箱字段
                                for email_field in field_mappings["email"]:
                                    set_clauses.append(f"{email_field} = ?")
                                    params.append(field_value)
                                    break
                        
                        if not set_clauses:
                            continue
                        
                        # 添加WHERE条件
                        params.append(current_username)
                        
                        update_sql = f"""
                            UPDATE {table}
                            SET {', '.join(set_clauses)}
                            WHERE {username_field} = ?
                        """
                        cursor.execute(update_sql, tuple(params))
                        
                    elif DB_TYPE.lower() == "postgresql":
                        check_table = f"""
                            SELECT COUNT(*) 
                            FROM information_schema.tables 
                            WHERE table_name = '{table.lower()}'
                        """
                        cursor.execute(check_table)
                        if cursor.fetchone()[0] == 0:
                            continue
                        
                        set_clauses = []
                        params = []
                        
                        for field_name, field_value in fields_to_reset.items():
                            if field_name == "password":
                                for password_field in field_mappings["password"]:
                                    set_clauses.append(f"{password_field} = %s")
                                    params.append(field_value)
                                    break
                            elif field_name == "username":
                                for username_field_update in field_mappings["username"]:
                                    set_clauses.append(f"{username_field_update} = %s")
                                    params.append(field_value)
                                    break
                            elif field_name == "email":
                                for email_field in field_mappings["email"]:
                                    set_clauses.append(f"{email_field} = %s")
                                    params.append(field_value)
                                    break
                        
                        if not set_clauses:
                            continue
                        
                        params.append(current_username)
                        
                        update_sql = f"""
                            UPDATE {table}
                            SET {', '.join(set_clauses)}
                            WHERE {username_field} = %s
                        """
                        cursor.execute(update_sql, tuple(params))
                    
                    elif DB_TYPE.lower() == "mysql":
                        check_table = f"""
                            SELECT COUNT(*) 
                            FROM information_schema.tables 
                            WHERE table_schema = '{DB_NAME}' 
                            AND table_name = '{table}'
                        """
                        cursor.execute(check_table)
                        if cursor.fetchone()[0] == 0:
                            continue
                        
                        set_clauses = []
                        params = []
                        
                        for field_name, field_value in fields_to_reset.items():
                            if field_name == "password":
                                for password_field in field_mappings["password"]:
                                    set_clauses.append(f"{password_field} = %s")
                                    params.append(field_value)
                                    break
                            elif field_name == "username":
                                for username_field_update in field_mappings["username"]:
                                    set_clauses.append(f"{username_field_update} = %s")
                                    params.append(field_value)
                                    break
                            elif field_name == "email":
                                for email_field in field_mappings["email"]:
                                    set_clauses.append(f"{email_field} = %s")
                                    params.append(field_value)
                                    break
                        
                        if not set_clauses:
                            continue
                        
                        params.append(current_username)
                        
                        update_sql = f"""
                            UPDATE {table}
                            SET {', '.join(set_clauses)}
                            WHERE {username_field} = %s
                        """
                        cursor.execute(update_sql, tuple(params))
                    
                    # 检查是否更新成功
                    if cursor.rowcount > 0:
                        conn.commit()
                        return True
                        
                except Exception as e:
                    # 表或字段不存在，继续尝试下一个
                    conn.rollback()
                    continue
        
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"  ❌ 数据库更新异常: {e}")
        return False
    finally:
        cursor.close()


def reset_password_in_db(conn, username: str, password_hash: str) -> bool:
    """
    重置密码（向后兼容的包装函数）
    """
    return reset_account_fields_in_db(conn, username, {"password": password_hash})


def reset_all_accounts(fields: List[str] = None):
    """
    重置账号池中所有账号的字段
    
    Args:
        fields: 要重置的字段列表，例如：
            - ["password"] - 只重置密码
            - ["username", "email"] - 重置用户名和邮箱
            - ["username", "email", "password"] - 重置所有字段
            如果为None，默认重置所有字段
    """
    if fields is None:
        fields = ["username", "email", "password"]
    
    field_names = {
        "username": "用户名",
        "email": "邮箱",
        "password": "密码"
    }
    fields_desc = "、".join([field_names.get(f, f) for f in fields])
    
    print(f"🚀 开始数据库直接重置账号字段...")
    print(f"   数据库类型: {DB_TYPE}")
    print(f"   重置字段: {fields_desc}")
    print("-" * 50)
    
    if not POOL_FILE.exists():
        print("❌ 账号池文件不存在")
        return
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    print(f"   检测账号: {len(accounts)} 个")
    print("-" * 50)
    
    # 连接数据库
    conn = get_db_connection()
    if not conn:
        print("❌ 无法连接数据库，请检查配置")
        return
    
    print("✅ 数据库连接成功")
    print("-" * 50)
    
    # 第一步：如果需要重置密码，从参考账号获取密码哈希
    reference_username = None
    password_hash = None
    
    if "password" in fields:
        for account in accounts:
            # 尝试找一个健康的账号作为参考
            if not account.get("is_locked", False):
                reference_username = account["username"]
                break
        
        if not reference_username and len(accounts) > 0:
            # 如果没有健康的账号，使用第一个账号
            reference_username = accounts[0]["username"]
        
        if reference_username:
            print(f"📋 使用参考账号 {reference_username} 获取密码哈希...")
            password_hash = get_password_hash_from_reference(conn, reference_username)
            if not password_hash:
                print("⚠️ 无法从参考账号获取密码哈希，尝试使用API重置参考账号...")
                # 如果无法获取，尝试通过API重置参考账号，然后再次获取
                import subprocess
                import sys
                api_script = Path(__file__).parent / "api_reset_passwords.py"
                if api_script.exists():
                    result = subprocess.run(
                        [sys.executable, str(api_script)],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        password_hash = get_password_hash_from_reference(conn, reference_username)
            
            if not password_hash:
                print("❌ 无法获取密码哈希，请确保至少有一个账号密码正确")
                conn.close()
                return
            
            print(f"✅ 获取到密码哈希（长度: {len(password_hash)}）")
            print("-" * 50)
        else:
            print("❌ 没有可用的参考账号")
            conn.close()
            return
    
    # 第二步：重置每个账号的字段
    success_count = 0
    failed_count = 0
    
    for account in accounts:
        username = account["username"]
        print(f"处理 {username}...", end=" ")
        
        # 构建要重置的字段字典
        fields_to_reset = {}
        
        if "username" in fields:
            fields_to_reset["username"] = account["username"]  # 重置为原始用户名
        
        if "email" in fields:
            fields_to_reset["email"] = account["email"]  # 重置为原始邮箱
        
        if "password" in fields and password_hash:
            fields_to_reset["password"] = password_hash
        
        if not fields_to_reset:
            print("⚠️ 没有要重置的字段")
            continue
        
        success = reset_account_fields_in_db(
            conn, 
            username, 
            fields_to_reset,
            reference_username if "password" in fields else None
        )
        
        if success:
            print("✅")
            success_count += 1
        else:
            print("❌")
            failed_count += 1
    
    conn.close()
    
    print("-" * 50)
    print("📊 重置结果统计:")
    print(f"   ✅ 成功: {success_count} 个")
    print(f"   ❌ 失败: {failed_count} 个")
    print("-" * 50)
    print("🏁 重置完成")


def reset_all_passwords():
    """
    重置所有账号的密码（向后兼容的包装函数）
    """
    reset_all_accounts(["password"])


def reset_account_to_original(
    username: str, 
    fields: List[str] = None,
    reference_username: Optional[str] = None
) -> bool:
    """
    将账号重置为原始状态（从账号池配置中读取原始值）
    
    Args:
        username: 要重置的账号用户名
        fields: 要重置的字段列表，例如 ["username", "email"] 或 ["password"]
                如果为None，则根据账号池配置自动判断
        reference_username: 参考账号（用于获取密码哈希，如果重置密码）
    
    Returns:
        bool: 是否成功
    """
    if not POOL_FILE.exists():
        return False
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    
    # 查找账号的原始配置
    original_account = None
    for account in accounts:
        if account["username"] == username:
            original_account = account
            break
    
    if not original_account:
        print(f"  ⚠️ 未找到账号 {username} 的原始配置")
        return False
    
    # 如果没有指定字段，自动判断
    if fields is None:
        # 默认重置所有字段（username, email, password）
        fields = ["username", "email", "password"]
    
    # 构建要重置的字段字典
    fields_to_reset = {}
    
    if "username" in fields:
        fields_to_reset["username"] = original_account["username"]
    
    if "email" in fields:
        fields_to_reset["email"] = original_account["email"]
    
    if "password" in fields:
        # 密码需要从参考账号获取哈希
        if not reference_username:
            # 从账号池中找一个健康的账号作为参考
            for account in accounts:
                if not account.get("is_locked", False) and account["username"] != username:
                    reference_username = account["username"]
                    break
        
        if not reference_username:
            print(f"  ⚠️ 无法找到参考账号来获取密码哈希")
            return False
    
    # 连接数据库并重置
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        success = reset_account_fields_in_db(
            conn, 
            username, 
            fields_to_reset,
            reference_username
        )
        return success
    finally:
        conn.close()


def reset_single_password(username: str, reference_username: Optional[str] = None) -> bool:
    """
    重置单个账号的密码（向后兼容的包装函数）
    """
    return reset_account_to_original(username, ["password"], reference_username)


if __name__ == "__main__":
    import sys
    
    # 支持命令行参数指定要重置的字段
    # 例如: python db_reset_passwords.py --fields username email
    # 或: python db_reset_passwords.py --fields password
    # 或: python db_reset_passwords.py --fields username email password
    
    fields = None
    if len(sys.argv) > 1 and sys.argv[1] == "--fields":
        if len(sys.argv) > 2:
            fields = sys.argv[2:]
        else:
            print("❌ 错误: --fields 参数后需要指定字段名")
            print("   示例: python db_reset_passwords.py --fields username email")
            print("   示例: python db_reset_passwords.py --fields password")
            sys.exit(1)
    
    if fields:
        reset_all_accounts(fields)
    else:
        # 默认重置所有字段
        reset_all_accounts()

