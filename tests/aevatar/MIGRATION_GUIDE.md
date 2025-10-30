# Aevatar 测试框架迁移指南

## 概述

本指南帮助你从旧的单文件测试脚本迁移到新的数据驱动测试框架。

## 主要变化

### 1. 文件结构变化

**旧版本（单文件）:**
```
tests/aevatar/
└── test_daily_regression_login.py & test_daily_regression_workflow.py  (449行)
```

**新版本（模块化）:**
```
tests/aevatar/
├── README.md               # 使用文档
├── MIGRATION_GUIDE.md      # 迁移指南（本文档）
├── conftest.py             # pytest配置和fixtures (200行)
├── utils.py                # 工具类 (190行)
├── test_login.py           # 登录测试 (200行)
└── test_workflow.py        # Workflow测试 (330行)

test-data/
└── aevatar_test_data.yaml  # 测试数据配置
```

### 2. 测试数据分离

**旧版本 - 硬编码:**
```python
class AevatarPytestTest:
    def __init__(self):
        self.LOGIN_URL = "http://env-273db67a-ui.station-testing.aevatar.ai/"
        self.EMAIL = "aevatarwh1@teml.net"
        self.PASSWORD = "Wh520520!"
```

**新版本 - YAML配置:**
```yaml
environment:
  login_url: "http://env-273db67a-ui.station-testing.aevatar.ai/"

login_scenarios:
  - id: "valid_login"
    email: "aevatarwh1@teml.net"
    password: "Wh520520!"
    expected_result: "success"
```

### 3. 测试函数变化

**旧版本:**
```python
@pytest.mark.asyncio
@pytest.mark.login
async def test_aevatar_login():
    """测试用例: Aevatar 有头模式登录"""
    test_instance = AevatarPytestTest()
    await test_instance.setup_browser()
    # ... 100多行代码
```

**新版本:**
```python
@pytest.mark.asyncio
@pytest.mark.login
async def test_login_scenarios(
    browser_context,
    environment_config,
    screenshot_helper,
    login_helper,
    login_scenario  # 自动参数化
):
    """参数化登录测试 - 自动运行所有场景"""
    # ... 简洁的代码
```

### 4. 浏览器管理变化

**旧版本 - 手动管理:**
```python
await test_instance.setup_browser()
try:
    # 测试代码
finally:
    await test_instance.teardown_browser()
```

**新版本 - Fixture自动管理:**
```python
async def test_something(browser_context):
    # 浏览器自动初始化和清理
    page = browser_context
    await page.goto("...")
```

## 迁移步骤

### Step 1: 安装新依赖

```bash
# 更新依赖（新增了pyyaml）
pip install -r requirements-pytest.txt
```

### Step 2: 备份旧文件（可选）

```bash
# 如果需要保留旧版本
cp tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py.bak
```

### Step 3: 验证新框架

```bash
# 运行新的测试框架
python run_aevatar_tests.py --test-file test_login.py -m smoke

# 或使用pytest直接运行
pytest tests/aevatar/test_login.py::test_valid_login_only -v
```

### Step 4: 对比测试结果

运行新旧两个版本的测试，确保结果一致。

### Step 5: 删除旧文件（可选）

确认新框架工作正常后，可以删除旧文件：
```bash
rm tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py
```

## 功能对比

| 功能 | 旧版本 | 新版本 |
|------|--------|--------|
| **文件行数** | 449行单文件 | 多个<400行的文件 |
| **测试场景** | 2个（登录+workflow） | 9个（7个登录+2个workflow） |
| **数据管理** | 硬编码 | YAML配置文件 |
| **参数化测试** | ❌ | ✅ |
| **异常场景** | ❌ | ✅ 7种异常场景 |
| **代码复用** | ❌ | ✅ Fixtures + 工具类 |
| **可扩展性** | 低 | 高 |
| **维护性** | 中 | 高 |

## 新增功能

### 1. 参数化测试

一个测试函数自动运行多个场景：
```python
# 自动运行7个登录场景
pytest tests/aevatar/test_login.py::TestAevatarLogin::test_login_scenarios -v
```

### 2. 标记过滤

按标记快速运行特定类型的测试：
```bash
pytest tests/aevatar/ -m smoke      # 冒烟测试
pytest tests/aevatar/ -m positive   # 正向测试
pytest tests/aevatar/ -m negative   # 负向测试
```

### 3. 快速测试函数

新增快速测试函数用于CI/CD：
```python
test_valid_login_only()           # 快速验证登录
test_invalid_credentials_only()   # 快速验证安全
test_basic_workflow_only()        # 快速验证workflow
```

### 4. 工具类

提供可复用的工具：
```python
# 数据加载
TestDataLoader.get_login_scenarios()
TestDataLoader.get_workflow_scenarios()

# 选择器查找
SelectorHelper.find_element_with_selectors(page, selectors)
SelectorHelper.check_error_message(page, keywords)
```

## 添加新测试场景

### 旧版本（需要修改代码）:
```python
# 需要复制粘贴整个测试函数，修改数据
@pytest.mark.asyncio
async def test_another_login():
    test_instance = AevatarPytestTest()
    # ... 重复100多行代码
```

### 新版本（只需添加数据）:
```yaml
# 在 aevatar_test_data.yaml 中添加
login_scenarios:
  - id: "new_scenario"
    description: "新的测试场景"
    email: "new@test.com"
    password: "password"
    expected_result: "error"
    tags: ["negative"]
```

**无需修改任何代码！** 测试框架会自动发现并运行新场景。

## 常见问题

### Q: 旧的测试用例还能运行吗？

A: 可以。旧文件 `test_daily_regression_login.py & test_daily_regression_workflow.py` 如果还在，仍然可以运行：
```bash
pytest tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py -v
```

但建议尽快迁移到新框架。

### Q: 新框架会影响现有的CI/CD流程吗？

A: 不会。新框架完全兼容pytest，所有现有的pytest命令和参数都可以使用。

### Q: 如何运行单个场景？

A: 使用pytest的选择器：
```bash
# 运行特定ID的场景
pytest tests/aevatar/test_login.py::TestAevatarLogin::test_login_scenarios[valid_login] -v

# 或使用快速测试函数
pytest tests/aevatar/test_login.py::test_valid_login_only -v
```

### Q: 如何修改超时时间等配置？

A: 在 `test-data/aevatar_test_data.yaml` 中修改：
```yaml
environment:
  timeout: 15000  # 修改为15秒
  slow_mo: 1000   # 修改操作间隔为1秒
```

### Q: 截图还保存在同一个位置吗？

A: 是的，仍然保存在 `test-screenshots/` 目录。

## 最佳实践

1. **优先使用新框架** - 新功能更强大，代码更清晰
2. **数据驱动** - 新场景优先在YAML中添加，不修改代码
3. **使用标记** - 合理使用标记组织测试，便于CI/CD分层执行
4. **快速测试** - 使用快速测试函数进行本地开发验证
5. **完整测试** - 使用参数化测试在CI/CD中执行完整回归

## 性能对比

| 指标 | 旧版本 | 新版本 |
|------|--------|--------|
| **测试场景** | 2个 | 9个 |
| **执行时间（串行）** | ~2分钟 | ~8分钟 |
| **执行时间（并行）** | 不支持 | ~3分钟 |
| **代码维护** | 修改1处需改多处 | 修改1处即可 |
| **添加场景** | 需写代码 | 只需加数据 |

## 回滚方案

如果新框架出现问题，可以快速回滚：

1. **临时回滚** - 运行旧文件：
```bash
pytest tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py -v
```

2. **永久回滚** - 恢复备份：
```bash
rm tests/aevatar/test_login.py tests/aevatar/test_workflow.py
rm tests/aevatar/conftest.py tests/aevatar/utils.py
git checkout tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py
```

## 技术支持

如遇到问题：
1. 查看 `tests/aevatar/README.md`
2. 查看测试日志和截图
3. 联系团队支持

## 总结

新的数据驱动测试框架带来：
- ✅ 更好的代码组织
- ✅ 更强的可扩展性
- ✅ 更多的测试场景覆盖
- ✅ 更低的维护成本
- ✅ 更高的开发效率

**建议尽快完成迁移！**

