import json
from pathlib import Path
from datetime import datetime

POOL_FILE = Path(__file__).parent.parent / "tests" / "aevatar_station" / "test-data" / "test_account_pool.json"

def reset_account_pool():
    if not POOL_FILE.exists():
        print(f"❌ 错误：账号池文件不存在: {POOL_FILE}")
        return
    
    with open(POOL_FILE, "r+", encoding="utf-8") as f:
        pool_data = json.load(f)
        
        reset_count = 0
        for account in pool_data.get("test_account_pool", []):
            # 无论是否 locked，都重置为可用，让测试去验证密码
            account["is_locked"] = False
            account["locked_reason"] = None
            account["in_use"] = False
            account["last_used"] = datetime.now().isoformat()
            reset_count += 1
        
        f.seek(0)
        f.truncate()
        json.dump(pool_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已强制重置 {reset_count} 个账号的状态为可用。")
    print("⚠️以此状态运行测试时，如果密码确实被修改，账号会被自动重新锁定。")

if __name__ == "__main__":
    reset_account_pool()

