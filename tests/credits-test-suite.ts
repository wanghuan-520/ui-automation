import { test, expect } from '@playwright/test';
import { checkAndLogout } from './check-login-status';

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
    // 输入邮箱
    const emailInput = page.locator('input[type="email"]');
    await emailInput.click();
    await emailInput.fill('playwright@teml.net');
    
    // 点击继续按钮
    await page.getByText('Continue with Email', { exact: true }).click();
    await page.waitForTimeout(3000);

    // 输入密码
    const passwordInput = page.locator('input[type="password"]');
    await passwordInput.fill('Wh520520!');
    await page.getByText('Continue', { exact: true }).click();
    await page.waitForTimeout(10000);
  });

  // 记录初始Credits值
  let initialCredits = 0;
  await test.step('记录初始Credits', async () => {
    // 等待页面加载完成
    await page.waitForLoadState('networkidle');
    
    // 查找Credits显示
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    await expect(creditsElement).toBeVisible({ timeout: 10000 });
    const creditsText = await creditsElement.textContent();
    initialCredits = parseInt(creditsText || '0');
    console.log(`初始Credits: ${initialCredits}`);
  });

  // 执行对话操作
  await test.step('执行对话操作', async () => {
    // 等待"What can I help with?"文本出现
    await expect(page.getByText('What can I help with?')).toBeVisible({ timeout: 10000 });
    
    // 等待输入框可用
    const chatInput = page.locator('input').filter({ hasText: /Ask anything/ });
    await expect(chatInput).toBeVisible({ timeout: 10000 });
    await chatInput.click();
    await chatInput.fill('Hello, this is a test message');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(10000);
  });

  // 验证Credits消耗
  await test.step('验证Credits消耗', async () => {
    // 等待页面加载完成
    await page.waitForLoadState('networkidle');
    
    // 查找Credits显示
    const creditsElement = page.locator('div').filter({ hasText: /^\d+$/ }).first();
    await expect(creditsElement).toBeVisible({ timeout: 10000 });
    const creditsText = await creditsElement.textContent();
    const currentCredits = parseInt(creditsText || '0');
    console.log(`当前Credits: ${currentCredits}`);
    expect(currentCredits).toBeLessThan(initialCredits);
    expect(initialCredits - currentCredits).toBe(10);
  });

  // 登出操作
  await test.step('执行登出', async () => {
    await checkAndLogout(page);
  });
}); 