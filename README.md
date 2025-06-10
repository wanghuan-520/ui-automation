# GodGPT 自动化测试

本项目包含 GodGPT 的自动化测试用例，使用 Playwright 框架实现。

## 环境要求

- Node.js 16+
- npm 或 yarn

## 安装

```bash
# 安装依赖
npm install

# 安装 Playwright 浏览器
npx playwright install
```

## 运行测试

```bash
# 运行所有测试
npm test

# 使用UI模式运行测试
npm run test:ui

# 有界面模式运行测试
npm run test:headed

# 查看测试报告
npm run report
```

## 测试用例

### 1. 新用户额度测试
- 测试新用户注册后的初始额度（320 Credits）
- 验证登录登出功能
- 确保额度显示正确

### 2. Credits消耗测试
- 测试用户对话时的Credits消耗
- 验证每次对话扣除10 Credits
- 确保额度变化正确记录

## 注意事项

1. 测试前请确保测试账号状态正确
2. 所有测试用例使用邮箱登录方式
3. 测试过程会自动记录截图和视频（仅失败时）
4. 测试报告位于 playwright-report 目录

# GodGPT V1.15.0 测试框架

## 目录结构

```
V1.15.0/
├── test-requirements/    # 测试依赖和要求
│   ├── env.ts          # 环境配置
│   ├── env.json        # 环境变量
│   └── dependencies.md # 依赖说明
├── test-cases/          # 测试用例文档
├── test-script/         # 测试脚本
├── test-results/        # 测试结果输出
│   ├── reports/        # 测试报告
│   ├── screenshots/    # 测试截图
│   └── logs/          # 测试日志
└── test-conditions.md   # 测试条件说明
```

## 项目结构

```
.
├── test-cases/          # 测试数据目录
│   ├── account/         # 账户管理相关测试数据
│   ├── subscription/    # 订阅相关测试数据
│   └── credits/         # 积分相关测试数据
├── test-script/         # 测试脚本目录
│   ├── account/         # 账户管理测试脚本
│   ├── subscription/    # 订阅测试脚本
│   └── credits/         # 积分测试脚本
├── test-results/        # 测试结果输出目录
├── test-requirements/   # 测试需求文档
├── package.json         # -> ../../../common/config/base/package.json
├── playwright.config.ts # -> ../../../common/config/base/playwright.config.ts
└── tsconfig.json       # -> ../../../common/config/base/tsconfig.json
```

## 配置说明

本测试框架使用通用配置（位于 `/common/config/base/` 目录），所有配置文件都集中在通用配置目录中管理。版本特定的环境配置位于 `test-requirements/env.ts`。

本项目使用统一的基础配置，通过符号链接指向共享配置目录：
- `package.json` - 项目依赖和脚本配置
- `playwright.config.ts` - Playwright 测试框架配置
- `tsconfig.json` - TypeScript 配置

### 配置继承
```typescript
// 在测试脚本中使用配置
import { baseConfig } from '../../../common/config/base/playwright.config';
import { basePackage } from '../../../common/config/base/package.json';
import { config as envConfig } from '../test-requirements/env';

// 使用配置
const config = {
  ...baseConfig,
  ...envConfig,
  // V1.15.0特定的配置覆盖
};
```

### 工具使用
```typescript
import { timeUtils } from '../../../common/utils/helpers/time';
import { setupTest } from '../../../common/utils/test/setup';
import { customExpects } from '../../../common/utils/assert/custom-expects';

// 使用工具函数
await timeUtils.wait(1000);
await setupTest.prepare();
await customExpects.toBeVisible(element);
```

## 测试模块说明

### 测试要求 (test-requirements/)
- 环境配置要求
  - Node.js版本
  - 依赖包版本
  - 环境变量设置
- 依赖包管理
  - 核心依赖
  - 开发依赖
  - 可选依赖
- 前置条件说明
  - 网络要求
  - 权限设置
  - 数据准备
- 测试环境准备
  - 环境初始化
  - 数据清理
  - 状态重置

### 测试用例 (test-cases/)
- UI测试用例
  - 页面布局
  - 交互响应
  - 适配性测试
- 集成测试用例
  - Credits系统
  - 用户管理
  - 权限控制
- 性能测试用例
  - 加载时间
  - 资源占用
  - 并发处理

### 测试脚本 (test-script/)
- UI测试脚本
  - 元素定位
  - 交互模拟
  - 视觉验证
- 集成测试脚本
  - 功能验证
  - 数据流转
  - 异常处理
- 工具脚本
  - 环境配置
  - 数据准备
  - 结果验证

### 测试结果 (test-results/)
- 测试报告
  - HTML报告
  - JSON数据
  - 统计分析
- 测试截图
  - 失败截图
  - 对比截图
  - 视觉差异
- 测试日志
  - 执行日志
  - 错误日志
  - 性能数据

## 运行说明

### 环境准备
```bash
# 安装依赖
cd ../../../common/config/base && npm install

# 安装浏览器
npx playwright install
```

### MCP 录制与测试
```bash
# 启动 MCP 录制模式并运行测试
npm run test:godgpt-v1.15.0 -- --mcp-record

# 在特定目录下保存录制的脚本
npm run test:godgpt-v1.15.0 -- --mcp-record --mcp-output-dir=./test-script/recorded

# 运行特定测试并录制
npm run test:godgpt-v1.15.0 -- --grep "测试名称" --mcp-record

# 调试模式下录制
npm run test:godgpt-v1.15.0:debug -- --mcp-record
```

注意事项：
- MCP 录制功能会自动捕获测试过程中的所有交互操作
- 录制的脚本默认保存在 `test-script/recorded` 目录下
- 录制文件命名格式为：`{测试名称}-{时间戳}.ts`
- 建议在录制完成后检查并优化生成的脚本
- 可以通过 `--mcp-config` 参数指定录制配置文件

### 运行测试
```bash
# 运行所有测试
npm run test:godgpt-v1.15.0

# 运行特定测试
npm run test:godgpt-v1.15.0 -- --grep "测试名称"

# 调试模式
npm run test:godgpt-v1.15.0:debug
```

## 注意事项

1. 测试编写规范
   - 使用中文注释
   - 遵循测试命名规范
   - 保持用例独立性
   - 合理使用断言
   - 处理异步操作
   - 清理测试数据

2. 环境管理
   - 遵循配置文件规范
   - 管理环境变量
   - 控制测试数据
   - 清理测试环境
   - 处理并发问题
   - 监控资源使用

3. 结果管理
   - 规范报告格式
   - 保存必要日志
   - 管理测试截图
   - 记录性能数据
   - 分析失败原因
   - 追踪问题修复

## 维护指南

1. 代码维护
   - 定期更新依赖
   - 优化测试性能
   - 清理无用代码
   - 更新测试用例
   - 重构重复代码
   - 完善错误处理

2. 文档维护
   - 更新测试说明
   - 维护配置文档
   - 记录变更历史
   - 更新使用指南
   - 补充常见问题
   - 添加示例代码

## 常见问题

1. UI测试问题
   - 元素定位失败
   - 页面加载超时
   - 视觉对比差异
   - 交互响应延迟

2. 性能问题
   - 页面加载慢
   - 资源占用高
   - 并发处理慢
   - 内存泄漏

3. 环境问题
   - 配置不正确
   - 依赖版本冲突
   - 权限不足
   - 网络不稳定

## 联系方式

如有问题请联系GodGPT测试团队。 