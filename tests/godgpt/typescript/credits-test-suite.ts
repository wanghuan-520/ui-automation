import { test, expect } from '@playwright/test';
import { checkAndLogout } from '../check-login-status';

/**
 * 测试套件：Credits功能测试
 */

// 用例1：新用户额度测试
test('新用户额度测试', async ({ page }) => {
  // 前置条件检查
  await test.step('前置条件检查', async () => {
    await page.goto('https://godgpt-ui-testnet.aelf.dev/');
    await checkAndLogout(page);
  });

  // 执行注册流程
  await test.step('执行注册流程', async () => {
    // 点击邮箱输入框
    const emailInput = page.locator('input[type="email"]');
    await emailInput.click();
    await emailInput.fill('playwright5@teml.net');
    
    // 点击继续按钮
    await page.getByText('Continue with Email', { exact: true }).click();
    await page.waitForTimeout(3000);

    // 输入密码
    const passwordInput = page.locator('input[type="password"]');
    await passwordInput.fill('Wh520520!');
    await page.getByText('Continue', { exact: true }).click();
    await page.waitForTimeout(10000);
  });

  // 验证初始额度
  await test.step('验证初始额度', async () => {
    // 等待页面加载完成
    await page.waitForLoadState('networkidle');
    
    // 查找Credits显示
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    await expect(creditsElement).toBeVisible({ timeout: 10000 });
    const creditsText = await creditsElement.textContent();
    expect(parseInt(creditsText || '0')).toBe(320);
  });

  // 登出操作
  await test.step('执行登出', async () => {
    await checkAndLogout(page);
  });
});

// 用例2：Credits消耗测试
test('Credits消耗测试', async ({ page }) => {
  // 前置条件检查
  await test.step('前置条件检查', async () => {
    await page.goto('https://godgpt-ui-testnet.aelf.dev/');
    await checkAndLogout(page);
  });

  // 执行登录流程
  await test.step('执行登录流程', async () => {
    const emailInput = page.locator('input[type="email"]');
    await emailInput.click();
    await emailInput.fill('playwright@teml.net');
    
    await page.getByText('Continue with Email', { exact: true }).click();
    await page.waitForTimeout(3000);

    const passwordInput = page.locator('input[type="password"]');
    await passwordInput.fill('Wh520520!');
    await page.getByText('Continue', { exact: true }).click();
    await page.waitForTimeout(10000);
  });

  let initialCredits: number;
  
  // 记录初始额度
  await test.step('记录初始额度', async () => {
    await page.waitForLoadState('networkidle');
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    await expect(creditsElement).toBeVisible({ timeout: 10000 });
    const creditsText = await creditsElement.textContent();
    initialCredits = parseInt(creditsText || '0');
    console.log(`初始Credits: ${initialCredits}`);
  });

  // 发送消息消耗Credits
  await test.step('发送消息消耗Credits', async () => {
    const messageInput = page.locator('textarea[placeholder*="Ask"]');
    await messageInput.click();
    await messageInput.fill('Hello, can you help me with a simple task?');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(5000);
  });

  // 验证Credits减少
  await test.step('验证Credits减少', async () => {
    await page.waitForTimeout(10000);
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    const updatedCreditsText = await creditsElement.textContent();
    const updatedCredits = parseInt(updatedCreditsText || '0');
    console.log(`更新后Credits: ${updatedCredits}`);
    expect(updatedCredits).toBeLessThan(initialCredits);
  });

  // 登出操作
  await test.step('执行登出', async () => {
    await checkAndLogout(page);
  });
});

// 用例3：Credits不足处理测试
test('Credits不足处理测试', async ({ page }) => {
  // 前置条件检查
  await test.step('前置条件检查', async () => {
    await page.goto('https://godgpt-ui-testnet.aelf.dev/');
    await checkAndLogout(page);
  });

  // 使用Credits为0的账号登录
  await test.step('使用Credits为0的账号登录', async () => {
    const emailInput = page.locator('input[type="email"]');
    await emailInput.click();
    await emailInput.fill('playwright-zero@teml.net');
    
    await page.getByText('Continue with Email', { exact: true }).click();
    await page.waitForTimeout(3000);

    const passwordInput = page.locator('input[type="password"]');
    await passwordInput.fill('Wh520520!');
    await page.getByText('Continue', { exact: true }).click();
    await page.waitForTimeout(10000);
  });

  // 验证Credits为0
  await test.step('验证Credits为0', async () => {
    await page.waitForLoadState('networkidle');
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    await expect(creditsElement).toBeVisible({ timeout: 10000 });
    const creditsText = await creditsElement.textContent();
    expect(parseInt(creditsText || '0')).toBe(0);
  });

  // 尝试发送消息
  await test.step('尝试发送消息', async () => {
    const messageInput = page.locator('textarea[placeholder*="Ask"]');
    await messageInput.click();
    await messageInput.fill('Test message with zero credits');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(3000);
  });

  // 验证Credits不足提示
  await test.step('验证Credits不足提示', async () => {
    // 这里应该验证出现Credits不足的提示信息
    // 具体的选择器需要根据实际页面来调整
    const errorMessage = page.locator('text=insufficient credits').or(page.locator('text=not enough credits'));
    await expect(errorMessage).toBeVisible({ timeout: 5000 });
  });

  // 登出操作
  await test.step('执行登出', async () => {
    await checkAndLogout(page);
  });
});
