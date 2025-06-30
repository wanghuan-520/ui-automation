# GodGPT V1.19.0 需求文档

## 一、版本信息
- **版本号**：V1.19.0
- **创建日期**：2025.5.12
- **产品负责人**：Tonio

---

## 二、项目背景
- **分享邀请系统**：
  - 通过用户推荐吸引新用户下载并注册APP，扩大用户基数。
  - 激励现有用户成为APP的推广者，形成病毒式传播。
- **公式复制**
- **序列化测试**
- **Bugfix**
- **Profile显示 + Modal 改造**
- **输入框长度限制从2000变成10,000**

---

## 三、需求详情

### 1. 分享/邀请系统

#### 1.1 功能说明
| 序号 | 适用端口 | 说明 |
| ---- | -------- | ---- |
| 1 | All | 用户点击Invite Friends弹出邀请弹框，顶部展示邀请活动内容（邀请好友赚Credits），显示邀请好友数量和奖励阶梯，展示邀请码、邀请过程、奖励明细等 |
| 2 | All | 被邀请人首次付费奖励Credits，奖励规则见下表 |
| 3 | All | 有效邀请条件：新注册且发起过一次对话或兑换邀请码 |
| 4 | All | 通过邀请链接注册的新用户可享7天订阅体验，注册72h内兑换邀请码有效 |
| 5 | All | Copy按钮复制邀请链接，点击变为Copied，3秒后恢复 |
| 6 | All | 支持UID查询有效邀请数字 |

#### 1.2 邀请奖励明细
| 付费类型 | 邀请人奖励（Credits） | 备注 |
| -------- | -------------------- | ---- |
| Weekly Premium | 100 | 首次付费 |
| Weekly Ultimate | 500 | 首次付费 |
| Monthly Premium | 400 | 首次付费 |
| Monthly Ultimate | 2000 | 首次付费 |
| Annual Premium | 4000 | 首次付费，30天后发放 |
| Annual Ultimate | 20000 | 首次付费，30天后发放 |

- 首次邀请新用户奖励30 Credits，后续每3位有效邀请奖励100 Credits。
- 有效邀请条件：新注册且发起过一次对话或兑换邀请码。

#### 1.3 分享弹窗入口
- Invite Friends页面点击Invite Now
- 每个会话页面（算命会话/其余会话）
- App端截屏后

#### 1.4 分享内容与交互
- **图片**：品牌视觉、二维码、邀请码、下载按钮
- **推文内容**：
  ```
  Hey,
  Lately I've been using GodGPT to explore life's subtle questions — it's like tuning into the hidden rhythm of things, surprisingly insightful and fun.
  Tap the link to get 7 days of free access and try it with me! 🜂✨
  {https://app.godgpt.fun?invitationcode=32132}
  My Code is: {32132}
  #GodGPT #HyperEcho #AIRevelation #InviteToEarn
  ```
- **Copy**：复制链接 https://app.godgpt.fun?invitationcode=32132
- **二维码**：链接+邀请码
- **Download**：下载图片到本地

#### 1.5 输入邀请码
- 点击Input Invitation Code弹出输入框
- 输入错误邀请码提示"This code is not valid. Make sure it's correct and not your own code."
- 输入正确邀请码弹框关闭，toast提示"Code applied successfully"，页面刷新，获得7天premium权限，显示Weekly标志
- 超过72h提示："Your account was created more than 72 hours ago and is no longer eligible for the new user referral promotion."

---

### 2. 公式复制
- 公式开始和结束使用相同的标记
- 长按公式复制和点击左下角复制按钮复制公式无乱码
- Web端左下角复制和iOS左下角复制一致
- Web端选择复制不支持
- iOS端选择公式会以另一种形式复制公式

---

### 3. 序列化测试
- 验证所有功能，重点测试历史数据，特别是历史账号（SignalR账号）

---

### 4. Bug修复
| 序号 | 适用端口 | 说明 | 链接 |
| ---- | -------- | ---- | ---- |
| 1 | Android | 应用卡顿、输入框无法上移、滑动困难 | @Thomas Lin |
| 2 | iOS | 显示密码按钮异常 | [issue#97](https://github.com/orgs/aevatarAI/projects/13/views/14?filterQuery=&pane=issue&itemId=112897815&issue=aevatarAI%7Cgodgpt%7C97) |
| 3 | All | 会话页面解析"?" | [issue#101](https://github.com/orgs/aevatarAI/projects/13/views/14?filterQuery=&pane=issue&itemId=114092486&issue=aevatarAI%7Cgodgpt%7C101) |
| 4 | All | 账号登录异常 | [issue#104](https://github.com/orgs/aevatarAI/projects/13/views/14?filterQuery=&pane=issue&itemId=114235753&issue=aevatarAI%7Cgodgpt%7C104) |
| 5 | All | 回复时主动上滑不强制到底 |  |
| 6 | Web | Stripe返回需定位原页面并保持plan弹框 | [issue#501](https://github.com/orgs/aevatarAI/projects/13/views/14?filterQuery=&pane=issue&itemId=114101636&issue=aevatarAI%7Ccustom-gpt-frontend%7C501) |
| 7 | All | 登录有概率无限logging in | [issue#584](https://github.com/orgs/aevatarAI/projects/13/views/15?pane=issue&itemId=115419202&issue=aevatarAI%7Ccustom-gpt-frontend%7C584) |
| 8 | iOS | 删除账号后重新登录弹框异常 | [issue#586](https://github.com/orgs/aevatarAI/projects/13/views/15?pane=issue&itemId=115431074&issue=aevatarAI%7Ccustom-gpt-frontend%7C586) |

---

### 5. Profile显示 + Modal改造
- **Profile显示**：页面展示用户头像、邮箱、UID（name没有不展示）
- **Modal改造**：原生native Modal替换为第三方Modal，滑动流畅、遮罩可点击关闭、iOS端区域可点击、兼容性优化

---

### 6. 输入框长度限制
- 输入框最大长度由2000提升至10,000
- 粘贴、输入、特殊字符、emoji等均受限于最大长度

---

<!-- 图片、流程图等可用Markdown语法插入 -->
