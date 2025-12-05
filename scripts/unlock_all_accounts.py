"""
快速解锁所有被锁定的账号
用于测试前快速恢复账号池状态
"""
import json
from pathlib import Path

POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

def unlock_all_accounts():
    """解锁所有账号，恢复可用状态"""
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool_data = json.load(f)
    
    accounts = pool_data.get("test_account_pool", [])
    
    unlocked_count = 0
    for account in accounts:
        if account.get("is_locked", False):
            account["is_locked"] = False
            account["in_use"] = False
            if "locked_reason" in account:
                del account["locked_reason"]
            unlocked_count += 1
            print(f"✅ 解锁: {account['username']}")
        elif account.get("in_use", False):
            account["in_use"] = False
            print(f"🔓 释放: {account['username']}")
    
    # 写回文件
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 解锁完成！共解锁 {unlocked_count} 个账号")
    print(f"总账号数: {len(accounts)}")
    print(f"可用账号: {sum(1 for a in accounts if not a.get('is_locked', False) and not a.get('in_use', False))}")

if __name__ == "__main__":
    unlock_all_accounts()

