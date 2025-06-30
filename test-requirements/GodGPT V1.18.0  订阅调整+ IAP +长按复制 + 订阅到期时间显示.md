# GodGPT V1.18.0 订阅调整+ IAP +长按复制 + 订阅到期时间显示

## 1. 版本信息
- 版本号：V1.18.0
- 创建日期：2025.6.5
- 产品负责人：Tonio

## 2. 项目背景
- 之前版本遗留问题 https://github.com/orgs/aevatarAI/projects/13/views/13 + GodGPT Integrations项目 Bug 管理
- 订阅修改
- iOS 支持 in-app purchase
  - IAP integration
  - Stripe integration
- App内实现长按复制功能
- iOS data streaming @Haylee Wang
- 后端API实现给某个用户增加Credit功能 @Haylee Wang

## 3. 需求详情
### 3.1 之前版本遗留问题
- 详见文档内各序号说明

### 3.2 iOS 支持 in-app purchase
- 替换Stripe Apple Pay为IAP Apple Pay
- 使用Apple的StoreKit框架实现IAP，支持订阅功能，覆盖现有Stripe Apple Pay的所有支付场景
- App Store Connect中配置产品ID、价格及订阅周期，支持促销优惠
- 支付成功后页面刷新，失败提示，充值弹框关闭
- 基于IAP的取消订阅，效果同V1.15.0
- 订阅模式修改，增加Ultimate订阅模式，无限交互
- 订阅badge优先显示高等级，时间优先使用高等级，升级订阅逻辑

### 3.3 App内实现长按复制功能
- 回复内容内长按复制

### 3.4 iOS/Android data streaming
- 数据流式传输

### 3.5 后端API实现给某个用户增加Credit功能
- 后端API支持

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 侧边栏历史记录Rename | 优化Rename功能 | iOS/Android/Web app |
| 2    | IAP订阅 | 支持Apple IAP订阅 | iOS |
| 3    | 订阅模式 | 增加Ultimate订阅模式 | All |
| 4    | 长按复制 | App内长按复制功能 | iOS/Android |
| 5    | 数据流 | iOS/Android数据流式传输 | iOS/Android |
| 6    | 后端API | 给用户增加Credit功能 | All |

## 5. 流程/用例/伪代码
- 详见文档内各流程说明

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 订阅、充值、Credits、限流、异常等需三端同步

## 8. UI/原型
- [图片]

## 9. 变更记录
- 暂无

