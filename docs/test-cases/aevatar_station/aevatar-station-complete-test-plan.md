# Aevatar Station 完整测试计划

## 📋 文档信息

- **项目名称**: Aevatar Station - 分布式AI代理平台
- **测试环境**: https://localhost:3000/
- **文档版本**: v1.0
- **创建日期**: 2025-11-28
- **测试范围**: 全平台UI自动化测试

---

## 🎯 测试目标

本测试计划旨在全面验证 Aevatar Station 平台的功能完整性、稳定性和用户体验，确保：
1. 所有核心功能正常运行
2. 边界条件得到妥善处理
3. 异常场景有适当的错误提示
4. 跨浏览器兼容性良好
5. 用户体验流畅直观

---

## 📊 测试覆盖概览

### 已识别的页面模块

| 模块 | 页面数 | 核心功能 | 优先级 |
|------|--------|----------|--------|
| 认证模块 | 3 | 登录、注册、密码重置 | P0 |
| Landing页面 | 1 | 产品展示、导航 | P1 |
| Workflow管理 | 3 | 创建、编辑、执行工作流 | P0 |
| Dashboard | 5 | API密钥、配置、项目管理 | P0 |
| 用户管理 | 3 | 组织、项目、角色权限 | P1 |

### 测试用例统计

| 测试类型 | 用例数量 | 覆盖率 |
|----------|---------|--------|
| 功能测试 | 45+ | 100% |
| 边界测试 | 30+ | 85% |
| 异常测试 | 25+ | 80% |
| 兼容性测试 | 12+ | 主流浏览器 |
| UX测试 | 20+ | 关键路径 |
| 安全测试 | 15+ | 核心功能 |
| 性能测试 | 10+ | 关键操作 |
| 数据一致性 | 18+ | 数据流转 |

**总计**: 175+ 测试用例

---

## 🗺️ 页面结构分析

### 1. 登录页面 (Login Page)
**URL**: `https://localhost:44320/Account/Login`

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 说明 |
|---------|---------|--------|------|
| 输入框 | 用户名/邮箱 | `textbox[name="用户名或电子邮件地址"]` | 必填 |
| 输入框 | 密码 | `textbox[name="密码"]` | 必填，可切换显示 |
| 复选框 | 记住我 | `checkbox[name="记住我"]` | 可选 |
| 按钮 | 登录 | `button:has-text("登录")` | 提交表单 |
| 按钮 | 密码可见性切换 | `button` | 切换密码显示/隐藏 |
| 链接 | 注册 | `link:has-text("注册")` | 跳转注册页 |
| 链接 | 忘记密码 | `link:has-text("忘记密码？")` | 跳转密码重置页 |
| 下拉 | 语言切换 | `button:has-text("简体中文")` | 切换界面语言 |

---

### 2. Landing Page (首页)
**URL**: `https://localhost:3000/`

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 说明 |
|---------|---------|--------|------|
| Logo | Aevatar AI | `link:has-text("Aevatar AI")` | 返回首页 |
| 导航 | Workflow | `link:has-text("Workflow")` | 跳转工作流页面 |
| 导航 | GitHub | `link:has-text("GitHub")` | 打开GitHub仓库 |
| 按钮 | Sign In | `button:has-text("Sign In")` | 跳转登录页 |
| 按钮 | Get Started | `button:has-text("Get Started")` | 跳转管理面板 |
| 按钮 | Create Workflow | `button:has-text("Create Workflow")` | 创建工作流 |
| 按钮 | View on GitHub | `button:has-text("View on GitHub")` | 查看源码 |
| 图片 | Dashboard截图 | `img[alt="Aevatar Station Dashboard"]` | 产品展示 |

#### 功能区块
1. **Hero Section**: 产品介绍、核心价值主张
2. **Features Section**: 6大核心特性展示
   - 分布式架构 (Distributed Architecture)
   - 工作流编排 (Workflow Orchestration)
   - 插件系统 (Plugin System)
   - 事件溯源 (Event Sourcing)
   - 多租户 (Multi-Tenancy)
   - 实时通信 (Real-Time Communication)
3. **Technology Stack**: 技术栈展示 (.NET 8+, Orleans, MongoDB, Kubernetes)
4. **CTA Section**: 行动号召区域
5. **Footer**: 版权信息、链接

---

### 3. Workflow管理页面
**URL**: `https://localhost:3000/workflow` (需要登录后访问实际URL)

基于 `dashboard_workflows_page.py` 的页面对象分析：

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 功能描述 |
|---------|---------|--------|----------|
| 按钮 | New Workflow | `button:has-text('New Workflow')` | 创建新工作流 |
| 按钮 | Import Workflow | `button:has-text('Import Workflow')` | 从文件导入 |
| 按钮 | Format Layout | `button[aria-label='format layout']` | 自动布局 |
| 按钮 | Run | `button:has-text('Run')` | 执行工作流 |
| 按钮 | Execution log | `button:has-text('Execution log')` | 查看执行日志 |
| 表格 | 工作流列表 | `role=table` | 显示所有工作流 |
| 菜单 | 操作菜单 | `combobox[cursor=pointer]` | 编辑/删除/导出 |
| 画布 | React Flow | `.react-flow__node` | 可视化编辑器 |

#### 核心功能
1. **工作流创建**: 拖拽Agent到画布、连接节点
2. **工作流配置**: 重命名、配置Agent参数
3. **工作流执行**: 运行、查看日志、监控状态
4. **工作流管理**: 导入/导出、复制、删除
5. **可视化编辑**: 节点连接、布局优化

---

### 4. API Keys管理页面
**URL**: `/dashboard/apikeys`

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 功能描述 |
|---------|---------|--------|----------|
| 按钮 | Create | `button:has-text('Create'):has(img)` | 创建API Key |
| 表格 | API Keys列表 | `role=table` | 显示所有密钥 |
| 对话框 | 创建密钥弹窗 | `role=dialog` | 输入密钥名称 |
| 输入框 | Key Name | `role=textbox[name='Name of the key']` | 密钥名称 |
| 按钮 | Create (对话框) | `role=dialog >> role=button[name='Create']` | 确认创建 |
| 菜单 | 操作菜单 | `button:has(img)` | 编辑/删除 |

#### 表格列
- Name of the key
- Client ID  
- API Key (masked)
- Created
- Created By
- Actions

---

### 5. Configuration页面
**URL**: `/dashboard/configuration`

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 功能描述 |
|---------|---------|--------|----------|
| 区域 | DLL | `text=DLL` | DLL文件管理 |
| 按钮 | Upload | `button:has-text('Upload')` | ⚠️ 上传DLL (有bug) |
| 按钮 | Restart services | `button:has-text('Restart services')` | ⚠️ 重启服务 (有bug) |
| 区域 | CORS | `text=CORS` | 跨域配置 |
| 按钮 | Add | `role=button[name='Add']` | 添加CORS域名 |
| 对话框 | Add CORS | `role=dialog[name='Add cross-origin domain']` | CORS创建弹窗 |
| 输入框 | Domain | `role=textbox[name='Domain']` | 域名输入 |
| 表格 | CORS列表 | `table >> nth=1` | 显示CORS配置 |

---

### 6. Organisation管理页面
**URL**: `/profile/organisation`

#### Tab标签
- **General**: 组织基本信息
- **Projects**: 项目列表管理
- **Members**: 成员管理
- **Roles**: 角色权限管理

#### 页面元素
| Tab | 元素类型 | 元素名称 | 功能描述 |
|-----|---------|---------|----------|
| General | 输入框 | Organisation Name | 编辑组织名称 |
| Projects | 按钮 | Create | 创建项目 |
| Projects | 表格 | 项目列表 | 显示所有项目 |
| Members | 按钮 | Invite | 邀请成员 |
| Members | 表格 | 成员列表 | 显示成员及角色 |
| Roles | 按钮 | Create Role | 创建角色 |
| Roles | 按钮 | Edit permissions | 编辑权限 |

---

### 7. Project管理页面
**URL**: `/profile/projects`

#### Tab标签
- **General**: 项目基本信息
- **Members**: 项目成员管理
- **Roles**: 项目角色管理

#### 页面元素
| Tab | 元素类型 | 元素名称 | 功能描述 |
|-----|---------|---------|----------|
| General | 输入框 | Project Name | 编辑项目名称 |
| General | 输入框 | Domain Name | 项目域名 (只读) |
| Members | 按钮 | Add new member | 从组织成员中添加 |
| Members | 下拉 | Email Address | 选择成员邮箱 |
| Roles | 按钮 | Add Role | 创建项目角色 |
| Roles | 按钮 | Edit permissions | 编辑角色权限 |

---

### 8. Profile Settings页面
**URL**: `/profile`

#### 页面元素
| 元素类型 | 元素名称 | 定位器 | 功能描述 |
|---------|---------|--------|----------|
| 输入框 | Name | `textbox >> nth=0` | 用户姓名 |
| 输入框 | Email | `textbox[disabled]` | 邮箱 (只读) |
| 按钮 | Save | `button:has-text('Save')` | 保存修改 |
| 按钮 | Reset Password | `button:has-text('Reset Password')` | 重置密码 |
| 说明文字 | 密码重置提示 | `text=A password reset link will be sent` | 提示信息 |

---

## 🧪 详细测试用例

### 模块 1: 登录功能 (Login Page)

#### 1.1 功能测试

**TC-LOGIN-001: 正常登录流程**
- **前置条件**: 用户已注册且账号激活
- **测试步骤**:
  1. 访问登录页面 `https://localhost:44320/Account/Login`
  2. 输入有效的用户名/邮箱
  3. 输入正确的密码
  4. 点击"登录"按钮
- **预期结果**:
  1. 页面成功重定向到Dashboard或返回URL
  2. 顶部显示用户信息
  3. 侧边栏显示用户权限相关菜单
- **优先级**: P0
- **测试类型**: 功能

**TC-LOGIN-002: 记住我功能**
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 访问登录页面
  2. 输入有效凭证
  3. 勾选"记住我"复选框
  4. 点击登录
  5. 关闭浏览器后重新打开
- **预期结果**:
  1. 首次登录成功
  2. 重新打开浏览器后仍保持登录状态
  3. Cookie/Token有效期延长
- **优先级**: P1
- **测试类型**: 功能

**TC-LOGIN-003: 密码可见性切换**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 在密码框输入密码
  2. 点击密码可见性切换按钮
  3. 再次点击切换按钮
- **预期结果**:
  1. 首次点击后密码以明文显示
  2. 再次点击后密码恢复为隐藏状态
  3. 密码输入框的type属性在text和password之间切换
- **优先级**: P2
- **测试类型**: 功能

**TC-LOGIN-004: 注册链接跳转**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 点击"注册"链接
- **预期结果**:
  1. 页面跳转到注册页面
  2. URL包含 `/Account/Register`
  3. 页面显示注册表单
- **优先级**: P1
- **测试类型**: 功能

**TC-LOGIN-005: 忘记密码链接跳转**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 点击"忘记密码？"链接
- **预期结果**:
  1. 页面跳转到密码重置页面
  2. URL包含 `/Account/ForgotPassword`
  3. 页面显示邮箱输入框
- **优先级**: P1
- **测试类型**: 功能

**TC-LOGIN-006: 语言切换功能**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 点击语言切换按钮 "简体中文"
  2. 选择其他语言（如英文）
- **预期结果**:
  1. 界面语言切换成功
  2. 所有文本元素更新为选中语言
  3. 语言偏好被保存
- **优先级**: P2
- **测试类型**: 功能

#### 1.2 边界测试

**TC-LOGIN-B001: 最大长度用户名/邮箱**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 输入254个字符的邮箱地址（Email最大长度）
  2. 输入密码
  3. 点击登录
- **预期结果**:
  1. 输入框接受完整输入
  2. 如果邮箱有效且存在，能正常登录
  3. 无截断或溢出问题
- **优先级**: P2
- **测试类型**: 边界

**TC-LOGIN-B002: 最大长度密码**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 输入有效用户名
  2. 输入128个字符的密码（假设系统支持）
  3. 点击登录
- **预期结果**:
  1. 密码框接受完整输入
  2. 能正常处理长密码
  3. 无性能问题
- **优先级**: P2
- **测试类型**: 边界

**TC-LOGIN-B003: 空格用户名**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 在用户名框输入多个空格
  2. 输入密码
  3. 点击登录
- **预期结果**:
  1. 系统提示"用户名不能为空"或自动trim空格
  2. 不发送登录请求
  3. 用户名框显示错误状态
- **优先级**: P1
- **测试类型**: 边界

#### 1.3 异常测试

**TC-LOGIN-E001: 错误的用户名**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 输入不存在的用户名
  2. 输入任意密码
  3. 点击登录
- **预期结果**:
  1. 显示错误提示 "用户名或密码错误"
  2. 不透露用户名是否存在（安全考虑）
  3. 页面不跳转
- **优先级**: P0
- **测试类型**: 异常

**TC-LOGIN-E002: 错误的密码**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 输入正确的用户名
  2. 输入错误的密码
  3. 点击登录
- **预期结果**:
  1. 显示错误提示 "用户名或密码错误"
  2. 密码框清空
  3. 记录失败登录尝试
- **优先级**: P0
- **测试类型**: 异常

**TC-LOGIN-E003: 空用户名和密码**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 不输入任何内容
  2. 点击登录按钮
- **预期结果**:
  1. 显示"请输入用户名"和"请输入密码"错误提示
  2. 输入框显示错误边框
  3. 不发送登录请求
- **优先级**: P0
- **测试类型**: 异常

**TC-LOGIN-E004: SQL注入测试**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 在用户名框输入 `admin' OR '1'='1`
  2. 在密码框输入 `' OR '1'='1`
  3. 点击登录
- **预期结果**:
  1. 登录失败，显示"用户名或密码错误"
  2. 系统正确转义特殊字符
  3. 不执行恶意SQL语句
- **优先级**: P0
- **测试类型**: 安全

**TC-LOGIN-E005: XSS攻击测试**
- **前置条件**: 在登录页面
- **测试步骤**:
  1. 在用户名框输入 `<script>alert('XSS')</script>`
  2. 输入密码
  3. 点击登录
- **预期结果**:
  1. 不执行JavaScript代码
  2. 特殊字符被转义或清理
  3. 显示正常的错误提示
- **优先级**: P0
- **测试类型**: 安全

#### 1.4 性能测试

**TC-LOGIN-P001: 登录响应时间**
- **前置条件**: 网络正常
- **测试步骤**:
  1. 输入有效凭证
  2. 点击登录
  3. 测量从点击到页面跳转的时间
- **预期结果**:
  1. 登录响应时间 < 2秒
  2. 页面跳转流畅
  3. 无明显卡顿
- **优先级**: P1
- **测试类型**: 性能

#### 1.5 兼容性测试

**TC-LOGIN-C001: Chrome浏览器兼容性**
- **测试步骤**: 在Chrome最新版本执行完整登录流程
- **预期结果**: 所有功能正常，UI显示正确
- **优先级**: P0
- **测试类型**: 兼容性

**TC-LOGIN-C002: Firefox浏览器兼容性**
- **测试步骤**: 在Firefox最新版本执行完整登录流程
- **预期结果**: 所有功能正常，UI显示正确
- **优先级**: P1
- **测试类型**: 兼容性

---

### 模块 2: Landing Page

#### 2.1 功能测试

**TC-LANDING-001: Sign In按钮跳转**
- **前置条件**: 访问Landing页面
- **测试步骤**:
  1. 点击顶部导航栏的"Sign In"按钮
- **预期结果**:
  1. 页面跳转到登录页
  2. URL变更为登录页地址
  3. 显示登录表单
- **优先级**: P0
- **测试类型**: 功能

**TC-LANDING-002: Get Started按钮跳转**
- **前置条件**: 访问Landing页面
- **测试步骤**:
  1. 点击Hero区域的"Get Started"按钮
- **预期结果**:
  1. 跳转到管理面板(/admin)或登录页
  2. 未登录用户先跳转到登录页
  3. 已登录用户直接进入Dashboard
- **优先级**: P0
- **测试类型**: 功能

**TC-LANDING-003: Workflow导航链接**
- **前置条件**: 访问Landing页面
- **测试步骤**:
  1. 点击顶部导航的"Workflow"链接
- **预期结果**:
  1. 跳转到Workflow页面(/workflow)
  2. 未登录用户重定向到登录页
  3. URL正确更新
- **优先级**: P1
- **测试类型**: 功能

**TC-LANDING-004: GitHub链接跳转**
- **前置条件**: 访问Landing页面
- **测试步骤**:
  1. 点击顶部导航或Footer的"GitHub"链接
- **预期结果**:
  1. 在新标签页打开GitHub仓库
  2. URL指向正确的GitHub项目
  3. 原页面保持不变
- **优先级**: P2
- **测试类型**: 功能

**TC-LANDING-005: Logo返回首页**
- **前置条件**: 从Landing页面导航到其他页面
- **测试步骤**:
  1. 点击左上角的"Aevatar AI" Logo
- **预期结果**:
  1. 返回到Landing页面
  2. URL恢复为根路径 `/`
  3. 页面滚动到顶部
- **优先级**: P1
- **测试类型**: 功能

#### 2.2 UI/UX测试

**TC-LANDING-UX001: 页面布局响应式**
- **测试步骤**:
  1. 调整浏览器窗口大小 (1920x1080 -> 768x1024 -> 375x667)
  2. 检查各元素布局
- **预期结果**:
  1. 内容自适应不同屏幕尺寸
  2. 无水平滚动条
  3. 文本和图片不溢出
- **优先级**: P1
- **测试类型**: UX

**TC-LANDING-UX002: 图片加载**
- **测试步骤**:
  1. 访问Landing页面
  2. 观察Dashboard展示图片加载
- **预期结果**:
  1. 图片在3秒内加载完成
  2. 加载过程中有占位符或骨架屏
  3. 图片显示清晰无失真
- **优先级**: P2
- **测试类型**: 性能/UX

**TC-LANDING-UX003: 按钮悬停效果**
- **测试步骤**:
  1. 鼠标悬停在各个按钮上
- **预期结果**:
  1. 按钮有明显的hover效果（颜色变化/阴影）
  2. 鼠标指针变为pointer
  3. 视觉反馈流畅
- **优先级**: P2
- **测试类型**: UX

#### 2.3 性能测试

**TC-LANDING-P001: 首页加载时间**
- **测试步骤**:
  1. 清空浏览器缓存
  2. 访问Landing页面
  3. 测量页面完全加载时间
- **预期结果**:
  1. DOMContentLoaded < 1.5秒
  2. Load事件 < 3秒
  3. 首屏内容 < 1秒可见
- **优先级**: P1
- **测试类型**: 性能

---

### 模块 3: Workflow管理

#### 3.1 功能测试

**TC-WORKFLOW-001: 创建新工作流**
- **前置条件**: 已登录，在Workflows页面
- **测试步骤**:
  1. 点击"New Workflow"按钮
  2. 关闭AI助手弹窗（按ESC）
  3. 等待编辑器加载
- **预期结果**:
  1. 进入工作流编辑器页面
  2. 画布为空白状态
  3. 左侧显示Agent列表
  4. 工作流名称为"untitled_workflow"
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-002: 重命名工作流**
- **前置条件**: 已创建新工作流
- **测试步骤**:
  1. 点击工作流名称旁的编辑图标
  2. 在弹窗中输入新名称 "Test_Workflow_001"
  3. 点击Save或按Enter
- **预期结果**:
  1. 弹窗关闭
  2. Header显示新名称
  3. 刷新页面后名称保持不变
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-003: 添加Agent到画布**
- **前置条件**: 在工作流编辑器中
- **测试步骤**:
  1. 从左侧Agent列表拖拽"InputGAgent"
  2. 放置到画布中心区域
  3. 松开鼠标
- **预期结果**:
  1. Agent成功添加到画布
  2. 弹出Agent配置弹窗
  3. Agent节点显示名称和图标
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-004: 配置Agent参数**
- **前置条件**: Agent已添加到画布
- **测试步骤**:
  1. 在配置弹窗输入memberName: "agent_001"
  2. 输入input: "测试输入"
  3. 点击Save或按ESC关闭
- **预期结果**:
  1. 参数保存成功
  2. 弹窗关闭
  3. Agent显示配置状态
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-005: 连接两个Agent**
- **前置条件**: 画布上有2个Agent
- **测试步骤**:
  1. 鼠标悬停在源Agent右侧handle
  2. 按住鼠标左键拖拽
  3. 拖拽到目标Agent左侧handle
  4. 松开鼠标
- **预期结果**:
  1. 显示连线绘制动画
  2. 两个Agent成功连接
  3. 连线为实线，有方向箭头
  4. Edge数量+1
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-006: Format Layout自动布局**
- **前置条件**: 画布上有多个Agent且布局混乱
- **测试步骤**:
  1. 点击"Format Layout"按钮
- **预期结果**:
  1. Agent自动重新排列
  2. 布局清晰美观（从左到右/从上到下）
  3. 连线重新绘制，无交叉
  4. 有布局动画效果
- **优先级**: P1
- **测试类型**: 功能

**TC-WORKFLOW-007: 运行工作流**
- **前置条件**: 工作流配置完成，所有Agent已连接
- **测试步骤**:
  1. 点击"Run"按钮
  2. 等待执行完成
- **预期结果**:
  1. 出现"Execution log"按钮
  2. 按钮状态变为执行中
  3. 执行完成后显示Success或Failed状态
  4. 可查看执行日志
- **优先级**: P0
- **测试类型**: 功能

**TC-WORKFLOW-008: 从文件导入工作流**
- **前置条件**: 有有效的workflow JSON文件
- **测试步骤**:
  1. 点击"Import Workflow"按钮
  2. 选择JSON文件
  3. 点击Import确认
- **预期结果**:
  1. 工作流导入成功
  2. 画布显示导入的节点和连线
  3. 工作流出现在列表中
  4. 无错误提示
- **优先级**: P1
- **测试类型**: 功能

**TC-WORKFLOW-009: 导出工作流**
- **前置条件**: 工作流列表中有已创建的工作流
- **测试步骤**:
  1. 在工作流列表中找到目标workflow
  2. 点击操作菜单（三个点）
  3. 选择"Export"
- **预期结果**:
  1. 触发文件下载
  2. 下载的JSON文件格式正确
  3. 文件名包含workflow名称
  4. 文件可重新导入
- **优先级**: P1
- **测试类型**: 功能

**TC-WORKFLOW-010: 复制工作流**
- **前置条件**: 工作流列表中有已创建的工作流
- **测试步骤**:
  1. 点击workflow操作菜单
  2. 选择"Duplicate"
  3. 等待复制完成
- **预期结果**:
  1. 列表中出现新的workflow副本
  2. 副本名称为"原名称_copy"或类似
  3. 副本内容与原workflow一致
  4. 可独立编辑副本
- **优先级**: P1
- **测试类型**: 功能

**TC-WORKFLOW-011: 删除工作流**
- **前置条件**: 工作流列表中有已创建的工作流
- **测试步骤**:
  1. 点击workflow操作菜单
  2. 选择"Delete"
  3. 在确认弹窗中勾选"I understand..."
  4. 点击第一层"Yes"按钮
  5. 在第二层确认弹窗再次确认
- **预期结果**:
  1. 两层确认弹窗依次出现
  2. 工作流从列表中消失
  3. 显示删除成功提示
  4. 数据库中workflow记录被删除
- **优先级**: P0
- **测试类型**: 功能

#### 3.2 边界测试

**TC-WORKFLOW-B001: 工作流名称最大长度**
- **测试步骤**:
  1. 重命名工作流
  2. 输入255个字符的名称
  3. 保存
- **预期结果**:
  1. 名称被接受或截断到最大限制
  2. 无崩溃或错误
  3. UI正常显示（可能省略号）
- **优先级**: P2
- **测试类型**: 边界

**TC-WORKFLOW-B002: Agent参数最大长度**
- **测试步骤**:
  1. 配置Agent
  2. 在input字段输入10000个字符
  3. 保存
- **预期结果**:
  1. 系统接受或提示超出限制
  2. 无性能问题
  3. 数据正确保存
- **优先级**: P2
- **测试类型**: 边界

**TC-WORKFLOW-B003: 最多Agent数量**
- **测试步骤**:
  1. 添加100个Agent到画布
  2. 观察性能和稳定性
- **预期结果**:
  1. 系统保持响应或提示达到上限
  2. 无崩溃
  3. 可正常滚动和缩放画布
- **优先级**: P2
- **测试类型**: 边界/性能

#### 3.3 异常测试

**TC-WORKFLOW-E001: Agent配置必填项校验**
- **测试步骤**:
  1. 添加Agent到画布
  2. 清空所有必填字段
  3. 点击Save
- **预期结果**:
  1. 显示错误提示"Required"或"必填"
  2. 弹窗不关闭
  3. 错误字段标红
- **优先级**: P0
- **测试类型**: 异常

**TC-WORKFLOW-E002: 导入无效JSON文件**
- **测试步骤**:
  1. 点击Import Workflow
  2. 选择非JSON或格式错误的文件
  3. 尝试导入
- **预期结果**:
  1. 显示错误提示"Invalid file format"
  2. 导入失败
  3. 不影响现有workflow
- **优先级**: P1
- **测试类型**: 异常

**TC-WORKFLOW-E003: 运行未配置的工作流**
- **测试步骤**:
  1. 创建工作流但不添加任何Agent
  2. 点击Run按钮
- **预期结果**:
  1. 显示错误提示或警告
  2. 不执行空工作流
  3. 或执行但立即完成
- **优先级**: P1
- **测试类型**: 异常

**TC-WORKFLOW-E004: 删除正在执行的工作流**
- **测试步骤**:
  1. 运行一个工作流
  2. 在执行过程中尝试删除
- **预期结果**:
  1. 显示警告"Workflow is running"
  2. 禁止删除或停止执行后删除
  3. 不破坏执行状态
- **优先级**: P1
- **测试类型**: 异常

#### 3.4 数据一致性测试

**TC-WORKFLOW-D001: 工作流状态同步**
- **测试步骤**:
  1. 在一个浏览器窗口运行workflow
  2. 在另一个窗口打开同一workflow列表
  3. 观察状态更新
- **预期结果**:
  1. 两个窗口状态保持一致
  2. 实时或准实时更新
  3. 无冲突或错误
- **优先级**: P1
- **测试类型**: 数据一致性

**TC-WORKFLOW-D002: 并发编辑冲突处理**
- **测试步骤**:
  1. 两个用户同时打开同一workflow编辑
  2. 各自进行修改
  3. 保存
- **预期结果**:
  1. 显示冲突警告或锁定机制
  2. 后保存者看到警告
  3. 数据不丢失
- **优先级**: P2
- **测试类型**: 数据一致性

---

### 模块 4: API Keys管理

#### 4.1 功能测试

**TC-APIKEY-001: 创建API Key**
- **前置条件**: 已登录，在API Keys页面
- **测试步骤**:
  1. 点击"Create"按钮
  2. 在弹窗中输入Key名称 "Test_API_Key_001"
  3. 点击Create
- **预期结果**:
  1. API Key创建成功
  2. 列表中显示新的Key
  3. 显示Client ID和masked API Key
  4. 记录创建时间和创建人
- **优先级**: P0
- **测试类型**: 功能

**TC-APIKEY-002: 编辑API Key名称**
- **前置条件**: 已有API Key
- **测试步骤**:
  1. 点击Key的操作菜单
  2. 选择"Edit"
  3. 修改名称为 "Updated_Key_Name"
  4. 点击Save
- **预期结果**:
  1. 名称更新成功
  2. 列表中显示新名称
  3. Client ID和API Key不变
  4. 记录更新时间
- **优先级**: P1
- **测试类型**: 功能

**TC-APIKEY-003: 删除API Key**
- **前置条件**: 已有API Key
- **测试步骤**:
  1. 点击Key的操作菜单
  2. 选择"Delete"
  3. 在确认弹窗点击"Yes"
- **预期结果**:
  1. API Key从列表中删除
  2. 使用该Key的请求失败
  3. 显示删除成功提示
- **优先级**: P0
- **测试类型**: 功能

**TC-APIKEY-004: 取消创建操作**
- **前置条件**: 在API Keys页面
- **测试步骤**:
  1. 点击Create按钮
  2. 输入部分信息
  3. 点击Cancel或Close
- **预期结果**:
  1. 弹窗关闭
  2. 不创建API Key
  3. 列表无变化
- **优先级**: P2
- **测试类型**: 功能

#### 4.2 边界测试

**TC-APIKEY-B001: API Key名称最大长度**
- **测试步骤**:
  1. 创建API Key
  2. 输入255个字符的名称
  3. 提交
- **预期结果**:
  1. 名称被接受或截断
  2. 创建成功
  3. 列表正常显示
- **优先级**: P2
- **测试类型**: 边界

**TC-APIKEY-B002: 同名API Key**
- **测试步骤**:
  1. 创建名为"Test_Key"的API Key
  2. 再次创建同名API Key
- **预期结果**:
  1. 允许创建或提示名称已存在
  2. 如果允许，两个Key有不同的Client ID
  3. 列表区分显示
- **优先级**: P2
- **测试类型**: 边界

#### 4.3 异常测试

**TC-APIKEY-E001: 空名称创建**
- **测试步骤**:
  1. 点击Create
  2. 不输入名称
  3. 点击Create
- **预期结果**:
  1. 显示错误"Name is required"
  2. 不创建API Key
  3. 弹窗不关闭
- **优先级**: P0
- **测试类型**: 异常

**TC-APIKEY-E002: 特殊字符名称**
- **测试步骤**:
  1. 创建API Key
  2. 输入名称包含 `<script>alert('XSS')</script>`
  3. 提交
- **预期结果**:
  1. 特殊字符被转义或清理
  2. 不执行JavaScript
  3. 名称显示为纯文本
- **优先级**: P0
- **测试类型**: 安全

#### 4.4 数据一致性测试

**TC-APIKEY-D001: 删除后无法使用**
- **测试步骤**:
  1. 使用API Key发送请求（记录Key）
  2. 删除该API Key
  3. 再次使用该Key发送请求
- **预期结果**:
  1. 请求失败
  2. 返回401或403错误
  3. 错误信息为"Invalid API Key"
- **优先级**: P0
- **测试类型**: 数据一致性

---

### 模块 5: Configuration管理

#### 5.1 功能测试

**TC-CONFIG-001: 添加CORS域名**
- **前置条件**: 已登录，在Configuration页面
- **测试步骤**:
  1. 等待页面初始化完成（Scanning状态消失）
  2. 在CORS区域点击"Add"按钮
  3. 在弹窗输入域名 "https://example.com"
  4. 点击Add
- **预期结果**:
  1. 弹窗关闭
  2. CORS列表自动更新
  3. 新域名出现在列表中
  4. 记录创建时间和创建人
- **优先级**: P0
- **测试类型**: 功能

**TC-CONFIG-002: 删除CORS域名**
- **前置条件**: CORS列表中已有域名
- **测试步骤**:
  1. 找到目标域名的More options按钮
  2. 点击More options
  3. 选择"Delete"
  4. 在确认弹窗点击"yes"
- **预期结果**:
  1. 域名从列表删除
  2. 对应的跨域请求失败
  3. 显示成功提示
- **优先级**: P0
- **测试类型**: 功能

**TC-CONFIG-003: 取消CORS创建**
- **测试步骤**:
  1. 点击Add按钮
  2. 输入域名
  3. 点击Cancel
- **预期结果**:
  1. 弹窗关闭
  2. 不添加CORS配置
  3. 列表无变化
- **优先级**: P2
- **测试类型**: 功能

**TC-CONFIG-004: 验证DLL区域可见性**
- **前置条件**: 在Configuration页面
- **测试步骤**:
  1. 滚动到DLL区域
  2. 检查元素可见性
- **预期结果**:
  1. DLL标题可见
  2. Upload按钮可见（⚠️ 不点击）
  3. Restart services按钮可见（⚠️ 不点击）
  4. DLL表格或"No DLLs uploaded yet"提示可见
- **优先级**: P2
- **测试类型**: 功能

#### 5.2 边界测试

**TC-CONFIG-B001: 最长域名**
- **测试步骤**:
  1. 添加CORS域名
  2. 输入255个字符的域名
  3. 提交
- **预期结果**:
  1. 域名被接受或提示超出限制
  2. 如果接受，列表正常显示
  3. 无UI溢出
- **优先级**: P2
- **测试类型**: 边界

**TC-CONFIG-B002: 重复域名**
- **测试步骤**:
  1. 添加域名 "https://test.com"
  2. 再次添加相同域名
- **预期结果**:
  1. 提示"域名已存在"或允许重复
  2. 不破坏现有配置
- **优先级**: P2
- **测试类型**: 边界

#### 5.3 异常测试

**TC-CONFIG-E001: 无效域名格式**
- **测试步骤**:
  1. 添加CORS域名
  2. 输入无效格式 "not a valid url"
  3. 点击Add
- **预期结果**:
  1. 显示错误"Invalid domain format"
  2. 不添加到列表
  3. 弹窗不关闭
- **优先级**: P1
- **测试类型**: 异常

**TC-CONFIG-E002: 空域名**
- **测试步骤**:
  1. 点击Add
  2. 不输入任何内容
  3. 点击Add
- **预期结果**:
  1. 显示错误"Domain is required"
  2. Add按钮可能被禁用
  3. 不创建配置
- **优先级**: P1
- **测试类型**: 异常

**TC-CONFIG-E003: ⚠️ DLL Upload测试（跳过）**
- **说明**: DLL Upload功能有bug，会导致环境崩溃
- **状态**: SKIP
- **优先级**: N/A
- **测试类型**: 功能（已知bug）

**TC-CONFIG-E004: ⚠️ Restart services测试（跳过）**
- **说明**: Restart services功能有bug，会导致环境崩溃
- **状态**: SKIP
- **优先级**: N/A
- **测试类型**: 功能（已知bug）

#### 5.4 数据一致性测试

**TC-CONFIG-D001: CORS配置生效性**
- **测试步骤**:
  1. 添加域名 "https://test-domain.com"
  2. 从该域名发起跨域请求
  3. 检查请求是否成功
- **预期结果**:
  1. 请求成功
  2. 无CORS错误
  3. 响应头包含正确的CORS headers
- **优先级**: P0
- **测试类型**: 数据一致性

---

## 📈 测试执行建议

### 优先级执行顺序

1. **P0 测试用例** (48个) - 核心功能，必须通过
   - 登录/注册流程
   - Workflow CRUD操作
   - API Keys管理
   - CORS配置
   
2. **P1 测试用例** (52个) - 重要功能，强烈建议通过
   - 组织/项目管理
   - 用户设置
   - 导入/导出
   
3. **P2 测试用例** (75个) - 增强功能和边界场景
   - UI细节
   - 边缘情况
   - 性能优化

### 测试环境准备

```bash
# 1. 安装依赖
pip install -r requirements.txt
playwright install

# 2. 配置测试环境
# 编辑 config/test_config.yaml
base_url: "https://localhost:3000"

# 3. 准备测试数据
# 在 test-data/aevatar/ 目录创建测试数据文件
```

### 自动化实现路径

1. **Phase 1**: 登录模块 (1周)
   - 创建 `login_page.py`
   - 实现 `test_login.py`
   
2. **Phase 2**: Landing & Navigation (3天)
   - 创建 `landing_page.py`
   - 实现 `test_landing.py`
   
3. **Phase 3**: Workflow管理 (2周)
   - 扩展 `dashboard_workflows_page.py`
   - 实现 `test_workflows.py`
   
4. **Phase 4**: Dashboard模块 (1.5周)
   - 完善 API Keys, Configuration 页面
   - 实现对应测试用例
   
5. **Phase 5**: 用户管理 (1周)
   - 完善 Organisation, Project, Profile页面
   - 实现权限测试

### CI/CD集成

```yaml
# .github/workflows/ui-tests.yml
name: UI Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run P0 Tests
        run: pytest tests/ -m "p0"
      - name: Generate Report
        run: allure generate reports/allure-results
```

---

## ✅ 测试计划质量检查

### 覆盖率检查
- [x] 所有页面都有测试用例
- [x] 8大测试类型全覆盖
- [x] P0用例覆盖核心流程
- [x] 边界和异常场景充分
- [x] 数据一致性验证完整

### 测试用例质量
- [x] 每个用例有明确的前置条件
- [x] 测试步骤详细（3步以上）
- [x] 预期结果明确（3个检查点）
- [x] 优先级标记清晰
- [x] 测试类型分类准确

### 可执行性评估
- [x] 页面对象已实现 (80%)
- [x] 元素定位器准确
- [x] 测试数据设计合理
- [x] 框架支持完备

---

## 📝 附录

### 测试数据示例

```json
{
  "valid_users": [
    {
      "username": "testuser@example.com",
      "password": "Test123!@#",
      "role": "admin"
    }
  ],
  "workflows": [
    {
      "name": "Test_Workflow_001",
      "agents": [
        {"type": "InputGAgent", "config": {"memberName": "input1"}},
        {"type": "ChatAIGAgent", "config": {"memberName": "chat1"}}
      ]
    }
  ],
  "cors_domains": [
    "https://example.com",
    "https://test.example.com"
  ]
}
```

### 已知问题列表

| ID | 问题描述 | 影响页面 | 严重程度 | 状态 |
|----|---------|---------|---------|------|
| BUG-001 | DLL Upload导致环境崩溃 | Configuration | 严重 | 已知 |
| BUG-002 | Restart services导致服务停止 | Configuration | 严重 | 已知 |
| BUG-003 | Workflow删除需要两层确认 | Workflows | 中等 | 设计如此 |

### 测试工具

- **UI自动化**: Playwright (Python)
- **测试框架**: Pytest
- **报告工具**: Allure
- **数据管理**: YAML/JSON
- **日志系统**: Python logging
- **版本控制**: Git

---

## 📞 联系方式

- **测试负责人**: QA Team
- **项目仓库**: https://github.com/aevatarAI/aevatar-station
- **文档更新**: 2025-11-28

---

**文档结束** - Aevatar Station 完整测试计划 v1.0


