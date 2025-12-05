"""
验证账号池中所有账号的登录状态
使用后端API快速检查哪些账号可以登录，哪些已失效
"""
import json
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
BASE_URL = "https://localhost:44320"
LOGIN_URL = f"{BASE_URL}/Account/Login"
POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

def verify_account(account):
    """
    验证单个账号是否可以登录
    
    Args:
        account: 账号信息字典 {username, email, password}
    
    Returns:
        dict: {username, email, can_login: bool, error_message: str}
    """
    username = account["username"]
    password = account["password"]
    email = account.get("email", "")
    
    try:
        # 创建session
        session = requests.Session()
        session.verify = False  # 忽略SSL证书验证
        
        # 第一步：获取登录页面（获取AntiForgeryToken）
        try:
            response = session.get(LOGIN_URL, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return {
                "username": username,
                "email": email,
                "can_login": False,
                "error_message": f"无法访问登录页面: {str(e)}"
            }
        
        # 从页面中提取AntiForgeryToken（ABP框架需要）
        import re
        token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', response.text)
        antiforgery_token = token_match.group(1) if token_match else None
        
        # 第二步：提交登录表单
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
        
        # 判断登录是否成功
        # 成功：通常会302重定向到首页
        # 失败：返回200并显示错误消息
        
        if response.status_code == 302:
            # 重定向说明登录成功
            redirect_url = response.headers.get("Location", "")
            if "/Account/Login" not in redirect_url:
                return {
                    "username": username,
                    "email": email,
                    "can_login": True,
                    "error_message": ""
                }
        
        # 检查响应内容中是否有错误消息
        if response.status_code == 200:
            # 可能是登录失败，检查常见错误消息
            error_keywords = [
                "Invalid login attempt",
                "invalid",
                "incorrect",
                "locked out",
                "locked",
                "锁定",
                "错误",
                "失败",
                "验证失败"
            ]
            
            response_lower = response.text.lower()
            for keyword in error_keywords:
                if keyword.lower() in response_lower:
                    # 尝试提取具体错误消息
                    error_match = re.search(r'<div[^>]*class="[^"]*text-danger[^"]*"[^>]*>([^<]+)</div>', response.text)
                    if error_match:
                        error_msg = error_match.group(1).strip()
                    else:
                        error_msg = f"登录失败（检测到关键词: {keyword}）"
                    
                    return {
                        "username": username,
                        "email": email,
                        "can_login": False,
                        "error_message": error_msg
                    }
        
        # 如果没有明确的失败消息，尝试检查是否有session cookie
        cookies = session.cookies.get_dict()
        if any("session" in k.lower() or "auth" in k.lower() or ".AspNetCore" in k for k in cookies.keys()):
            return {
                "username": username,
                "email": email,
                "can_login": True,
                "error_message": ""
            }
        
        # 无法确定状态
        return {
            "username": username,
            "email": email,
            "can_login": False,
            "error_message": f"登录状态不明确（HTTP {response.status_code}）"
        }
        
    except requests.exceptions.Timeout:
        return {
            "username": username,
            "email": email,
            "can_login": False,
            "error_message": "请求超时"
        }
    except Exception as e:
        return {
            "username": username,
            "email": email,
            "can_login": False,
            "error_message": f"异常: {str(e)}"
        }

def main():
    """主函数：批量验证账号池"""
    print("=" * 80)
    print("🔍 开始验证账号池中的所有账号...")
    print("=" * 80)
    print()
    
    # 读取账号池
    if not POOL_FILE.exists():
        print(f"❌ 错误：账号池文件不存在: {POOL_FILE}")
        return
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    if not accounts:
        print("❌ 错误：账号池为空")
        return
    
    print(f"📊 账号池信息:")
    print(f"   文件路径: {POOL_FILE}")
    print(f"   账号总数: {len(accounts)}个")
    print(f"   验证URL: {LOGIN_URL}")
    print()
    print("=" * 80)
    print()
    
    # 并行验证所有账号（使用5个线程）
    print("⚡ 开始并行验证（使用5个线程）...")
    print()
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交所有验证任务
        future_to_account = {executor.submit(verify_account, account): account for account in accounts}
        
        # 收集结果
        completed = 0
        for future in as_completed(future_to_account):
            completed += 1
            result = future.result()
            results.append(result)
            
            # 实时显示验证结果
            status_icon = "✅" if result["can_login"] else "❌"
            status_text = "成功" if result["can_login"] else "失败"
            error_info = f" ({result['error_message']})" if result["error_message"] else ""
            
            print(f"[{completed:2d}/{len(accounts)}] {status_icon} {result['username']:20} | {status_text:4}{error_info}")
    
    # 统计结果
    print()
    print("=" * 80)
    print("📈 验证结果统计")
    print("=" * 80)
    
    can_login_list = [r for r in results if r["can_login"]]
    cannot_login_list = [r for r in results if not r["can_login"]]
    
    print(f"✅ 可以登录: {len(can_login_list)}个")
    print(f"❌ 无法登录: {len(cannot_login_list)}个")
    print(f"📊 成功率: {len(can_login_list) * 100 // len(results)}%")
    print()
    
    if can_login_list:
        print("✅ 可以登录的账号:")
        for r in can_login_list:
            print(f"   • {r['username']:20} ({r['email']})")
        print()
    
    if cannot_login_list:
        print("❌ 无法登录的账号:")
        for r in cannot_login_list:
            print(f"   • {r['username']:20} ({r['email']})")
            if r['error_message']:
                print(f"     原因: {r['error_message']}")
        print()
    
    # 保存详细结果到JSON文件
    result_file = POOL_FILE.parent / f"account_verification_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "verification_time": datetime.now().isoformat(),
            "total_accounts": len(accounts),
            "can_login_count": len(can_login_list),
            "cannot_login_count": len(cannot_login_list),
            "success_rate": f"{len(can_login_list) * 100 // len(results)}%",
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 详细结果已保存到: {result_file}")
    print()
    print("=" * 80)
    print("🏁 验证完成")
    print("=" * 80)

if __name__ == "__main__":
    main()

