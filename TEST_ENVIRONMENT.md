# Aevatar 测试环境配置

## 🌐 统一测试环境

所有测试均使用 **Staging 环境**：

```
https://aevatar-station-ui-staging.aevatar.ai
```

## 📋 配置文件位置

### 1. 数据驱动测试框架配置

**文件**: `test-data/aevatar_test_data.yaml`

```yaml
environment:
  base_url: "https://aevatar-station-ui-staging.aevatar.ai"
  login_url: "https://aevatar-station-ui-staging.aevatar.ai"
  dashboard_url: "https://aevatar-station-ui-staging.aevatar.ai/dashboard/workflows"
```

### 2. 旧版测试配置

**文件**: `tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py`

```python
self.BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
self.LOGIN_URL = "https://aevatar-station-ui-staging.aevatar.ai"
```

### 3. 日常回归测试配置

**文件**: 
- `tests/aevatar/test_daily_regression_project.py`
- `tests/aevatar/test_daily_regression_organisation.py`
- `tests/aevatar/test_daily_regression_dashboard.py`

```python
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
```

## 🔄 环境切换

### 方式1：修改YAML配置（推荐）

编辑 `test-data/aevatar_test_data.yaml`:

```yaml
environment:
  base_url: "https://your-new-environment.aevatar.ai"
  login_url: "https://your-new-environment.aevatar.ai"
  dashboard_url: "https://your-new-environment.aevatar.ai/dashboard/workflows"
```

### 方式2：使用环境变量

```bash
# 设置环境变量
export AEVATAR_BASE_URL="https://your-new-environment.aevatar.ai"

# 运行测试
pytest tests/aevatar/
```

### 方式3：命令行参数

```bash
# 通过pytest参数传递
pytest tests/aevatar/ --base-url="https://your-new-environment.aevatar.ai"
```

## 📊 环境列表

| 环境 | URL | 用途 |
|------|-----|------|
| **Staging** ⭐ | https://aevatar-station-ui-staging.aevatar.ai | 当前使用 - 测试环境 |
| Production | https://aevatar-station.aevatar.ai | 生产环境（谨慎使用） |
| Development | https://aevatar-station-ui-dev.aevatar.ai | 开发环境 |

## 🔐 测试账号

**Email**: `aevatarwh1@teml.net`  
**Password**: `Wh520520!`

⚠️ **注意**: 请勿在生产环境使用测试账号！

## ✅ 验证环境配置

运行以下命令验证环境配置：

```bash
# 1. 检查YAML配置
cat test-data/aevatar_test_data.yaml | grep base_url

# 2. 检查日常回归测试配置
grep "TEST_BASE_URL" tests/aevatar/test_daily_regression_*.py

# 3. 运行快速验证测试
pytest tests/aevatar/test_daily_regression_login.py & test_daily_regression_workflow.py::test_aevatar_login -v -s
```

## 📝 更新记录

- **2025-10-23**: 统一所有测试环境为 Staging
  - 更新 YAML 配置文件
  - 更新旧版测试文件
  - 日常回归测试已使用正确URL

## 🚀 快速运行

```bash
# 运行所有测试（使用staging环境）
pytest tests/aevatar/ -v -n auto

# 只运行日常回归测试
pytest tests/aevatar/test_daily_regression_*.py -v -n auto

# 运行数据驱动测试
pytest tests/aevatar/test_login.py tests/aevatar/test_workflow.py -v
```

## 📞 支持

如需更改测试环境，请联系测试团队或查看 [配置文档](tests/aevatar/README.md)。

---

**环境状态**: ✅ 已统一  
**最后更新**: 2025-10-23  
**维护者**: HyperEcho

