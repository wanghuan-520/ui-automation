import { FullConfig } from '@playwright/test';

/**
 * 全局设置函数
 * 在所有测试开始前执行
 */
async function globalSetup(config: FullConfig) {
  console.log('开始执行全局设置...');
  
  // 设置全局超时
  process.env.PLAYWRIGHT_TIMEOUT = '60000';
  
  // 设置测试环境
  process.env.TEST_ENV = 'testnet';
  process.env.BASE_URL = 'https://godgpt-ui-testnet.aelf.dev/';
  
  console.log('全局设置完成');
}

export default globalSetup; 