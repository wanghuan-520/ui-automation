import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // 测试目录
  testDir: './tests',
  
  // 每个测试的超时时间
  timeout: 45000,
  
  // 期望每个测试都能独立运行
  fullyParallel: true,
  
  // 失败重试次数
  retries: 2,
  
  // 测试工作者数量
  workers: 1,
  
  // Reporter配置
  reporter: 'html',
  
  // 共享的配置
  use: {
    // 基础URL
    baseURL: 'https://godgpt-ui-testnet.aelf.dev/',
    
    // 自动截图
    screenshot: 'on',
    
    // 记录视频
    video: 'on',
    
    // 记录跟踪
    trace: 'retain-on-failure',
    
    // 视窗大小
    viewport: { width: 1280, height: 720 },
    
    // 操作超时
    actionTimeout: 15000,
    
    // 导航超时
    navigationTimeout: 30000,
  },
  
  // 项目配置
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
}); 