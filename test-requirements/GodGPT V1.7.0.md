# GodGPT V1.7.0

## 1. 版本信息
- 版本号：V1.7.0
- 创建日期：2025.4.15
- 产品负责人：Tonio

## 2. 项目背景
- 基于V1.6.0产品优化

## 3. 需求详情
### 3.1 产品优化
- 侧边栏优化、Profile弹框优化等

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 侧边栏优化 | 会话分组、宽度、滚动、缓存、菜单等 | All |
| 2    | Profile弹框 | Profile弹窗位置与交互优化 | Web |

## 5. 流程/用例/伪代码
- 详见设计稿：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-19021&m=dev

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 无

## 8. UI/原型
- 设计稿：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-19021&m=dev
- https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-20790&m=dev

## 9. 变更记录
- 暂无

一、 版本信息
版本号：V1.7.0
创建日期: 2025.4.15
产品负责人：Tonio
二、项目背景
- 基于V1.6.0产品优化
三、需求详情
产品优化
序号
适用端口
说明
截图
备注
1. 侧边栏优化

All

1. 没有会话的时候会显示 "No Chats As you talk with GodGPT, your conversations will appear here. "
2. 侧边栏打开后按照时间由近及远显示当前用户所有的会话
按照时间分为
  1. Today
  2. Previous 7 Days 【前7天，今天）
  3. Previous 30 Days 【前30天，前7天）
  4. 30 Days Ago 
3. 侧边栏背景色调整
4. 侧边栏宽度调整
（mobile端）Title右侧menu icon改为长按
（Web端）Title右侧menu icon 改为hover时显示（由于技术原因不太好处理）  维持不变
5. Title 文字超长省略方式，在最右侧渐隐，（固定显示宽度，超出最右侧渐变遮盖)
具体参考设计稿：
https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-19021&m=dev

6. Rename点击后，用户输入完毕后点击回车或者点击侧边栏范围内，侧边栏不关闭；光标自动到末尾
7. 用户点击delete后，侧边栏不关闭
8. 侧边栏的历史消息应该保存到浏览器本地缓存,本地缓存最多保存100条会话记录，超出后按时间顺序覆盖最早记录
9. 用户每开一个新的会话需要更新本地的记录
10. 侧边栏滚动轴

[图片]
[图片]
[图片]

[图片]
[图片]
[图片]
[图片]

2. web端Profile弹框优化

PC Webpage

Profile弹窗改为在左下角/右上角弹出的小弹窗，点击Profile 任意按钮，弹框消失
具体看设计稿：
https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-20790&m=dev

[图片]


