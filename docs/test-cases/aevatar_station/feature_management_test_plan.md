# Feature Management 页面测试计划

## 页面信息

**测试页面**: Feature Management Tab  
**URL**: `https://localhost:3000/admin/settings/feature-management`  
**测试目的**: 验证ABP功能管理模块的正确性，包括功能开关、对话框交互等

---

## 测试范围

### 功能模块

1. **Tab导航**
   - Feature Management Tab访问
   - Tab激活状态验证

2. **功能管理主界面**
   - 功能管理描述文本
   - "Manage Host Features"按钮

3. **Features对话框**
   - 对话框打开/关闭
   - 功能列表显示
   - 空状态提示
   - 保存/取消按钮

4. **功能开关（如果有定义的Features）**
   - Toggle开关切换
   - 配额设置
   - 数据保存和持久化

---

## 测试用例

### TC-FEATURE-001: 验证Feature Management页面加载

**优先级**: P0  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问 `/admin/settings/feature-management` 页面
2. 等待页面加载完成
3. 验证Feature Management Tab处于激活状态
4. 截图：页面初始加载

**预期结果**:
- 页面成功加载
- Tab正确高亮
- 页面内容可见

---

### TC-FEATURE-002: 验证功能管理描述文本

**优先级**: P1  
**前置条件**: 用户已访问Feature Management页面  

**测试步骤**:
1. 定位页面描述文本
2. 验证文本内容
3. 截图：描述文本

**预期结果**:
- 显示功能管理说明
- 文本内容清晰准确
- 提示用户点击按钮管理功能

---

### TC-FEATURE-003: 验证"Manage Host Features"按钮

**优先级**: P0  
**前置条件**: 用户已访问Feature Management页面  

**测试步骤**:
1. 定位 "Manage Host Features" 按钮
2. 验证按钮可见且可点击
3. 截图：按钮状态

**预期结果**:
- 按钮正确显示
- 按钮可交互
- 按钮样式正确

---

### TC-FEATURE-004: 验证Features对话框打开

**优先级**: P0  
**前置条件**: 用户已访问Feature Management页面  

**测试步骤**:
1. 截图：点击前状态
2. 点击 "Manage Host Features" 按钮
3. 等待对话框出现
4. 验证对话框标题
5. 截图：对话框已打开

**预期结果**:
- 对话框成功打开
- 对话框标题为 "Features"
- 对话框内容可见
- 背景遮罩出现

---

### TC-FEATURE-005: 验证空功能列表提示

**优先级**: P1  
**前置条件**: 系统未定义任何Feature，对话框已打开  

**测试步骤**:
1. 在Features对话框中查找提示文本
2. 验证显示 "There isn't any available feature."
3. 截图：空功能提示

**预期结果**:
- 显示空状态提示
- 文本准确清晰
- 提示用户当前无可用功能

---

### TC-FEATURE-006: 验证对话框取消按钮

**优先级**: P1  
**前置条件**: Features对话框已打开  

**测试步骤**:
1. 定位 "Cancel" 按钮
2. 截图：按钮状态
3. 点击 "Cancel" 按钮
4. 验证对话框关闭
5. 截图：对话框已关闭

**预期结果**:
- Cancel按钮可点击
- 点击后对话框关闭
- 回到Feature Management页面
- 无数据保存

---

### TC-FEATURE-007: 验证对话框关闭按钮（X）

**优先级**: P1  
**前置条件**: Features对话框已打开  

**测试步骤**:
1. 定位对话框右上角关闭按钮（X）
2. 截图：关闭按钮
3. 点击关闭按钮
4. 验证对话框关闭
5. 截图：对话框已关闭

**预期结果**:
- 关闭按钮可见
- 点击后对话框关闭
- 功能与Cancel相同

---

### TC-FEATURE-008: 验证ESC键关闭对话框

**优先级**: P2  
**前置条件**: Features对话框已打开  

**测试步骤**:
1. 按下ESC键
2. 验证对话框关闭
3. 截图：对话框关闭后

**预期结果**:
- ESC键可关闭对话框
- 回到主页面
- 交互流畅

---

### TC-FEATURE-009: 验证对话框Save按钮（空功能）

**优先级**: P2  
**前置条件**: Features对话框已打开，无可用功能  

**测试步骤**:
1. 定位 "Save" 按钮
2. 验证按钮状态
3. 点击 "Save" 按钮
4. 验证行为
5. 截图：点击Save后

**预期结果**:
- Save按钮可见
- 点击后对话框关闭（无功能可保存）
- 或显示相应提示

---

### TC-FEATURE-010: 验证从Settings Tab访问Feature Management

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 访问 `/admin/settings` (Emailing Tab)
2. 截图：Emailing Tab
3. 点击 "Feature Management" Tab
4. 验证URL变化
5. 验证页面内容
6. 截图：Feature Management页面

**预期结果**:
- URL更新为 `/admin/settings/feature-management`
- Feature Management内容正确显示
- Tab导航流畅

---

### TC-FEATURE-011: 验证页面刷新保持状态

**优先级**: P2  
**前置条件**: 用户已访问Feature Management页面  

**测试步骤**:
1. 确认在Feature Management页面
2. 截图：刷新前
3. 刷新页面
4. 验证仍在Feature Management Tab
5. 截图：刷新后

**预期结果**:
- 刷新后保持在Feature Management Tab
- 页面内容正确显示
- URL保持不变

---

### TC-FEATURE-012: 验证对话框外部点击关闭

**优先级**: P2  
**前置条件**: Features对话框已打开  

**测试步骤**:
1. 截图：对话框打开状态
2. 点击对话框外部区域（遮罩层）
3. 验证对话框是否关闭
4. 截图：点击后状态

**预期结果**:
- 根据设计决定：
  - 方案A：对话框关闭（常见行为）
  - 方案B：对话框保持打开（防误触）

---

### TC-FEATURE-013: 验证对话框层级（Z-index）

**优先级**: P2  
**前置条件**: Features对话框已打开  

**测试步骤**:
1. 打开Features对话框
2. 验证对话框在最上层
3. 验证背景遮罩可见
4. 验证主页面内容被遮挡
5. 截图：对话框层级

**预期结果**:
- 对话框在最上层显示
- 背景遮罩半透明
- 聚焦在对话框上
- 无法点击背景元素

---

### TC-FEATURE-014: 验证多次打开关闭对话框

**优先级**: P2  
**前置条件**: 用户已访问Feature Management页面  

**测试步骤**:
1. 打开Features对话框
2. 关闭对话框
3. 再次打开
4. 再次关闭
5. 重复3次
6. 截图：最后状态

**预期结果**:
- 对话框可多次打开/关闭
- 无性能问题
- 无UI异常
- 交互流畅

---

## 扩展测试用例（功能启用后）

### TC-FEATURE-015: 验证功能开关切换

**优先级**: P0  
**前置条件**: 系统已定义Features，对话框已打开  

**测试步骤**:
1. 定位功能列表
2. 找到某个功能的Toggle开关
3. 切换开关状态
4. 截图：开关切换
5. 点击Save保存
6. 刷新验证状态保持

**预期结果**:
- 开关正常切换
- 状态正确保存
- 刷新后保持不变

---

### TC-FEATURE-016: 验证功能配额设置

**优先级**: P1  
**前置条件**: 系统有配额类型的Feature  

**测试步骤**:
1. 找到配额输入框
2. 输入配额值（如 100）
3. 保存配置
4. 刷新验证
5. 截图：配额设置

**预期结果**:
- 配额值正确保存
- 数值验证正确
- 数据持久化

---

## 测试数据

### 测试用户
```json
{
  "username": "haylee2",
  "password": "Wh520520!",
  "role": "Host Admin"
}
```

### Features示例（当系统定义Features后）
```json
{
  "features": [
    {
      "name": "Aevatar.Workflow",
      "displayName": "AI Workflow",
      "type": "toggle",
      "defaultValue": false
    },
    {
      "name": "Aevatar.StorageQuota",
      "displayName": "Storage Quota (GB)",
      "type": "numeric",
      "defaultValue": 100
    }
  ]
}
```

---

## 非功能测试

### UI/UX测试
- **对话框动画**: 打开/关闭流畅
- **按钮反馈**: 点击有视觉反馈
- **焦点管理**: 对话框打开后焦点在对话框内
- **键盘导航**: Tab键可在对话框内导航

### 性能测试
- **对话框打开时间**: < 500ms
- **功能列表加载**: < 1秒
- **保存操作**: < 2秒

### 兼容性测试
- **不同租户**: Host vs Tenant权限
- **不同角色**: Admin vs 普通用户
- **无功能场景**: 空列表正确显示

---

## 测试环境

- **测试环境**: https://localhost:3000
- **后端服务**: https://localhost:44320
- **浏览器**: Chromium (Playwright)
- **分辨率**: 1920x1080

---

## 缺陷严重级别定义

- **Blocker**: 对话框无法打开，页面崩溃
- **Critical**: 功能开关不工作，数据无法保存
- **Major**: 对话框无法关闭，UI显示异常
- **Minor**: 动画卡顿，文案错误
- **Trivial**: 样式细节问题

---

## 测试执行记录

| 用例编号 | 用例标题 | 执行结果 | 执行人 | 执行时间 | 备注 |
|---------|---------|---------|-------|---------|------|
| TC-FEATURE-001 | 验证Feature Management页面加载 | | | | |
| TC-FEATURE-002 | 验证功能管理描述文本 | | | | |
| TC-FEATURE-003 | 验证"Manage Host Features"按钮 | | | | |

---

## 附录

### ABP Feature Management概念

#### 功能类型
- **Toggle**: 布尔值开关（启用/禁用）
- **Numeric**: 数值型（配额、限制）
- **Free Text**: 自由文本

#### 功能层级
- **Global**: 全局默认值
- **Host**: 宿主层设置
- **Tenant**: 租户层设置
- **User**: 用户层设置

### 关键截图说明

1. **feature_mgmt_initial.png**: 页面初始状态
2. **feature_mgmt_button.png**: Manage Host Features按钮
3. **feature_mgmt_dialog_open.png**: 对话框打开
4. **feature_mgmt_empty_state.png**: 空功能列表提示
5. **feature_mgmt_dialog_close.png**: 对话框关闭
6. **feature_mgmt_tab_switch.png**: Tab切换
7. **feature_mgmt_after_refresh.png**: 刷新后状态

---

**文档版本**: 1.0  
**创建日期**: 2025-12-02  
**最后更新**: 2025-12-02  
**创建人**: Test Team

