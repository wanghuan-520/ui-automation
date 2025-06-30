# GodGPT V1.13.0 增加 Refresh token

## 1. 版本信息
- 版本号：V1.13.0
- 创建日期：2025.5.6
- 产品负责人：Tonio

## 2. 项目背景
- 当前后端Token有效期为48小时，导致用户每两天需重新登录，严重影响连续体验。为提升用户留存与交互流畅性，计划引入Refresh Token机制，实现活跃状态下自动续期，无需手动登录。

## 3. 需求详情
### 3.1 双Token机制
- Access Token：用于正常鉴权，生命周期2天
- Refresh Token：用于在Access Token过期后刷新获取新的Access Token，生命周期14天
- 刷新策略：若accessToken过期后，使用refresh Token获取新的access token和refresh token，覆盖当前浏览器内的两者。用户需重新登录的条件是：access token及refresh token均过期。

### 3.2 适用范围
- 国际版 WebApp
- 国际版 iOS / Android
- 中国版 WebApp
- 中国版 iOS

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 双Token机制 | Access/Refresh Token自动续期 | 无 |
| 2    | 刷新策略 | accessToken过期后自动刷新 | 无 |
| 3    | 适用范围 | 四端环境一致性 | 无 |

## 5. 流程/用例/伪代码
- 若accessToken过期，自动用refreshToken刷新，刷新失败则需重新登录

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 保证测试与生产环境稳定一致，响应需快速准确

## 8. UI/原型
- 无

## 9. 变更记录
- 暂无

GodGPT Github 
- Backend https://github.com/aevatarAI/aevatar-station/tree/feature/godgpt
  - will migrate to https://github.com/aevatarAI/godgpt
- Frontend https://github.com/aevatarAI/custom-gpt-frontend
- Frontend links GodGPT web/mobile apps