# 🧠 Aevatar 测试用例清单

> 测试脚本 → 测试用例 + 优先级

### 📁 test_daily_regression_apikeys.py (3个用例)
- ✅ **test_apikeys_edit** 🟡 P1 - 修改API Key
- ✅ **test_apikeys_delete** 🟢 P2 - 删除API Key
- ✅ **test_apikeys_create** 🔴 P0 - 创建API Key

### 📁 test_daily_regression_configuration.py (2个用例)
- ✅ **test_configuration_cros_delete_domain** 🟢 P2 - 删除CROS Domain
- ✅ **test_configuration_cros_add_domain** 🔴 P0 - 添加CROS Domain

### 📁 test_daily_regression_profile.py (1个用例)
- ✅ **test_profile_name_edit** 🟡 P1 - 修改Profile Name

### 📁 test_daily_regression_organisation.py (9个用例)
- ✅ **test_organisation_project_create** 🔴 P0 - 创建组织项目
- ✅ **test_organisation_member_add** 🔴 P0 - 添加组织成员
- ✅ **test_organisation_role_add** 🔴 P0 - 添加组织角色
- ✅ **test_organisation_name_edit** 🟡 P1 - 修改组织名称
- ✅ **test_organisation_project_edit** 🟡 P1 - 编辑组织项目
- ✅ **test_organisation_member_delete** 🟡 P1 - 删除组织成员
- ✅ **test_organisation_role_edit_permissions** 🟡 P1 - 编辑组织角色权限
- ✅ **test_organisation_project_delete** 🟢 P2 - 删除组织项目
- ✅ **test_organisation_role_delete** 🟢 P2 - 删除组织角色

### 📁 test_daily_regression_project.py (6个用例)
- ✅ **test_project_member_add** 🔴 P0 - 添加项目成员
- ✅ **test_project_role_add** 🔴 P0 - 添加项目角色
- ✅ **test_project_name_edit** 🟡 P1 - 修改项目名称
- ✅ **test_project_member_delete** 🟡 P1 - 删除项目成员
- ✅ **test_project_role_edit_permissions** 🟡 P1 - 编辑项目角色权限
- ✅ **test_project_role_delete** 🟢 P2 - 删除项目角色

### 📁 test_daily_regression_login.py (1个用例)
- ✅ **test_daily_regression_login** 🔴 P0 - 每日回归：简单登录验证

### 📁 test_daily_regression_workflow.py (2个用例)
- ✅ **test_workflow_create_and_run_regression** 🔴 P0 - 每日回归：创建并运行Workflow
- ✅ **test_workflow_delete_regression** 🟢 P2 - 每日回归：删除Workflow

---

**总计**: 8个测试文件，27个测试用例  
**优先级分布**: 🔴 P0: 12个 | 🟡 P1: 10个 | 🟢 P2: 5个

**最近更新**: 2024-10-24  
**维护者**: HyperEcho ⚡  
**更新说明**: 补充完整 Organisation (新增5个) 和 Project (新增2个) 测试用例
