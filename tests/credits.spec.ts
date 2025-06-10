import { test, expect } from '@playwright/test';
import { TestHelpers } from './utils/test-helpers';

// 测试新用户注册后的初始额度
test('新用户额度测试', async ({ page }) => {
  // 导航到测试环境
  await page.goto('https://godgpt-ui-testnet.aelf.dev/');
  
  // 点击邮箱登录按钮
  await page.getByText('Continue with Email').click();
  
  // 填写邮箱
  await page.getByRole('textbox', { name: 'Enter your email' }).fill('playwright7@teml.net');
  await page.getByText('Continue with Email').click();
  
  // 填写密码
  await page.getByRole('textbox', { name: 'Enter your password' }).fill('Wh520520!');
  await page.getByText('Continue', { exact: true }).click();
  
  // 等待并验证初始Credits
  await TestHelpers.retryAssertion(async () => {
    const credits = await TestHelpers.getCreditsWithRetry(page);
    expect(credits).toBeGreaterThan(0);
  });
  
  // 执行登出操作
  await TestHelpers.logout(page);
});

// 测试Credits消耗
test('Credits消耗测试', async ({ page }) => {
  // 导航到测试环境
  await page.goto('https://godgpt-ui-testnet.aelf.dev/');
  
  // 点击邮箱登录按钮
  await page.getByText('Continue with Email').click();
  
  // 填写邮箱
  await page.getByRole('textbox', { name: 'Enter your email' }).fill('playwright@teml.net');
  await page.getByText('Continue with Email').click();
  
  // 填写密码
  await page.getByRole('textbox', { name: 'Enter your password' }).fill('Wh520520!');
  await page.getByText('Continue', { exact: true }).click();
  
  // 等待并记录初始Credits
  const initialCredits = await TestHelpers.getCreditsWithRetry(page);
  console.log(`Initial Credits: ${initialCredits}`);
  
  // 发送对话消息
  await page.getByRole('textbox', { name: 'Ask anything' }).click();
  await page.getByRole('textbox', { name: 'Ask anything' }).fill('Hello, can you help me with a simple task?');
  await page.getByRole('textbox', { name: 'Ask anything' }).press('Enter');
  
  // 等待并验证Credits扣除
  const updatedCredits = await TestHelpers.waitForCreditsChange(page, initialCredits);
  console.log(`Updated Credits: ${updatedCredits}`);
  expect(updatedCredits).toBeLessThan(initialCredits);
  
  // 执行登出操作
  await TestHelpers.logout(page);
}); 