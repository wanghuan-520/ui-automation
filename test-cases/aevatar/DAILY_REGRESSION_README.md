# Aevatar 日常回归测试使用指南

## 📋 目录

- [概述](#概述)
- [测试用例概览](#测试用例概览)
- [环境准备](#环境准备)
- [快速开始](#快速开始)
- [运行选项](#运行选项)
- [测试文件结构](#测试文件结构)
- [测试用例详情](#测试用例详情)
- [常见问题](#常见问题)

---

## 概述

本测试套件包含 **25 个自动化回归测试用例**（其中23个执行，2个SKIPPED），覆盖 Aevatar 平台的核心功能模块：

- ✅ **登录验证**
- ✅ **Dashboard 功能** (API Keys、Workflows、Configuration)
- ✅ **Profile 配置**
- ✅ **Organisation 管理** (Settings、Projects、Members、Roles)
- ✅ **Project 管理** (Settings、Members、Roles)

### 测试优先级分布

| 优先级 | 数量 | 说明 |
|:---:|:---:|:---|
| 🔴 **P0** | 9 | 核心功能，必须通过 |
| 🟡 **P1** | 8 | 重要功能，高优先级 |
| 🟢 **P2** | 6 | 一般功能，常规验证 |
| ⏭️ **SKIP** | 2 | 已被组合测试替代 |

**实际执行**: 23个测试（9+8+6）  
**总用例数**: 25个（包含2个SKIPPED）

---

## 测试用例概览

### 按模块分类

```
📊 Dashboard 功能 (10个)
├─ 🔐 登录验证 [P0]
├─ 🔑 API Keys 管理
│  ├─ 添加 API Key [P0]
│  ├─ 修改 API Key [P1]
│  └─ 删除 API Key [P2]
├─ 🔄 Workflows 管理
│  ├─ 创建 Workflow [P0]
│  └─ 删除 Workflow [P2]
└─ ⚙️ Configuration
   ├─ 添加 CROS Domain [P0]
   └─ 删除 CROS Domain [P2]

👤 Profile & Organisation (11个)
├─ 修改 Profile Name [P1]
├─ 修改 Organisation Name [P1]
├─ Organisation Projects
│  ├─ 创建 Project [P0]
│  ├─ 编辑 Project [P1]
│  └─ 删除 Project [P2]
├─ Organisation Members
│  ├─ 添加 Member [P0]
│  └─ 删除 Member [P1]
└─ Organisation Roles
   ├─ 添加 Role [P0]
   ├─ 编辑权限 [P1]
   └─ 删除 Role [P2]

📂 Project 管理 (7个，其中2个SKIPPED)
├─ 修改 Project Name [P1]
├─ Project Members
│  ├─ 添加+删除 Member (组合测试) [P0] ✅
│  ├─ 添加 Member [P0] ⏭️ SKIPPED
│  └─ 删除 Member [P1] ⏭️ SKIPPED
└─ Project Roles
   ├─ 添加 Role [P0]
   ├─ 编辑权限 [P1]
   └─ 删除 Role [P2]

**✨ Project模块优化**:
- 智能Project选择：自动扫描并选择最适合的测试Project
- 组合测试策略：Add+Delete在同一session中执行，确保环境一致性
- 详细文档：见 PROJECT_TEST_OPTIMIZATION_SUMMARY.md
```

---

## 环境准备

### 1. Python 环境

```bash
# Python 3.8+ 
python3 --version
```

### 2. 安装依赖

```bash
# 安装测试依赖
pip install -r requirements-pytest.txt

# 主要依赖包括:
# - pytest
# - pytest-asyncio
# - pytest-html
# - playwright
```

### 3. 安装 Playwright 浏览器

```bash
# 安装 Chromium 浏览器
playwright install chromium

# 或使用系统 Chrome
# 测试脚本默认使用 /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

### 4. 配置测试账号

编辑测试文件中的账号信息（在生产环境中建议使用环境变量）：

```python
TEST_EMAIL = "your_test_email@example.com"
TEST_PASSWORD = "your_test_password"
```

---

## 快速开始

### 运行所有测试

```bash
# 运行全部26个测试用例
python3 run_daily_regression_tests.py

# 或直接使用 pytest
pytest tests/aevatar/test_daily_regression_*.py -v
```

### 运行特定优先级测试

```bash
# 只运行 P0 核心功能测试 (10个)
python3 run_daily_regression_tests.py -p p0

# 只运行 P1 重要功能测试 (9个)
python3 run_daily_regression_tests.py -p p1

# 只运行 P2 一般功能测试 (7个)
python3 run_daily_regression_tests.py -p p2
```

### 运行特定模块测试

```bash
# Dashboard 模块
python3 run_daily_regression_tests.py -m login
python3 run_daily_regression_tests.py -m apikeys
python3 run_daily_regression_tests.py -m workflows
python3 run_daily_regression_tests.py -m configuration

# Organisation 模块
python3 run_daily_regression_tests.py -m organisation

# Project 模块
python3 run_daily_regression_tests.py -m project
```

### 组合过滤

```bash
# 运行 Organisation 模块的 P0 测试
pytest tests/aevatar/test_daily_regression_organisation.py -m p0 -v

# 运行 Dashboard 模块的 P0 和 P1 测试
pytest tests/aevatar/test_daily_regression_dashboard.py -m "p0 or p1" -v
```

---

## 运行选项

### 主运行脚本选项

```bash
python3 run_daily_regression_tests.py [OPTIONS]

选项:
  -p, --priority {p0,p1,p2}    按优先级过滤测试
  -m, --module {MODULE}        按模块过滤测试
  -v, --verbose                显示详细输出
  --list                       列出所有测试用例
  -h, --help                   显示帮助信息
```

### Pytest 直接运行选项

```bash
# 显示详细输出
pytest tests/aevatar/test_daily_regression_dashboard.py -v

# 只显示失败的测试
pytest tests/aevatar/test_daily_regression_dashboard.py --tb=short

# 生成HTML报告
pytest tests/aevatar/test_daily_regression_dashboard.py --html=report.html --self-contained-html

# 显示执行最慢的10个测试
pytest tests/aevatar/test_daily_regression_dashboard.py --durations=10

# 在第一个失败后停止
pytest tests/aevatar/test_daily_regression_dashboard.py -x

# 显示本地变量
pytest tests/aevatar/test_daily_regression_dashboard.py -l
```

---

## 测试文件结构

```
tests/aevatar/
├── test_daily_regression_dashboard.py      # Dashboard 模块测试 (10个用例)
├── test_daily_regression_organisation.py   # Organisation 模块测试 (11个用例)
├── test_daily_regression_project.py        # Project 模块测试 (5个用例)
├── conftest.py                             # Pytest 配置和 fixtures
└── utils.py                                # 测试工具类

test-cases/aevatar/
├── daily_regression_test.md                # 测试用例表格
├── daily_regression_test_mindmap.md        # 测试用例脑图
└── DAILY_REGRESSION_README.md              # 本文档

reports/
├── daily_regression_report_*.html          # 测试报告
└── pytest-*.html                           # 模块测试报告

test-screenshots/
└── *.png                                   # 测试截图
```

---

## 测试用例详情

### Dashboard 模块测试

#### test_daily_regression_dashboard.py

| 测试用例 | 优先级 | Pytest 标记 | 描述 |
|:---|:---:|:---|:---|
| `test_login_page_validation` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.login` | 登录页面验证 |
| `test_apikeys_create` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.apikeys` | 创建 API Key |
| `test_apikeys_edit` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.apikeys` | 修改 API Key |
| `test_apikeys_delete` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.apikeys` | 删除 API Key |
| `test_workflows_create` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.workflows` | 创建 Workflow |
| `test_workflows_delete` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.workflows` | 删除 Workflow |
| `test_configuration_cros_add_domain` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.configuration` | 添加 CROS Domain |
| `test_configuration_cros_delete_domain` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.configuration` | 删除 CROS Domain |

### Organisation 模块测试

#### test_daily_regression_organisation.py

| 测试用例 | 优先级 | Pytest 标记 | 描述 |
|:---|:---:|:---|:---|
| `test_profile_modify_name` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.profile` | 修改 Profile Name |
| `test_organisation_modify_name` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.organisation` | 修改 Organisation Name |
| `test_organisation_project_create` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.organisation` | 创建 Organisation Project |
| `test_organisation_project_edit` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.organisation` | 编辑 Organisation Project |
| `test_organisation_project_delete` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.organisation` | 删除 Organisation Project |
| `test_organisation_member_add` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.organisation` | 添加 Organisation Member |
| `test_organisation_member_delete` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.organisation` | 删除 Organisation Member |
| `test_organisation_role_add` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.organisation` | 添加 Organisation Role |
| `test_organisation_role_edit_permissions` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.organisation` | 编辑 Organisation Role 权限 |
| `test_organisation_role_delete` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.organisation` | 删除 Organisation Role |

### Project 模块测试

#### test_daily_regression_project.py

| 测试用例 | 优先级 | Pytest 标记 | 描述 |
|:---|:---:|:---|:---|
| `test_project_settings_modify_name` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.project` | 修改 Project Name |
| `test_project_member_add` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.project` | 添加 Project Member |
| `test_project_member_delete` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.project` | 删除 Project Member |
| `test_project_role_add` | P0 | `@pytest.mark.p0`<br>`@pytest.mark.project` | 添加 Project Role |
| `test_project_role_edit_permissions` | P1 | `@pytest.mark.p1`<br>`@pytest.mark.project` | 编辑 Project Role 权限 |
| `test_project_role_delete` | P2 | `@pytest.mark.p2`<br>`@pytest.mark.project` | 删除 Project Role |

---

## 查看测试报告

### 🎨 Allure 报告（推荐）

Allure提供了更加专业和美观的测试报告界面：

```bash
# 方式1：使用便捷脚本（推荐）
./view_project_allure_report.sh

# 方式2：重新运行测试并查看报告
./view_project_allure_report.sh --rerun

# 方式3：手动生成和查看
pytest tests/aevatar/test_daily_regression_project.py --alluredir=allure-results
allure serve allure-results -p 8888
```

**Allure报告地址**: http://localhost:8888

**Allure报告优势**:
- ✅ 可视化测试结果（通过/失败/跳过）
- ✅ 详细的测试步骤展示
- ✅ 失败原因分析和堆栈跟踪
- ✅ 历史趋势对比
- ✅ 测试执行时间统计
- ✅ 自动附件（截图、日志）

> **注意**: 直接打开 `allure-report/index.html` 会显示 "Loading"（CORS限制）。必须使用 `allure serve` 启动服务器。

### HTML 报告

测试完成后会在 `reports/` 目录生成 HTML 报告：

```bash
# 主报告
open reports/daily_regression_report_YYYYMMDD_HHMMSS.html

# 模块报告
open reports/pytest-dashboard-report.html
open reports/pytest-organisation-report.html
open reports/pytest-project-report.html
```

### 截图

测试过程中的截图保存在 `test-screenshots/` 目录：

```bash
ls test-screenshots/

# 输出示例:
# login_page.png
# apikey_created.png
# workflow_executed.png
# ...
```

---

## 常见问题

### 1. 浏览器路径错误

**问题**: `executable_path` 找不到 Chrome

**解决**:
```python
# 编辑测试文件，修改 Chrome 路径
executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# macOS 默认路径
# Linux: "/usr/bin/google-chrome"
# Windows: "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

### 2. 元素定位失败

**问题**: 测试报告显示 "未找到元素"

**解决**:
- 检查页面是否加载完成
- 增加等待时间 `await page.wait_for_timeout(3000)`
- 更新选择器（UI可能有变化）
- 查看截图确认页面状态

### 3. Toast 消息验证失败

**问题**: toast 消息未找到或不匹配

**解决**:
- 增加等待时间让 toast 出现
- 检查 toast 选择器是否正确
- 使用模糊匹配而不是精确匹配

### 4. 测试数据冲突

**问题**: 创建的数据已存在

**解决**:
- 测试使用随机名称生成 `generate_random_name()`
- 在测试前清理旧数据
- 使用独立的测试账号

### 5. 登录失败

**问题**: 所有测试都失败，原因是登录失败

**解决**:
- 检查测试账号密码是否正确
- 确认测试环境 URL 是否可访问
- 检查网络连接
- 查看登录页面截图确认问题

---

## 最佳实践

### 1. 定期执行

建议每日执行一次完整回归测试：

```bash
# 添加到 cron 或 CI/CD
# 每天早上9点执行
0 9 * * * cd /path/to/project && python3 run_daily_regression_tests.py
```

### 2. 优先级策略

- **提交前**: 运行 P0 测试（10个，约15分钟）
- **每日回归**: 运行 P0 + P1 测试（19个，约30分钟）
- **发版前**: 运行全部测试（26个，约45分钟）

### 3. 测试隔离

每个测试用例应该：
- ✅ 独立运行，不依赖其他测试
- ✅ 使用 fixture 管理浏览器实例
- ✅ 清理测试数据（或使用随机数据）
- ✅ 捕获并记录关键步骤截图

### 4. 持续改进

- 定期更新选择器以适应UI变化
- 优化等待策略，减少不必要的固定等待
- 添加更多断言验证业务逻辑
- 收集测试指标，分析失败原因

---

## 技术栈

- **测试框架**: pytest 
- **异步支持**: pytest-asyncio
- **浏览器自动化**: Playwright (Chromium)
- **报告生成**: pytest-html
- **日志记录**: Python logging

---

## 联系支持

如有问题或建议，请联系测试团队。

**Happy Testing! 🚀**

