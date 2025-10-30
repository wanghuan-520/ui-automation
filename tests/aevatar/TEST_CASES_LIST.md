# 🌟 Aevatar 测试用例完整清单

> 生成时间: 2023-10-23  
> 总测试用例: 23个

## 📊 概览

| 优先级 | 数量 | 占比 | 说明 |
|--------|------|------|------|
| 🔴 P0 | 10 | 43.5% | 核心功能测试 |
| 🟡 P1 | 5 | 21.7% | 重要功能测试 |
| 🟢 P2 | 3 | 13.0% | 一般功能测试 |
| ⚪ N/A | 5 | 21.7% | 其他测试 |

---

## 🔴 P0 核心功能测试 (10个)

### 1. test_aevatar_login
- **文件**: `test_daily_regression_login.py`
- **描述**: 测试用例: Aevatar 用户登录
- **标记**: `login`, `smoke`, `p0`, `asyncio`
- **说明**: 核心登录功能测试，验证用户能成功登录系统

### 2. test_aevatar_workflow
- **文件**: `test_daily_regression_workflow.py`
- **描述**: 测试用例: Aevatar Workflow创建和运行
- **标记**: `workflow`, `workflows`, `integration`, `p0`, `asyncio`
- **说明**: 端到端Workflow创建和运行流程测试

### 3. test_apikeys_create
- **文件**: `test_daily_regression_complete.py`
- **描述**: P0 测试: 创建 API Key
- **标记**: `apikeys`, `smoke`, `p0`, `asyncio`
- **地址**: `/dashboard/apikeys`

### 4. test_workflows_create
- **文件**: `test_daily_regression_complete.py`
- **描述**: P0 测试: 创建并运行 Workflow
- **标记**: `workflows`, `smoke`, `p0`, `asyncio`
- **地址**: `/dashboard/workflows`

### 5. test_configuration_cros_add_domain
- **文件**: `test_daily_regression_complete.py`
- **描述**: P0 测试: 添加 CROS Domain
- **标记**: `configuration`, `p0`, `asyncio`
- **地址**: `/dashboard/configuration`

### 6. test_organisation_project_create
- **文件**: `test_daily_regression_organisation.py`
- **描述**: P0 测试: 创建 Organisation Project
- **标记**: `organisation`, `p0`, `asyncio`
- **地址**: `/profile/organisation/project`

### 7. test_organisation_member_add
- **文件**: `test_daily_regression_organisation.py`
- **描述**: P0 测试: 添加 Organisation Member
- **标记**: `organisation`, `p0`, `asyncio`
- **地址**: `/profile/organisation/member`

### 8. test_organisation_role_add
- **文件**: `test_daily_regression_organisation.py`
- **描述**: P0 测试: 添加 Organisation Role
- **标记**: `organisation`, `p0`, `asyncio`
- **地址**: `/profile/organisation/role`

### 9. test_project_member_add
- **文件**: `test_daily_regression_project.py`
- **描述**: P0 测试: 添加 Project Member
- **标记**: `project`, `p0`, `asyncio`
- **地址**: `/profile/projects/member`

### 10. test_project_role_add
- **文件**: `test_daily_regression_project.py`
- **描述**: P0 测试: 添加 Project Role
- **标记**: `project`, `p0`, `asyncio`
- **地址**: `/profile/projects/role`

---

## 🟡 P1 重要功能测试 (5个)

### 11. test_apikeys_edit
- **文件**: `test_daily_regression_dashboard.py`
- **描述**: P1 测试: 修改 API Key
- **标记**: `apikeys`, `p1`, `asyncio`
- **地址**: `/dashboard/apikeys`

### 12. test_profile_name_edit
- **文件**: `test_daily_regression_dashboard.py`
- **描述**: P1 测试: 修改 Profile Name
- **标记**: `profile`, `p1`, `asyncio`
- **地址**: `/profile/profile/general`

### 13. test_organisation_name_edit
- **文件**: `test_daily_regression_organisation.py`
- **描述**: P1 测试: 修改 Organisation Name
- **标记**: `organisation`, `p1`, `asyncio`
- **地址**: `/profile/organisation/settings`

### 14. test_project_name_edit
- **文件**: `test_daily_regression_project.py`
- **描述**: P1 测试: 修改 Project Name
- **标记**: `project`, `p1`, `asyncio`
- **地址**: `/profile/projects/settings`

### 15. test_project_role_edit_permissions
- **文件**: `test_daily_regression_project.py`
- **描述**: P1 测试: 编辑 Project Role 权限
- **标记**: `project`, `p1`, `asyncio`
- **地址**: `/profile/projects/role`

---

## 🟢 P2 一般功能测试 (3个)

### 16. test_apikeys_delete
- **文件**: `test_daily_regression_dashboard.py`
- **描述**: P2 测试: 删除 API Key
- **标记**: `apikeys`, `p2`, `asyncio`
- **地址**: `/dashboard/apikeys`

### 17. test_workflows_delete
- **文件**: `test_daily_regression_dashboard.py`
- **描述**: P2 测试: 删除 Workflow
- **标记**: `workflows`, `p2`, `asyncio`
- **地址**: `/dashboard/workflows`

### 18. test_configuration_cros_delete_domain
- **文件**: `test_daily_regression_dashboard.py`
- **描述**: P2 测试: 删除 CROS Domain
- **标记**: `configuration`, `p2`, `asyncio`
- **地址**: `/dashboard/configuration`

---

## ⚪ 其他测试 (5个)

### 19. test_valid_login_only
- **文件**: `test_login.py`
- **标记**: `positive`, `smoke`, `asyncio`
- **说明**: 快速冒烟测试 - 仅测试正常登录

### 20. test_invalid_credentials_only
- **文件**: `test_login.py`
- **标记**: `negative`, `asyncio`
- **说明**: 快速安全测试 - 仅测试错误凭证

### 21. test_login_scenarios
- **文件**: `test_login.py`
- **说明**: 参数化登录场景测试

### 22. test_basic_workflow_only
- **文件**: `test_workflow.py`
- **标记**: `integration`, `smoke`, `asyncio`
- **说明**: 快速集成测试 - 仅测试基础workflow

### 23. test_workflow_scenarios
- **文件**: `test_workflow.py`
- **说明**: 参数化workflow场景测试

---

## 📁 按文件分布

| 文件 | 用例数 | 占比 | 主要功能 |
|------|--------|------|----------|
| `test_daily_regression_dashboard.py` | 5 | 21.7% | API Keys编辑/删除、Workflow删除、CROS删除、Profile编辑 |
| `test_daily_regression_organisation.py` | 4 | 17.4% | 组织项目/成员/角色创建、组织名称编辑 |
| `test_daily_regression_project.py` | 4 | 17.4% | 项目成员/角色添加、项目名称编辑、角色权限编辑 |
| `test_daily_regression_complete.py` | 3 | 13.0% | API Keys/Workflows/CROS创建 |
| `test_login.py` | 3 | 13.0% | 登录相关测试 |
| `test_workflow.py` | 2 | 8.7% | Workflow相关测试 |
| `test_daily_regression_login.py` | 1 | 4.3% | 主要登录测试 |
| `test_daily_regression_workflow.py` | 1 | 4.3% | 主要Workflow测试 |

---

## 🏷️ 按功能模块分布

| 模块 | 用例数 | 占比 | 说明 |
|------|--------|------|------|
| 🔐 organisation | 4 | 17.4% | 组织管理 |
| 📦 project | 4 | 17.4% | 项目管理 |
| 🔑 apikeys | 3 | 13.0% | API密钥管理 |
| 🔄 workflows | 3 | 13.0% | 工作流管理 |
| ⚙️ configuration | 2 | 8.7% | 配置管理 |
| 👤 login | 1 | 4.3% | 登录功能 |
| 🎯 workflow | 1 | 4.3% | 工作流 |
| 📝 profile | 1 | 4.3% | 用户配置 |

---

## 🚀 快速运行命令

### 按优先级运行

```bash
# 运行所有P0测试（核心功能，推荐每日运行）
pytest tests/aevatar/ -m "p0" -v

# 运行所有P1测试（重要功能）
pytest tests/aevatar/ -m "p1" -v

# 运行所有P2测试（一般功能）
pytest tests/aevatar/ -m "p2" -v

# 运行P0+P1测试（核心+重要）
pytest tests/aevatar/ -m "p0 or p1" -v
```

### 按模块运行

```bash
# API Keys测试
pytest tests/aevatar/ -m "apikeys" -v

# Workflows测试
pytest tests/aevatar/ -m "workflows" -v

# Organisation测试
pytest tests/aevatar/ -m "organisation" -v

# Project测试
pytest tests/aevatar/ -m "project" -v

# Configuration测试
pytest tests/aevatar/ -m "configuration" -v

# Profile测试
pytest tests/aevatar/ -m "profile" -v
```

### 按类型运行

```bash
# 冒烟测试（快速验证）
pytest tests/aevatar/ -m "smoke" -v

# 集成测试
pytest tests/aevatar/ -m "integration" -v

# 正向测试
pytest tests/aevatar/ -m "positive" -v

# 负向测试
pytest tests/aevatar/ -m "negative" -v
```

### 运行单个测试文件

```bash
# 登录测试
pytest tests/aevatar/test_daily_regression_login.py -v

# Workflow测试
pytest tests/aevatar/test_daily_regression_workflow.py -v

# Dashboard测试
pytest tests/aevatar/test_daily_regression_dashboard.py -v

# Organisation测试
pytest tests/aevatar/test_daily_regression_organisation.py -v

# Project测试
pytest tests/aevatar/test_daily_regression_project.py -v

# Complete测试
pytest tests/aevatar/test_daily_regression_complete.py -v
```

### 运行所有测试

```bash
# 串行运行
pytest tests/aevatar/ -v

# 并行运行（2个进程）
pytest tests/aevatar/ -n 2 -v

# 并行运行（4个进程）
pytest tests/aevatar/ -n 4 -v
```

### 生成测试报告

```bash
# HTML报告
pytest tests/aevatar/ -v --html=reports/pytest-report.html --self-contained-html

# Allure报告
pytest tests/aevatar/ -v --alluredir=allure-results
allure serve allure-results

# 使用便捷脚本
python3 run_daily_regression_allure.py --stable
```

---

## 💡 推荐测试策略

### 1. 每日冒烟测试 (5-10分钟)
快速验证核心功能是否正常
```bash
pytest tests/aevatar/ -m "smoke" -v
```

### 2. 核心功能回归 (20-30分钟)
验证所有核心功能
```bash
pytest tests/aevatar/ -m "p0" -v
```

### 3. 完整回归测试 (45-60分钟)
完整的功能验证
```bash
pytest tests/aevatar/ -m "p0 or p1 or p2" -v
```

### 4. 特定模块测试 (按需)
针对性测试特定功能模块
```bash
pytest tests/aevatar/ -m "apikeys or workflows" -v
```

### 5. 并行快速测试
提高测试效率
```bash
pytest tests/aevatar/ -m "p0" -n 2 -v
```

---

## 📊 测试覆盖范围

### 核心功能覆盖
- ✅ 用户登录认证
- ✅ Workflow创建和运行
- ✅ API Keys管理（创建、编辑、删除）
- ✅ 组织管理（项目、成员、角色）
- ✅ 项目管理（成员、角色、权限）
- ✅ CROS配置管理
- ✅ 用户Profile配置

### 测试类型覆盖
- ✅ 冒烟测试 (Smoke)
- ✅ 功能测试 (Functional)
- ✅ 集成测试 (Integration)
- ✅ 正向测试 (Positive)
- ✅ 负向测试 (Negative)

---

## 🎯 测试质量指标

| 指标 | 当前状态 |
|------|----------|
| 总用例数 | 23 |
| P0覆盖率 | 43.5% |
| 自动化率 | 100% |
| 模块覆盖 | 8个主要模块 |
| 代码复用 | 高（base_test, utils, conftest） |
| 可维护性 | 高（模块化设计） |
| 可扩展性 | 高（支持参数化和数据驱动） |

---

## 📝 维护说明

### 添加新测试用例
1. 确定测试优先级（P0/P1/P2）
2. 选择合适的测试文件或创建新文件
3. 添加适当的pytest标记
4. 编写清晰的测试文档字符串
5. 更新本清单

### 修改现有用例
1. 修改测试代码
2. 更新文档字符串
3. 验证测试通过
4. 更新本清单（如需要）

### 删除过时用例
1. 确认用例确实过时
2. 从测试文件中删除
3. 更新本清单

---

## 🔗 相关文档

- [README.md](./README.md) - Aevatar测试框架总览
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始指南
- [DAILY_REGRESSION_GUIDE.md](./DAILY_REGRESSION_GUIDE.md) - 每日回归测试指南
- [base_test.py](./base_test.py) - 测试基类
- [utils.py](./utils.py) - 测试工具函数
- [conftest.py](./conftest.py) - Pytest配置

---

**最后更新**: 2023-10-23  
**维护者**: HyperEcho ⚡

