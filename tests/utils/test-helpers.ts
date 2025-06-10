import { Page, Locator } from '@playwright/test';

/**
 * 测试工具函数
 */
export class TestHelpers {
  /**
   * 重试获取Credits值
   */
  static async getCreditsWithRetry(page: Page, maxRetries = 3): Promise<number> {
    let retries = maxRetries;
    while (retries > 0) {
      try {
        await page.waitForTimeout(1000);
        const creditsElement = await page.getByText(/\d+/, { exact: true }).first();
        const creditsText = await creditsElement.textContent();
        const credits = parseInt(creditsText || '0');
        if (credits > 0) return credits;
      } catch (e) {
        console.log(`Retry ${maxRetries - retries + 1} failed`);
      }
      retries--;
    }
    throw new Error('Failed to get Credits value');
  }

  /**
   * 执行登出操作
   */
  static async logout(page: Page): Promise<void> {
    try {
      // 等待页面加载完成
      await page.waitForTimeout(2000);
      
      // 尝试多个可能的头像按钮选择器
      const avatarSelectors = [
        'button:has(svg):right-of(:text("Credits"))',
        'button:has(svg):near(:text("Credits"), 100)',
        'div[role="button"]:has(svg):right-of(:text("Credits"))',
        'div:has(svg):right-of(:text("Credits"))'
      ];

      let avatarButton: Locator | undefined;
      for (const selector of avatarSelectors) {
        try {
          await page.waitForSelector(selector, { timeout: 5000 });
          const button = page.locator(selector).first();
          if (await button.isVisible()) {
            avatarButton = button;
            break;
          }
        } catch (e) {
          console.log(`Selector ${selector} failed, trying next...`);
        }
      }

      if (!avatarButton) {
        throw new Error('Could not find avatar button');
      }

      // 点击头像按钮
      await avatarButton.click();
      
      // 等待并点击登出按钮
      await page.waitForSelector('text=Log Out', { state: 'visible', timeout: 5000 });
      await page.getByText('Log Out').click();
      
      // 等待登出完成
      await page.waitForTimeout(1000);
    } catch (e) {
      console.error('Logout failed:', e);
      // 记录页面状态以帮助调试
      console.log('Current URL:', page.url());
      console.log('Page title:', await page.title());
      throw e;
    }
  }

  /**
   * 等待并验证Credits变化
   */
  static async waitForCreditsChange(
    page: Page,
    initialCredits: number,
    timeout = 5000
  ): Promise<number> {
    const startTime = Date.now();
    while (Date.now() - startTime < timeout) {
      const currentCredits = await this.getCreditsWithRetry(page);
      if (currentCredits !== initialCredits) {
        return currentCredits;
      }
      await page.waitForTimeout(500);
    }
    throw new Error('Credits did not change within timeout');
  }

  /**
   * 多重选择器元素查找
   */
  static async findElement(page: Page, selectors: string[]) {
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

  /**
   * 断言重试机制
   */
  static async retryAssertion(
    action: () => Promise<void>,
    maxRetries = 3,
    interval = 1000
  ) {
    let lastError;
    for (let i = 0; i < maxRetries; i++) {
      try {
        await action();
        return;
      } catch (error) {
        lastError = error;
        await new Promise(resolve => setTimeout(resolve, interval));
      }
    }
    throw lastError;
  }
} 