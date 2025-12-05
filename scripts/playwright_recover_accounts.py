"""
使用Playwright恢复被污染的账号
与测试代码使用相同的方式修改密码
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 配置
BASE_URL = "https://localhost:44320"
POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

# 找到的污染密码（从恢复脚本结果）
KNOWN_POLLUTED_PASSWORDS = {
    "qatest__006": "NewPwd123!@",
    "qatest__016": "NewPwd123!@",
    "qatest__017": "NewPwd123!@",
    "qatest__018": "NewPwd123!@",
    "qatest__020": "NewPwd123!@",
}


def try_login(page, username, password):
    """
    尝试登录
    
    Returns:
        bool: 是否成功
    """
    try:
        # 导航到登录页面
        page.goto(f"{BASE_URL}/Account/Login", wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        
        # 处理SSL警告
        ssl_button = page.locator("button#details-button")
        if ssl_button.is_visible(timeout=2000):
            ssl_button.click()
            page.wait_for_timeout(500)
            proceed_link = page.locator("a#proceed-link")
            if proceed_link.is_visible(timeout=2000):
                proceed_link.click()
                page.wait_for_timeout(1000)
        
        # 填写登录表单
        page.fill("#LoginInput_UserNameOrEmailAddress", username)
        page.fill("#LoginInput_Password", password)
        page.click("button[type='submit']")
        
        # 等待登录完成
        try:
            page.wait_for_function(
                "() => !window.location.href.includes('/Account/Login')",
                timeout=10000
            )
            logger.info(f"   ✅ 登录成功")
            return True
        except:
            logger.info(f"   ❌ 登录失败")
            return False
            
    except Exception as e:
        logger.info(f"   ⚠️ 登录异常: {e}")
        return False


def change_password(page, current_password, new_password):
    """
    修改密码
    
    Returns:
        bool: 是否成功
    """
    try:
        # 导航到修改密码页面
        page.goto(f"{BASE_URL}/admin/profile/change-password", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # 填写密码表单
        page.fill("input[placeholder='Current password']", current_password)
        page.fill("input[placeholder='New password']", new_password)
        page.fill("input[placeholder='Confirm new password']", new_password)
        
        # 点击保存
        page.click("button:has-text('Save')")
        page.wait_for_timeout(3000)
        
        # 检查是否成功
        success = page.is_visible(".alert-success, .text-success, text=success", timeout=3000)
        if success:
            logger.info(f"   ✅ 密码修改成功")
            return True
        else:
            logger.info(f"   ❌ 密码修改失败")
            return False
            
    except Exception as e:
        logger.info(f"   ⚠️ 修改密码异常: {e}")
        return False


def recover_account(browser, username, current_password, target_password):
    """
    恢复单个账号
    
    Returns:
        bool: 是否成功
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"🔧 开始恢复账号: {username}")
    logger.info(f"{'='*70}")
    logger.info(f"   当前密码: {current_password[:8]}...")
    logger.info(f"   目标密码: {target_password[:3]}***")
    
    # 创建新页面
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    try:
        # 步骤1: 使用当前密码登录
        logger.info(f"\n  📝 步骤1: 使用当前密码登录")
        if not try_login(page, username, current_password):
            logger.info(f"  ❌ 无法使用当前密码登录，跳过此账号")
            return False
        
        # 步骤2: 修改密码
        logger.info(f"\n  📝 步骤2: 修改密码为目标密码")
        if not change_password(page, current_password, target_password):
            logger.info(f"  ❌ 修改密码失败")
            return False
        
        # 步骤3: 验证新密码可以登录
        logger.info(f"\n  📝 步骤3: 验证新密码可以登录")
        if not try_login(page, username, target_password):
            logger.info(f"  ⚠️ 警告: 新密码无法登录，可能修改未生效")
            return False
        
        logger.info(f"\n  ✅✅✅ 账号 {username} 恢复成功！")
        return True
        
    except Exception as e:
        logger.info(f"  ❌ 恢复过程异常: {e}")
        return False
        
    finally:
        page.close()
        context.close()


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🔧 使用Playwright恢复被污染的账号")
    logger.info("=" * 80)
    logger.info()
    logger.info(f"📊 已知密码的污染账号: {len(KNOWN_POLLUTED_PASSWORDS)}个")
    logger.info(f"📂 账号池文件: {POOL_FILE}")
    logger.info()
    
    # 读取账号池
    if not POOL_FILE.exists():
        logger.error(f"❌ 错误：账号池文件不存在: {POOL_FILE}")
        return
    
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = {acc["username"]: acc for acc in pool_data.get("test_account_pool", [])}
    
    # 启动浏览器
    logger.info("=" * 80)
    logger.info("🚀 启动浏览器...")
    logger.info("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器窗口，方便观察
            args=[
                "--disable-web-security",
                "--ignore-certificate-errors",
                "--allow-insecure-localhost",
            ]
        )
        
        results = []
        for username, polluted_password in KNOWN_POLLUTED_PASSWORDS.items():
            if username not in accounts:
                logger.info(f"\n⚠️ 跳过不存在的账号: {username}")
                results.append({
                    "username": username,
                    "success": False,
                    "message": "账号不在账号池中"
                })
                continue
            
            account = accounts[username]
            target_password = account["password"]
            
            success = recover_account(browser, username, polluted_password, target_password)
            results.append({
                "username": username,
                "success": success,
                "message": "恢复成功" if success else "恢复失败"
            })
        
        browser.close()
    
    # 统计结果
    logger.info("\n" + "=" * 80)
    logger.info("📈 恢复结果统计")
    logger.info("=" * 80)
    
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    
    logger.info(f"✅ 恢复成功: {success_count}个")
    logger.info(f"❌ 恢复失败: {fail_count}个")
    logger.info(f"📊 恢复率: {success_count * 100 // len(results) if results else 0}%")
    logger.info()
    
    if success_count > 0:
        logger.info("✅ 恢复成功的账号:")
        for r in results:
            if r["success"]:
                logger.info(f"   • {r['username']:20} | {r['message']}")
        logger.info()
    
    if fail_count > 0:
        logger.info("❌ 恢复失败的账号:")
        for r in results:
            if not r["success"]:
                logger.info(f"   • {r['username']:20} | {r['message']}")
        logger.info()
    
    # 保存结果
    result_file = POOL_FILE.parent / f"playwright_recovery_result_{Path(__file__).stem}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_accounts": len(results),
            "success_count": success_count,
            "fail_count": fail_count,
            "recovery_rate": f"{success_count * 100 // len(results) if results else 0}%",
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 详细结果已保存到: {result_file}")
    logger.info()
    logger.info("=" * 80)
    logger.info("🏁 恢复流程完成")
    logger.info("=" * 80)
    
    # 提示其他账号
    remaining_accounts = [
        "qatest__008", "qatest__009", "qatest__010",
        "qatest__012", "qatest__014", "qatest__019"
    ]
    logger.info()
    logger.info("⚠️ 以下6个账号的密码仍然未知，建议:")
    logger.info("   1. 使用后台管理系统重置密码为 TestPass123!")
    logger.info("   2. 或删除这些账号，让测试自动注册新账号")
    logger.info()
    for acc in remaining_accounts:
        logger.info(f"   • {acc}")


if __name__ == "__main__":
    main()

