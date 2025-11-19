# aevatar.ai 登录页面测试计划

## 1. 页面概述

### 1.1 基本信息
- **页面URL**: http://localhost:5173/login
- **页面标题**: aevatar station frontend
- **页面用途**: 用户登录认证入口
- **测试账户**: haylee@test.com / Wh520520!

### 1.2 功能描述
aevatar.ai登录页面是系统的入口页面，提供多种登录方式：
- 邮箱密码登录
- Google第三方登录
- Github第三方登录
- 注册入口
- 密码重置功能

## 2. 页面元素映射

### 2.1 元素定位表

| 元素类型 | 元素名称 | 定位方式 | 定位器 |
|---------|---------|---------|--------|
| 标题 | 页面主标题 | Role | `role=heading[name='aevatar.ai']` |
| 文本 | 页面副标题 | Text | `text=The future of on-chain` |
| 输入框 | 邮箱输入框 | Placeholder | `input[placeholder='Enter your email']` |
| 输入框 | 密码输入框 | Type | `input[type='password']` |
| 按钮 | 登录按钮 | Text | `button:has-text('Log in')` |
| 链接 | 注册链接 | Text | `text=Register` |
| 链接 | 忘记密码链接 | Text | `text=Forgot Password?` |
| 按钮 | Google登录按钮 | Text | `button:has-text('Google')` |
| 按钮 | Github登录按钮 | Text | `button:has-text('Github')` |
| 链接 | 官网链接 | URL | `link:has-text('Website')` |
| 链接 | Github链接 | URL | `link:has-text('Github')` |
| 链接 | 文档链接 | URL | `link:has-text('Docs')` |

### 2.2 页面对象设计

```python
class AevatarLoginPage(BasePage):
    """aevatar.ai登录页面对象"""
    
    # 页面URL
    LOGIN_URL = "http://localhost:5173/login"
    
    # 页面元素定位器
    PAGE_TITLE = "role=heading[name='aevatar.ai']"
    PAGE_SUBTITLE = "text=The future of on-chain"
    
    # 登录表单
    EMAIL_INPUT = "input[placeholder='Enter your email']"
    PASSWORD_INPUT = "input[type='password']"
    LOGIN_BUTTON = "button:has-text('Log in')"
    
    # 链接和按钮
    REGISTER_LINK = "text=Register"
    FORGOT_PASSWORD_LINK = "text=Forgot Password?"
    GOOGLE_LOGIN_BUTTON = "button:has-text('Google')"
    GITHUB_LOGIN_BUTTON = "button:has-text('Github')"
    
    # 错误提示
    ERROR_MESSAGE = ".error-message, [role='alert']"
    
    def navigate(self):
        """导航到登录页面"""
        self.page.goto(self.LOGIN_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查登录页面是否已加载"""
        try:
            self.page.wait_for_selector(self.PAGE_TITLE, timeout=5000)
            return True
        except:
            return False
    
    def login_with_email(self, email: str, password: str):
        """使用邮箱和密码登录"""
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(2000)
```

## 3. 测试用例设计

### 3.1 P0级测试用例（核心功能）

#### TC-LOGIN-P0-001: 正常登录流程
- **优先级**: P0
- **前置条件**: 
  - 浏览器已打开登录页面
  - 测试账户：haylee@test.com / Wh520520!
- **测试步骤**:
  1. 访问登录页面 http://localhost:5173/login
  2. 在邮箱输入框输入 "haylee@test.com"
  3. 在密码输入框输入 "Wh520520!"
  4. 点击"Log in"按钮
- **预期结果**: 
  - 登录成功，跳转到 /dashboard/workflows 页面
  - 页面显示用户工作空间
- **测试数据**: `valid_users` in `localhost_login_data.json`

#### TC-LOGIN-P0-002: 错误密码登录
- **优先级**: P0
- **前置条件**: 浏览器已打开登录页面
- **测试步骤**:
  1. 访问登录页面
  2. 在邮箱输入框输入 "haylee@test.com"
  3. 在密码输入框输入错误密码 "WrongPassword123!"
  4. 点击"Log in"按钮
- **预期结果**: 
  - 登录失败，停留在登录页面
  - 显示错误提示信息（密码错误相关）
- **测试数据**: `invalid_passwords` in `localhost_login_data.json`

#### TC-LOGIN-P0-003: 空邮箱登录
- **优先级**: P0
- **前置条件**: 浏览器已打开登录页面
- **测试步骤**:
  1. 访问登录页面
  2. 邮箱输入框保持为空
  3. 在密码输入框输入 "Wh520520!"
  4. 点击"Log in"按钮
- **预期结果**: 
  - 登录失败
  - 显示"邮箱为必填项"或类似提示
- **测试数据**: `invalid_emails` (empty email)

#### TC-LOGIN-P0-004: 空密码登录
- **优先级**: P0
- **前置条件**: 浏览器已打开登录页面
- **测试步骤**:
  1. 访问登录页面
  2. 在邮箱输入框输入 "haylee@test.com"
  3. 密码输入框保持为空
  4. 点击"Log in"按钮
- **预期结果**: 
  - 登录失败
  - 显示"密码为必填项"或类似提示
- **测试数据**: `invalid_passwords` (empty password)

#### TC-LOGIN-P0-005: 登录按钮状态验证
- **优先级**: P0
- **前置条件**: 浏览器已打开登录页面
- **测试步骤**:
  1. 访问登录页面
  2. 检查登录按钮初始状态
  3. 输入有效邮箱和密码
  4. 再次检查登录按钮状态
- **预期结果**: 
  - 登录按钮始终可点击（或根据输入状态动态变化）

### 3.2 P1级测试用例（重要功能）

#### TC-LOGIN-P1-001: 无效邮箱格式
- **优先级**: P1
- **测试步骤**:
  1. 输入无效邮箱格式（如 "invalid-email"）
  2. 输入有效密码
  3. 点击登录按钮
- **预期结果**: 
  - 显示"邮箱格式不正确"提示
- **测试数据**: 
  ```json
  ["invalid-email", "test@", "@domain.com", "test @domain.com"]
  ```

#### TC-LOGIN-P1-002: 不存在的账户登录
- **优先级**: P1
- **测试步骤**:
  1. 输入未注册的邮箱 "nonexistent@test.com"
  2. 输入任意密码
  3. 点击登录按钮
- **预期结果**: 
  - 显示"用户不存在"或"邮箱或密码错误"提示
- **测试数据**: `unregistered_users`

#### TC-LOGIN-P1-003: 注册链接跳转
- **优先级**: P1
- **测试步骤**:
  1. 访问登录页面
  2. 点击"Register"链接
- **预期结果**: 
  - 跳转到注册页面

#### TC-LOGIN-P1-004: 忘记密码链接
- **优先级**: P1
- **测试步骤**:
  1. 访问登录页面
  2. 点击"Forgot Password?"链接
- **预期结果**: 
  - 跳转到密码重置页面或显示密码重置对话框

#### TC-LOGIN-P1-005: 邮箱大小写敏感性
- **优先级**: P1
- **测试步骤**:
  1. 使用大写邮箱 "HAYLEE@TEST.COM" 登录
  2. 使用混合大小写 "Haylee@Test.com" 登录
- **预期结果**: 
  - 根据系统设计，验证邮箱是否大小写敏感
- **测试数据**: `case_sensitivity_tests`

#### TC-LOGIN-P1-006: 底部链接验证
- **优先级**: P1
- **测试步骤**:
  1. 点击"Website"链接
  2. 点击"Github"链接
  3. 点击"Docs"链接
- **预期结果**: 
  - Website: 跳转到 https://aevatar.ai
  - Github: 跳转到 https://github.com/aevatarAI
  - Docs: 打开白皮书PDF

### 3.3 P2级测试用例（边界与安全）

#### TC-LOGIN-P2-001: 边界值测试 - 超长密码
- **优先级**: P2
- **测试步骤**:
  1. 输入有效邮箱
  2. 输入超长密码（100+字符）
  3. 点击登录按钮
- **预期结果**: 
  - 系统正常处理或提示密码长度限制
- **测试数据**: `boundary_passwords`

#### TC-LOGIN-P2-002: 边界值测试 - 单字符密码
- **优先级**: P2
- **测试步骤**:
  1. 输入有效邮箱
  2. 输入单字符密码 "a"
  3. 点击登录按钮
- **预期结果**: 
  - 显示密码长度不足提示

#### TC-LOGIN-P2-003: 特殊字符密码测试
- **优先级**: P2
- **测试步骤**:
  1. 输入有效邮箱
  2. 输入包含特殊字符的密码
  3. 点击登录按钮
- **预期结果**: 
  - 系统正常处理特殊字符
- **测试数据**: 
  ```json
  ["!@#$%^&*()_+-=[]{}|;:',.<>?/`~", "password with spaces", "密码测试123", "Pass🔒Word123"]
  ```

#### TC-LOGIN-P2-004: SQL注入测试
- **优先级**: P2
- **测试步骤**:
  1. 输入SQL注入payload作为邮箱
  2. 点击登录按钮
- **预期结果**: 
  - 系统安全处理，不执行SQL命令
- **测试数据**: 
  ```json
  ["admin' OR '1'='1", "'; DROP TABLE users--"]
  ```

#### TC-LOGIN-P2-005: XSS攻击测试
- **优先级**: P2
- **测试步骤**:
  1. 输入XSS payload作为邮箱或密码
  2. 点击登录按钮
- **预期结果**: 
  - 系统安全处理，不执行脚本
- **测试数据**: 
  ```json
  ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
  ```

#### TC-LOGIN-P2-006: Google登录功能
- **优先级**: P2
- **测试步骤**:
  1. 点击"Google"登录按钮
  2. 完成Google OAuth流程
- **预期结果**: 
  - 跳转到Google登录页面
  - 授权后返回并登录成功

#### TC-LOGIN-P2-007: Github登录功能
- **优先级**: P2
- **测试步骤**:
  1. 点击"Github"登录按钮
  2. 完成Github OAuth流程
- **预期结果**: 
  - 跳转到Github登录页面
  - 授权后返回并登录成功

#### TC-LOGIN-P2-008: 多次错误密码锁定
- **优先级**: P2
- **测试步骤**:
  1. 连续输入错误密码5次
  2. 观察系统响应
- **预期结果**: 
  - 系统可能触发账户锁定或验证码机制

## 4. 测试数据设计

### 4.1 有效登录数据
```json
{
  "valid_users": [
    {
      "email": "haylee@test.com",
      "password": "Wh520520!",
      "description": "正常测试用户账号"
    }
  ]
}
```

### 4.2 无效邮箱数据
```json
{
  "invalid_emails": [
    {"email": "invalid-email", "expected_error": "邮箱格式不正确"},
    {"email": "test@", "expected_error": "邮箱格式不正确"},
    {"email": "@domain.com", "expected_error": "邮箱格式不正确"},
    {"email": "test @domain.com", "expected_error": "邮箱格式不正确"},
    {"email": "", "expected_error": "请输入邮箱"}
  ]
}
```

### 4.3 无效密码数据
```json
{
  "invalid_passwords": [
    {
      "email": "haylee@test.com",
      "password": "WrongPassword123!",
      "expected_error": "密码错误"
    },
    {
      "email": "haylee@test.com",
      "password": "",
      "expected_error": "请输入密码"
    }
  ]
}
```

### 4.4 边界测试数据
```json
{
  "boundary_passwords": [
    {"description": "单字符密码", "password": "a"},
    {"description": "超长密码", "password": "aaaa...100个字符"},
    {"description": "特殊字符密码", "password": "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"},
    {"description": "包含空格的密码", "password": "password with spaces"},
    {"description": "中文字符密码", "password": "密码测试123"},
    {"description": "Emoji密码", "password": "Pass🔒Word123"}
  ]
}
```

### 4.5 安全测试数据
```json
{
  "security_test_data": [
    {
      "type": "SQL注入",
      "email": "admin' OR '1'='1",
      "password": "' OR '1'='1"
    },
    {
      "type": "XSS攻击",
      "email": "<script>alert('XSS')</script>",
      "password": "password"
    }
  ]
}
```

## 5. 自动化实现建议

### 5.1 页面类实现
- ✅ 已实现：`pages/aevatar/aevatar_login_page.py`
- 继承自 `BasePage`
- 实现核心方法：`navigate()`, `is_loaded()`, `login_with_email()`
- 添加业务操作封装：`verify_login_success()`, `verify_login_failed()`

### 5.2 测试类实现
参考现有测试：
- `tests/aevatar/test_localhost_login.py` - 本地登录测试
- 使用pytest标记分类：`@pytest.mark.smoke`, `@pytest.mark.P0`
- 集成数据驱动测试：使用 `@pytest.mark.parametrize`

### 5.3 示例测试代码

```python
import pytest
import allure
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage

@allure.feature("登录功能")
@allure.story("邮箱密码登录")
class TestEmailLogin:
    
    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.title("TC-LOGIN-P0-001: 正常登录流程")
    def test_valid_login(self, page):
        """测试有效账户登录"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        login_page.verify_login_success()
    
    @pytest.mark.P0
    @allure.title("TC-LOGIN-P0-002: 错误密码登录")
    def test_invalid_password(self, page):
        """测试错误密码登录"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "WrongPassword!")
        login_page.verify_login_failed()
    
    @pytest.mark.P1
    @pytest.mark.parametrize("email", [
        "invalid-email",
        "test@",
        "@domain.com"
    ])
    @allure.title("TC-LOGIN-P1-001: 无效邮箱格式")
    def test_invalid_email_format(self, page, email):
        """测试无效邮箱格式"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email(email, "Wh520520!")
        login_page.verify_login_failed()
```

### 5.4 配置建议
- ✅ 已配置：`test-data/aevatar/localhost_login_data.json`
- ✅ 已配置：`test-data/aevatar/aevatar_test_data.yaml`
- 运行参数：`pytest tests/aevatar/test_localhost_login.py -v --allure-results=allure-results`

## 6. 执行计划

### 6.1 测试阶段
- **P0测试**: 每次构建必须执行，预计耗时 5分钟
- **P1测试**: 每日回归测试，预计耗时 10分钟
- **P2测试**: 每周完整测试，预计耗时 15分钟

### 6.2 验收标准
- P0测试用例通过率 100%
- P1测试用例通过率 ≥ 95%
- P2测试用例通过率 ≥ 90%
- 无阻塞性缺陷

### 6.3 风险评估
- **高风险**: 第三方登录依赖外部服务（Google/Github）
- **中风险**: 错误提示信息可能随版本变化
- **低风险**: UI元素定位器可能需要更新

## 7. 测试报告

### 7.1 Allure报告生成
```bash
# 运行测试并生成报告
pytest tests/aevatar/test_localhost_login.py --alluredir=allure-results

# 查看报告
allure serve allure-results
```

### 7.2 报告内容
- 测试用例执行结果
- 测试步骤截图
- 错误日志和堆栈跟踪
- 测试数据附件

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

