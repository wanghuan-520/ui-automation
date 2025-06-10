# GodGPT V1.15.0 需求文档

## 一、版本信息

- 版本号：V1.15.0
- 创建日期: 2025.5.7
- 产品负责人：Tonio

## 二、项目背景

目前GodGPT 单次对话成本 $0.07美金，为了控制成本，需要对用户免费行为进行限制：

- 用户可以免费使用32次
- 用户可以进行充值继续使用

## 三、需求详情

### 3.1 产品优化

#### REQ-001: 余额系统
##### 基础显示
- 登录状态下显示余额
- 账户Credits显示（新用户默认320 Credits，永久有效）
- Credits位置：
  - 首页：右上角
  - 对话页面：居中显示

##### 订阅状态
- 订阅用户首页显示Badge
- 对话页面：
  - 不显示Badge和Credits
  - 中间显示GodGPT字段

##### 功能操作
- 新对话按钮：保持原有
- 分享按钮：新增
- Credits消耗：
  - 每次对话消耗10 Credits
  - 实时扣除（三端同步）
  - 网络延迟处理：提示"余额同步中，请稍后"

##### 使用限制
- 消息限制：
  - 非订阅用户：25个令牌/3小时
  - 订阅用户：100个令牌/3小时
- 限制提示：
  - Credits耗尽："You've run out of credits."
  - 达到限制："Message limit reached. Please try again later."

#### REQ-002: 充值系统
##### 订阅方案
- 日订阅：
  - 1美金/24h（国区¥13.99）
  - 自动续费
- 月订阅：
  - 20美金/30天（国区¥139.99）
  - 自动续费
- 年订阅：
  - 200美金/390天（国区¥1499.99）
  - 自动续费
  - 支持30天内退款

##### 支付功能
- 支付方式：
  - Stripe支付（三端支持）
  - Card支付（必须）
  - Apple Pay（iOS）
- 支付流程：
  - 等待Subscription创建成功
  - 成功：重定向首页，提示"Payment successful"
  - 失败：提示"Payment failed. Please try again."

#### REQ-003: Profile页面更新
- 增加充值栏：Upgrade your plan
- 充值弹框增加Contact Us按钮
- 联系方式：https://form.portkey.finance/godgpt-contact

#### REQ-004: 账户删除优化
##### 确认弹框内容
Title: Confirm Account Deletion
Content:
```
Deleting your account will permanently remove all access to GodGPT services, along with your account information and chat history.

Important:
- Refunds cannot be processed after account deletion — make sure to resolve any refund requests beforehand.
- If you have an active subscription, please cancel it first to avoid continued charges.
- Repeated deletion attempts may be flagged as suspicious activity and could lead to restrictions or permanent suspension.
- This action is irreversible.
```

##### 更新原因
- 付费功能影响：删除账号后付款记录被删除，无法处理退款
- 订阅处理：删除账号不会自动取消订阅
- 状态重置：删除后所有订阅状态重置为新用户

## 四、平台支持
- Web
- Mobile

## 五、备注
- UI走查问题已整理
- 所有金额显示需遵循本地化规则
- 需要确保三端数据同步的实时性