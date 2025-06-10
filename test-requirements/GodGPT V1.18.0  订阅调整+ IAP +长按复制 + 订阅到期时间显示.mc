# GodGPT V1.18.0 需求文档

## 一、版本信息

- 版本号：V1.18.0
- 创建日期：2025.6.5
- 产品负责人：Tonio

## 二、项目背景

- 之前版本遗留问题：https://github.com/orgs/aevatarAI/projects/13/views/13 + [GodGPT Integrations项目 Bug 管理](https://aelfblockchain.sg.larksuite.com/wiki/OaxOw3wFYiTiSykkZWYlMPiMgBb?from=from_copylink)
- 点击支付后会有一个弹框闪现
- 从stripe页面回到godgpt内，返回页面配置不正确
- Account接口报错
- iOS 首次下载无法使用问题（不可点击）
- 信息收集页面，生日选择时未显示用户之前选中的日期
- Rename功能优化
- 移动端的消息没有及时同步到web端
- Android 会话内容滑动时，底部的输入框位置会移动
- 会话详情页面有概率滑不动
- openai账号余额不足的情况下，用户创建个新会话，发送消息。在侧边栏再次点击消息，这种情况下会出现两次发送对话
- 订阅修改
- iOS 支持 in-app purchase
- IAP integration
- Stripe integration
- 用户订阅到期时间显示
- App内实现长按复制功能

## 三、需求详情

### 3.1 之前版本遗留问题

#### 3.1.1 侧边栏历史记录Rename功能优化
- 适用端口：iOS/Android/Web app
- 当前效果：用户点击侧边栏历史记录的"Rename"后，标题变为输入框，光标定位至末尾，用户可编辑内容，按回车键确认修改。
- 优化后效果：
  1. 用户点击"Rename"后，菜单栏收起，键盘弹出，同时弹出"Rename Chat"对话框，光标自动定位至标题末尾。
  2. 用户可编辑标题：
     - 点击"Cancel"按钮：键盘收起，弹框关闭。
     - 点击"Confirm"按钮：保存修改后的标题，键盘收起，弹框关闭。

### 3.2 iOS 支持 in-app purchase

#### 3.2.1 替换Stripe Apple Pay为IAP Apple Pay
- 适用端口：iOS
- 说明：
  1. 使用Apple的StoreKit框架实现IAP，支持订阅功能，覆盖现有Stripe Apple Pay的所有支付场景（如GodGPT的订阅功能）。
  2. 在App Store Connect中配置产品ID、价格及订阅周期（周、月、年），并支持促销优惠（如免费试用）。
  3. 支付成功后会被重新定位到首页，页面刷新（credits隐藏），toast提示"Payment successful"；若支付失败则显示"Payment failed. Please try again." 充值弹框关闭，回到原页面保持不变。
  4. 基于IAP的取消订阅，效果同[GodGPT V1.15.0（带充值版本）](https://aelfblockchain.sg.larksuite.com/wiki/MG1Jwh7x8id8DCkCaNLlbZtogle?from=from_copylink)中的2.5

#### 3.2.2 订阅模式修改
- 适用端口：All
- 说明：
  - 将原有的日订阅修改为周订阅
  - 增加订阅模式切换按钮，增加Ultimate订阅模式，Ultimate订阅模式下，用户交互没有限流限制
  - 原说明：Unlimited AI conversations & fate readings. Pick your access plan
  - 修改为：Unlock deeper AI conversations & fate readings. Pick your access plan.
- 订阅方案：
  - Weekly：$6 just $0.85/day，Start for $6，Perfect for a 7-day glimpse into your future。
    - ✅Full access to all AI features — chat, insights, and fate reading
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅No ads for now (may change in future)
  - Monthly：$20 just $0.66/day，Upgrade for $20，Stay aligned. Daily insights for your month ahead。
    - ✅30 days full access to AI chat & fate tools
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅No ads for now (may change in future)
  - Annual：$200 only $0.51/day，Go Annual & Save，Save big & stay connected all year。
    - ✅12-month full access to AI guidance & destiny tools
    - ✅30-day no-questions-asked refund
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅Guaranteed ad-free experience
  - Premium plans have a rate limit of 100 messages per 3 hours.
  - Weekly Ultimate：$60，Start for $60，Perfect for a 7-day glimpse into your future。
    - ✅Full access to all AI features — chat, insights, and fate reading
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅No ads for now (may change in future)
    - ✅No interaction limits
  - Monthly Ultimate：$200，Upgrade for $200，Stay aligned. Daily insights for your month ahead。
    - ✅30 days full access to AI chat & fate tools
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅No ads for now (may change in future)
    - ✅No interaction limits
  - Annual Ultimate：$2000，Go Annual & Save，Save big & stay connected all year。
    - ✅12-month full access to AI guidance & destiny tools
    - ✅30-day no-questions-asked refund
    - ✅Your privacy is protected — no tracking, storing, or training usage.
    - ✅Guaranteed ad-free experience
    - ✅No interaction limits
  - Unlimited subject to abuse guardrails.
- Payment history品类变更（同badge品类）：
  - Weekly Premium
  - Weekly Ultimate
  - Monthly Premium
  - Monthly Ultimate
  - Annual Premium（原Manage Subscription里是Annually Premium）
  - Annual Ultimate
- 订阅badge与时间规则：
  1. 优先显示用户最高等级的订阅badge，有ultimate就显示ultimate，再显示Premium；
  2. 优先使用高等级的时间（Ultimate）；
  3. 同级别的订阅时间会结合，不同级别的订阅时间不会结合；
  4. 只能升级订阅（如果用户订阅了Weekly Ultimate，用户只能升级订阅例如Monthly Ultimate，Annual Ultimate；Premium的所有plan按钮置灰，显示Already on Ultimate）。
    - lv0: Weekly Premium
    - lv1: Monthly Premium
    - lv2: Annual Premium
    - lv3: Weekly Ultimate
    - lv4: Monthly Ultimate
    - lv5: Annual Ultimate
  - 例：
    - 用户先订阅了Weekly Premium，显示Weekly Badge，订阅有效期7天
    - 然后订阅了Annual Premium，显示Annual Badge，订阅有效期（7 + 390）天
    - 然后订阅了Weekly Ultimate，显示Weekly Ultimate Badge，订阅是7天无限，7天过后会变成Annual Premium；优先使用Ultimate时间；
    - 然后订阅了Annual Ultimate，显示Annual Ultimate Badge，订阅是（7+390）天无限

#### 3.2.3 增加用户订阅到期时间显示
- 适用端口：All
- 说明：
  - 未订阅：不显示
  - 已订阅Premium未取消：Your premium plan renews on {January 23,2024}
  - 已订阅Premium已取消：Your premium plan expires on {January 23,2024}
  - 已订阅Ultimate且有Premium剩余时间且未取消：Your ultimate plan renews on {January 23,2024}. After that, your premium plan expires on {January 23,2024}
  - 已订阅Ultimate且有Premium剩余时间且已取消：Your ultimate plan expires on {January 23,2024}. After that, your premium plan expires on {January 23,2024}
  - 已订阅Ultimate无Premium且未取消：Your ultimate plan renews on {January 23,2024}.
  - 已订阅Ultimate无Premium且已取消：Your ultimate plan expires on {January 23,2024}.

### 3.3 App内实现长按复制功能

#### 3.3.1 回复内容内长按复制
- 适用端口：iOS/Android
- 当前问题：iOS/Android App中，长按回复内容无法复制。
- 预期功能：
  - 长按选词：用户长按回复内容时，自动选中离点击位置最近的2个字或1个单词。出现"Copy"按钮，供用户复制选中的内容。
  - 拖动选择：用户可拖动选中范围（向上或向下）扩展或缩小选中文字。拖动时"Copy"按钮暂时隐藏，拖动结束后，"Copy"按钮重新出现。
  - 取消选中：点击已选中的文字，关闭"Copy"按钮；再次点击，打开"Copy"按钮。点击非选中区域，关闭"Copy"按钮，取消选中状态。
  - 点击复制：以纯文本的模式复制用户所选的区域内的内容。
  - Copy
  - Select All（iOS没有，Android有）：点击Select All后选中所有回答，功能框保持打开状态，Select All按钮隐藏
  - Look Up（默认功能）
  - Translate（默认功能）
  - Search Web（默认功能）
  - Share...（默认功能）



