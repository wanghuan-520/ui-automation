# Aevatar 日常回归测试脑图

## 🎯 测试环境
- **测试环境地址**: https://aevatar-station-ui-staging.aevatar.ai
- **优先级说明**: 🔴 P0（核心功能） | 🟡 P1（重要功能） | 🟢 P2（一般功能）

---

## 🔐 登录模块 🔴 P0

### 登录页面验证
- **前置条件**
  - 访问 URL：https://aevatar-station-ui-staging.aevatar.ai
- **测试步骤**
  - 进行邮箱登录
  - Email：[测试邮箱]
  - 密码：[测试密码]
- **预期结果**
  - ✅ 输入有效邮箱/密码后跳转 dashboard
  - ✅ 无布局问题

---

## 📊 Dashboard 功能模块

### 🔑 API Keys 管理
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/dashboard/apikeys

#### ➕ 添加 API Key 🔴 P0
- **测试步骤**
  1. 点击右上角 Create 按钮
  2. Create new API key 弹窗
     - Name of the key：随机生成
     - Project：默认
- **预期结果**
  - ✅ 创建成功，toast 提示：Successfully created
  - ✅ 创建成功后，Create 按钮不可点击

#### ✏️ 修改 API Key 🟡 P1
- **前置条件**
  - API key 已经存在
- **测试步骤**
  1. 点击列表右侧三个点，点击 Edit 按钮
  2. Edit API Key 弹窗，修改 Name of the Key 字段
  3. 点击 Save 按钮
- **预期结果**
  - ✅ 修改成功，toast 提示：Successfully saved
  - ✅ 不刷新的情况下，列表的 name 变成最新修改内容

#### 🗑️ 删除 API Key 🟢 P2
- **前置条件**
  - API key 已经存在
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功
  - ✅ 不刷新的情况下，列表变为空

---

### 🔄 Workflows 管理
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/dashboard/workflows

#### ➕ 创建 Workflow 🔴 P0
- **测试步骤**
  1. 点击右上角 New Workflow 按钮
  2. Workflow configuration 页面，拖拽 InputGAgent
  3. 点击 InputGAgent，在 Agent configuration 页面输入参数：
     - memberName：test
     - Input：Chinese food
  4. 点击右上角 Run
- **预期结果**
  - ✅ Workflow 运行成功，提示：workflow executed successfully
  - ✅ InputGAgent 下方展示 Success
  - ✅ 点击后查看 Agent logs，Output 展示：Chinese food

#### 🗑️ 删除 Workflow 🟢 P2
- **前置条件**
  - 存在 Workflows 列表
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功
  - ✅ 不刷新的情况下，列表变为空

---

### ⚙️ Configuration 配置
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/dashboard/configuration

#### 📦 Configuration-DLL
- **状态**: ⚠️ 功能存在问题，暂时不能用

#### 🌐 Configuration-CROS

##### ➕ 添加 Domain 🔴 P0
- **测试步骤**
  1. CROS 模块，点击右上角 Add 按钮
  2. Add cross-origin domain 弹窗，输入 Domain 内容（随机域名）
  3. 点击 Add 按钮
  4. 规则：Please enter a valid URL, e.g. https://example.com
- **预期结果**
  - ✅ 修改成功，toast 提示：Cross-origin domain added
  - ✅ 不刷新的情况下，列表显示新添加的内容

##### 🗑️ 删除 Domain 🟢 P2
- **前置条件**
  - domain 已经存在
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功，toast 提示：Cross-origin domain deleted
  - ✅ 不刷新的情况下，删除的 domain 记录消失

---

## 👤 Profile 配置模块

### 个人设置
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/profile/general

#### ✏️ 修改 Name 🟡 P1
- **测试步骤**
  1. 输入新的 Name
  2. 点击右侧 Save 按钮
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 点击右上角 Profile，显示最新 name

---

## 🏢 Organisation 管理模块

### ⚙️ Organisation Settings
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/organisation/general

#### ✏️ 修改 Organisation Name 🟡 P1
- **测试步骤**
  1. 输入新的 Organisation Name
  2. 点击下方的 Save 按钮
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 不刷新页面的情况下，查看页面左上角展示了新的 Organisation Name

---

### 📁 Organisation Projects
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/organisation/project

#### ➕ 创建 Project 🔴 P0
- **测试步骤**
  1. 点击右上角 Create 按钮
  2. Create Project 弹窗中输入 Project Name
  3. 点击右下角 Create 按钮保存
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 点击右上角 Profile，显示最新 name

#### ✏️ 编辑 Project 🟡 P1
- **前置条件**
  - 存在 Project 列表
- **测试步骤**
  1. 点击列表右侧三个点，点击 Edit 按钮
  2. Edit Project 弹窗，输入新的 Project Name
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 不刷新情况下，列表的 name 变为最新修改内容

#### 🗑️ 删除 Project 🟢 P2
- **前置条件**
  - 存在 Project 列表
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功，toast 提示：Successfully deleted
  - ✅ 不刷新的情况下，删除的 Project 记录消失

---

### 👥 Organisation Members
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/organisation/member

#### ➕ 添加 Member 🔴 P0
- **测试步骤**
  1. 点击右上角 Add new Member
  2. Invite Team Members 弹窗中输入：
     - Email Address
     - Role 下拉列表选择 Reader
  3. 点击右下角 Invite 按钮
- **预期结果**
  - ✅ 邀请后，toast 提示：successfully invited
  - ✅ 不刷新情况下，列表增加一条新记录

#### 🗑️ 删除 Member 🟡 P1
- **前置条件**
  - 存在 member 列表
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功，toast 提示：successfully removed
  - ✅ 不刷新的情况下，删除的 member 记录消失

---

### 🎭 Organisation Roles
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/organisation/role

#### ➕ 添加 Role 🔴 P0
- **测试步骤**
  1. 点击右上角 Add Role 按钮
  2. Create Role 弹窗中输入 Role Name
  3. 点击右下角 Create 按钮
- **预期结果**
  - ✅ 添加后，toast 提示：Successfully saved
  - ✅ 不刷新情况下，列表多一条记录

#### ✏️ 编辑 Role 权限 🟡 P1
- **前置条件**
  - 存在自定义 Role 记录
- **测试步骤**
  1. 点击列表中 Edit permissions 按钮
  2. Permission - manager 弹窗，勾选 grant all permissions
  3. 点击右下角 Save 按钮进行保存
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 再次点击列表中 Edit permissions 按钮，自动勾选了 grant all permissions

#### 🗑️ 删除 Role 🟢 P2
- **前置条件**
  - 存在自定义 Role 记录
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功，toast 提示：Successfully deleted
  - ✅ 不刷新的情况下，删除的 role 记录消失

---

## 📂 Project 管理模块
- **测试文件**: `test_daily_regression_project.py`
- **✨ 智能Project选择**: 自动扫描所有Project并选择最适合的测试Project
  - 优先选择有≥2个members的Project（确保add/delete测试可执行）
  - 每次测试选择同一个Project（确保环境一致性）
  - 支持自动刷新重试机制

### ⚙️ Project Settings
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/projects/general

#### ✏️ 修改 Project Name 🟡 P1
- **测试步骤**
  1. 输入新的 Project Name
  2. 点击 Save 按钮
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 不刷新情况下，右上角的 Project name 变成最新修改后内容

---

### 👥 Project Members
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/projects/member

#### 🔄 添加+删除 Member (组合测试) 🔴 P0
- **测试函数**: `test_project_member_add_and_delete`
- **执行时间**: ~90秒
- **优势**: 
  - ✅ 同一session中执行add→delete，确保环境一致
  - ✅ Add操作保证有数据供Delete使用
  - ✅ 避免测试间环境冲突，提高稳定性

**第一部分：添加 Member**
- **测试步骤**
  1. 记录初始Member数量
  2. 点击右上角 Add new Member
  3. Add team members 弹窗中：
     - Email Address 下拉列表选择一个 Email
     - Role 下拉列表选择 Reader
  4. 点击右下角 Add 按钮
  5. 刷新页面验证
- **预期结果**
  - ✅ Member数量增加
  - ✅ 新成员出现在列表中

**第二部分：删除 Member**
- **测试步骤**
  1. 定位刚添加的Member（第二行）
  2. 点击列表右侧三个点
  3. 点击 Delete 按钮
  4. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功
  - ✅ Member数量恢复到初始值
  - ✅ 成员从列表中移除

> **📝 说明**: 原独立的 `test_project_member_add` 和 `test_project_member_delete` 已被此组合测试替代（标记为SKIPPED），避免环境冲突。如需单独测试，可移除 `@pytest.mark.skip` 装饰器。

---

### 🎭 Project Roles
- **访问地址**: https://aevatar-station-ui-staging.aevatar.ai/profile/projects/role

#### ➕ 添加 Role 🔴 P0
- **测试步骤**
  1. 点击右上角 Add Role 按钮
  2. Create Role 弹窗中输入 Role Name
  3. 点击右下角 Create 按钮
- **预期结果**
  - ✅ 添加后，toast 提示：Successfully saved
  - ✅ 不刷新情况下，列表多一条记录

#### ✏️ 编辑 Role 权限 🟡 P1
- **前置条件**
  - 存在自定义 Role 记录
- **测试步骤**
  1. 点击列表中 Edit permissions 按钮
  2. Permission - manager 弹窗，勾选 grant all permissions
  3. 点击右下角 Save 按钮进行保存
- **预期结果**
  - ✅ 保存后，toast 提示：Successfully saved
  - ✅ 再次点击列表中 Edit permissions 按钮，自动勾选了 grant all permissions

#### 🗑️ 删除 Role 🟢 P2
- **前置条件**
  - 存在自定义 Role 记录
- **测试步骤**
  1. 点击列表右侧三个点，点击 Delete 按钮
  2. 再次确认弹窗，点击 Yes
- **预期结果**
  - ✅ 删除成功，toast 提示：Successfully deleted
  - ✅ 不刷新的情况下，删除的 role 记录消失

---

## 📊 测试用例统计

### 按优先级分类
- 🔴 **P0 核心功能**: 9 个测试用例
  - 登录验证
  - API Keys 添加
  - Workflow 创建
  - CROS 添加 domain
  - Organisation: Project/Member/Role 创建
  - Project: Member添加+删除（组合测试）、Role 添加

- 🟡 **P1 重要功能**: 8 个测试用例
  - API Keys 修改
  - Profile Name 修改
  - Organisation: Name/Project/Member/Role 编辑
  - Project: Name/Role 编辑

- 🟢 **P2 一般功能**: 6 个测试用例
  - API Keys/Workflow/CROS 删除
  - Organisation: Project/Role 删除
  - Project: Role 删除

- ⏭️ **SKIPPED**: 2 个测试用例
  - Project: Member 添加（已被组合测试替代）
  - Project: Member 删除（已被组合测试替代）

### 按模块分类
- 🔐 登录模块: 1 个
- 📊 Dashboard 功能: 6 个
- 👤 Profile 配置: 1 个
- 🏢 Organisation 管理: 10 个
- 📂 Project 管理: 7 个（5个执行，2个SKIPPED）
  - Project Settings: 1个
  - Project Members: 3个（1个组合测试✅ + 2个SKIPPED⏭️）
  - Project Roles: 3个

**总计**: 25 个测试用例（23个执行，2个SKIPPED）

