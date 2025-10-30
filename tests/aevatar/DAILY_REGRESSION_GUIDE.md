# Aevatar 日常回归测试指南

## 📋 目录

- [概览](#概览)
- [测试覆盖](#测试覆盖)
- [快速开始](#快速开始)
- [测试文件说明](#测试文件说明)
- [运行方式](#运行方式)
- [优先级说明](#优先级说明)
- [测试报告](#测试报告)

---

## 🎯 概览

基于 `daily_regression_test_mindmap.md` 创建的完整日常回归测试套件，覆盖 Aevatar 平台的所有核心功能模块。

**测试环境**: https://aevatar-station-ui-staging.aevatar.ai

**总计测试用例**: 26个
- 🔴 **P0 核心功能**: 10个
- 🟡 **P1 重要功能**: 9个
- 🟢 **P2 一般功能**: 7个

---

## 📊 测试覆盖

### 1. Dashboard 功能模块

#### 🔑 API Keys 管理
- ✅ **P0**: 创建 API Key
- ✅ **P1**: 修改 API Key
- ✅ **P2**: 删除 API Key

#### 🔄 Workflows 管理
- ✅ **P0**: 创建并运行 Workflow
- ✅ **P2**: 删除 Workflow

#### 🌐 Configuration 配置
- ✅ **P0**: 添加 CROS Domain
- ✅ **P2**: 删除 CROS Domain

### 2. Profile 配置模块

#### 👤 个人设置
- ✅ **P1**: 修改 Profile Name

### 3. Organisation 管理模块

#### ⚙️ Organisation Settings
- ✅ **P1**: 修改 Organisation Name

#### 📁 Organisation Projects
- ✅ **P0**: 创建 Project
- ✅ **P1**: 编辑 Project
- ✅ **P2**: 删除 Project

#### 👥 Organisation Members
- ✅ **P0**: 添加 Member
- ✅ **P1**: 删除 Member

#### 🎭 Organisation Roles
- ✅ **P0**: 添加 Role
- ✅ **P1**: 编辑 Role 权限
- ✅ **P2**: 删除 Role

### 4. Project 管理模块

#### ⚙️ Project Settings
- ✅ **P1**: 修改 Project Name

#### 👥 Project Members
- ✅ **P0**: 添加 Member
- ✅ **P1**: 删除 Member

#### 🎭 Project Roles
- ✅ **P0**: 添加 Role
- ✅ **P1**: 编辑 Role 权限
- ✅ **P2**: 删除 Role

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip3 install -r requirements-pytest.txt

# 安装pytest-xdist（用于并行执行）
pip3 install pytest-xdist
```

### 2. 运行所有测试

```bash
# 方式1: 使用主运行脚本
python3 run_daily_regression.py --all

# 方式2: 直接使用pytest
pytest tests/aevatar/test_daily_regression_*.py -v
```

### 3. 运行特定优先级测试

```bash
# 只运行P0核心功能测试
python3 run_daily_regression.py --p0

# 只运行P1重要功能测试
python3 run_daily_regression.py --p1
```

### 4. 运行特定模块测试

```bash
# Dashboard功能测试
python3 run_daily_regression.py --dashboard

# Organisation管理测试
python3 run_daily_regression.py --organisation

# Project管理测试
python3 run_daily_regression.py --project

# Profile配置测试
python3 run_daily_regression.py --profile
```

### 5. 并行执行（推荐）

```bash
# 并行运行所有测试
python3 run_daily_regression.py --all --parallel

# 并行运行P0测试
python3 run_daily_regression.py --p0 --parallel
```

---

## 📂 测试文件说明

### 核心测试文件

| 文件名 | 说明 | 测试用例数 |
|--------|------|-----------|
| `test_daily_regression_complete.py` | 完整回归测试（包含最核心的P0测试） | 3个P0用例 |
| `test_daily_regression_dashboard.py` | Dashboard + Profile 功能测试 | 7个用例 |
| `test_daily_regression_organisation.py` | Organisation 管理测试 | 4个用例 |
| `test_daily_regression_project.py` | Project 管理测试 | 5个用例 |

### 辅助脚本

| 文件名 | 说明 |
|--------|------|
| `run_daily_regression.py` | 主运行脚本，提供多种运行选项 |
| `test_daily_regression_login.py & test_daily_regression_workflow.py` | 原始登录和Workflow测试（稳定版） |

---

## 🏃 运行方式

### 方式1: 使用主脚本（推荐）

```bash
# 查看帮助
python3 run_daily_regression.py --help

# 运行示例
python3 run_daily_regression.py --all              # 运行所有测试
python3 run_daily_regression.py --p0               # 只运行P0核心功能
python3 run_daily_regression.py --dashboard        # 只运行Dashboard测试
python3 run_daily_regression.py --organisation --parallel  # 并行运行Organisation测试
```

### 方式2: 直接使用pytest

```bash
# 运行所有日常回归测试
pytest tests/aevatar/test_daily_regression_*.py -v --html=reports/report.html

# 按优先级运行
pytest tests/aevatar/ -v -m "p0"           # P0核心功能
pytest tests/aevatar/ -v -m "p1"           # P1重要功能
pytest tests/aevatar/ -v -m "p2"           # P2一般功能

# 按模块运行
pytest tests/aevatar/ -v -m "dashboard"    # Dashboard功能
pytest tests/aevatar/ -v -m "organisation" # Organisation管理
pytest tests/aevatar/ -v -m "project"      # Project管理
pytest tests/aevatar/ -v -m "profile"      # Profile配置
pytest tests/aevatar/ -v -m "apikeys"      # API Keys管理
pytest tests/aevatar/ -v -m "workflows"    # Workflows管理
```

### 方式3: 运行单个测试文件

```bash
# 运行Dashboard测试
python3 tests/aevatar/test_daily_regression_dashboard.py

# 运行Organisation测试
python3 tests/aevatar/test_daily_regression_organisation.py

# 运行Project测试
python3 tests/aevatar/test_daily_regression_project.py
```

---

## 📌 优先级说明

### 🔴 P0 - 核心功能（必须每日回归）
- 登录验证
- API Keys 创建
- Workflow 创建和运行
- CROS Domain 添加
- Organisation: Project/Member/Role 创建
- Project: Member/Role 添加

**特点**: 影响核心业务流程，必须确保稳定

### 🟡 P1 - 重要功能（建议每日回归）
- API Keys 修改
- Profile Name 修改
- Organisation: Name/Project/Member/Role 编辑
- Project: Name/Member/Role 编辑

**特点**: 影响用户体验，需要定期验证

### 🟢 P2 - 一般功能（可按需回归）
- API Keys/Workflow/CROS 删除
- Organisation: Project/Member/Role 删除
- Project: Member/Role 删除

**特点**: 辅助功能，影响范围较小

---

## 📊 测试报告

### HTML报告

测试完成后会自动生成HTML报告：

```
reports/daily-regression-report.html
```

报告包含：
- ✅ 测试通过/失败统计
- 📸 失败测试的截图
- ⏱️ 测试执行时间
- 📝 详细错误日志

### 查看报告

```bash
# 在浏览器中打开报告
open reports/daily-regression-report.html

# 或使用http服务器
python3 -m http.server 8000
# 然后访问: http://localhost:8000/reports/daily-regression-report.html
```

### 截图位置

测试过程中的截图保存在：

```
test-screenshots/daily-regression/     # 综合测试截图
test-screenshots/dashboard/            # Dashboard测试截图
test-screenshots/organisation/         # Organisation测试截图
test-screenshots/project/              # Project测试截图
```

---

## 🔧 高级用法

### 1. 并行执行（提升速度）

```bash
# 使用所有可用CPU核心
pytest tests/aevatar/test_daily_regression_*.py -n auto -v

# 指定并行进程数
pytest tests/aevatar/test_daily_regression_*.py -n 4 -v
```

### 2. 失败重试

```bash
# 失败后重试3次
pytest tests/aevatar/ -v --reruns 3 --reruns-delay 5
```

### 3. 只运行失败的用例

```bash
# 第一次运行
pytest tests/aevatar/ -v --lf

# 重新运行失败的用例
pytest tests/aevatar/ -v --lf
```

### 4. 调试模式

```bash
# 第一个失败后停止
pytest tests/aevatar/ -v -x

# 详细输出
pytest tests/aevatar/ -v -s --capture=no
```

---

## 💡 最佳实践

### 1. 每日回归建议

**推荐顺序**:
1. 运行 P0 核心功能测试（必须）
2. 运行 P1 重要功能测试（建议）
3. 根据需要运行 P2 一般功能测试

```bash
# 每日核心回归
python3 run_daily_regression.py --p0 --parallel

# 完整回归（周末或版本发布前）
python3 run_daily_regression.py --all --parallel
```

### 2. 模块测试建议

当某个模块有更新时，针对性地运行该模块测试：

```bash
# Dashboard模块更新
python3 run_daily_regression.py --dashboard

# Organisation模块更新
python3 run_daily_regression.py --organisation
```

### 3. CI/CD集成

```yaml
# .github/workflows/daily-regression.yml 示例
- name: Run Daily Regression Tests
  run: |
    python3 run_daily_regression.py --p0 --parallel
    
- name: Upload Test Report
  uses: actions/upload-artifact@v2
  with:
    name: test-report
    path: reports/
```

---

## 🐛 故障排查

### 1. 浏览器未安装

```bash
# 安装Playwright浏览器
playwright install chromium
```

### 2. 依赖缺失

```bash
# 重新安装所有依赖
pip3 install -r requirements-pytest.txt
```

### 3. 测试超时

```bash
# 增加超时时间
pytest tests/aevatar/ -v --timeout=300
```

### 4. 元素定位失败

- 检查测试环境是否可访问
- 查看截图确认页面状态
- 检查选择器是否正确

---

## 📞 技术支持

如有问题，请查看：
1. 测试报告中的详细错误信息
2. 截图文件夹中的页面截图
3. 日志文件中的完整日志

---

**文档更新日期**: 2025-10-23
**测试环境**: https://aevatar-station-ui-staging.aevatar.ai
**维护者**: Aevatar QA Team

