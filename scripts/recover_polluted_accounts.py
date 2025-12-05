"""
尝试恢复被污染的账号
根据测试代码分析，尝试所有可能的污染密码，找到正确的当前密码后恢复为原始密码
"""
import json
import requests
from pathlib import Path
from datetime import datetime
import urllib3
import re

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
BASE_URL = "https://localhost:44320"
LOGIN_URL = f"{BASE_URL}/Account/Login"
POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

# 污染账号列表（从验证结果获得）
POLLUTED_ACCOUNTS = [
    "qatest__006", "qatest__008", "qatest__009", "qatest__010", "qatest__012",
    "qatest__014", "qatest__016", "qatest__017", "qatest__018", "qatest__019", "qatest__020"
]

# 可能的污染密码（根据测试代码分析）
POSSIBLE_POLLUTED_PASSWORDS = [
    # TC-PWD-010 使用的密码
    "NewPwd123!@",
    
    # TC-PWD-006 (test_p1_password_length_boundary) 边界值
    "Ab1!56",                # 6字符（最小边界）
    "Ab1!234",               # 7字符（小于最小）
    "Ab1!2345",              # 8字符（大于最小）
    "Ab1!2345678901234567890",  # 超长测试
    "Ab1!23456789012345678901234567890123456789012345678901234567890123456",  # 最大边界
    
    # 其他可能的测试密码
    "TestNew123!",           # 可能的变体
    "Changed123!",           # 可能的变体
]


def try_login(username, password):
    """
    尝试使用给定密码登录
    
    Returns:
        bool: 登录是否成功
    """
    try:
        session = requests.Session()
        session.verify = False
        
        # 获取登录页面
        response = session.get(LOGIN_URL, timeout=10)
        response.raise_for_status()
        
        # 提取AntiForgeryToken
        token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', response.text)
        antiforgery_token = token_match.group(1) if token_match else None
        
        # 提交登录
        login_data = {
            "LoginInput.UserNameOrEmailAddress": username,
            "LoginInput.Password": password,
            "LoginInput.RememberMe": "false",
        }
        if antiforgery_token:
            login_data["__RequestVerificationToken"] = antiforgery_token
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_URL,
        }
        
        response = session.post(LOGIN_URL, data=login_data, headers=headers, timeout=10, allow_redirects=False)
        
        # 检查登录结果
        if response.status_code == 302:
            redirect_url = response.headers.get("Location", "")
            if "/Account/Login" not in redirect_url:
                return True, session
        
        return False, None
        
    except Exception as e:
        print(f"      ⚠️ 登录尝试异常: {e}")
        return False, None


def change_password(session, current_password, new_password):
    """
    修改密码
    
    Args:
        session: 已登录的session
        current_password: 当前密码
        new_password: 新密码
    
    Returns:
        bool: 修改是否成功
    """
    try:
        # 获取修改密码页面
        change_pwd_url = f"{BASE_URL}/App/Profile?tabName=ChangePassword"
        response = session.get(change_pwd_url, timeout=10)
        response.raise_for_status()
        
        # 提取AntiForgeryToken
        token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', response.text)
        antiforgery_token = token_match.group(1) if token_match else None
        
        # 提交修改密码请求
        change_data = {
            "CurrentPassword": current_password,
            "NewPassword": new_password,
            "NewPasswordRepeat": new_password,
        }
        if antiforgery_token:
            change_data["__RequestVerificationToken"] = antiforgery_token
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": change_pwd_url,
        }
        
        response = session.post(change_pwd_url, data=change_data, headers=headers, timeout=10, allow_redirects=False)
        
        # 检查是否成功（通常返回200或302）
        if response.status_code in [200, 302]:
            # 检查响应中是否有success相关信息
            if "success" in response.text.lower() or response.status_code == 302:
                return True
        
        return False
        
    except Exception as e:
        print(f"      ⚠️ 修改密码异常: {e}")
        return False


def recover_account(username, original_password):
    """
    尝试恢复单个账号
    
    Args:
        username: 用户名
        original_password: 原始密码（账号池中的密码）
    
    Returns:
        dict: {success: bool, current_password: str, message: str}
    """
    print(f"\n{'='*70}")
    print(f"🔧 开始恢复账号: {username}")
    print(f"{'='*70}")
    
    # 首先尝试原始密码（可能未被污染）
    print(f"  1️⃣ 尝试原始密码: {original_password[:3]}***")
    success, session = try_login(username, original_password)
    if success:
        print(f"  ✅ 账号未被污染，无需恢复")
        return {
            "success": True,
            "current_password": original_password,
            "message": "账号未被污染"
        }
    
    # 尝试所有可能的污染密码
    print(f"  2️⃣ 账号已被污染，尝试 {len(POSSIBLE_POLLUTED_PASSWORDS)} 个可能的污染密码...")
    
    for idx, polluted_pwd in enumerate(POSSIBLE_POLLUTED_PASSWORDS, 1):
        print(f"     [{idx}/{len(POSSIBLE_POLLUTED_PASSWORDS)}] 尝试: {polluted_pwd[:8]}{'...' if len(polluted_pwd) > 8 else ''}")
        
        success, session = try_login(username, polluted_pwd)
        if success:
            print(f"     ✅ 找到当前密码: {polluted_pwd[:8]}...")
            print(f"  3️⃣ 开始恢复密码为原始密码...")
            
            # 尝试修改回原始密码
            change_success = change_password(session, polluted_pwd, original_password)
            if change_success:
                print(f"  ✅✅✅ 恢复成功！密码已改回 {original_password[:3]}***")
                return {
                    "success": True,
                    "current_password": polluted_pwd,
                    "message": f"成功恢复（原密码:{polluted_pwd[:8]}...）"
                }
            else:
                print(f"  ❌ 修改密码失败，可能需要手动处理")
                return {
                    "success": False,
                    "current_password": polluted_pwd,
                    "message": f"找到密码但修改失败（当前:{polluted_pwd[:8]}...）"
                }
    
    # 所有密码都尝试失败
    print(f"  ❌ 未找到正确的当前密码，无法恢复")
    return {
        "success": False,
        "current_password": "unknown",
        "message": "未找到正确的当前密码"
    }


def main():
    """主函数"""
    print("=" * 80)
    print("🔧 污染账号恢复工具")
    print("=" * 80)
    print()
    print(f"📊 污染账号数量: {len(POLLUTED_ACCOUNTS)}个")
    print(f"🔑 尝试密码数量: {len(POSSIBLE_POLLUTED_PASSWORDS)}个")
    print(f"📂 账号池文件: {POOL_FILE}")
    print()
    
    # 读取账号池
    if not POOL_FILE.exists():
        print(f"❌ 错误：账号池文件不存在: {POOL_FILE}")
        return
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = {acc["username"]: acc for acc in pool_data.get("test_account_pool", [])}
    
    # 验证污染账号是否存在于账号池
    missing_accounts = [username for username in POLLUTED_ACCOUNTS if username not in accounts]
    if missing_accounts:
        print(f"⚠️ 警告：以下账号不在账号池中: {missing_accounts}")
    
    # 开始恢复
    print("=" * 80)
    print("🚀 开始恢复流程...")
    print("=" * 80)
    
    results = []
    for username in POLLUTED_ACCOUNTS:
        if username not in accounts:
            print(f"\n⚠️ 跳过不存在的账号: {username}")
            results.append({
                "username": username,
                "success": False,
                "current_password": "N/A",
                "message": "账号不在账号池中"
            })
            continue
        
        account = accounts[username]
        original_password = account["password"]
        
        result = recover_account(username, original_password)
        results.append({
            "username": username,
            **result
        })
    
    # 统计结果
    print("\n" + "=" * 80)
    print("📈 恢复结果统计")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    
    print(f"✅ 恢复成功: {success_count}个")
    print(f"❌ 恢复失败: {fail_count}个")
    print(f"📊 恢复率: {success_count * 100 // len(results)}%")
    print()
    
    if success_count > 0:
        print("✅ 恢复成功的账号:")
        for r in results:
            if r["success"]:
                print(f"   • {r['username']:20} | {r['message']}")
        print()
    
    if fail_count > 0:
        print("❌ 恢复失败的账号:")
        for r in results:
            if not r["success"]:
                print(f"   • {r['username']:20} | {r['message']}")
        print()
    
    # 保存结果
    result_file = POOL_FILE.parent / f"account_recovery_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "recovery_time": datetime.now().isoformat(),
            "total_accounts": len(results),
            "success_count": success_count,
            "fail_count": fail_count,
            "recovery_rate": f"{success_count * 100 // len(results)}%",
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 详细结果已保存到: {result_file}")
    print()
    
    if fail_count > 0:
        print("⚠️ 建议:")
        print("   1. 对于恢复失败的账号，可以尝试手动在后台管理系统重置密码")
        print("   2. 或者删除这些账号，让测试自动注册新账号")
        print("   3. 检查是否有其他未知的测试密码导致污染")
    
    print()
    print("=" * 80)
    print("🏁 恢复流程完成")
    print("=" * 80)


if __name__ == "__main__":
    main()

