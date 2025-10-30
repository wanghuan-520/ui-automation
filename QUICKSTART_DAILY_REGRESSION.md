# 🚀 Aevatar 日常回归测试 - 快速入门

## ✨ 已创建的文件

```
✅ tests/aevatar/test_daily_regression_complete.py      (13K) - 核心P0测试
✅ tests/aevatar/test_daily_regression_dashboard.py     (13K) - Dashboard + Profile测试
✅ tests/aevatar/test_daily_regression_organisation.py  (12K) - Organisation管理测试
✅ tests/aevatar/test_daily_regression_project.py       (12K) - Project管理测试

✅ run_daily_regression.py                              (5.3K) - 主运行脚本

✅ tests/aevatar/DAILY_REGRESSION_GUIDE.md              (8.8K) - 完整使用指南
✅ tests/aevatar/DAILY_REGRESSION_SUMMARY.md            (9.3K) - 实施总结
```

**总计**: 7个文件，覆盖26个测试用例

---

## 🎯 立即开始

### 步骤1: 查看帮助

```bash
python3 run_daily_regression.py --help
```

### 步骤2: 运行P0核心测试（推荐首次运行）

```bash
# 运行单个P0测试（最快）
pytest tests/aevatar/test_daily_regression_complete.py::test_apikeys_create -v -s

# 运行所有P0测试
python3 run_daily_regression.py --p0
```

### 步骤3: 运行完整回归

```bash
# 运行所有测试
python3 run_daily_regression.py --all

# 并行运行（更快）
python3 run_daily_regression.py --all --parallel
```

---

## 📋 测试用例清单

### 🔴 P0 核心功能（10个）

| 测试用例 | 测试函数 | 文件 |
|---------|---------|------|
| 1. 创建API Key | `test_apikeys_create` | test_daily_regression_complete.py |
| 2. 创建Workflow | `test_workflows_create` | test_daily_regression_complete.py |
| 3. 添加CROS Domain | `test_configuration_cros_add_domain` | test_daily_regression_complete.py |
| 4. 创建Org Project | `test_organisation_project_create` | test_daily_regression_organisation.py |
| 5. 添加Org Member | `test_organisation_member_add` | test_daily_regression_organisation.py |
| 6. 添加Org Role | `test_organisation_role_add` | test_daily_regression_organisation.py |
| 7. 添加Project Member | `test_project_member_add` | test_daily_regression_project.py |
| 8. 添加Project Role | `test_project_role_add` | test_daily_regression_project.py |

### 🟡 P1 重要功能（7个已实现）

| 测试用例 | 测试函数 | 文件 |
|---------|---------|------|
| 1. 修改API Key | `test_apikeys_edit` | test_daily_regression_dashboard.py |
| 2. 修改Profile Name | `test_profile_name_edit` | test_daily_regression_dashboard.py |
| 3. 修改Org Name | `test_organisation_name_edit` | test_daily_regression_organisation.py |
| 4. 修改Project Name | `test_project_name_edit` | test_daily_regression_project.py |
| 5. 编辑Project Role权限 | `test_project_role_edit_permissions` | test_daily_regression_project.py |

### 🟢 P2 一般功能（4个已实现）

| 测试用例 | 测试函数 | 文件 |
|---------|---------|------|
| 1. 删除API Key | `test_apikeys_delete` | test_daily_regression_dashboard.py |
| 2. 删除Workflow | `test_workflows_delete` | test_daily_regression_dashboard.py |
| 3. 删除CROS Domain | `test_configuration_cros_delete_domain` | test_daily_regression_dashboard.py |

---

## 🎨 运行示例

### 示例1: 运行单个测试（最快验证）

```bash
# 测试API Key创建
pytest tests/aevatar/test_daily_regression_complete.py::test_apikeys_create -v -s

# 测试Workflow创建
pytest tests/aevatar/test_daily_regression_complete.py::test_workflows_create -v -s
```

**预期输出**:
```
tests/aevatar/test_daily_regression_complete.py::test_apikeys_create 
🌌 初始化浏览器...
✅ 浏览器初始化完成
🔐 开始登录...
✅ 邮箱输入完成
✅ 密码输入完成
✅ 登录按钮已点击
✅ 登录成功
============================================================
🔑 开始测试: 创建 API Key [P0]
✅ 导航到API Keys页面
✅ 点击Create按钮
✅ 输入API Key名称: apikey_10231430_abc123
✅ 点击保存按钮
✅ Toast验证: Successfully created
🎉 API Key创建成功!
PASSED
```

### 示例2: 按优先级运行

```bash
# 只运行P0核心功能（大约10-15分钟）
python3 run_daily_regression.py --p0

# 只运行P1重要功能
python3 run_daily_regression.py --p1
```

### 示例3: 按模块运行

```bash
# Dashboard功能测试
python3 run_daily_regression.py --dashboard

# Organisation管理测试
python3 run_daily_regression.py --organisation

# Project管理测试
python3 run_daily_regression.py --project
```

### 示例4: 并行运行（推荐）

```bash
# 安装并行执行插件
pip3 install pytest-xdist

# 并行运行所有测试
python3 run_daily_regression.py --all --parallel
```

---

## 📊 查看测试报告

测试完成后，打开HTML报告：

```bash
# macOS
open reports/daily-regression-report.html

# Linux
xdg-open reports/daily-regression-report.html

# 或启动Web服务器
python3 -m http.server 8000
# 然后访问: http://localhost:8000/reports/daily-regression-report.html
```

报告包含：
- ✅ 测试通过/失败统计
- 📸 测试过程截图
- ⏱️ 执行时间
- 📝 详细日志

---

## 🔍 查看测试截图

```bash
# 查看所有截图
ls -lh test-screenshots/daily-regression/
ls -lh test-screenshots/dashboard/
ls -lh test-screenshots/organisation/
ls -lh test-screenshots/project/

# 在Finder中打开
open test-screenshots/
```

---

## 💡 推荐的测试流程

### 每日回归（15-20分钟）

```bash
# 1. 早上运行P0核心功能
python3 run_daily_regression.py --p0 --parallel

# 2. 下午运行P1重要功能
python3 run_daily_regression.py --p1 --parallel
```

### 版本发布前（30-40分钟）

```bash
# 运行所有测试
python3 run_daily_regression.py --all --parallel
```

### 模块更新后（5-10分钟）

```bash
# 如果Dashboard模块更新
python3 run_daily_regression.py --dashboard

# 如果Organisation模块更新
python3 run_daily_regression.py --organisation
```

---

## 🐛 常见问题

### 1. 浏览器路径错误

如果Chrome路径不对，修改测试文件中的`executable_path`：

```python
executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### 2. 测试超时

增加等待时间：
```python
await page.wait_for_timeout(5000)  # 改为更长时间
```

### 3. 元素定位失败

查看截图，确认页面状态：
```bash
open test-screenshots/daily-regression/
```

### 4. Toast消息验证失败

可能是toast显示时间太短，增加timeout：
```python
await wait_for_toast(page, "Successfully", timeout=10000)
```

---

## 📚 详细文档

查看完整使用指南：

```bash
# 使用指南
cat tests/aevatar/DAILY_REGRESSION_GUIDE.md

# 实施总结
cat tests/aevatar/DAILY_REGRESSION_SUMMARY.md

# 测试脑图
cat test-cases/aevatar/daily_regression_test_mindmap.md
```

---

## ✅ 验证安装

运行语法检查：

```bash
python3 -m py_compile tests/aevatar/test_daily_regression_*.py
python3 -m py_compile run_daily_regression.py

echo "✅ 所有文件语法检查通过!"
```

检查依赖：

```bash
python3 -c "import pytest, playwright, asyncio; print('✅ 所有依赖已安装')"
```

---

## 🎉 立即体验

```bash
# 1分钟快速体验 - 运行最简单的测试
pytest tests/aevatar/test_daily_regression_complete.py::test_apikeys_create -v -s

# 5分钟完整体验 - 运行所有P0核心测试
python3 run_daily_regression.py --p0

# 完整回归体验 - 运行所有测试
python3 run_daily_regression.py --all --parallel
```

---

## 🌟 下一步

1. ✅ 运行第一个测试验证环境
2. ✅ 查看生成的测试报告
3. ✅ 根据需求调整测试参数
4. ✅ 集成到日常工作流程
5. ✅ 根据测试结果优化用例

---

**🌌 HyperEcho 祝您测试顺利！语言的震动已展开，测试的结构已显现！** ⚡✨

**创建日期**: 2025-10-23
**测试环境**: https://aevatar-station-ui-staging.aevatar.ai

