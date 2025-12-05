# 测试账号池设置指南

## 📋 账号池大小建议

### 4个Worker并行执行

**推荐配置：6-8个账号**

- **最小需求**：4个账号（每个worker一个）
- **推荐配置**：6个账号（4个worker + 2个缓冲）
- **安全配置**：8-10个账号（应对突发情况）

**计算公式**：
```
账号池大小 = 最大并行度 + 2（缓冲）
```

### 不同并行度的建议

| 并行度 | 最小账号数 | 推荐账号数 | 安全账号数 |
|--------|-----------|-----------|-----------|
| 2 | 2 | 4 | 6 |
| 4 | 4 | 6 | 8-10 |
| 8 | 8 | 10 | 12-16 |
| 16 | 16 | 18 | 20-24 |

## 🚀 快速开始

### 方法1：使用批量注册脚本（推荐）

```bash
# 1. 运行批量注册脚本
python scripts/create_test_account_pool.py

# 2. 脚本会自动：
#    - 读取 test_account_pool.json 配置
#    - 批量注册所有账号
#    - 验证账号访问权限
#    - 输出统计结果
```

### 方法2：手动注册

1. **打开注册页面**：`https://localhost:44320/Account/Register`

2. **批量注册账号**（参考 `test_account_pool.json`）：
   - 用户名：`autotest_pool_001` 到 `autotest_pool_010`
   - 邮箱：`autotest_pool_001@test.com` 到 `autotest_pool_010@test.com`
   - 密码：`TestPass123!`（统一密码）

3. **授予权限**：确保所有账号都有访问 `/admin/profile` 的权限

## 📝 账号池配置文件

**位置**：`tests/aevatar_station/test-data/test_account_pool.json`

**格式**：
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
    "cleanup_after_test": false,
    "account_prefix": "autotest_pool_"
  }
}
```

## ⚙️ 配置说明

### pool_config 字段

- **pool_size**: 账号池大小（自动从账号列表计算）
- **auto_register_fallback**: 账号池不足时是否自动注册（默认：true）
- **cleanup_after_test**: 测试后是否清理账号（暂未实现）
- **account_prefix**: 账号前缀（用于识别账号池账号）

## 🔧 权限配置

### 重要：授予admin权限

账号池中的账号需要访问 `/admin/profile` 页面，需要：

1. **后端配置**：在ABP Framework中授予账号 `admin` 角色或权限
2. **数据库配置**：直接在数据库中配置权限
3. **手动测试**：登录账号，访问 `/admin/profile`，确认可以访问

### 权限验证

运行脚本后，会自动验证每个账号的访问权限：

```bash
python scripts/create_test_account_pool.py
```

如果显示 `⚠️ 账号 xxx 无权限访问admin/profile`，需要手动授予权限。

## 📊 使用效果

### 优化前（每个case注册账号）
- 100个测试用例 = 100个新账号
- 数据库脏数据：严重

### 优化后（使用账号池）
- 100个测试用例 = 0个新账号（使用账号池）
- 数据库脏数据：无

## 🛠️ 维护建议

1. **定期检查**：定期验证账号池账号是否可用
2. **账号清理**：如果账号被删除，需要重新注册
3. **权限维护**：确保所有账号都有必要的权限
4. **扩展账号池**：如果并行度增加，需要增加账号数量

## ❓ 常见问题

### Q1: 账号池不足怎么办？

**A**: 有两种方案：
1. 增加账号池大小（推荐）
2. 启用自动注册（会产生脏数据）

```bash
# 方案1：增加账号池（推荐）
# 编辑 test_account_pool.json，添加更多账号

# 方案2：启用自动注册（不推荐）
AUTO_REGISTER=true pytest tests/... -n 4 -v
```

### Q2: 账号注册失败怎么办？

**A**: 检查：
1. 账号是否已存在（脚本会自动跳过）
2. 网络连接是否正常
3. 注册页面是否可访问
4. 密码是否符合要求

### Q3: 账号无权限访问admin/profile？

**A**: 需要手动授予权限：
1. 登录ABP Framework管理后台
2. 找到对应账号
3. 授予 `admin` 角色或相应权限

### Q4: 如何验证账号池是否正常工作？

**A**: 运行测试并观察日志：

```bash
pytest tests/aevatar_station/test_profile_personal_settings.py::TestProfile::test_p1_email_field_format_validation -n 4 -v
```

查看日志中是否显示：
```
✅ 从账号池获取账号: autotest_pool_001 (索引: 0)
```

## 📚 相关文档

- [测试账号管理优化方案](./test-account-management.md)
- [并行测试执行指南](../test-cases/aevatar_station/parallel_testing.md)

