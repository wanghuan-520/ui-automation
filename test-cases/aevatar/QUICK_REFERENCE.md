# Aevatar 回归测试快速参考

## 🚀 快速命令

### 运行所有测试（26个用例）
```bash
python3 run_daily_regression_tests.py
```

### 按优先级运行

```bash
# P0 核心功能 (10个用例)
python3 run_daily_regression_tests.py -p p0

# P1 重要功能 (9个用例)
python3 run_daily_regression_tests.py -p p1

# P2 一般功能 (7个用例)
python3 run_daily_regression_tests.py -p p2
```

### 按模块运行

```bash
# Dashboard 模块
python3 run_daily_regression_tests.py -m login
python3 run_daily_regression_tests.py -m apikeys
python3 run_daily_regression_tests.py -m workflows
python3 run_daily_regression_tests.py -m configuration

# Profile & Organisation 模块
python3 run_daily_regression_tests.py -m profile
python3 run_daily_regression_tests.py -m organisation

# Project 模块
python3 run_daily_regression_tests.py -m project
```

### 直接使用 pytest

```bash
# 运行单个测试文件
pytest tests/aevatar/test_daily_regression_dashboard.py -v

# 运行特定测试用例
pytest tests/aevatar/test_daily_regression_dashboard.py::test_login_page_validation -v

# 按标记过滤
pytest tests/aevatar/test_daily_regression_*.py -m p0 -v
pytest tests/aevatar/test_daily_regression_*.py -m "p0 or p1" -v

# 生成报告
pytest tests/aevatar/test_daily_regression_*.py --html=report.html --self-contained-html
```

---

## 📊 测试用例统计

| 优先级 | 数量 | 模块分布 |
|:---:|:---:|:---|
| 🔴 P0 | 9 | 登录(1) + API Keys(1) + Workflows(1) + CROS(1) + Org Projects(1) + Org Members(1) + Org Roles(1) + Project Members组合(1) + Project Roles(1) |
| 🟡 P1 | 8 | API Keys(1) + Profile(1) + Org Name(1) + Org Projects(1) + Org Members(1) + Org Roles(1) + Project Name(1) + Project Roles(1) |
| 🟢 P2 | 6 | API Keys(1) + Workflows(1) + CROS(1) + Org Projects(1) + Org Roles(1) + Project Roles(1) |
| ⏭️ SKIP | 2 | Project Members Add/Delete（已被组合测试替代） |

**实际执行**: 23个（9个P0 + 8个P1 + 6个P2）  
**总用例数**: 25个（包含2个SKIPPED）

---

## 🗂️ 测试文件

```
tests/aevatar/
├── test_daily_regression_dashboard.py      # 10个用例
├── test_daily_regression_organisation.py   # 11个用例
└── test_daily_regression_project.py        #  7个用例（5个执行，2个SKIPPED）
```

---

## 📝 测试用例列表

### Dashboard 模块 (10个)

| 序号 | 测试用例 | 优先级 | 函数名 |
|:---:|:---|:---:|:---|
| 1 | 登录页面验证 | P0 | `test_login_page_validation` |
| 2 | 添加 API Key | P0 | `test_apikeys_create` |
| 3 | 修改 API Key | P1 | `test_apikeys_edit` |
| 4 | 删除 API Key | P2 | `test_apikeys_delete` |
| 5 | 创建 Workflow | P0 | `test_workflows_create` |
| 6 | 删除 Workflow | P2 | `test_workflows_delete` |
| 7 | 添加 CROS Domain | P0 | `test_configuration_cros_add_domain` |
| 8 | 删除 CROS Domain | P2 | `test_configuration_cros_delete_domain` |

### Organisation 模块 (11个)

| 序号 | 测试用例 | 优先级 | 函数名 |
|:---:|:---|:---:|:---|
| 9 | 修改 Profile Name | P1 | `test_profile_modify_name` |
| 10 | 修改 Organisation Name | P1 | `test_organisation_modify_name` |
| 11 | 创建 Organisation Project | P0 | `test_organisation_project_create` |
| 12 | 编辑 Organisation Project | P1 | `test_organisation_project_edit` |
| 13 | 删除 Organisation Project | P2 | `test_organisation_project_delete` |
| 14 | 添加 Organisation Member | P0 | `test_organisation_member_add` |
| 15 | 删除 Organisation Member | P1 | `test_organisation_member_delete` |
| 16 | 添加 Organisation Role | P0 | `test_organisation_role_add` |
| 17 | 编辑 Organisation Role 权限 | P1 | `test_organisation_role_edit_permissions` |
| 18 | 删除 Organisation Role | P2 | `test_organisation_role_delete` |

### Project 模块 (7个，其中2个SKIPPED)

| 序号 | 测试用例 | 优先级 | 函数名 | 状态 |
|:---:|:---|:---:|:---|:---:|
| 19 | 添加+删除 Project Member (组合) | P0 | `test_project_member_add_and_delete` | ✅ PASS |
| 20 | 添加 Project Member | P0 | `test_project_member_add` | ⏭️ SKIP |
| 21 | 删除 Project Member | P1 | `test_project_member_delete` | ⏭️ SKIP |
| 22 | 添加 Project Role | P0 | `test_project_role_add` | ✅ PASS |
| 23 | 修改 Project Name | P1 | `test_project_name_edit` | ✅ PASS |
| 24 | 编辑 Project Role 权限 | P1 | `test_project_role_edit_permissions` | ✅ PASS |
| 25 | 删除 Project Role | P2 | `test_project_role_delete` | ✅ PASS |

> **注意**: 测试用例20和21已被组合测试(用例19)替代，标记为SKIPPED以避免环境冲突。

---

## 🔍 查看测试列表

```bash
# 列出所有测试用例
python3 run_daily_regression_tests.py --list

# 或使用 pytest
pytest tests/aevatar/test_daily_regression_*.py --collect-only
```

---

## 📊 查看报告

### HTML报告
```bash
# 主报告（在 reports/ 目录）
open reports/daily_regression_report_*.html

# 模块报告
open reports/pytest-dashboard-report.html
open reports/pytest-organisation-report.html
open reports/pytest-project-report.html

# 截图（在 test-screenshots/ 目录）
ls test-screenshots/
```

### 🎨 Allure报告（推荐）

```bash
# 方式1：使用便捷脚本（推荐）
./view_project_allure_report.sh

# 方式2：重新运行测试并查看报告
./view_project_allure_report.sh --rerun

# 方式3：手动启动
pytest tests/aevatar/test_daily_regression_project.py --alluredir=allure-results
allure serve allure-results -p 8888
```

**Allure报告地址**: http://localhost:8888

**Allure报告优势**:
- ✅ 可视化测试结果
- ✅ 详细的执行步骤
- ✅ 失败原因分析
- ✅ 历史趋势对比
- ✅ 附件（截图/日志）

---

## ⚙️ 配置

### 测试环境
- URL: `https://aevatar-station-ui-staging.aevatar.ai`
- 浏览器: Chrome (有头模式)
- 超时: 10秒
- 操作间隔: 1秒

### 修改配置

编辑测试文件中的常量：

```python
TEST_BASE_URL = "https://aevatar-station-ui-staging.aevatar.ai"
TEST_EMAIL = "your_email@example.com"
TEST_PASSWORD = "your_password"
```

---

## 🐛 调试技巧

### 1. 运行单个测试
```bash
pytest tests/aevatar/test_daily_regression_dashboard.py::test_login_page_validation -v -s
```

### 2. 显示完整错误信息
```bash
pytest tests/aevatar/test_daily_regression_dashboard.py --tb=long -v
```

### 3. 保留浏览器窗口（调试时）
修改代码：
```python
headless=False,  # 保持有头模式
slow_mo=2000,    # 增加操作间隔到2秒
```

### 4. 查看截图
每个测试步骤都会截图，保存在 `test-screenshots/` 目录

### 5. 跳过慢速测试
```bash
pytest tests/aevatar/test_daily_regression_*.py -m "not workflows" -v
```

---

## 📦 依赖安装

```bash
pip install pytest pytest-asyncio pytest-html playwright
playwright install chromium
```

---

## 💡 提示

1. **首次运行**: 确保浏览器已安装且路径正确
2. **网络**: 确保能访问测试环境
3. **账号**: 使用专门的测试账号，避免影响真实数据
4. **并发**: 当前测试不支持并发，按顺序执行
5. **数据清理**: 测试使用随机名称，避免数据冲突

---

## 📞 获取帮助

```bash
# 查看运行脚本帮助
python3 run_daily_regression_tests.py --help

# 查看 pytest 帮助
pytest --help
```

---

**测试环境**: Staging  
**最后更新**: 2025-10-29  
**总用例数**: 25（23个执行，2个SKIPPED）

