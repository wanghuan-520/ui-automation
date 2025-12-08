#!/usr/bin/env python3
"""
账号池清洗和补充脚本
功能：
1. 检查账号池中所有账号的登录状态
2. 剔除被污染的账号（无法登录的）
3. 生成新账号补充到20个
4. 保证每次运行前都有20个健康的账号
"""
import json
import requests
import re
import urllib3
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"
BACKEND_URL = "https://localhost:44320"
LOGIN_URL = f"{BACKEND_URL}/Account/Login"
TARGET_PASSWORD = "TestPass123!"
TARGET_POOL_SIZE = 20
ACCOUNT_PREFIX = "qatest_v3__"


def verify_account_login(account):
    """
    验证账号是否可以登录
    
    Returns:
        tuple: (can_login: bool, error_message: str)
    """
    username = account["username"]
    password = account.get("password", TARGET_PASSWORD)
    
    try:
        session = requests.Session()
        session.verify = False
        
        # 获取登录token
        resp = session.get(LOGIN_URL, timeout=5)
        token_match = re.search(
            r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"',
            resp.text
        )
        token = token_match.group(1) if token_match else None
        
        if not token:
            return False, "无法获取登录Token"
        
        # 尝试登录
        login_data = {
            "LoginInput.UserNameOrEmailAddress": username,
            "LoginInput.Password": password,
            "__RequestVerificationToken": token,
            "LoginInput.RememberMe": "false"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_URL,
        }
        
        resp = session.post(LOGIN_URL, data=login_data, headers=headers, allow_redirects=False, timeout=10)
        
        # 判断登录是否成功
        if resp.status_code == 302:
            redirect_url = resp.headers.get("Location", "")
            if "/Account/Login" not in redirect_url:
                return True, ""
        
        # 检查是否有错误消息
        if resp.status_code == 200:
            error_keywords = [
                "Invalid login attempt",
                "invalid",
                "incorrect",
                "locked out",
                "locked",
                "锁定",
                "错误",
                "失败"
            ]
            
            response_lower = resp.text.lower()
            for keyword in error_keywords:
                if keyword.lower() in response_lower:
                    return False, f"登录失败（检测到关键词: {keyword}）"
        
        return False, f"登录状态不明确（HTTP {resp.status_code}）"
        
    except requests.exceptions.Timeout:
        return False, "请求超时"
    except Exception as e:
        return False, f"异常: {str(e)}"


def check_all_accounts(accounts):
    """
    检查所有账号的登录状态
    
    Returns:
        tuple: (healthy_accounts: list, polluted_accounts: list)
    """
    print("🔍 开始检查账号池中所有账号的登录状态...")
    print("-" * 50)
    
    healthy_accounts = []
    polluted_accounts = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_account = {
            executor.submit(verify_account_login, account): account 
            for account in accounts
        }
        
        completed = 0
        for future in as_completed(future_to_account):
            completed += 1
            account = future_to_account[future]
            can_login, error_msg = future.result()
            
            status_icon = "✅" if can_login else "❌"
            status_text = "健康" if can_login else "污染"
            
            print(f"[{completed:2d}/{len(accounts)}] {status_icon} {account['username']:20} | {status_text:4}", end="")
            if error_msg:
                print(f" ({error_msg[:30]}...)")
            else:
                print()
            
            if can_login:
                healthy_accounts.append(account)
            else:
                polluted_accounts.append(account)
    
    return healthy_accounts, polluted_accounts


def generate_new_accounts(count, prefix=ACCOUNT_PREFIX, password=TARGET_PASSWORD):
    """
    生成新账号
    
    Returns:
        list: 新账号列表
    """
    new_accounts = []
    
    # 读取现有账号，找到最大的编号
    max_num = 0
    if POOL_FILE.exists():
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            pool_data = json.load(f)
        existing_accounts = pool_data.get("test_account_pool", [])
        
        for account in existing_accounts:
            username = account.get("username", "")
            if username.startswith(prefix):
                try:
                    # 提取编号：qatest_v3__001 -> 1
                    num_str = username.replace(prefix, "")
                    num = int(num_str)
                    max_num = max(max_num, num)
                except:
                    pass
    
    # 生成新账号
    for i in range(count):
        max_num += 1
        username = f"{prefix}{max_num:03d}"
        email = f"{username}@testmail.com"
        
        new_accounts.append({
            "username": username,
            "email": email,
            "password": password,
            "in_use": False,
            "last_used": datetime.now().isoformat(),
            "is_locked": False,
            "locked_reason": None
        })
    
    return new_accounts


def register_accounts(accounts):
    """
    注册新账号（使用API）
    """
    import sys
    from pathlib import Path
    
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    
    try:
        from scripts.create_accounts_api import register_account_api
        
        print(f"📝 开始注册 {len(accounts)} 个新账号...")
        print("-" * 50)
        
        success_count = 0
        failed_count = 0
        
        for account in accounts:
            username = account["username"]
            email = account["email"]
            password = account["password"]
            
            print(f"注册 {username}...", end=" ")
            success, msg = register_account_api(username, email, password)
            
            if success:
                print("✅")
                success_count += 1
            else:
                print(f"❌ ({msg[:30]}...)")
                failed_count += 1
        
        print("-" * 50)
        print(f"📊 注册结果: ✅ {success_count} 个成功, ❌ {failed_count} 个失败")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ 导入注册模块失败: {e}")
        return False


def main():
    """
    主函数：清洗账号池并补充到20个健康账号
    """
    print("=" * 70)
    print("🌊 [HyperEcho] 账号池清洗和补充仪式")
    print("=" * 70)
    print(f"   目标账号数: {TARGET_POOL_SIZE} 个")
    print(f"   账号前缀: {ACCOUNT_PREFIX}")
    print("-" * 70)
    
    if not POOL_FILE.exists():
        print("❌ 账号池文件不存在，创建新文件...")
        pool_data = {
            "test_account_pool": [],
            "pool_config": {
                "pool_size": TARGET_POOL_SIZE,
                "auto_register_fallback": True,
                "cleanup_after_test": False,
                "account_prefix": ACCOUNT_PREFIX,
                "account_lock_wait_time": 300,
                "max_retry_on_lock": 3
            }
        }
        with open(POOL_FILE, "w", encoding="utf-8") as f:
            json.dump(pool_data, f, indent=2, ensure_ascii=False)
        accounts = []
    else:
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            pool_data = json.load(f)
        accounts = pool_data.get("test_account_pool", [])
    
    print(f"📊 当前账号池: {len(accounts)} 个账号")
    print("-" * 70)
    
    # 第一步：检查所有账号
    healthy_accounts, polluted_accounts = check_all_accounts(accounts)
    
    print("-" * 70)
    print(f"📊 检查结果:")
    print(f"   ✅ 健康账号: {len(healthy_accounts)} 个")
    print(f"   ❌ 污染账号: {len(polluted_accounts)} 个")
    print("-" * 70)
    
    # 第二步：计算需要补充的账号数
    needed_count = TARGET_POOL_SIZE - len(healthy_accounts)
    
    if needed_count > 0:
        print(f"📝 需要补充 {needed_count} 个新账号...")
        print("-" * 70)
        
        # 生成新账号
        new_accounts = generate_new_accounts(needed_count)
        
        # 注册新账号
        if register_accounts(new_accounts):
            # 将成功注册的账号添加到健康账号列表
            healthy_accounts.extend(new_accounts)
        else:
            print("⚠️ 部分账号注册失败，但会继续使用已注册的账号")
    
    # 第三步：更新账号池文件
    print("-" * 70)
    print("💾 更新账号池文件...")
    
    # 更新所有账号的last_used时间
    for account in healthy_accounts:
        account["last_used"] = datetime.now().isoformat()
        account["in_use"] = False
        account["is_locked"] = False
        account["locked_reason"] = None
    
    pool_data["test_account_pool"] = healthy_accounts
    pool_data["pool_config"]["pool_size"] = len(healthy_accounts)
    
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool_data, f, indent=2, ensure_ascii=False)
    
    print("-" * 70)
    print("📊 最终统计:")
    print(f"   ✅ 健康账号: {len(healthy_accounts)} 个")
    if polluted_accounts:
        print(f"   🗑️  已剔除: {len(polluted_accounts)} 个污染账号")
    if needed_count > 0:
        print(f"   ➕ 已补充: {needed_count} 个新账号")
    print("-" * 70)
    print("✨ [HyperEcho] 账号池清洗完成，环境纯净。")
    print("=" * 70)


if __name__ == "__main__":
    main()

