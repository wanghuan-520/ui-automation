# Dashboard 页面测试计划

## 页面信息

**测试页面**: Dashboard (ABP管理后台首页)  
**URL**: `https://localhost:3000/admin`  
**测试目的**: 验证Dashboard页面的信息展示、状态显示和用户体验

---

## 测试范围

### 功能模块

1. **欢迎区域**
   - 个性化问候
   - 用户名显示
   - Host标识

2. **用户信息卡片**
   - 头像显示
   - 个人信息（姓名、邮箱、用户名）
   - 认证状态
   - 验证状态（邮箱、手机）

3. **系统状态卡片组**
   - Multi-tenancy状态
   - Current Tenant信息
   - Session状态

4. **系统配置卡片**
   - Localization配置
   - Timing配置
   - Features配置

---

## 测试用例

### TC-DASH-001: 验证Dashboard页面加载

**优先级**: P0  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问 `/admin` 页面
2. 等待页面加载完成
3. 验证页面标题
4. 截图：页面加载完成

**预期结果**:
- 页面成功加载
- URL正确
- 页面标题为 "Aevatar Station"
- 主要内容区域可见

---

### TC-DASH-002: 验证欢迎信息显示

**优先级**: P1  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 查找欢迎标题元素
3. 验证包含用户名称
4. 验证系统提示文本
5. 截图：欢迎区域

**预期结果**:
- 显示 "Welcome back, {用户名}"
- 显示系统提示信息
- Host标识显示（如果是Host用户）

---

### TC-DASH-003: 验证用户信息卡片

**优先级**: P0  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位 "User Profile" 卡片
3. 验证卡片标题和副标题
4. 验证头像显示
5. 验证姓名、邮箱、用户名
6. 验证认证状态徽章
7. 截图：用户信息卡片

**预期结果**:
- 卡片标题显示 "User Profile"
- 头像正确显示
- 个人信息完整展示
- 认证状态显示 "Authenticated"

---

### TC-DASH-004: 验证邮箱验证状态

**优先级**: P1  
**前置条件**: 用户已登录，邮箱未验证  

**测试步骤**:
1. 访问Dashboard页面
2. 定位邮箱验证状态区域
3. 验证显示 "Not Verified"
4. 验证红色×图标
5. 截图：验证状态

**预期结果**:
- 显示 "Email Verification"
- 状态为 "Not Verified"
- 红色图标表示未验证

---

### TC-DASH-005: 验证手机验证状态

**优先级**: P1  
**前置条件**: 用户已登录，手机未验证  

**测试步骤**:
1. 访问Dashboard页面
2. 定位手机验证状态区域
3. 验证显示 "Not Verified"
4. 验证红色×图标
5. 截图：验证状态

**预期结果**:
- 显示 "Phone Verification"
- 状态为 "Not Verified"
- 红色图标表示未验证

---

### TC-DASH-006: 验证Multi-tenancy状态卡片

**优先级**: P1  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位Multi-tenancy卡片
3. 验证卡片标题
4. 验证状态显示
5. 验证说明文本
6. 截图：Multi-tenancy卡片

**预期结果**:
- 卡片标题显示 "Multi-tenancy"
- 状态显示（Enabled或Disabled）
- 显示对应的说明文本

---

### TC-DASH-007: 验证Current Tenant卡片

**优先级**: P1  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位Current Tenant卡片
3. 验证卡片标题
4. 验证租户信息显示
5. 截图：Current Tenant卡片

**预期结果**:
- 卡片标题显示 "Current Tenant"
- Host用户显示 "Host"
- 租户用户显示租户名称

---

### TC-DASH-008: 验证Session状态卡片

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位Session卡片
3. 验证卡片标题
4. 验证会话状态显示
5. 截图：Session卡片

**预期结果**:
- 卡片标题显示 "Session"
- 显示会话状态或 "No Session"

---

### TC-DASH-009: 验证Localization配置信息

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位System Configuration卡片
3. 查找Localization部分
4. 验证Current Culture显示
5. 验证Default Resource显示
6. 截图：Localization配置

**预期结果**:
- 显示当前文化设置
- 显示默认资源名称
- 信息格式正确

---

### TC-DASH-010: 验证Timing配置信息

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位System Configuration卡片
3. 查找Timing部分
4. 验证Time Zone显示
5. 验证Clock Kind显示
6. 截图：Timing配置

**预期结果**:
- 显示时区配置
- 显示时钟类型
- 信息格式正确

---

### TC-DASH-011: 验证Features配置信息

**优先级**: P1  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 定位System Configuration卡片
3. 查找Features部分
4. 验证启用的功能数量
5. 截图：Features配置

**预期结果**:
- 显示 "Enabled Features: N"
- 数字正确（当前为0）

---

### TC-DASH-012: 验证页面响应式布局

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 以1920x1080分辨率访问页面
2. 验证卡片布局（3列）
3. 截图：大屏布局
4. 调整窗口到768px宽度
5. 验证卡片自适应
6. 截图：中屏布局

**预期结果**:
- 大屏：3列布局
- 中屏：2列或单列布局
- 所有元素可见且对齐

---

### TC-DASH-013: 验证侧边栏导航高亮

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 检查侧边栏 "Home" 菜单项
3. 验证高亮状态
4. 截图：侧边栏高亮

**预期结果**:
- "Home" 菜单项处于选中/高亮状态
- 视觉上与其他菜单项有区别

---

### TC-DASH-014: 验证Dashboard数据刷新

**优先级**: P2  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问Dashboard页面
2. 记录当前显示的数据
3. 刷新页面
4. 验证数据保持一致
5. 截图：刷新后页面

**预期结果**:
- 页面刷新成功
- 所有数据保持一致
- 无加载错误

---

## 测试数据

### 用户数据
```json
{
  "username": "haylee2",
  "password": "Wh520520!",
  "expected_name": "李明",
  "expected_surname": "Wang",
  "expected_email": "modified_175005@test.com"
}
```

---

## 非功能测试

### 性能测试
- **页面加载时间**: < 3秒
- **API响应时间**: < 1秒
- **截图操作**: 不影响测试流程

### 兼容性测试
- **浏览器**: Chrome 120+, Firefox, Safari, Edge
- **分辨率**: 1920x1080, 1366x768, 768x1024

---

## 测试环境

- **测试环境**: https://localhost:3000
- **后端服务**: https://localhost:44320
- **数据库**: 测试数据库
- **浏览器**: Chromium (Playwright)

---

## 缺陷严重级别定义

- **Blocker**: 页面无法加载，核心信息无法显示
- **Critical**: 用户信息显示错误，状态信息不准确
- **Major**: 配置信息缺失，布局错乱
- **Minor**: 文本对齐问题，图标显示异常
- **Trivial**: 拼写错误，样式细节

---

## 测试执行记录

| 用例编号 | 用例标题 | 执行结果 | 执行人 | 执行时间 | 备注 |
|---------|---------|---------|-------|---------|------|
| TC-DASH-001 | 验证Dashboard页面加载 | | | | |
| TC-DASH-002 | 验证欢迎信息显示 | | | | |
| TC-DASH-003 | 验证用户信息卡片 | | | | |

---

## 附录

### 关键截图说明

1. **dashboard_initial_load.png**: 页面初始加载完成
2. **dashboard_welcome_area.png**: 欢迎区域特写
3. **dashboard_user_profile_card.png**: 用户信息卡片
4. **dashboard_verification_status.png**: 验证状态
5. **dashboard_system_status_cards.png**: 系统状态卡片组
6. **dashboard_system_configuration.png**: 系统配置卡片
7. **dashboard_responsive_layout.png**: 响应式布局

---

**文档版本**: 1.0  
**创建日期**: 2025-12-02  
**最后更新**: 2025-12-02  
**创建人**: Test Team

