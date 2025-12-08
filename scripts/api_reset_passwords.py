#!/usr/bin/env python3
"""
API账号清洗脚本
功能：尝试使用所有已知密码登录账号，一旦成功，通过API强制将密码重置为初始密码。
速度：极快（多线程并发）
"""
import json
import requests
import urllib3
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
# 注意：前端和后端URL不同
FRONTEND_URL = "https://localhost:3000"  # 前端（管理员后台在这里）
BACKEND_URL = "https://localhost:44320"  # 后端（登录API在这里）
LOGIN_URL = f"{BACKEND_URL}/Account/Login"

# 用户API端点
CHANGE_PWD_API = f"{BACKEND_URL}/api/account/my-profile/change-password" 
CHANGE_PWD_API_ALT = f"{BACKEND_URL}/api/identity/my-profile/change-password"

# 管理员API端点
# 注意：前端API需要JWT token，后端API使用session cookie
ADMIN_USERS_API_FRONTEND = f"{FRONTEND_URL}/api/identity/users"
ADMIN_USERS_API_BACKEND = f"{BACKEND_URL}/api/identity/users"

POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

# 管理员账号
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1q2w3E*"

# 目标密码（初始密码）
TARGET_PASSWORD = "TestPass123!"

# 已知可能被修改成的密码列表（撞库列表）
POSSIBLE_PASSWORDS = [
    "TestPass123!",            # 初始密码
    "NewPwd123!@",             # TC-PWD-010
    "Ab1!56",                  # 6字符边界
    "Ab1!567",                 # 7字符边界
    "Ab1!5678901234567890123456789012", # 32字符边界
    "NewPassword123!",         # 其他测试
    "Changed123!",
    "WrongPassword123!",
]

def get_anti_forgery_token(session, url=LOGIN_URL):
    """从登录页面获取防伪令牌"""
    try:
        resp = session.get(url, verify=False, timeout=5)
        match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', resp.text)
        return match.group(1) if match else None
    except:
        return None

def admin_login():
    """
    管理员登录，返回带权限的Session
    """
    session = requests.Session()
    session.verify = False
    
    try:
        # 获取Token
        token = get_anti_forgery_token(session)
        if not token:
            return None, "无法获取登录Token"
        
        # 管理员登录
        login_data = {
            "LoginInput.UserNameOrEmailAddress": ADMIN_USERNAME,
            "LoginInput.Password": ADMIN_PASSWORD,
            "__RequestVerificationToken": token,
            "LoginInput.RememberMe": "false"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_URL,
        }
        
        resp = session.post(LOGIN_URL, data=login_data, headers=headers, allow_redirects=False, timeout=10)
        
        if resp.status_code == 302 and "/Account/Login" not in resp.headers.get("Location", ""):
            return session, "登录成功"
        else:
            return None, f"登录失败 (HTTP {resp.status_code})"
            
    except Exception as e:
        return None, f"登录异常: {str(e)}"

def get_user_by_username(admin_session, username):
    """
    通过用户名获取用户信息（包括ID）
    使用后端API（因为前端API需要JWT token）
    支持分页获取所有用户
    """
    xsrf = admin_session.cookies.get("XSRF-TOKEN") or admin_session.cookies.get("xsrf-token")
    headers = {
        "Content-Type": "application/json",
    }
    if xsrf:
        headers["X-XSRF-TOKEN"] = xsrf
    
    # 尝试后端API（使用MaxResultCount获取所有用户）
    try:
        resp = admin_session.get(f"{ADMIN_USERS_API_BACKEND}?MaxResultCount=1000", headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # ABP返回的数据结构可能是 items 数组
            users = data.get("items", []) if isinstance(data, dict) else data
            for user in users:
                if user.get("userName") == username:
                    return user
    except Exception as e:
        print(f"  ⚠️ 获取用户列表失败: {e}")
    
    return None

def admin_delete_user(admin_session, username):
    """
    使用管理员权限删除用户
    步骤：
    1. 通过用户名获取用户信息（包括ID）
    2. 尝试硬删除（DELETE），如果失败则尝试软删除（PUT标记isDeleted=true）
    """
    # 获取XSRF Token
    xsrf = admin_session.cookies.get("XSRF-TOKEN") or admin_session.cookies.get("xsrf-token")
    
    headers = {
        "Content-Type": "application/json",
    }
    if xsrf:
        headers["X-XSRF-TOKEN"] = xsrf
    
    # 第一步：获取用户信息
    user_info = get_user_by_username(admin_session, username)
    if not user_info:
        return False, "无法找到用户"
    
    user_id = user_info.get("id")
    if not user_id:
        return False, "用户ID不存在"
    
    # 第二步：尝试硬删除（DELETE）
    delete_url = f"{ADMIN_USERS_API_BACKEND}/{user_id}"
    try:
        resp = admin_session.delete(delete_url, headers=headers, timeout=10)
        if resp.status_code in [200, 204]:
            return True, "硬删除成功"
    except Exception as e:
        pass
    
    # 第三步：如果硬删除失败，尝试软删除（标记isDeleted=true）
    try:
        # 获取完整的用户数据，然后标记为已删除
        user_info["isDeleted"] = True
        user_info["deletionTime"] = None  # ABP会自动设置
        
        update_url = f"{ADMIN_USERS_API_BACKEND}/{user_id}"
        resp = admin_session.put(update_url, json=user_info, headers=headers, timeout=10)
        if resp.status_code in [200, 204]:
            return True, "软删除成功（标记为已删除）"
        else:
            error_text = resp.text[:100] if resp.text else "无响应"
            return False, f"软删除失败 (HTTP {resp.status_code}, {error_text})"
    except Exception as e:
        return False, f"删除异常: {str(e)}"

def admin_recreate_user(account):
    """
    重新注册用户（删除后重新创建）
    """
    import sys
    from pathlib import Path
    
    # 修复导入路径
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    
    try:
        from scripts.create_accounts_api import register_account_api
        
        username = account["username"]
        email = account["email"]
        password = TARGET_PASSWORD
        
        success, msg = register_account_api(username, email, password)
        
        if success:
            return True, "重新注册成功"
        else:
            return False, f"重新注册失败: {msg}"
    except Exception as e:
        return False, f"导入异常: {str(e)}"

def try_login_and_reset(account):
    username = account["username"]
    
    # 先检查账号是否被锁定（通过尝试登录检测）
    session = requests.Session()
    session.verify = False
    
    try:
        token = get_anti_forgery_token(session)
        if token:
            login_data = {
                "LoginInput.UserNameOrEmailAddress": username,
                "LoginInput.Password": TARGET_PASSWORD,
                "__RequestVerificationToken": token,
                "LoginInput.RememberMe": "false"
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": LOGIN_URL,
            }
            resp = session.post(LOGIN_URL, data=login_data, headers=headers, allow_redirects=False, timeout=10)
            
            # 检查是否被锁定
            if "locked out" in resp.text.lower() or "已锁定" in resp.text:
                return f"🔒 {username}: 账号被锁定（需要等待或使用管理员API）"
    except:
        pass
    
    # 尝试所有密码
    for pwd in POSSIBLE_PASSWORDS:
        session = requests.Session()
        session.verify = False
        
        try:
            # 1. 获取登录页Token
            token = get_anti_forgery_token(session)
            if not token:
                continue

            # 2. 尝试登录（使用正确的字段名：LoginInput.*）
            login_data = {
                "LoginInput.UserNameOrEmailAddress": username,
                "LoginInput.Password": pwd,
                "__RequestVerificationToken": token,
                "LoginInput.RememberMe": "false"
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": LOGIN_URL,
            }
            
            resp = session.post(LOGIN_URL, data=login_data, headers=headers, allow_redirects=False, timeout=10)
            
            # 调试：输出响应状态
            redirect_location = resp.headers.get("Location", "")
            
            # 检查是否登录成功（通常是302跳转，且不跳回登录页）
            if resp.status_code == 302:
                if "/Account/Login" not in redirect_location:
                    # 登录成功！
                    
                    # 如果当前密码已经是目标密码，无需重置
                    if pwd == TARGET_PASSWORD:
                        return f"✅ {username}: 健康 (密码正确)"
                    
                    # 3. 调用API重置密码
                    # 尝试多种可能的payload格式
                    reset_payloads = [
                        {
                            "currentPassword": pwd,
                            "newPassword": TARGET_PASSWORD
                        },
                        {
                            "currentPassword": pwd,
                            "newPassword": TARGET_PASSWORD,
                            "confirmNewPassword": TARGET_PASSWORD
                        },
                    ]
                    
                    # 获取XSRF-TOKEN（ABP通常从Cookie获取）
                    xsrf = session.cookies.get("XSRF-TOKEN") or session.cookies.get("xsrf-token")
                    
                    api_headers = {
                        "Content-Type": "application/json",
                    }
                    
                    if xsrf:
                        api_headers["X-XSRF-TOKEN"] = xsrf
                    
                    # 尝试主要API端点
                    for reset_payload in reset_payloads:
                        api_resp = session.post(CHANGE_PWD_API, json=reset_payload, headers=api_headers, timeout=10)
                        
                        if api_resp.status_code in [200, 204]:
                            return f"♻️ {username}: 已修复 (从 {pwd[:8]}... 重置成功)"
                        
                        if api_resp.status_code == 404:
                            # 尝试备用端点
                            api_resp = session.post(CHANGE_PWD_API_ALT, json=reset_payload, headers=api_headers, timeout=10)
                            if api_resp.status_code in [200, 204]:
                                return f"♻️ {username}: 已修复 (从 {pwd[:8]}... 重置成功，使用备用端点)"
                    
                    # 所有尝试都失败
                    error_detail = api_resp.text[:100] if api_resp.text else "无响应内容"
                    return f"❌ {username}: 登录成功但重置失败 (API: {api_resp.status_code}, {error_detail})"
                else:
                    # 302但跳回登录页，说明登录失败（密码错误）
                    continue
            elif resp.status_code == 200:
                # 200状态码，可能是登录失败（密码错误），继续尝试下一个密码
                continue
            else:
                # 其他状态码，可能是网络错误
                continue
                    
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            # 调试：输出异常信息（仅对第一个账号输出，避免刷屏）
            if username == account.get("username", ""):
                pass  # 暂时不输出，避免干扰
            continue
            
    return f"💀 {username}: 彻底丢失 (无法匹配任何密码)"

def force_reregister_account(account):
    """
    强制重新注册账号
    注意：如果账号已存在，注册API不会真正重置密码，只是返回"已存在"
    真正的重置需要管理员API或等待锁定时间过去
    """
    import sys
    from pathlib import Path
    
    # 修复导入路径
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    
    try:
        from scripts.create_accounts_api import register_account_api
        
        username = account["username"]
        email = account["email"]
        password = TARGET_PASSWORD
        
        success, msg = register_account_api(username, email, password)
        
        if success:
            # 即使返回"已存在"，我们也认为成功（因为账号存在）
            return f"🔄 {username}: {msg}"
        else:
            return f"❌ {username}: 重新注册失败 ({msg})"
    except Exception as e:
        return f"❌ {account['username']}: 导入失败 ({str(e)})"

def admin_reset_all_passwords(admin_session, accounts):
    """
    使用管理员权限批量重置所有账号密码
    """
    results = []
    for account in accounts:
        username = account["username"]
        success, msg = admin_reset_password(admin_session, username, TARGET_PASSWORD)
        if success:
            results.append(f"✅ {username}: {msg}")
        else:
            results.append(f"❌ {username}: {msg}")
    return results

def main():
    print("🚀 开始 API 极速账号清洗...")
    print(f"   目标密码: {TARGET_PASSWORD}")
    print(f"   策略: 普通用户登录+重置 → 失败则删除+重新注册")
    
    if not POOL_FILE.exists():
        print("❌ 账号池文件不存在")
        return

    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    print(f"   检测账号: {len(accounts)} 个")
    print("-" * 50)
    
    # 第一步：尝试普通用户登录+重置
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(try_login_and_reset, acc) for acc in accounts]
        
        for future in as_completed(futures):
            res = future.result()
            print(res)
            results.append(res)
    
    # 第二步：对于失败的账号，尝试删除+重新注册
    # 注意：results顺序可能和accounts不一致（并发导致），需要通过username匹配
    failed_accounts = []
    for res in results:
        if "彻底丢失" in res or "重置失败" in res or "被锁定" in res:
            # 从结果中提取username（格式：前缀 username: 后缀）
            import re
            username_match = re.search(r'([a-zA-Z0-9_]+):', res)
            if username_match:
                username = username_match.group(1)
                # 在accounts中查找对应的账号
                for account in accounts:
                    if account["username"] == username:
                        failed_accounts.append(account)
                        break
    
    if failed_accounts:
        print("-" * 50)
        print(f"⚠️ 发现 {len(failed_accounts)} 个账号需要删除+重新注册...")
        print("🔐 尝试管理员登录...")
        
        admin_session, login_msg = admin_login()
        if admin_session:
            print(f"✅ 管理员登录成功！")
            print("-" * 50)
            
            # 创建username到result的映射（用于更新results）
            import re
            results_dict = {}
            for r in results:
                username_match = re.search(r'([a-zA-Z0-9_]+):', r)
                if username_match:
                    results_dict[username_match.group(1)] = r
            
            for account in failed_accounts:
                username = account["username"]
                print(f"处理 {username}...")
                
                # 尝试删除用户
                delete_success, delete_msg = admin_delete_user(admin_session, username)
                if delete_success:
                    print(f"  ✅ 删除成功: {delete_msg}")
                    # 等待一下，确保删除完成
                    import time
                    time.sleep(0.5)
                else:
                    print(f"  ⚠️ 删除失败: {delete_msg}，尝试直接重新注册...")
                
                # 无论删除是否成功，都尝试重新注册
                # 如果用户已存在，注册API会返回"已存在"，但不会更新密码
                # 所以如果删除失败，重新注册也可能失败
                recreate_success, recreate_msg = admin_recreate_user(account)
                if recreate_success:
                    print(f"  ✅ 重新注册成功")
                    # 更新results中对应的结果
                    if username in results_dict:
                        results_dict[username] = f"🔄 {username}: 已重新注册"
                else:
                    print(f"  ❌ 重新注册失败: {recreate_msg}")
                    if "已存在" in recreate_msg or "already exists" in recreate_msg.lower():
                        if username in results_dict:
                            results_dict[username] = f"⚠️ {username}: 用户已存在，无法重新注册（需要手动删除）"
                    else:
                        if username in results_dict:
                            results_dict[username] = f"❌ {username}: 重新注册失败 ({recreate_msg})"
            
            # 更新results列表（保持原有顺序）
            updated_results = []
            for r in results:
                username_match = re.search(r'([a-zA-Z0-9_]+):', r)
                if username_match and username_match.group(1) in results_dict:
                    updated_results.append(results_dict[username_match.group(1)])
                else:
                    updated_results.append(r)
            results = updated_results
        else:
            print(f"❌ 管理员登录失败: {login_msg}")
            print("⚠️ 无法执行删除+重新注册，失败的账号需要手动处理")
    
    # 统计结果
    healthy_count = sum(1 for r in results if "健康" in r)
    fixed_count = sum(1 for r in results if "已修复" in r)
    recreated_count = sum(1 for r in results if "重新注册" in r or "已重新注册" in r)
    failed_count = sum(1 for r in results if "彻底丢失" in r or ("失败" in r and "重新注册失败" in r) or ("需要手动删除" in r))
    
    print("-" * 50)
    print("📊 清洗结果统计:")
    print(f"   ✅ 健康: {healthy_count} 个")
    print(f"   ♻️  已修复: {fixed_count} 个")
    print(f"   🔄 重新注册: {recreated_count} 个")
    print(f"   ❌ 失败: {failed_count} 个")
    print("-" * 50)
    
    print("🏁 清洗完成")

if __name__ == "__main__":
    main()

