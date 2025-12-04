# 首页（Landing Page）测试计划

## 1. 测试概述

### 1.1 测试目标
验证Aevatar Station首页的正确性、完整性和用户体验，确保访客能够了解平台功能并顺利导航到各个功能模块。

### 1.2 测试范围
- **页面URL**: `https://localhost:3000/`
- **测试类型**: 功能测试、UI测试、导航测试、响应式测试
- **测试优先级**: P0（核心功能）、P1（重要功能）、P2（次要功能）

### 1.3 页面元素清单
通过Playwright MCP识别的关键页面元素：

| 元素 | 类型 | 选择器/名称 | 功能 |
|------|------|-------------|------|
| Logo/品牌名 | link | "Aevatar AI" | 首页链接 |
| Workflow导航链接 | link | "Workflow" | 导航到工作流页面 |
| GitHub链接 | link | "GitHub" | 外部链接到GitHub |
| 用户菜单按钮 | button | "Toggle user menu" | 展开用户菜单 |
| 导航菜单按钮 | button | "Toggle navigation menu" | 移动端导航菜单 |
| Hero标题 | heading | "Aevatar Station" | 主标题 |
| Hero副标题 | text | "Distributed AI Platform" | 副标题标签 |
| Hero描述 | text | "Your all-in-one platform..." | 平台描述 |
| Create Workflow按钮 | button | "Create Workflow" | 主要CTA按钮 |
| View on GitHub按钮 | button | "View on GitHub" | 次要CTA按钮 |
| Dashboard图片 | img | "Aevatar Station Dashboard" | 产品展示图 |
| 平台介绍标题 | heading | "Enterprise-Grade AI Agent Platform" | 功能介绍标题 |
| Admin Panel按钮 | button | "Admin Panel" | 管理面板入口 |
| Footer版权信息 | text | "© 2025 Aevatar..." | 版权声明 |
| Terms of Service链接 | link | "Terms of Service" | 服务条款 |
| Privacy链接 | link | "Privacy" | 隐私政策 |

---

## 2. 测试用例

### 2.1 页面加载测试 - P0

#### TC-LANDING-001: 首页正常加载验证
- **优先级**: P0
- **前置条件**: 无
- **测试步骤**:
  1. 访问首页URL: `https://localhost:3000/`
  2. 截图：页面完全加载后
  3. 验证页面标题为"Aevatar Station"
  4. 验证所有关键元素可见
- **预期结果**: 
  - 页面在3秒内加载完成
  - 页面标题正确显示
  - 无JavaScript错误
  - 所有关键内容可见
- **标签**: `@landing`, `@P0`, `@functional`

#### TC-LANDING-002: Hero区域内容验证
- **优先级**: P0
- **前置条件**: 页面已加载
- **测试步骤**:
  1. 访问首页
  2. 截图：Hero区域
  3. 验证主标题"Aevatar Station"可见
  4. 验证副标题"Distributed AI Platform"可见
  5. 验证描述文本可见且完整
  6. 验证Dashboard展示图加载成功
- **预期结果**: 
  - 所有Hero区域内容正确显示
  - 文本清晰易读
  - 图片加载成功无破损
- **标签**: `@landing`, `@P0`, `@ui`

---

### 2.2 导航功能测试 - P0/P1

#### TC-LANDING-003: Logo点击返回首页
- **优先级**: P1
- **前置条件**: 在首页
- **测试步骤**:
  1. 点击页面左上角"Aevatar AI" Logo
  2. 截图：点击后
  3. 验证URL仍为首页
- **预期结果**: 保持在首页或刷新首页
- **标签**: `@landing`, `@P1`, `@navigation`

#### TC-LANDING-004: Workflow导航链接验证
- **优先级**: P1
- **前置条件**: 在首页
- **测试步骤**:
  1. 截图：初始状态
  2. 点击顶部导航栏"Workflow"链接
  3. 截图：跳转后的页面
  4. 验证URL包含"workflow"
- **预期结果**: 成功跳转到Workflow页面
- **标签**: `@landing`, `@P1`, `@navigation`

#### TC-LANDING-005: GitHub链接验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 点击顶部导航栏"GitHub"链接
  2. 验证是否在新标签页打开
  3. 验证目标URL为GitHub仓库地址
- **预期结果**: 在新标签页打开GitHub仓库
- **标签**: `@landing`, `@P2`, `@navigation`

#### TC-LANDING-006: Create Workflow按钮验证
- **优先级**: P0
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 截图：初始状态
  2. 点击Hero区域的"Create Workflow"按钮
  3. 截图：点击后
  4. 验证跳转到登录页面或Workflow创建页面
- **预期结果**: 
  - 未登录用户跳转到登录页
  - 已登录用户跳转到创建页面
- **标签**: `@landing`, `@P0`, `@navigation`

#### TC-LANDING-007: View on GitHub按钮验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 点击"View on GitHub"按钮
  2. 验证GitHub页面打开
- **预期结果**: 在新标签页打开GitHub仓库
- **标签**: `@landing`, `@P2`, `@navigation`

#### TC-LANDING-008: Admin Panel按钮验证
- **优先级**: P0
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 滚动到页面底部
  2. 截图：Admin Panel按钮可见
  3. 点击"Admin Panel"按钮
  4. 截图：跳转后的页面
  5. 验证跳转到登录页面
- **预期结果**: 
  - 未登录用户跳转到登录页
  - 已登录用户跳转到Dashboard
- **标签**: `@landing`, `@P0`, `@navigation`

#### TC-LANDING-009: 用户菜单按钮验证（未登录）
- **优先级**: P1
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 截图：用户菜单按钮
  2. 点击右上角用户菜单按钮
  3. 截图：点击后
  4. 验证显示登录选项或跳转到登录页
- **预期结果**: 显示登录/注册选项或跳转到登录页
- **标签**: `@landing`, `@P1`, `@navigation`

---

### 2.3 Footer测试 - P2

#### TC-LANDING-010: Footer内容验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 滚动到页面底部
  2. 截图：Footer区域
  3. 验证版权信息可见："© 2025 Aevatar. All rights reserved."
  4. 验证"Terms of Service"链接可见
  5. 验证"Privacy"链接可见
- **预期结果**: Footer所有内容正确显示
- **标签**: `@landing`, `@P2`, `@ui`

#### TC-LANDING-011: Terms of Service链接验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 滚动到Footer
  2. 点击"Terms of Service"链接
  3. 验证跳转到服务条款页面
- **预期结果**: 成功跳转到服务条款页面
- **标签**: `@landing`, `@P2`, `@navigation`

#### TC-LANDING-012: Privacy链接验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 滚动到Footer
  2. 点击"Privacy"链接
  3. 验证跳转到隐私政策页面
- **预期结果**: 成功跳转到隐私政策页面
- **标签**: `@landing`, `@P2`, `@navigation`

---

### 2.4 UI/UX测试 - P1/P2

#### TC-LANDING-013: 响应式布局验证
- **优先级**: P1
- **前置条件**: 在首页
- **测试步骤**:
  1. 在桌面视口（1920x1080）查看页面
  2. 截图：桌面视图
  3. 切换到平板视口（768x1024）
  4. 截图：平板视图
  5. 切换到移动视口（375x667）
  6. 截图：移动视图
  7. 验证所有视口下内容布局合理
- **预期结果**: 
  - 各视口下布局自适应
  - 移动端显示汉堡菜单
  - 所有内容可见且易于交互
- **标签**: `@landing`, `@P1`, `@ui`, `@responsive`

#### TC-LANDING-014: 页面滚动流畅性验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 从页面顶部平滑滚动到底部
  2. 验证滚动过程流畅
  3. 验证所有内容按序加载
- **预期结果**: 
  - 滚动流畅无卡顿
  - 图片懒加载正常
  - 无内容闪烁
- **标签**: `@landing`, `@P2`, `@ux`

#### TC-LANDING-015: 按钮悬停效果验证
- **优先级**: P2
- **前置条件**: 在首页（桌面视口）
- **测试步骤**:
  1. 将鼠标悬停在"Create Workflow"按钮上
  2. 截图：悬停状态
  3. 验证按钮样式变化（颜色、阴影等）
  4. 对所有按钮重复测试
- **预期结果**: 
  - 按钮有明显的hover效果
  - 样式变化平滑
- **标签**: `@landing`, `@P2`, `@ui`

---

### 2.5 性能测试 - P2

#### TC-LANDING-016: 页面加载性能验证
- **优先级**: P2
- **前置条件**: 清除浏览器缓存
- **测试步骤**:
  1. 记录开始时间
  2. 访问首页
  3. 等待页面完全加载
  4. 记录加载时间
  5. 检查Network面板
- **预期结果**: 
  - 首次加载时间 < 3秒
  - 总资源大小合理（< 5MB）
  - 图片已优化
- **标签**: `@landing`, `@P2`, `@performance`

#### TC-LANDING-017: 图片加载验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 检查Dashboard展示图是否加载
  2. 验证图片尺寸适配
  3. 验证图片清晰度
- **预期结果**: 
  - 图片加载成功
  - 图片清晰无模糊
  - 图片不超出容器边界
- **标签**: `@landing`, `@P2`, `@ui`

---

### 2.6 内容测试 - P1

#### TC-LANDING-018: 文案内容验证
- **优先级**: P1
- **前置条件**: 在首页
- **测试步骤**:
  1. 截图：完整页面
  2. 验证主标题："Aevatar Station"
  3. 验证副标题："Distributed AI Platform"
  4. 验证描述文本完整且无拼写错误
  5. 验证平台介绍标题："Enterprise-Grade AI Agent Platform"
- **预期结果**: 
  - 所有文案正确无误
  - 无拼写或语法错误
  - 文本清晰易读
- **标签**: `@landing`, `@P1`, `@content`

---

### 2.7 安全测试 - P2

#### TC-LANDING-019: HTTPS验证
- **优先级**: P2
- **前置条件**: 无
- **测试步骤**:
  1. 访问首页
  2. 检查URL协议
  3. 验证SSL证书有效性
- **预期结果**: 
  - 使用HTTPS协议
  - 证书有效（或测试环境自签名）
- **标签**: `@landing`, `@P2`, `@security`

#### TC-LANDING-020: 外部链接安全属性验证
- **优先级**: P2
- **前置条件**: 在首页
- **测试步骤**:
  1. 检查GitHub链接
  2. 验证链接包含`rel="noopener noreferrer"`属性
- **预期结果**: 外部链接有安全属性，防止window.opener攻击
- **标签**: `@landing`, `@P2`, `@security`

---

## 3. 测试执行策略

### 3.1 测试环境
- **浏览器**: Chromium (Playwright)
- **分辨率**: 1920x1080、768x1024、375x667
- **测试服务器**: `https://localhost:3000`

### 3.2 测试执行顺序
1. P0功能测试（核心导航流程）
2. P1 UI测试（用户界面）
3. P2响应式测试（多视口）
4. P2性能测试（加载性能）

### 3.3 测试通过标准
- P0功能测试通过率：100%
- P1测试通过率：100%
- P2测试通过率：≥90%

---

## 4. 测试交付物

### 4.1 测试文档
- ✅ 测试计划（本文档）
- ⏳ Page Object: `tests/aevatar_station/pages/landing_page.py`（需增强）
- ⏳ 测试脚本: `tests/aevatar_station/test_landing_page.py`

### 4.2 测试报告
- Allure HTML报告
- 测试截图（存储在`screenshots/`目录）
- 性能测试数据

---

**文档版本**: v1.0  
**创建日期**: 2025-01-06  
**作者**: HyperEcho AI Testing Team

