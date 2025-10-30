# GodGPT 自动化测试套件

## 概述

本测试套件包含了 GodGPT 项目的完整自动化测试，主要覆盖用户注册、登录、Credits管理和消息功能等核心业务流程。

## 文件说明

### 测试文件
- `credits.spec.ts` - Credits功能基础测试
- `credits-test-suite.ts` - Credits功能完整测试套件
- `check-login-status.ts` - 登录状态检查和登出功能

### 辅助工具
- `../utils/test-helpers.ts` - 测试辅助函数库

## 测试覆盖范围

### Credits功能测试

#### 1. 新用户额度测试
- **测试目标**: 验证新用户注册后获得正确的初始Credits
- **测试步骤**:
  - 导航到GodGPT测试环境
  - 执行邮箱注册流程
  - 验证初始Credits为320
  - 执行登出操作

#### 2. Credits消耗测试
- **测试目标**: 验证发送消息时Credits正确扣除
- **测试步骤**:
  - 使用现有账号登录
  - 记录初始Credits数量
  - 发送测试消息
  - 验证Credits减少
  - 执行登出操作

#### 3. Credits不足处理测试
- **测试目标**: 验证Credits为0时的系统行为
- **测试步骤**:
  - 使用Credits为0的测试账号
  - 尝试发送消息
  - 验证系统提示Credits不足
  - 验证消息发送被阻止

### 登录状态管理

#### 登录状态检查
- **功能**: 自动检测当前登录状态
- **用途**: 为其他测试提供干净的测试环境
- **实现**: `checkAndLogout()` 函数

## 测试账号配置

### 标准测试账号
- **邮箱**: `playwright@teml.net`
- **密码**: `Wh520520!`
- **用途**: 基础功能测试

### 新用户测试账号
- **邮箱**: `playwright5@teml.net`, `playwright7@teml.net`
- **密码**: `Wh520520!`
- **用途**: 新用户注册测试

### 零Credits测试账号
- **邮箱**: `playwright-zero@teml.net`
- **密码**: `Wh520520!`
- **用途**: Credits不足场景测试

## 运行方式

### 运行所有GodGPT测试

```bash
# 运行整个godgpt目录的测试
npx playwright test tests/godgpt/

# 显示浏览器窗口运行
npx playwright test tests/godgpt/ --headed
```

### 运行特定测试文件

```bash
# 运行Credits基础测试
npx playwright test tests/godgpt/credits.spec.ts

# 运行完整测试套件
npx playwright test tests/godgpt/credits-test-suite.ts

# 运行登录状态检查
npx playwright test tests/godgpt/check-login-status.ts
```

### 运行特定测试用例

```bash
# 运行新用户额度测试
npx playwright test tests/godgpt/credits-test-suite.ts -g "新用户额度测试"

# 运行Credits消耗测试
npx playwright test tests/godgpt/credits.spec.ts -g "Credits消耗测试"
```

## 测试环境

### 目标环境
- **URL**: https://godgpt-ui-testnet.aelf.dev/
- **环境类型**: 测试网环境
- **浏览器支持**: Chromium, Firefox, Safari

### 页面元素定位策略

#### Credits显示
```typescript
// 通用Credits元素定位
const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();

// 特定class定位
const creditsElement = page.locator('div[class*="credits"]').first();
```

#### 登录表单
```typescript
// 邮箱输入框
const emailInput = page.locator('input[type="email"]');

// 密码输入框
const passwordInput = page.locator('input[type="password"]');

// 继续按钮
await page.getByText('Continue with Email', { exact: true }).click();
```

#### 消息输入
```typescript
// 消息输入框
const messageInput = page.locator('textarea[placeholder*="Ask"]');
```

## 测试数据管理

### Credits预期值
- **新用户初始Credits**: 320
- **最小消耗Credits**: 根据消息长度和复杂度变化
- **零Credits阈值**: 0

### 测试消息内容
- **标准测试消息**: "Hello, can you help me with a simple task?"
- **零Credits测试消息**: "Test message with zero credits"

## 错误处理和重试机制

### 超时设置
```typescript
// 页面加载超时
await page.waitForTimeout(5000);

// 元素可见性超时
await expect(element).toBeVisible({ timeout: 10000 });

// 网络空闲等待
await page.waitForLoadState('networkidle');
```

### 重试机制
- 使用 `TestHelpers.retryAssertion()` 进行断言重试
- 使用 `TestHelpers.getCreditsWithRetry()` 进行Credits获取重试
- 使用 `TestHelpers.waitForCreditsChange()` 等待Credits变化

## 测试辅助功能

### 登录状态清理
```typescript
// 在测试开始前清理登录状态
await checkAndLogout(page);
```

### 测试步骤分组
```typescript
// 使用test.step进行步骤分组
await test.step('执行登录流程', async () => {
  // 登录相关操作
});
```

## 项目结构

```
tests/godgpt/
├── README.md                    # 本文档
├── credits.spec.ts             # Credits基础测试
├── credits-test-suite.ts       # Credits完整测试套件
└── check-login-status.ts       # 登录状态管理
```

## 故障排除

### 常见问题

1. **Credits元素定位失败**
   - 检查页面是否完全加载
   - 验证Credits显示的DOM结构
   - 尝试不同的选择器策略

2. **登录流程失败**
   - 确认测试账号状态正常
   - 检查网络连接
   - 验证页面元素是否有变化

3. **消息发送失败**
   - 确认消息输入框可用
   - 检查Credits是否足够
   - 验证网络请求是否正常

### 调试技巧

1. **启用详细日志**
   ```bash
   npx playwright test tests/godgpt/ --debug
   ```

2. **截图调试**
   ```typescript
   await page.screenshot({ path: 'debug.png' });
   ```

3. **控制台输出**
   ```typescript
   console.log(`当前Credits: ${credits}`);
   ```

## 维护指南

### 定期检查事项
- 测试账号状态和有效性
- 页面元素选择器的准确性
- Credits计算规则的变化
- 新功能的测试覆盖

### 更新测试用例
- 根据产品功能变更调整测试步骤
- 添加新的边界条件测试
- 优化测试执行效率
- 更新测试数据和预期结果

---

*由 HyperEcho 语言震动体创建 - 2025-09-25*
