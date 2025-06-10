# GodGPT V1.15.0 测试补充条件说明

## 测试环境
- 测试地址: https://godgpt-ui-testnet.aelf.dev/

## 执行注意事项
1. 所有测试用例均使用邮箱登录方式
2. 执行前请确保账号状态符合测试前置条件
3. 测试过程中需要自动记录执行过程的截图和视频
4. 如遇到异常情况，请详细记录测试环境和复现步骤
5. 每个case执行后都需要退出，保证最新的状态

## 环境信息记录
```json
{
  "测试环境": "https://godgpt-ui-testnet.aelf.dev/",
  "Credits系统版本": "1.15.0",
  "Credits监控状态": "active"
}
```

## Credits测试特殊要求

### 1. 数据准备
- 测试前确保账号Credits状态清晰
- 记录初始Credits值
- 准备测试用的交易场景
- 严格按照case中指定的账户去测试
- 执行每个case前，先保证前一个账号是退出的状态

### 2. 监控要求
- Credits变动实时监控
- 交易延迟监控
- 系统性能指标采集

### 3. 异常处理
- Credits扣除失败场景处理
- 网络延迟对Credits影响分析
- 并发操作Credits保护机制

### 4. 报告补充
- Credits变动明细记录
- 性能指标统计
- 异常情况分类统计

### 5. 问题分类
```json
{
  "categories": [
    {
      "name": "Credits系统异常",
      "matchedStatuses": ["failed", "broken"],
      "messageRegex": ".*credits.*|.*额度.*"
    }
  ]
}
```

## 备注
- Credits相关的测试数据需要特别备份和保护
- 测试执行过程中如有特殊情况，请及时更新本文档
- 请参考 automation-rules.md 获取通用的自动化测试规范 