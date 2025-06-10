# GodGPT Credits 自动化测试

## 测试用例说明

### 1. 新用户额度测试 (credits.spec.ts)
测试新用户注册后的初始Credits额度及其稳定性
- 验证初始额度为320 Credits
- 验证登出登录后额度保持不变
- 测试账号: playwright7@teml.net

### 2. Credits消耗测试 (credits.spec.ts)
测试用户进行对话操作时Credits的消耗情况
- 验证单次对话消耗10 Credits
- 验证登出登录后额度保持一致
- 测试账号: playwright@teml.net

## 环境要求
- Node.js >= 14.0.0
- Playwright 最新稳定版
- 测试环境: https://godgpt-ui-testnet.aelf.dev/

## 执行方法

1. 安装依赖
```bash
npm install
npx playwright install
```

2. 执行测试
```bash
# 执行所有测试
npx playwright test

# 执行单个测试文件
npx playwright test credits.spec.ts

# 执行特定测试用例
npx playwright test -g "新用户额度测试"
```

3. 查看报告
```bash
npx playwright show-report
```

## 注意事项
1. 执行测试前确保测试账号状态正确
2. 每个测试用例执行后会自动退出登录
3. 测试过程会自动保存截图和视频（仅失败时）
4. 测试报告位于 test-results 目录

## 测试结果
测试结果将保存在以下位置：
- HTML报告: playwright-report/
- JSON报告: test-results/test-results.json
- 失败截图: test-results/screenshots/
- 失败视频: test-results/videos/ 