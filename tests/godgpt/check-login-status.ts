import { test, expect } from '@playwright/test';

/**
 * 检查登录状态并执行登出操作的测试用例
 */
test('检查登录状态并登出', async ({ page }) => {
  // 导航到测试页面
  await page.goto('https://godgpt-ui-testnet.aelf.dev/');
  
  // 等待页面加载完成
  await page.waitForTimeout(5000);
  
  // 检查是否显示Credits数值（登录状态标志）
  const creditsElement = page.locator('div[class*="credits"]').first();
  const isLoggedIn = await creditsElement.isVisible();
  
  if (isLoggedIn) {
    console.log('检测到登录状态，执行登出操作');
    
    // 点击用户菜单
    await page.locator('img[alt*="user"]').last().click();
    await page.waitForTimeout(1000);
    
    // 点击登出按钮
    await page.getByText('Log Out').click();
    await page.waitForTimeout(5000);
    
    // 验证登出成功
    const loginButton = page.getByText('Continue with Email');
    await expect(loginButton).toBeVisible();
    console.log('登出成功');
  } else {
    console.log('当前为未登录状态');
  }
});

/**
 * 导出登录状态检查函数供其他测试用例使用
 */
export async function checkAndLogout(page) {
  await test.step('检查并清理登录状态', async () => {
    // 等待页面加载
    await page.waitForTimeout(5000);
    
    // 检查Credits显示
    const creditsElement = page.locator('div[class*="credits"]').first();
    const isLoggedIn = await creditsElement.isVisible();
    
    if (isLoggedIn) {
      // 执行登出操作
      await page.locator('img[alt*="user"]').last().click();
      await page.waitForTimeout(1000);
      await page.getByText('Log Out').click();
      await page.waitForTimeout(5000);
    }
  });
}
