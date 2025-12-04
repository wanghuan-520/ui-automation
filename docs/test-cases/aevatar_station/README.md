# Aevatar Station 测试用例汇总

## 📚 测试用例文档索引

本目录包含Aevatar Station系统的所有测试用例文档。

---

## 📋 已完成的测试计划

### 1. Dashboard 页面测试计划

**文档**: `dashboard_test_plan.md`  
**测试页面**: Dashboard (Admin首页)  
**URL**: `https://localhost:3000/admin`  
**测试用例数量**: 14个  

**覆盖功能**:
- ✅ 页面加载验证
- ✅ 欢迎信息显示
- ✅ 用户信息卡片（头像、姓名、邮箱、手机）
- ✅ 邮箱/手机验证状态
- ✅ Multi-tenancy状态
- ✅ Current Tenant显示
- ✅ Session状态
- ✅ Localization配置
- ✅ Timing配置
- ✅ Features配置
- ✅ Host标识
- ✅ 页面刷新一致性

**优先级分布**:
- P0: 3个
- P1: 8个
- P2: 3个

---

### 2. Settings (Emailing) 页面测试计划

**文档**: `settings_test_plan.md`  
**测试页面**: Settings - Emailing Tab  
**URL**: `https://localhost:3000/admin/settings`  
**测试用例数量**: 15个  

**覆盖功能**:
- ✅ 页面加载验证
- ✅ Tab切换功能
- ✅ 表单字段显示
- ✅ SMTP配置保存（Gmail）
- ✅ SMTP配置保存（Office 365）
- ✅ 配置数据持久化
- ✅ From Address格式校验
- ✅ Port端口号范围校验
- ✅ Enable SSL开关功能
- ✅ Use Default Credentials开关
- ✅ 密码字段安全性
- ✅ Host字段不同格式
- ✅ Domain字段（可选）
- ✅ 配置修改覆盖
- ✅ 清空配置功能

**测试数据**:
- Gmail SMTP配置
- Office 365 SMTP配置
- QQ邮箱SMTP配置
- 无效邮箱格式
- 端口边界值测试

**优先级分布**:
- P0: 3个
- P1: 10个
- P2: 2个

---

### 3. Feature Management 页面测试计划

**文档**: `feature_management_test_plan.md`  
**测试页面**: Feature Management Tab  
**URL**: `https://localhost:3000/admin/settings/feature-management`  
**测试用例数量**: 16个（14个基础 + 2个扩展）  

**覆盖功能**:
- ✅ 页面加载验证
- ✅ 功能管理描述文本
- ✅ "Manage Host Features"按钮
- ✅ Features对话框打开
- ✅ 空功能列表提示
- ✅ 对话框取消按钮
- ✅ 对话框关闭按钮（X）
- ✅ ESC键关闭对话框
- ✅ 对话框Save按钮
- ✅ 从Settings Tab访问Feature Management
- ✅ 页面刷新保持状态
- ✅ 对话框外部点击关闭
- ✅ 对话框层级（Z-index）
- ✅ 多次打开关闭对话框
- ✅ 功能开关切换（扩展）
- ✅ 功能配额设置（扩展）

**优先级分布**:
- P0: 3个
- P1: 6个
- P2: 7个

---

## 🎯 测试覆盖总览

```yaml
总测试用例数: 45个

页面覆盖:
  ✅ Dashboard (Admin首页) - 14个用例
  ✅ Settings (Emailing) - 15个用例
  ✅ Feature Management - 16个用例

优先级分布:
  P0 (Critical): 9个
  P1 (High): 24个
  P2 (Medium): 12个

测试类型:
  ✅ 功能测试 (Functional)
  ✅ 边界值测试 (Boundary)
  ✅ 数据验证测试 (Validation)
  ✅ 数据一致性测试 (Data Persistence)
  ✅ UI/UX测试
  ✅ 性能测试
  ✅ 安全性测试

自动化覆盖:
  ✅ Page Objects: 3个
  ✅ 自动化测试脚本: 36个pytest测试
  ✅ 测试数据文件: 1个
```

---

## 📂 文件结构

```
docs/test-cases/aevatar_station/
├── README.md                           # 本文件：测试用例汇总索引
├── dashboard_test_plan.md              # Dashboard测试计划（14个用例）
├── settings_test_plan.md               # Settings测试计划（15个用例）
├── feature_management_test_plan.md     # Feature Management测试计划（16个用例）
└── aevatar-station-complete-test-plan.md  # 完整测试计划（历史版本）

tests/aevatar_station/
├── pages/
│   ├── dashboard_page.py               # Dashboard Page Object
│   ├── settings_emailing_page.py       # Settings Page Object
│   └── feature_management_page.py      # Feature Management Page Object
├── test-data/
│   └── email_config_data.json          # SMTP配置测试数据
├── test_dashboard.py                   # Dashboard自动化测试（12个测试）
├── test_settings_emailing.py           # Settings自动化测试（12个测试）
└── test_feature_management.py          # Feature Management自动化测试（12个测试）
```

---

## 🚀 快速开始

### 查看测试用例文档

```bash
# Dashboard测试用例
cat docs/test-cases/aevatar_station/dashboard_test_plan.md

# Settings测试用例
cat docs/test-cases/aevatar_station/settings_test_plan.md

# Feature Management测试用例
cat docs/test-cases/aevatar_station/feature_management_test_plan.md
```

### 运行自动化测试

```bash
# 运行所有新模块测试
pytest tests/aevatar_station/test_dashboard.py \
       tests/aevatar_station/test_settings_emailing.py \
       tests/aevatar_station/test_feature_management.py \
       -v --alluredir=allure-results

# 只运行P0优先级测试
pytest tests/aevatar_station/ -m P0 -v

# 只运行Dashboard测试
pytest tests/aevatar_station/test_dashboard.py -v

# 只运行Settings测试
pytest tests/aevatar_station/test_settings_emailing.py -v

# 只运行Feature Management测试
pytest tests/aevatar_station/test_feature_management.py -v
```

### 生成Allure报告

```bash
# 生成报告
allure generate allure-results -o allure-report --clean

# 打开报告
allure open allure-report
```

---

## 📊 测试用例详细列表

### Dashboard 测试用例

| 用例编号 | 用例标题 | 优先级 | 类型 |
|---------|---------|-------|------|
| TC-DASHBOARD-001 | 验证Dashboard页面加载 | P0 | Functional |
| TC-DASHBOARD-002 | 验证欢迎信息显示 | P1 | UI |
| TC-DASHBOARD-003 | 验证用户信息卡片显示 | P0 | Functional |
| TC-DASHBOARD-004 | 验证邮箱验证状态显示 | P1 | Functional |
| TC-DASHBOARD-005 | 验证手机验证状态显示 | P1 | Functional |
| TC-DASHBOARD-006 | 验证Multi-tenancy状态显示 | P1 | Functional |
| TC-DASHBOARD-007 | 验证Current Tenant显示 | P1 | Functional |
| TC-DASHBOARD-008 | 验证Session状态显示 | P2 | Functional |
| TC-DASHBOARD-009 | 验证Localization配置显示 | P2 | Functional |
| TC-DASHBOARD-010 | 验证Timing配置显示 | P2 | Functional |
| TC-DASHBOARD-011 | 验证Features配置显示 | P1 | Functional |
| TC-DASHBOARD-012 | 验证Host标识显示 | P1 | Functional |
| TC-DASHBOARD-013 | 验证页面刷新数据一致性 | P0 | Data |
| TC-DASHBOARD-014 | 验证用户头像显示 | P1 | UI |

### Settings (Emailing) 测试用例

| 用例编号 | 用例标题 | 优先级 | 类型 |
|---------|---------|-------|------|
| TC-SETTINGS-001 | 验证Settings页面加载 | P0 | Functional |
| TC-SETTINGS-002 | 验证Tab切换功能 | P1 | Functional |
| TC-SETTINGS-003 | 验证所有表单字段显示 | P1 | UI |
| TC-SETTINGS-004 | 验证SMTP配置保存（Gmail） | P0 | Functional |
| TC-SETTINGS-005 | 验证配置数据持久化 | P0 | Data |
| TC-SETTINGS-006 | 验证From Address格式校验 | P1 | Validation |
| TC-SETTINGS-007 | 验证Port端口号范围校验 | P1 | Boundary |
| TC-SETTINGS-008 | 验证Enable SSL开关功能 | P1 | Functional |
| TC-SETTINGS-009 | 验证Use Default Credentials开关 | P2 | Functional |
| TC-SETTINGS-010 | 验证密码字段安全性 | P1 | Security |
| TC-SETTINGS-011 | 验证Office 365配置 | P1 | Functional |
| TC-SETTINGS-012 | 验证清空配置功能 | P2 | Functional |
| TC-SETTINGS-013 | 验证Host字段输入 | P1 | Validation |
| TC-SETTINGS-014 | 验证Domain字段（可选） | P2 | Functional |
| TC-SETTINGS-015 | 验证配置修改覆盖 | P1 | Data |

### Feature Management 测试用例

| 用例编号 | 用例标题 | 优先级 | 类型 |
|---------|---------|-------|------|
| TC-FEATURE-001 | 验证Feature Management页面加载 | P0 | Functional |
| TC-FEATURE-002 | 验证功能管理描述文本 | P1 | UI |
| TC-FEATURE-003 | 验证"Manage Host Features"按钮 | P0 | Functional |
| TC-FEATURE-004 | 验证Features对话框打开 | P0 | Functional |
| TC-FEATURE-005 | 验证空功能列表提示 | P1 | UI |
| TC-FEATURE-006 | 验证对话框取消按钮 | P1 | Functional |
| TC-FEATURE-007 | 验证对话框关闭按钮（X） | P1 | Functional |
| TC-FEATURE-008 | 验证ESC键关闭对话框 | P2 | UX |
| TC-FEATURE-009 | 验证对话框Save按钮（空功能） | P2 | Functional |
| TC-FEATURE-010 | 验证从Settings Tab访问Feature Management | P1 | Functional |
| TC-FEATURE-011 | 验证页面刷新保持状态 | P2 | Data |
| TC-FEATURE-012 | 验证对话框外部点击关闭 | P2 | UX |
| TC-FEATURE-013 | 验证对话框层级（Z-index） | P2 | UI |
| TC-FEATURE-014 | 验证多次打开关闭对话框 | P2 | Performance |
| TC-FEATURE-015 | 验证功能开关切换 | P0 | Functional |
| TC-FEATURE-016 | 验证功能配额设置 | P1 | Functional |

---

## 📝 测试执行记录

### 执行状态说明
- ✅ 通过
- ❌ 失败
- ⏸️ 阻塞
- ⏭️ 跳过
- 🔄 待执行

### 最近执行记录

| 测试模块 | 执行日期 | 执行人 | 状态 | 备注 |
|---------|---------|-------|------|------|
| Dashboard | 2025-12-02 | 自动化 | 🔄 | 等待服务器启动 |
| Settings | 2025-12-02 | 自动化 | 🔄 | 等待服务器启动 |
| Feature Management | 2025-12-02 | 自动化 | 🔄 | 等待服务器启动 |

---

## 🔗 相关文档

- [项目README](../../../README.md)
- [测试环境配置](../../../docs/setup.md)
- [Allure报告使用指南](../../../docs/allure-guide.md)

---

## 📧 联系方式

如有问题或建议，请联系测试团队。

**文档版本**: 1.0  
**创建日期**: 2025-12-02  
**最后更新**: 2025-12-02  
**维护人**: Test Team

