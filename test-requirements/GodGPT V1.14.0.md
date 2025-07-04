# GodGPT V1.14.0

## 1. 版本信息
- 版本号：V1.14.0
- 创建日期：2025.5.6
- 产品负责人：Tonio

## 2. 项目背景
- 将iOS和Android更新至webapp最新版本，后端迁移，强制更新（老用户+新用户）

## 3. 需求详情
### 3.1 全局优化
- iOS/Android页面背景色、输入框、Suggest、导航栏等统一优化
- 回复消息菜单栏优化，发送消息框背景色、Copy & Copied状态
- 侧边栏优化，按时间分组显示历史会话，最多本地缓存100条，超出顺序覆盖
- 侧边栏宽度、背景色、menu icon长按、Title超长省略、滚动轴等细节优化
- 一键回到底部、profile页面优化、sharelink功能调试、http请求接口调整、模型切换优先gpt 4o-latest
- 渲染适配，包括字体、行间距、公式渲染、逐字渲染等

### 3.2 后端迁移与强制更新
- 后端迁移（SignalR --> http），便于后续版本管理和维护
- 增加强制更新功能，用户打开APP时检测版本，低于最低要求则弹窗提示并引导更新
- 动态配置最低版本号和提示内容，便于快速调整

## 4. 详细需求列表
| 序号 | 功能点 | 需求描述 | 备注 |
|------|--------|----------|------|
| 1    | 全局优化 | 页面、输入框、导航栏、菜单栏等统一 | [图片] |
| 2    | 侧边栏 | 时间分组、宽度、滚动、缓存等 | [图片] |
| 3    | 一键回到底部 | 快捷操作 | [图片] |
| 4    | profile页面 | 优化展示 | [图片] |
| 5    | sharelink | 功能调试 | [图片] |
| 6    | http请求 | 接口调整 | 无 |
| 7    | 模型切换 | 优先gpt 4o-latest | 无 |
| 8    | 渲染适配 | 字体、行间距、公式等 | 无 |
| 9    | 强制更新 | 低版本弹窗提示并引导 | 无 |

## 5. 流程/用例/伪代码
- 参考Figma设计稿：https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-19021&m=dev

## 6. 埋点/数据
- 无

## 7. 兼容性/异常/边界说明
- 保证本地缓存、接口、强制更新等在iOS/Android一致

## 8. UI/原型
- [图片]
- https://www.figma.com/design/eXNLz0INx6G6Zif0DYlRZA/GodGPT?node-id=1666-19021&m=dev

## 9. 变更记录
- 暂无
