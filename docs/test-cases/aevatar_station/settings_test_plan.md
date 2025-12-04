# Settings (Emailing) 页面测试计划

## 页面信息

**测试页面**: Settings - Emailing Tab  
**URL**: `https://localhost:3000/admin/settings`  
**测试目的**: 验证SMTP邮件配置功能的正确性和数据持久化

---

## 测试范围

### 功能模块

1. **Tab导航**
   - Emailing Tab
   - Feature Management Tab

2. **SMTP配置表单**
   - 基础配置（Display Name, From Address）
   - 服务器配置（Host, Port）
   - 安全选项（SSL, Default Credentials）
   - 认证信息（Domain, Username, Password）

3. **数据验证**
   - 必填字段校验
   - 格式验证（Email, Port）
   - 边界值测试

4. **数据持久化**
   - 配置保存
   - 页面刷新后验证

---

## 测试用例

### TC-SETTINGS-001: 验证Settings页面加载

**优先级**: P0  
**前置条件**: 用户已登录系统  

**测试步骤**:
1. 访问 `/admin/settings` 页面
2. 等待页面加载完成
3. 验证Emailing Tab处于激活状态
4. 截图：页面初始加载

**预期结果**:
- 页面成功加载
- Emailing Tab高亮显示
- 表单字段全部可见

---

### TC-SETTINGS-002: 验证Tab切换功能

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 点击 "Feature Management" Tab
2. 验证切换成功
3. 截图：Feature Management Tab
4. 点击 "Emailing" Tab
5. 验证切换回Emailing
6. 截图：Emailing Tab

**预期结果**:
- Tab切换流畅
- 内容正确切换
- 选中状态正确显示

---

### TC-SETTINGS-003: 验证所有表单字段显示

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 定位所有表单字段
2. 验证以下字段可见：
   - Default from display name
   - Default from address
   - Host
   - Port
   - Enable SSL checkbox
   - Use default credentials checkbox
   - Domain
   - User name
   - Password
3. 截图：完整表单

**预期结果**:
- 所有9个表单字段可见
- 字段标签正确显示
- 输入框可交互

---

### TC-SETTINGS-004: 验证SMTP配置保存（Gmail）

**优先级**: P0  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 填写Gmail SMTP配置：
   - Display Name: "Aevatar System"
   - From Address: "noreply@aevatar.ai"
   - Host: "smtp.gmail.com"
   - Port: 587
   - Enable SSL: 勾选
   - Username: "test@gmail.com"
   - Password: "app_password_here"
2. 截图：填写完成
3. 点击保存按钮（如果有）或触发保存
4. 等待保存完成
5. 截图：保存成功

**预期结果**:
- 数据成功保存
- 显示成功消息（如果有）
- 无错误提示

---

### TC-SETTINGS-005: 验证配置数据持久化

**优先级**: P0  
**前置条件**: 已保存SMTP配置  

**测试步骤**:
1. 记录当前配置数据
2. 刷新页面
3. 验证所有字段值保持一致
4. 截图：刷新后页面

**预期结果**:
- 刷新后配置保持不变
- 所有字段值正确显示
- 密码字段显示为masked

---

### TC-SETTINGS-006: 验证From Address格式校验

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 在From Address输入无效邮箱：
   - "invalidemail"
   - "test@"
   - "@example.com"
2. 尝试保存或失焦触发验证
3. 验证错误提示
4. 截图：错误提示

**预期结果**:
- 显示邮箱格式错误提示
- 无法保存无效配置
- 错误提示清晰明确

---

### TC-SETTINGS-007: 验证Port端口号范围校验

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 测试边界值：
   - 输入 0（无效）
   - 输入 1（最小有效值）
   - 输入 587（常用值）
   - 输入 65535（最大有效值）
   - 输入 70000（无效）
2. 验证每个值的校验结果
3. 截图：边界值测试

**预期结果**:
- 0和70000显示错误
- 1和65535允许输入
- 587正常使用
- 错误提示准确

---

### TC-SETTINGS-008: 验证Enable SSL开关功能

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 勾选 "Enable SSL"
2. 验证checkbox状态
3. 截图：SSL已启用
4. 取消勾选
5. 验证checkbox状态
6. 截图：SSL已禁用

**预期结果**:
- checkbox响应正常
- 状态切换流畅
- 保存后状态保持

---

### TC-SETTINGS-009: 验证Use Default Credentials开关

**优先级**: P2  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 勾选 "Use default credentials"
2. 验证checkbox状态
3. 观察是否影响认证字段
4. 截图：功能状态
5. 取消勾选
6. 验证恢复正常

**预期结果**:
- checkbox正常工作
- 状态正确保存
- 功能符合预期

---

### TC-SETTINGS-010: 验证密码字段安全性

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 在Password字段输入密码
2. 验证显示为 ••••••
3. 保存配置
4. 刷新页面
5. 验证密码仍为masked
6. 截图：密码安全显示

**预期结果**:
- 密码输入时masked
- 保存后密码加密存储
- 刷新后不显示明文
- 安全性得到保障

---

### TC-SETTINGS-011: 验证Office 365配置

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 填写Office 365配置：
   - Host: "smtp.office365.com"
   - Port: 587
   - Enable SSL: 勾选
   - From Address: "admin@company.com"
   - Username: "admin@company.com"
   - Password: "secure_password"
2. 保存配置
3. 刷新验证
4. 截图：Office 365配置

**预期结果**:
- Office 365配置正确保存
- 数据持久化正常
- 所有字段正确显示

---

### TC-SETTINGS-012: 验证清空配置功能

**优先级**: P2  
**前置条件**: 已有保存的配置  

**测试步骤**:
1. 清空所有必填字段
2. 尝试保存
3. 验证必填字段提示
4. 截图：必填字段提示

**预期结果**:
- 必填字段显示错误提示
- 无法保存空配置
- 原有配置保持不变

---

### TC-SETTINGS-013: 验证Host字段输入

**优先级**: P1  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 测试不同格式的Host：
   - "smtp.gmail.com"（域名）
   - "192.168.1.100"（IP地址）
   - "localhost"（本地）
2. 保存并验证
3. 截图：不同格式

**预期结果**:
- 域名格式正常保存
- IP地址格式支持
- localhost支持
- 所有格式都能正确使用

---

### TC-SETTINGS-014: 验证Domain字段（可选）

**优先级**: P2  
**前置条件**: 用户已访问Settings页面  

**测试步骤**:
1. 留空Domain字段
2. 配置其他必填项
3. 保存配置
4. 验证保存成功
5. 填写Domain: "company.local"
6. 保存并验证
7. 截图：Domain配置

**预期结果**:
- Domain为可选字段
- 留空时正常保存
- 填写时正确保存
- Windows域认证场景支持

---

### TC-SETTINGS-015: 验证配置修改覆盖

**优先级**: P1  
**前置条件**: 已有保存的Gmail配置  

**测试步骤**:
1. 记录当前Gmail配置
2. 修改为Office 365配置
3. 保存
4. 刷新验证新配置
5. 截图：配置已更新

**预期结果**:
- 新配置覆盖旧配置
- 数据正确更新
- 无残留旧数据

---

## 测试数据

### Gmail配置
```json
{
  "display_name": "Aevatar System",
  "from_address": "noreply@aevatar.ai",
  "host": "smtp.gmail.com",
  "port": 587,
  "enable_ssl": true,
  "username": "test@gmail.com",
  "password": "app_password_here"
}
```

### Office 365配置
```json
{
  "display_name": "Company Notification",
  "from_address": "noreply@company.com",
  "host": "smtp.office365.com",
  "port": 587,
  "enable_ssl": true,
  "username": "admin@company.com",
  "password": "secure_password"
}
```

### 无效测试数据
```json
{
  "invalid_email": [
    "invalidemail",
    "test@",
    "@example.com",
    "test@.com"
  ],
  "invalid_port": [0, -1, 70000, 99999],
  "valid_port_boundary": [1, 25, 587, 465, 65535]
}
```

---

## 非功能测试

### 性能测试
- **表单提交时间**: < 2秒
- **配置加载时间**: < 1秒
- **页面刷新时间**: < 3秒

### 安全测试
- **密码加密**: 密码不以明文存储
- **密码显示**: 界面上显示为masked
- **SQL注入**: 特殊字符正确处理
- **XSS防护**: HTML标签正确转义

### 兼容性测试
- **SMTP服务器**: Gmail, Office 365, 自建服务器
- **认证方式**: 用户名密码, 默认凭据, Windows域
- **端口范围**: 25, 465, 587, 自定义

---

## 测试环境

- **测试环境**: https://localhost:3000
- **后端服务**: https://localhost:44320
- **SMTP测试**: 模拟SMTP服务器或真实配置
- **浏览器**: Chromium (Playwright)

---

## 缺陷严重级别定义

- **Blocker**: 页面无法加载，配置无法保存
- **Critical**: 数据丢失，密码明文显示
- **Major**: 验证不正确，数据不持久化
- **Minor**: 提示信息不清晰，布局小问题
- **Trivial**: 文案错误，样式细节

---

## 测试执行记录

| 用例编号 | 用例标题 | 执行结果 | 执行人 | 执行时间 | 备注 |
|---------|---------|---------|-------|---------|------|
| TC-SETTINGS-001 | 验证Settings页面加载 | | | | |
| TC-SETTINGS-002 | 验证Tab切换功能 | | | | |
| TC-SETTINGS-003 | 验证所有表单字段显示 | | | | |

---

## 附录

### SMTP常用配置参考

| 服务商 | Host | Port | SSL |
|-------|------|------|-----|
| Gmail | smtp.gmail.com | 587 | TLS |
| Gmail | smtp.gmail.com | 465 | SSL |
| Office 365 | smtp.office365.com | 587 | TLS |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| QQ邮箱 | smtp.qq.com | 587 | TLS |
| 163邮箱 | smtp.163.com | 465 | SSL |
| 自建 | mail.company.com | 25/587 | - |

### 关键截图说明

1. **settings_initial_load.png**: 页面初始加载
2. **settings_emailing_form.png**: Emailing表单完整视图
3. **settings_filled_form.png**: 填写完整配置
4. **settings_save_success.png**: 保存成功状态
5. **settings_after_refresh.png**: 刷新后验证持久化
6. **settings_validation_error.png**: 验证错误提示
7. **settings_tab_switch.png**: Tab切换功能

---

**文档版本**: 1.0  
**创建日期**: 2025-12-02  
**最后更新**: 2025-12-02  
**创建人**: Test Team

