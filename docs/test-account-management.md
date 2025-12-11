# 测试账号管理优化方案

## 📋 问题背景

每个测试用例都自动注册新账号会导致数据库出现大量脏数据，影响数据库性能和后续测试。

## 🎯 优化目标

1. **减少脏数据**：最小化自动注册的账号数量
2. **测试隔离**：确保并行执行时测试之间不互相干扰
3. **灵活配置**：支持多种执行模式和配置选项

## 🚀 优化方案

### 策略1：串行执行 → 使用预设账号

**场景**：单线程执行测试（`pytest` 不带 `-n` 参数）

**方案**：直接使用预设账号（`haylee13`），因为串行执行不存在数据冲突。

**优势**：
- ✅ 零脏数据（不注册新账号）
- ✅ 执行速度快（无需注册流程）
- ✅ 简单可靠

### 策略2：并行执行 → 优先使用账号池

**场景**：多线程执行测试（`pytest -n 4`）

**方案**：从预配置的账号池中获取账号，每个worker使用不同的账号。

**优势**：
- ✅ 零脏数据（复用已有账号）
- ✅ 测试隔离（不同worker使用不同账号）
- ✅ 可配置账号数量（根据并行度调整）

**账号池配置**：`tests/aevatar_station/test-data/test_account_pool.json`

```json
{
  "test_account_pool": [
    {
      "username": "autotest_pool_001",
      "email": "autotest_pool_001@test.com",
      "password": "TestPass123!",
      "in_use": false,
      "last_used": null
    },
    // ... 更多账号
  ],
  "pool_config": {
    "pool_size": 10,
    "auto_register_fallback": true,
    "cleanup_after_test": false
  }
}
```

### 策略3：账号池不足 → 可配置自动注册

**场景**：并行度超过账号池大小，或账号池未配置

**方案**：根据环境变量配置决定是否自动注册新账号。

**配置选项**：
- `AUTO_REGISTER=auto`（默认）：并行时启用，串行时禁用
- `AUTO_REGISTER=true`：强制启用自动注册
- `AUTO_REGISTER=false`：禁用自动注册（回退到预设账号）

**优势**：
- ✅ 灵活控制（可根据需要选择）
- ✅ 避免意外脏数据（默认仅在必要时注册）

### 策略4：最后备选 → 预设账号

**场景**：所有策略都失败时

**方案**：回退到使用预设账号（`haylee13`）

**优势**：
- ✅ 保证测试可以执行（即使配置错误）
- ⚠️ 可能产生数据冲突（并行执行时）

## 📊 方案对比

| 执行模式 | 账号来源 | 脏数据 | 测试隔离 | 推荐度 |
|---------|---------|--------|---------|--------|
| 串行执行 | 预设账号 | ✅ 无 | ✅ 是 | ⭐⭐⭐⭐⭐ |
| 并行执行 | 账号池 | ✅ 无 | ✅ 是 | ⭐⭐⭐⭐⭐ |
| 并行执行 | 自动注册 | ❌ 有 | ✅ 是 | ⭐⭐⭐ |
| 并行执行 | 预设账号 | ✅ 无 | ❌ 否 | ⭐ |

## 🔧 使用方法

### 1. 串行执行（推荐用于开发调试）

```bash
# 使用预设账号，零脏数据
pytest tests/aevatar_station/test_profile_personal_settings.py -v
```

### 2. 并行执行（推荐用于CI/CD）

```bash
# 使用账号池，零脏数据
pytest tests/aevatar_station/test_profile_personal_settings.py -n 4 -v
```

### 3. 强制使用账号池（禁用自动注册）

```bash
# 即使账号池不足，也不自动注册
AUTO_REGISTER=false pytest tests/aevatar_station/test_profile_personal_settings.py -n 4 -v
```

### 4. 强制启用自动注册

```bash
# 即使串行执行，也自动注册（不推荐）
AUTO_REGISTER=true pytest tests/aevatar_station/test_profile_personal_settings.py -v
```

### 5. 禁用账号池（直接使用预设账号）

```bash
# 不使用账号池，直接使用预设账号（并行时可能冲突）
USE_ACCOUNT_POOL=false pytest tests/aevatar_station/test_profile_personal_settings.py -n 4 -v
```

## 📝 账号池管理

### 创建账号池

1. 手动注册10个测试账号（用户名：`autotest_pool_001` 到 `autotest_pool_010`）
2. 更新 `tests/aevatar_station/test-data/test_account_pool.json`
3. 确保所有账号都有访问 `/admin/profile` 的权限

### 账号池大小建议

- **并行度 ≤ 4**：账号池 ≥ 4个账号
- **并行度 ≤ 8**：账号池 ≥ 8个账号
- **并行度 ≤ 16**：账号池 ≥ 16个账号

**建议**：账号池大小 = 最大并行度 + 2（预留缓冲）

## ⚠️ 注意事项

1. **账号权限**：账号池中的账号必须有访问 `/admin/profile` 的权限
2. **账号清理**：定期清理测试账号（如果后端支持批量删除API）
3. **数据隔离**：虽然使用不同账号，但测试仍应避免修改共享数据
4. **环境变量**：CI/CD环境建议设置 `AUTO_REGISTER=false` 避免意外注册

## 🔄 未来优化方向

1. **自动清理**：测试结束后自动删除自动注册的账号（需要后端API支持）
2. **账号池自动扩展**：账号池不足时自动注册并加入池中
3. **数据库事务回滚**：使用数据库事务，测试结束后自动回滚（需要后端支持）




















