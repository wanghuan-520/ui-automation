# GodGPT V1.16.0 广告投放落地页需求

## 1. 版本信息
- 版本号：V1.16.0
- 创建日期：2025.5.23
- 产品负责人：Tonio

## 2. 项目背景
- 以 $9,000 的广告预算，测试 GodGPT 订阅功能在不同平台及用户来源下的付费转化率。验证产品落地页在广告投放中的效果，收集用户留存及获客成本数据，为后续大规模投放提供决策依据。

## 3. 需求详情
### 3.1 落地页需求
- 需有独立落地页作为产品讲解、用户引流和效果追踪使用。
- 域名：godgpt.fun（新增主页设计作为落地页，主域名）
- 设计稿参考：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=4024-20594&t=GfNByKbnk2IANi2s-0
- 需实现/landing-page路由，跟进figma设计，主网更新
- 需实现首页与app页的埋点追踪
- 广告投放平台：Twitter Ads、TikTok（红人合作）、Telegram Ads
- 需配置GA、GTM，UTM参数，支持多渠道追踪

### 3.2 数据追踪机制
- Google Analytics (GA) 配置，埋点事件包括：页面访问、按钮点击、时间停留、注册、订阅、支付等
- UTM参数结构：utm_source、utm_medium、utm_campaign、utm_content、utm_term
- 埋点事件与转化率、获客成本、广告回报等数据统计
- 每日简报、每周报告，分析各渠道点击、注册、订阅、CAC、ROAS等

### 3.3 域名与部署
- godgpt.fun主域名配置GA，子域名go.godgpt.fun纳入GA追踪范围
- DevOps需配置CNAME，指向主网landing-page

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 落地页 | 独立主页，产品讲解与引流 | [图片] |
| 2    | 广告追踪 | GA、GTM、UTM参数配置 | 无 |
| 3    | 数据埋点 | 注册、订阅、支付等事件追踪 | 无 |
| 4    | 多渠道 | Twitter、TikTok、Telegram投放 | 无 |
| 5    | 域名配置 | 主域名及子域名GA追踪 | 无 |
| 6    | DevOps | CNAME配置，主网部署 | 无 |

## 5. 流程/用例/伪代码
- 广告投放、用户访问、注册、订阅、支付、数据追踪等流程详见原文与Figma原型

## 6. 埋点/数据
- GA、GTM、UTM参数、事件埋点、转化率、CAC、ROAS等

## 7. 兼容性/异常/边界说明
- 保证各平台、各渠道数据追踪一致，UTM参数准确传递

## 8. UI/原型
- [图片]
- https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=4024-20594&t=GfNByKbnk2IANi2s-0

## 9. 变更记录
- 暂无
