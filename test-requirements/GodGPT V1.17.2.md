# GodGPT V1.17.2

## 1. 版本信息
- 版本号：V1.17.2
- 创建日期：2025.6.14
- 产品负责人：Tonio

## 2. 项目背景
- 为QuestN增加邮箱验证接口

## 3. 需求详情
### 3.1 增加邮箱验证API接口
- 为支持QuestN拉新验证，需开发一个后端API接口，用于验证用户提供的邮箱是否已注册。接口需支持验证一种登录方式：邮箱登录。

#### 接口详情
- 接口名称：邮箱注册验证接口
- 功能：根据提供的邮箱地址，判断该邮箱是否已在系统中注册成功。
- 支持的登录方式：
  - 苹果登录  (不支持）
  - 谷歌账号登录    (不支持）
  - 邮箱登录
- 接口地址：
  - 测试环境（不删档）：https://station-developer-staging.aevatar.ai/godgpt-client/api/godgpt/check-email-registered?email={email}
  - 生产环境（主网）：https://station-developer.aevatar.ai/godgptprod-client/api/godgpt/check-email-registered?email={email}
- 请求方式：GET
- 请求参数：
  - email（必填）：用户提供的邮箱地址，字符串格式。
- 响应格式：
  - json
  - code：响应状态码，"20000"表示成功。
  - data.result：布尔值，true表示邮箱已注册，false表示未注册。
  - message：错误或提示信息，成功时为空字符串。

- 需求说明：
  - 需保证接口在测试环境和生产环境的稳定性与一致性。
  - 响应需快速、准确，符合QuestN拉新验证的业务需求。

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 邮箱验证API | 支持QuestN拉新邮箱验证 | 无 |

## 5. 流程/用例/伪代码
- 无

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 需保证接口稳定性与一致性

## 8. UI/原型
- 无

## 9. 变更记录
- 暂无