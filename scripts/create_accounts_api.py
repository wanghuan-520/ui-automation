#!/usr/bin/env python3
"""
使用API接口快速批量创建测试账号池
极快速度：预计30秒内完成20个账号创建

使用方法：
    python scripts/create_accounts_api.py
"""
import json
import requests
import urllib3
from pathlib import Path
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
BASE_URL = "https://localhost:44320"
REGISTER_URL = f"{BASE_URL}/Account/Register"
POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"


def register_account_api(username, email, password):
    """
    使用API注册单个账号
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # 创建session
        session = requests.Session()
        session.verify = False  # 忽略SSL证书验证
        
        # 第一步：获取注册页面（获取AntiForgeryToken）
        try:
            response = session.get(REGISTER_URL, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return False, f"无法访问注册页面: {str(e)}"
        
        # 从页面中提取AntiForgeryToken（ABP框架需要）
        import re
        token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', response.text)
        antiforgery_token = token_match.group(1) if token_match else None
        
        # 第二步：提交注册表单
        register_data = {
            "Input.UserName": username,
            "Input.EmailAddress": email,
            "Input.Password": password,
        }
        
        if antiforgery_token:
            register_data["__RequestVerificationToken"] = antiforgery_token
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": REGISTER_URL,
        }
        
        response = session.post(REGISTER_URL, data=register_data, headers=headers, timeout=10, allow_redirects=False)
        
        # 判断注册是否成功
        # 成功：通常会302重定向
        # 失败：返回200并显示错误消息
        
        if response.status_code == 302:
            # 重定向说明注册成功
            redirect_url = response.headers.get("Location", "")
            if "/Account/Register" not in redirect_url:
                return True, "注册成功"
        
        # 检查响应内容中是否有错误消息
        if response.status_code == 200:
            # 可能是注册失败，检查常见错误消息
            error_keywords = [
                "already registered",
                "already exists",
                "User name",
                "Email",
                "is already taken",
                "已注册",
                "已存在",
            ]
            
            response_lower = response.text.lower()
            for keyword in error_keywords:
                if keyword.lower() in response_lower:
                    # 如果是账号已存在，也算成功
                    if "already" in keyword.lower() or "exist" in keyword.lower() or "已" in keyword:
                        return True, "账号已存在（跳过）"
                    
                    # 其他错误
                    error_match = re.search(r'<div[^>]*class="[^"]*text-danger[^"]*"[^>]*>([^<]+)</div>', response.text)
                    if error_match:
                        error_msg = error_match.group(1).strip()
                        return False, f"注册失败: {error_msg}"
                    
                    return False, f"注册失败（检测到关键词: {keyword}）"
        
        # 如果状态码是其他值
        return False, f"注册状态不明确（HTTP {response.status_code}）"
        
    except requests.exceptions.Timeout:
        return False, "请求超时"
    except Exception as e:
        return False, f"异常: {str(e)}"


def register_single_account(account, idx, total):
    """注册单个账号（带进度）"""
    username = account["username"]
    email = account["email"]
    password = account["password"]
    
    start_time = time.time()
    success, message = register_account_api(username, email, password)
    elapsed = time.time() - start_time
    
    status_icon = "✅" if success else "❌"
    print(f"[{idx:2d}/{total}] {status_icon} {username:20} | {message:30} ({elapsed:.1f}s)")
    
    return {
        "username": username,
        "success": success,
        "message": message,
        "time": elapsed
    }


def main():
    print("\n" + "=" * 80)
    print("🚀 使用API接口批量创建测试账号池")
    print("=" * 80)
    print("目标：30秒内完成20个账号创建")
    print("=" * 80 + "\n")
    
    # 读取账号池配置
    if not POOL_FILE.exists():
        print(f"❌ 错误：账号池文件不存在: {POOL_FILE}")
        return 1
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    if not accounts:
        print("❌ 错误：账号池为空")
        return 1
    
    pool_size = len(accounts)
    
    print(f"📊 账号池信息:")
    print(f"   文件路径: {POOL_FILE}")
    print(f"   账号总数: {pool_size}个")
    print(f"   注册URL: {REGISTER_URL}")
    print(f"   并行数: 5个线程")
    print()
    print("=" * 80)
    print()
    
    # 记录开始时间
    start_time = time.time()
    
    # 并行注册（使用5个线程）
    print("⚡ 开始并行注册（使用5个线程）...")
    print()
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交所有注册任务
        future_to_account = {
            executor.submit(register_single_account, account, idx, pool_size): account 
            for idx, account in enumerate(accounts, 1)
        }
        
        # 收集结果
        for future in as_completed(future_to_account):
            results.append(future.result())
    
    # 计算统计
    total_time = time.time() - start_time
    success_count = sum(1 for r in results if r["success"])
    failed_count = len(results) - success_count
    avg_time = sum(r["time"] for r in results) / len(results) if results else 0
    
    # 输出结果
    print()
    print("=" * 80)
    print("📊 创建结果统计")
    print("=" * 80)
    print(f"  总账号数: {pool_size}")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {failed_count}")
    print(f"  ⏱️  总耗时: {total_time:.1f}秒")
    print(f"  ⚡ 平均速度: {avg_time:.1f}秒/账号")
    print(f"  🎯 目标达成: {'✅ 是' if total_time <= 30 else '❌ 否（超过30秒）'}")
    print("=" * 80)
    
    if failed_count > 0:
        print()
        print("❌ 失败的账号:")
        for r in results:
            if not r["success"]:
                print(f"   • {r['username']:20} | {r['message']}")
        print()
        print("⚠️ 建议：手动在后台管理系统创建失败的账号")
        return 1
    
    print()
    print("✅ 所有账号创建完成！")
    print()
    print("💡 下一步:")
    print("   1. 验证账号池: python3 scripts/verify_account_pool.py")
    print("   2. 运行测试: pytest --workers=4 tests/...")
    print()
    
    return 0


if __name__ == "__main__":
    exit(main())
