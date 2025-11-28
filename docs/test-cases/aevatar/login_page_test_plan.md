# aevatar.ai 登录页面测试计划

## 1. 测试概述

### 1.1 页面信息
- **页面URL**: http://localhost:5173/login
- **页面标题**: aevatar.ai - The future of on-chain autonomous intelligence
- **测试环境**: localhost:5173
- **测试凭证**: 
  - 邮箱: haylee@test.com
  - 密码: Wh520520!

### 1.2 测试目标
- 验证登录功能的完整性和正确性
- 确保各种输入场景下系统的稳定性
- 验证用户体验的流畅性和友好性
- 检测潜在的安全风险
- 评估页面性能和响应速度

### 1.3 测试范围
- ✅ 邮箱密码登录功能
- ✅ 第三方登录（Google/Github）
- ✅ 表单验证机制
- ✅ 错误提示和用户引导
- ✅ 页面链接跳转
- ✅ UI/UX交互体验
- ✅ 安全防护机制
- ✅ 性能和加载速度

### 1.4 不在测试范围
- ❌ 后端API的单元测试
- ❌ 数据库连接测试
- ❌ 第三方OAuth服务本身的功能
- ❌ 浏览器兼容性测试（本次仅测试Chromium）

---

## 2. 页面元素分析

### 2.1 元素定位映射表

| 元素类型 | 元素名称 | 定位方式 | 定位器 | 元素引用 |
|---------|---------|---------|--------|---------|
| 输入框 | 邮箱输入框 | CSS Selector | `input[type='email']` | ref=e27 |
| 输入框 | 密码输入框 | CSS Selector | `input[type='password']` | ref=e30 |
| 按钮 | 登录按钮 | Text | `button:has-text('Log in')` | ref=e32 |
| 按钮 | Google登录 | Text | `button:has-text('Google')` | ref=e37 |
| 按钮 | Github登录 | Text | `button:has-text('Github')` | ref=e39 |
| 链接 | 注册链接 | Text | `text=Register` | ref=e20 |
| 链接 | 忘记密码 | Text | `text=Forgot Password?` | ref=e33 |
| 链接 | Website链接 | URL | `a[href='https://aevatar.ai']` | ref=e42 |
| 链接 | Github链接 | URL | `a[href*='github.com/aevatarAI']` | ref=e43 |
| 链接 | Docs链接 | URL | `a[href*='whitepaper']` | ref=e44 |
| 标题 | 页面主标题 | Text | `h1:has-text('aevatar.ai')` | ref=e14 |
| 标题 | 登录标题 | Text | `h2:has-text('Login')` | ref=e19 |
| 文本 | 副标题 | Text | `text=The future of on-chain autonomous intelligence` | ref=e15 |

### 2.2 页面对象设计

基于现有的 `LocalhostEmailLoginPage` 类，包含以下核心方法：

```python
class LocalhostEmailLoginPage(BasePage):
    # 元素定位器
    EMAIL_INPUT = "input[type='email']"
    PASSWORD_INPUT = "input[type='password']"
    LOGIN_BUTTON = "button:has-text('Log in')"
    GOOGLE_LOGIN_BUTTON = "button:has-text('Google')"
    GITHUB_LOGIN_BUTTON = "button:has-text('Github')"
    FORGET_PASSWORD_LINK = "text=Forgot Password?"
    SIGNUP_LINK = "text=Register"
    WEBSITE_LINK = "a[href='https://aevatar.ai']"
    GITHUB_LINK = "a[href*='github.com/aevatarAI']"
    DOCS_LINK = "a[href*='whitepaper']"
    ERROR_MESSAGE = ".ant-message, .toast, [role='alert']"
    
    def navigate(self) -> None:
        """导航到登录页面"""
        
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        
    def enter_email(self, email: str) -> bool:
        """输入邮箱"""
        
    def enter_password(self, password: str) -> bool:
        """输入密码"""
        
    def click_login(self) -> bool:
        """点击登录按钮"""
        
    def login(self, email: str, password: str) -> bool:
        """完整登录流程"""
        
    def click_google_login(self) -> bool:
        """点击Google登录"""
        
    def click_github_login(self) -> bool:
        """点击Github登录"""
        
    def click_forget_password(self) -> bool:
        """点击忘记密码链接"""
        
    def click_signup(self) -> bool:
        """点击注册链接"""
        
    def get_error_message(self) -> Optional[str]:
        """获取错误提示信息"""
        
    def is_login_successful(self, timeout: int = 5000) -> bool:
        """判断是否登录成功"""
```

---

## 3. 测试用例设计

### 3.1 功能测试用例

#### TC001: 正常邮箱登录
- **前置条件**: 
  - 用户已注册账号（haylee@test.com / Wh520520!）
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页 http://localhost:5173/login
  2. 在邮箱输入框输入 "haylee@test.com"
  3. 在密码输入框输入 "Wh520520!"
  4. 点击 "Log in" 按钮
  5. 等待页面响应
- **预期结果**:
  - 登录成功，URL跳转到主页/仪表板
  - 不显示任何错误提示
  - 用户登录状态保持
- **优先级**: 🔴 P0 (Critical)
- **标签**: `smoke`, `login`, `critical`

#### TC002: Google第三方登录
- **前置条件**: 
  - Google OAuth服务可用
  - 用户有Google账号
- **测试步骤**:
  1. 访问登录页
  2. 点击 "Google" 按钮
  3. 在弹出窗口中完成Google授权
- **预期结果**:
  - 跳转到Google授权页面
  - 授权成功后返回并登录系统
- **优先级**: 🟡 P1 (High)
- **标签**: `oauth`, `third-party`, `high_priority`

#### TC003: Github第三方登录
- **前置条件**: 
  - Github OAuth服务可用
  - 用户有Github账号
- **测试步骤**:
  1. 访问登录页
  2. 点击 "Github" 按钮
  3. 在弹出窗口中完成Github授权
- **预期结果**:
  - 跳转到Github授权页面
  - 授权成功后返回并登录系统
- **优先级**: 🟡 P1 (High)
- **标签**: `oauth`, `third-party`, `high_priority`

#### TC004: 忘记密码功能
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 点击 "Forgot Password?" 链接
- **预期结果**:
  - 跳转到密码重置页面 或 弹出密码重置对话框
  - 页面/对话框包含邮箱输入框和提交按钮
- **优先级**: 🟡 P1 (High)
- **标签**: `ui`, `navigation`, `medium_priority`

#### TC005: 注册链接跳转
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 点击 "Register" 链接
- **预期结果**:
  - 跳转到注册页面
  - URL包含 "register" 或 "signup"
- **优先级**: 🟡 P1 (High)
- **标签**: `ui`, `navigation`, `medium_priority`

#### TC006: Website链接跳转
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 点击底部 "Website" 链接
- **预期结果**:
  - 在新标签页打开 https://aevatar.ai
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `navigation`, `low_priority`

#### TC007: Github链接跳转
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 点击底部 "Github" 链接
- **预期结果**:
  - 在新标签页打开 https://github.com/aevatarAI
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `navigation`, `low_priority`

#### TC008: Docs链接跳转
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 点击底部 "Docs" 链接
- **预期结果**:
  - 在新标签页打开白皮书PDF文件
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `navigation`, `low_priority`

---

### 3.2 边界测试用例

#### TC011: 空邮箱提交验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 邮箱输入框留空
  3. 输入密码 "Wh520520!"
  4. 点击登录按钮
- **预期结果**:
  - 显示错误提示："请输入邮箱" 或 "Email is required"
  - 表单不提交，停留在登录页
  - 邮箱输入框高亮显示错误状态
- **优先级**: 🟡 P1 (High)
- **标签**: `boundary`, `validation`, `high_priority`

#### TC012: 无效邮箱格式验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试数据**:
  - "invalid-email" (缺少@符号)
  - "test@" (缺少域名)
  - "@domain.com" (缺少用户名)
  - "test@domain" (缺少顶级域名)
  - "test..@domain.com" (连续点号)
- **测试步骤**:
  1. 访问登录页
  2. 输入无效邮箱格式
  3. 输入任意密码
  4. 点击登录按钮
- **预期结果**:
  - 显示错误提示："邮箱格式不正确"
  - 表单不提交
  - 邮箱输入框显示错误状态
- **优先级**: 🟡 P1 (High)
- **标签**: `boundary`, `validation`, `high_priority`

#### TC013: 空密码提交验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入邮箱 "haylee@test.com"
  3. 密码输入框留空
  4. 点击登录按钮
- **预期结果**:
  - 显示错误提示："请输入密码" 或 "Password is required"
  - 表单不提交
  - 密码输入框显示错误状态
- **优先级**: 🟡 P1 (High)
- **标签**: `boundary`, `validation`, `high_priority`

#### TC014: 超长邮箱输入
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入超长邮箱（256字符以上）
  3. 输入密码
  4. 点击登录按钮
- **预期结果**:
  - 系统限制邮箱最大长度 或 显示错误提示
  - 不会造成页面崩溃
- **优先级**: 🟢 P2 (Medium)
- **标签**: `boundary`, `validation`, `medium_priority`

#### TC015: 超长密码输入
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入有效邮箱
  3. 输入超长密码（1000字符以上）
  4. 点击登录按钮
- **预期结果**:
  - 系统限制密码最大长度 或 正常处理
  - 不会造成页面崩溃或性能问题
- **优先级**: 🟢 P2 (Medium)
- **标签**: `boundary`, `validation`, `medium_priority`

#### TC016: 特殊字符邮箱输入
- **前置条件**: 
  - 浏览器已打开登录页
- **测试数据**:
  - "test+tag@domain.com" (加号)
  - "test.name@domain.com" (点号)
  - "test_name@domain.com" (下划线)
- **测试步骤**:
  1. 访问登录页
  2. 输入包含特殊字符但合法的邮箱
  3. 输入密码
  4. 点击登录按钮
- **预期结果**:
  - 系统正确接受合法的特殊字符邮箱
  - 表单正常提交
- **优先级**: 🟢 P2 (Medium)
- **标签**: `boundary`, `validation`, `medium_priority`

---

### 3.3 异常测试用例

#### TC021: 错误密码登录验证
- **前置条件**: 
  - 用户已注册（haylee@test.com）
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入正确邮箱 "haylee@test.com"
  3. 输入错误密码 "WrongPassword123!"
  4. 点击登录按钮
  5. 等待服务器响应
- **预期结果**:
  - 显示错误提示："密码错误" 或 "Invalid password"
  - 登录失败，停留在登录页
  - 不暴露任何敏感信息（如用户是否存在）
- **优先级**: 🔴 P0 (Critical)
- **标签**: `exception`, `security`, `critical`

#### TC022: 未注册邮箱登录验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入未注册邮箱 "nonexistent@test.com"
  3. 输入任意密码 "AnyPassword123!"
  4. 点击登录按钮
- **预期结果**:
  - 显示错误提示："邮箱或密码错误" (不明确指出邮箱未注册，保护用户隐私)
  - 登录失败，停留在登录页
- **优先级**: 🟡 P1 (High)
- **标签**: `exception`, `security`, `high_priority`

#### TC023: 多次登录失败锁定测试
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 使用错误密码连续尝试登录5次
  3. 第6次尝试登录
- **预期结果**:
  - 第5次失败后显示警告："尝试次数过多"
  - 第6次提示账号被暂时锁定
  - 提供锁定时长信息（如"请15分钟后重试"）
- **优先级**: 🟡 P1 (High)
- **标签**: `exception`, `security`, `high_priority`

#### TC024: 网络断开场景测试
- **前置条件**: 
  - 浏览器已打开登录页
  - 通过开发者工具模拟离线状态
- **测试步骤**:
  1. 访问登录页（页面已缓存）
  2. 断开网络连接
  3. 输入有效凭证
  4. 点击登录按钮
- **预期结果**:
  - 显示网络错误提示："网络连接失败，请检查网络"
  - 不会造成页面崩溃
  - 提供重试选项
- **优先级**: 🟢 P2 (Medium)
- **标签**: `exception`, `network`, `medium_priority`

#### TC025: 服务器500错误处理
- **前置条件**: 
  - 模拟后端返回500错误
- **测试步骤**:
  1. 访问登录页
  2. 输入有效凭证
  3. 点击登录（后端返回500错误）
- **预期结果**:
  - 显示友好的错误提示："服务器错误，请稍后重试"
  - 不暴露技术细节或堆栈信息
  - 提供联系支持的方式
- **优先级**: 🟡 P1 (High)
- **标签**: `exception`, `error_handling`, `high_priority`

---

### 3.4 UI/UX测试用例

#### TC031: 密码默认隐藏验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 在密码框输入密码
  3. 检查密码显示状态
- **预期结果**:
  - 密码默认以 "•••" 或 "***" 形式隐藏显示
  - input type="password"
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `ux`, `medium_priority`

#### TC032: Tab键切换焦点
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 使用Tab键在元素间切换
  3. 观察焦点顺序
- **预期结果**:
  - 焦点顺序：邮箱 → 密码 → 登录按钮 → 忘记密码 → Google → Github → 注册
  - 当前焦点元素有明显视觉反馈（高亮边框）
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `accessibility`, `medium_priority`

#### TC033: Enter键提交登录
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入邮箱和密码
  3. 在密码框按下Enter键
- **预期结果**:
  - 触发登录提交，等同于点击登录按钮
  - 表单正常提交
- **优先级**: 🟡 P1 (High)
- **标签**: `ui`, `ux`, `high_priority`

#### TC034: 错误提示显示和消失
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入错误凭证触发错误提示
  3. 观察错误提示显示时长
  4. 修改输入内容
- **预期结果**:
  - 错误提示以Toast或Alert形式显示
  - 3-5秒后自动消失 或 用户修改输入时消失
  - 错误提示位置明显但不遮挡关键内容
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `ux`, `medium_priority`

#### TC035: 响应式设计验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 在不同屏幕尺寸下访问登录页
     - 桌面: 1920x1080
     - 平板: 768x1024
     - 手机: 375x667
  2. 检查页面布局
- **预期结果**:
  - 所有元素在不同屏幕下正确显示
  - 移动端不出现横向滚动条
  - 文字大小和间距适配屏幕
  - 按钮和输入框大小适合触控操作
- **优先级**: 🟡 P1 (High)
- **标签**: `ui`, `responsive`, `high_priority`

#### TC036: 加载状态提示
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入有效凭证
  3. 点击登录按钮
  4. 观察提交过程中的UI状态
- **预期结果**:
  - 点击登录后按钮显示加载状态（loading图标或文字变化）
  - 按钮变为禁用状态，防止重复提交
  - 加载期间光标变为等待状态
- **优先级**: 🟢 P2 (Medium)
- **标签**: `ui`, `ux`, `medium_priority`

---

### 3.5 安全测试用例

#### TC041: SQL注入攻击防护
- **前置条件**: 
  - 浏览器已打开登录页
- **测试数据**:
  - `admin' OR '1'='1`
  - `admin'--`
  - `' OR '1'='1' --`
  - `admin' DROP TABLE users--`
- **测试步骤**:
  1. 访问登录页
  2. 在邮箱框输入SQL注入测试语句
  3. 输入任意密码
  4. 点击登录按钮
- **预期结果**:
  - 系统拒绝登录
  - SQL语句被转义或过滤，不执行
  - 不暴露数据库结构信息
  - 登录失败日志被记录
- **优先级**: 🔴 P0 (Critical)
- **标签**: `security`, `injection`, `critical`

#### TC042: XSS跨站脚本攻击防护
- **前置条件**: 
  - 浏览器已打开登录页
- **测试数据**:
  - `<script>alert('XSS')</script>`
  - `<img src=x onerror=alert('XSS')>`
  - `javascript:alert('XSS')`
  - `<svg onload=alert('XSS')>`
- **测试步骤**:
  1. 访问登录页
  2. 在邮箱或密码框输入XSS攻击代码
  3. 点击登录按钮
  4. 观察页面是否执行脚本
- **预期结果**:
  - 脚本不被执行
  - 输入被HTML转义显示（如 `&lt;script&gt;`）
  - 不弹出alert对话框
  - 页面不被劫持
- **优先级**: 🔴 P0 (Critical)
- **标签**: `security`, `xss`, `critical`

#### TC043: CSRF跨站请求伪造防护
- **前置条件**: 
  - 用户已在系统中登录
  - 模拟外部站点发起登录请求
- **测试步骤**:
  1. 用户登录系统
  2. 从外部页面构造登录请求
  3. 尝试绕过同源策略提交
- **预期结果**:
  - 请求被拒绝
  - 系统检查CSRF Token或Origin header
  - 返回403 Forbidden或相关错误
- **优先级**: 🟡 P1 (High)
- **标签**: `security`, `csrf`, `high_priority`

#### TC044: 密码明文传输检测
- **前置条件**: 
  - 浏览器已打开登录页
  - 开启浏览器开发者工具Network面板
- **测试步骤**:
  1. 访问登录页
  2. 输入有效凭证
  3. 点击登录
  4. 查看Network请求内容
- **预期结果**:
  - 密码在传输前被加密（Hash）
  - 使用HTTPS协议传输
  - Network面板中看不到明文密码
  - Request Payload中密码字段为密文
- **优先级**: 🔴 P0 (Critical)
- **标签**: `security`, `encryption`, `critical`

#### TC045: 敏感信息泄露检测
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 输入错误凭证
  3. 查看错误提示内容
  4. 查看页面源代码和控制台
- **预期结果**:
  - 错误提示模糊化（不区分邮箱不存在还是密码错误）
  - 页面源代码不包含敏感配置信息
  - 控制台不输出敏感调试信息
  - HTTP响应头不暴露服务器版本信息
- **优先级**: 🟡 P1 (High)
- **标签**: `security`, `information_leak`, `high_priority`

---

### 3.6 性能测试用例

#### TC051: 页面加载时间测试
- **前置条件**: 
  - 清除浏览器缓存
  - 网络状况良好
- **测试步骤**:
  1. 访问登录页 http://localhost:5173/login
  2. 记录页面完全加载时间
  3. 使用Performance API或Lighthouse测试
- **预期结果**:
  - 首屏加载时间 < 2秒
  - DOMContentLoaded < 1秒
  - 所有资源加载完成 < 3秒
  - Lighthouse性能评分 > 90分
- **优先级**: 🟢 P2 (Medium)
- **标签**: `performance`, `load_time`, `medium_priority`

#### TC052: 登录请求响应时间
- **前置条件**: 
  - 浏览器已打开登录页
  - 网络状况良好
- **测试步骤**:
  1. 输入有效凭证
  2. 点击登录按钮
  3. 记录从点击到收到响应的时间
- **预期结果**:
  - 登录API响应时间 < 1秒
  - 前端处理和页面跳转 < 500ms
  - 总体登录流程 < 2秒
- **优先级**: 🟢 P2 (Medium)
- **标签**: `performance`, `api_response`, `medium_priority`

#### TC053: 并发登录测试
- **前置条件**: 
  - 准备多个测试账号
- **测试步骤**:
  1. 模拟10个用户同时登录
  2. 观察系统响应时间
  3. 检查是否有登录失败
- **预期结果**:
  - 所有用户都能成功登录
  - 响应时间不超过正常情况的2倍
  - 服务器不出现崩溃或错误
  - 数据库连接池正常工作
- **优先级**: 🟢 P2 (Medium)
- **标签**: `performance`, `concurrency`, `medium_priority`

#### TC054: 资源优化验证
- **前置条件**: 
  - 浏览器已打开登录页
- **测试步骤**:
  1. 访问登录页
  2. 检查Network面板
  3. 分析资源加载情况
- **预期结果**:
  - 图片使用WebP或优化格式
  - CSS和JS文件已压缩（minified）
  - 启用Gzip或Brotli压缩
  - 静态资源使用CDN加速
  - 合理使用缓存策略（Cache-Control）
- **优先级**: 🟢 P2 (Medium)
- **标签**: `performance`, `optimization`, `medium_priority`

---

## 4. 测试数据设计

### 4.1 测试数据文件
文件位置: `/test-data/aevatar/localhost_login_data.json`

```json
{
  "valid_users": [
    {
      "email": "haylee@test.com",
      "password": "Wh520520!",
      "description": "有效用户-主测试账号"
    }
  ],
  "invalid_passwords": [
    {
      "email": "haylee@test.com",
      "password": "WrongPassword123!",
      "expected_error": "邮箱或密码错误"
    }
  ],
  "unregistered_users": [
    {
      "email": "nonexistent@test.com",
      "password": "AnyPassword123!",
      "expected_error": "邮箱或密码错误"
    }
  ],
  "invalid_email_formats": [
    {
      "email": "invalid-email",
      "password": "TestPassword123!",
      "expected_error": "邮箱格式不正确"
    },
    {
      "email": "test@",
      "password": "TestPassword123!",
      "expected_error": "邮箱格式不正确"
    },
    {
      "email": "@domain.com",
      "password": "TestPassword123!",
      "expected_error": "邮箱格式不正确"
    }
  ],
  "boundary_data": {
    "empty_email": {
      "email": "",
      "password": "TestPassword123!",
      "expected_error": "请输入邮箱"
    },
    "empty_password": {
      "email": "haylee@test.com",
      "password": "",
      "expected_error": "请输入密码"
    },
    "long_email": {
      "email": "a".repeat(250) + "@test.com",
      "password": "TestPassword123!",
      "expected_behavior": "限制长度或正常处理"
    },
    "long_password": {
      "email": "haylee@test.com",
      "password": "A".repeat(1000),
      "expected_behavior": "限制长度或正常处理"
    }
  },
  "security_test_data": {
    "sql_injection": [
      "admin' OR '1'='1",
      "admin'--",
      "' OR '1'='1' --",
      "admin' DROP TABLE users--"
    ],
    "xss_payloads": [
      "<script>alert('XSS')</script>",
      "<img src=x onerror=alert('XSS')>",
      "javascript:alert('XSS')",
      "<svg onload=alert('XSS')>"
    ]
  },
  "third_party_logins": {
    "google": {
      "provider": "google",
      "expected_redirect": "accounts.google.com"
    },
    "github": {
      "provider": "github",
      "expected_redirect": "github.com/login"
    }
  }
}
```

---

## 5. 自动化实现建议

### 5.1 页面对象类实现

**文件位置**: `pages/aevatar/localhost_email_login_page.py`

已存在完整的页面对象类，建议扩展以下方法：

```python
def click_google_login(self) -> bool:
    """点击Google登录按钮"""
    try:
        logger.info("点击Google登录按钮")
        self.page.click(self.GOOGLE_LOGIN_BUTTON)
        self.page.wait_for_timeout(2000)
        return True
    except Exception as e:
        logger.error(f"点击Google登录失败: {str(e)}")
        return False

def click_github_login(self) -> bool:
    """点击Github登录按钮"""
    try:
        logger.info("点击Github登录按钮")
        self.page.click(self.GITHUB_LOGIN_BUTTON)
        self.page.wait_for_timeout(2000)
        return True
    except Exception as e:
        logger.error(f"点击Github登录失败: {str(e)}")
        return False

def click_website_link(self) -> bool:
    """点击Website链接"""
    try:
        logger.info("点击Website链接")
        with self.page.expect_popup() as popup_info:
            self.page.click(self.WEBSITE_LINK)
        popup = popup_info.value
        logger.info(f"新标签页URL: {popup.url}")
        return True
    except Exception as e:
        logger.error(f"点击Website链接失败: {str(e)}")
        return False

def get_loading_state(self) -> bool:
    """检查登录按钮是否处于加载状态"""
    try:
        button = self.page.locator(self.LOGIN_BUTTON).first
        is_disabled = button.is_disabled()
        aria_busy = button.get_attribute("aria-busy")
        return is_disabled or aria_busy == "true"
    except Exception as e:
        logger.error(f"检查加载状态失败: {str(e)}")
        return False
```

### 5.2 测试类实现

**文件位置**: `tests/aevatar/test_login.py`

已存在测试类 `TestLocalhostLogin`，建议补充以下测试方法：

```python
@pytest.mark.oauth
@pytest.mark.high_priority
@allure.title("TC002: Google第三方登录")
def test_tc002_google_login(self):
    """TC002: 验证Google登录功能"""
    self.login_page.navigate()
    assert self.login_page.is_loaded()
    
    # 点击Google登录并验证跳转
    with self.page.expect_popup() as popup_info:
        self.login_page.click_google_login()
    popup = popup_info.value
    assert "accounts.google.com" in popup.url
    logger.info("✅ Google登录跳转成功")

@pytest.mark.performance
@pytest.mark.medium_priority
@allure.title("TC051: 页面加载性能测试")
def test_tc051_page_load_performance(self):
    """TC051: 验证登录页加载性能"""
    import time
    start_time = time.time()
    self.login_page.navigate()
    load_time = time.time() - start_time
    
    assert load_time < 2.0, f"页面加载时间过长: {load_time:.2f}秒"
    logger.info(f"✅ 页面加载时间: {load_time:.2f}秒")

@pytest.mark.ui
@pytest.mark.high_priority
@allure.title("TC033: Enter键提交登录")
def test_tc033_enter_key_submit(self):
    """TC033: 验证Enter键提交功能"""
    self.login_page.navigate()
    self.login_page.enter_email("haylee@test.com")
    self.login_page.enter_password("Wh520520!")
    
    # 在密码框按Enter键
    self.page.locator(self.login_page.PASSWORD_INPUT).press("Enter")
    self.page.wait_for_timeout(2000)
    
    # 验证登录提交
    assert self.login_page.is_login_successful() or self.login_page.get_error_message()
    logger.info("✅ Enter键提交功能正常")
```

### 5.3 配置建议

#### pytest.ini 标记配置
```ini
[pytest]
markers =
    smoke: 冒烟测试
    login: 登录功能测试
    oauth: 第三方登录测试
    boundary: 边界测试
    exception: 异常场景测试
    security: 安全测试
    performance: 性能测试
    ui: UI/UX测试
    critical: P0优先级
    high_priority: P1优先级
    medium_priority: P2优先级
    low_priority: P3优先级
```

#### 运行命令示例
```bash
# 运行所有登录测试
pytest tests/aevatar/test_login.py -v

# 仅运行冒烟测试
pytest tests/aevatar/test_login.py -m smoke

# 运行高优先级测试
pytest tests/aevatar/test_login.py -m "critical or high_priority"

# 运行安全测试
pytest tests/aevatar/test_login.py -m security

# 生成Allure报告
pytest tests/aevatar/test_login.py --alluredir=allure-results
allure serve allure-results
```

---

## 6. 执行计划

### 6.1 测试阶段划分

#### 阶段1: 核心功能验证（P0）- 预计1天
- ✅ TC001: 正常邮箱登录
- ✅ TC021: 错误密码登录验证
- ✅ TC041: SQL注入攻击防护
- ✅ TC042: XSS跨站脚本攻击防护
- ✅ TC044: 密码明文传输检测

#### 阶段2: 完整功能测试（P1）- 预计2天
- ✅ TC002-TC008: 第三方登录和链接跳转
- ✅ TC011-TC013: 边界测试（空输入、格式验证）
- ✅ TC022-TC023: 异常场景测试
- ✅ TC033: Enter键提交
- ✅ TC035: 响应式设计验证
- ✅ TC043: CSRF防护测试
- ✅ TC045: 敏感信息泄露检测

#### 阶段3: 补充测试（P2）- 预计1天
- ✅ TC014-TC016: 边界测试（超长输入、特殊字符）
- ✅ TC024-TC025: 网络异常和服务器错误
- ✅ TC031-TC032, TC034, TC036: UI/UX细节测试
- ✅ TC051-TC054: 性能测试

### 6.2 人力资源安排
- **测试工程师**: 1人
- **开发支持**: 0.5人（修复缺陷）
- **自动化工程师**: 1人（编写和维护自动化脚本）

### 6.3 环境要求
- **测试环境**: localhost:5173
- **浏览器**: Chromium (Playwright默认)
- **Python版本**: 3.8+
- **依赖包**: 见 requirements.txt

### 6.4 验收标准

#### 功能验收标准
- ✅ 所有P0测试用例100%通过
- ✅ 所有P1测试用例通过率 ≥ 95%
- ✅ 所有P2测试用例通过率 ≥ 90%
- ✅ 无阻塞性缺陷
- ✅ 所有高危安全漏洞已修复

#### 性能验收标准
- ✅ 页面首屏加载时间 < 2秒
- ✅ 登录API响应时间 < 1秒
- ✅ Lighthouse性能评分 > 90分
- ✅ 10并发用户场景下系统稳定

#### 安全验收标准
- ✅ 无SQL注入漏洞
- ✅ 无XSS跨站脚本漏洞
- ✅ 密码加密传输
- ✅ CSRF防护机制有效
- ✅ 敏感信息不泄露

#### 自动化验收标准
- ✅ P0和P1用例100%自动化
- ✅ 自动化脚本执行成功率 ≥ 95%
- ✅ 单次完整回归测试耗时 < 15分钟
- ✅ CI/CD集成完成

---

## 7. 风险评估

### 7.1 技术风险
| 风险项 | 风险等级 | 应对措施 |
|--------|---------|---------|
| 第三方OAuth服务不稳定 | 中 | Mock第三方响应，减少依赖 |
| 网络环境不稳定 | 低 | 增加重试机制和超时处理 |
| 浏览器兼容性问题 | 低 | 本次仅测试Chromium，后续扩展 |

### 7.2 项目风险
| 风险项 | 风险等级 | 应对措施 |
|--------|---------|---------|
| 测试数据不足 | 低 | 提前准备测试账号和数据 |
| 测试环境不稳定 | 中 | 建立独立测试环境 |
| 自动化脚本维护成本高 | 中 | 采用Page Object模式，降低维护成本 |

---

## 8. 附录

### 8.1 相关文档
- 页面对象类: `pages/aevatar/localhost_email_login_page.py`
- 测试类: `tests/aevatar/test_login.py`
- 测试数据: `test-data/aevatar/localhost_login_data.json`
- 基类: `pages/base_page.py`
- 工具类: `utils/page_utils.py`, `utils/logger.py`

### 8.2 测试报告
- Allure报告: `allure-report/index.html`
- 截图目录: `reports/screenshots/`
- 日志目录: `logs/`

### 8.3 联系方式
- **测试负责人**: [待定]
- **开发负责人**: [待定]
- **问题反馈**: [待定]

---

## 9. 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|------|------|---------|--------|
| 2025-11-27 | v2.0 | 基于页面快照重新生成完整测试计划 | HyperEcho |
| [日期] | v1.0 | 初始版本 | [作者] |

---

**文档状态**: ✅ 已完成  
**最后更新**: 2025-11-27  
**下一步行动**: 开始执行阶段1（P0核心功能验证）
