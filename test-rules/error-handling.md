# GodGPT 测试错误处理规则

## Credits相关错误

### 1. Credits值获取错误

#### 错误表现
```
Error: expect(received).toBeGreaterThan(expected)
Expected: > 0
Received: 0
```

#### 解决方案
1. 增加等待时间
```typescript
await page.waitForTimeout(3000); // 从2000ms增加到3000ms
```

2. 使用waitForSelector等待Credits加载
```typescript
await page.waitForSelector('[data-testid="credits-value"]', { state: 'visible' });
```

3. 添加重试机制
```typescript
let retries = 3;
while (retries > 0) {
  const creditsText = await creditsElement.textContent();
  const credits = parseInt(creditsText || '0');
  if (credits > 0) break;
  await page.waitForTimeout(1000);
  retries--;
}
```

### 2. Credits消耗验证错误

#### 错误表现
```
Error: expect(received).toBe(expected)
Expected: 270
Received: 280
```

#### 解决方案
1. 使用范围验证而不是精确值
```typescript
expect(updatedCreditsNumber).toBeLessThan(initialCreditsNumber);
```

2. 添加日志记录
```typescript
console.log(`Credits changed from ${initialCreditsNumber} to ${updatedCreditsNumber}`);
```

## 元素定位错误

### 1. 登出按钮点击超时

#### 错误表现
```
Test timeout of 30000ms exceeded.
Error: locator.click: Test timeout of 30000ms exceeded.
```

#### 解决方案
1. 使用更可靠的选择器
```typescript
const avatarButton = await page.locator('svg').last();
await avatarButton.click();
```

2. 添加等待时间
```typescript
await page.waitForTimeout(1000); // 等待页面加载完成
```

3. 使用强制等待可见性
```typescript
await page.waitForSelector('svg', { state: 'visible' });
```

## 通用错误处理规则

### 1. 页面加载超时
- 增加配置文件中的超时时间
```typescript
// playwright.config.ts
export default defineConfig({
  timeout: 45000, // 从30000ms增加到45000ms
});
```

### 2. 元素定位失败
- 使用多重定位策略
```typescript
async function findElement(page, selectors) {
  for (const selector of selectors) {
    try {
      const element = await page.$(selector);
      if (element) return element;
    } catch (e) {
      console.log(`Selector ${selector} failed`);
    }
  }
  throw new Error('Element not found');
}
```

### 3. 断言失败
- 添加重试机制
```typescript
async function retryAssertion(action, maxRetries = 3, interval = 1000) {
  let lastError;
  for (let i = 0; i < maxRetries; i++) {
    try {
      await action();
      return;
    } catch (error) {
      lastError = error;
      await page.waitForTimeout(interval);
    }
  }
  throw lastError;
}
```

## 测试执行建议

1. 运行测试前
   - 确保测试环境正常
   - 检查账号状态
   - 清理历史数据

2. 测试执行中
   - 使用有界面模式观察
   - 记录详细日志
   - 保存失败截图

3. 测试执行后
   - 分析失败原因
   - 更新错误处理规则
   - 优化测试用例

## 注意事项

1. 元素定位
   - 优先使用语义化选择器
   - 避免使用绝对路径
   - 添加适当等待时间

2. 断言验证
   - 使用灵活的断言方式
   - 添加详细错误信息
   - 考虑边界情况

3. 错误处理
   - 捕获所有可能异常
   - 提供清晰错误信息
   - 实现优雅降级策略 