import json
from pathlib import Path
from datetime import datetime

POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

def generate_new_pool(count=20, prefix="qatest_v3__", password="TestPass123!"):
    new_accounts = []
    for i in range(1, count + 1):
        username = f"{prefix}{i:03d}"
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
    
    pool_data = {
        "test_account_pool": new_accounts,
        "pool_config": {
            "pool_size": count,
            "auto_register_fallback": True,
            "cleanup_after_test": False,
            "account_prefix": prefix,
            "account_lock_wait_time": 300,
            "max_retry_on_lock": 3
        }
    }
    
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已生成 {count} 个新账号配置到 {POOL_FILE}")
    print(f"   前缀: {prefix}")

if __name__ == "__main__":
    generate_new_pool()
