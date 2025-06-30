# GodGPT V1.2.0

## 1. 版本信息
- 版本号：V1.2.0
- 创建日期：2025.3.21
- 产品负责人：Tonio

## 2. 项目背景
- 基于 V1.1.0版本的优化

## 3. 需求详情
### 3.1 产品优化
- 增加APK下载链接、iOS公式展示问题、消息输入框样式、行距、分割线、数据追踪等。

### 3.2 bug处理
- Apple ID登录、并发问题等修复。

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | APK下载 | 增加APK下载链接 | web端 |
| 2    | 公式展示 | iOS公式展示兼容与优化 | iOS |
| 3    | 输入框样式 | 消息输入框样式优化 | All |
| 4    | 行距 | 显示行距优化 | All |
| 5    | 分割线 | web端分割线颜色调整 | web端 |
| 6    | 数据追踪 | Webpage端用户数据追踪 | web端 |
| 7    | Apple ID登录 | Apple ID登录问题修复 | All |
| 8    | 并发问题 | 并发压测与优化 | All |

## 5. 流程/用例/伪代码
- 无

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 无

## 8. UI/原型
- Web设计：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=778-3681&t=Gsapb7XPO0Nm92lF-1
- App设计：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=724-2598&t=Gsapb7XPO0Nm92lF-1

## 9. 变更记录
- 暂无

一、 版本信息
版本号：V1.2.0
创建日期: 2025.3.21
产品负责人：Tonio
二、项目背景
基于 V1.1.0版本的优化

三、需求详情
产品优化
序号
说明
截图
备注
1. 增加 APK 下载链接

web端
鼠标悬浮至Get App按钮后显示
"Get iOS App"
https://apps.apple.com/us/app/godgpt/id6743791875
"Get Android APK"
https://godgpt-download.portkey.finance/android/godgpt-v1.1.0.apk

[图片]

[图片]

2. iOS 里面公式展示问题

由于支持流式响应后，文字逐段输出，无法保证公式能被正确解析和渲染，目前仍需解决方案。

还引起过多空行+无空行的问题：公式展示的时候进行的调整导致，在公式展示完成之后可再校验

Markdown转译格式见：Markdown转译格式

[图片]
目前可能的解决方案：@Huaya Hu 
"后端在返给文本的时候，就要考虑到把能简单处理的先处理一遍，然后再返给前端。然后前端再去专注于匹配公式，把公式正常渲染，这样的话能防止在前端同时处理Markdown、case、Latex的这三种文本的时候，它们交叉的影响."
4. 发送消息框

消息输入框不悬浮

Web端输入框：
距底部边距：24px
高度：90px
宽度：最大800px（对话文字整体宽度也是800px）
屏幕宽度小于848，则跟随屏幕宽度适配，左右边距固定24px
圆角：24

App端输入框：
高度：90px
宽度：跟随手机宽度适配（左右边距10px）
圆角：24

具体查看设计稿
Web：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=778-3681&t=Gsapb7XPO0Nm92lF-1
App：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=724-2598&t=Gsapb7XPO0Nm92lF-1
[图片]

[图片]
@Leon Zhang @Fred Tran 

5. 显示行距

Web端：
字体与大小：Archivo，16px
行高：24px
段落间距：20px(与开发沟通，由于LLM默认，不太好改，暂不修改）
同步优化发送者文字框样式，按照设计稿

App端：
同Web端

[图片]

@Huaya Hu 
6. web端分割线

回答文案中的分割线颜色改为：#636363
1px 线粗细

[图片]
@Huaya Hu 
7. Webpage data tracking
实现webpage 端用户数据跟踪

@Fred Tran 

bug处理
序号
说明
截图
备注
1. 解决 Apple ID 登录问题

PC web端/Mobile web端/iOS APP端
使用Apple ID登录无法登录
[图片]


2. 解决并发问题
宣传需要，需要对产品进行压测
Godgpt压测压测结果来看，50个用户同时访问时，创建session时常过长
[图片]


