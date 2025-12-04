# Aevatar Station 自动化测试

本目录包含 Aevatar Station 系统的完整自动化测试套件。

## 📁 目录结构

```
tests/aevatar-station/
├── pages/                      # Page Object模式页面类
│   ├── base_page.py           # 基础页面类
│   ├── landing_page.py        # 首页
│   ├── login_page.py          # 登录页
│   ├── workflow_page.py       # 工作流页面
│   ├── admin_panel_page.py    # 管理面板
│   ├── profile_settings_page.py  # 个人设置
│   ├── change_password_page.py   # 修改密码
│   └── email_settings_page.py    # 邮件设置
│
├── test_login.py              # 登录功能测试
├── test_workflow.py           # 工作流功能测试
├── test_profile.py            # 个人信息测试
├── test_password.py           # 密码管理测试
├── test_user_menu.py          # 用户菜单测试
│
├── test-data/                 # 测试数据文件
│   ├── login_data.json
│   ├── profile_data.json
│   └── settings_data.json
│
├── conftest.py                # Pytest配置和fixtures
├── pytest.ini                 # Pytest配置文件
└── README.md                  # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 运行所有测试

```bash
cd tests/aevatar-station
pytest
```

### 3. 运行特定模块的测试

```bash
# 运行登录测试
pytest test_login.py

# 运行工作流测试
pytest test_workflow.py

# 运行个人信息测试
pytest test_profile.py
```

### 4. 按标记运行测试

```bash
# 运行所有P0优先级测试
pytest -m P0

# 运行登录相关测试
pytest -m login

# 运行功能测试
pytest -m functional

# 运行安全测试
pytest -m security
```

### 5. 并行运行测试

```bash
# 使用pytest-xdist并行运行
pytest -n auto
```

## 📋 测试标记

测试用例使用以下标记进行分类：

### 功能模块标记
- `@pytest.mark.login` - 登录功能测试
- `@pytest.mark.workflow` - 工作流功能测试
- `@pytest.mark.profile` - 个人信息测试
- `@pytest.mark.password` - 密码管理测试
- `@pytest.mark.user_menu` - 用户菜单测试

### 测试类型标记
- `@pytest.mark.functional` - 功能测试
- `@pytest.mark.boundary` - 边界测试
- `@pytest.mark.exception` - 异常测试
- `@pytest.mark.security` - 安全测试
- `@pytest.mark.performance` - 性能测试
- `@pytest.mark.compatibility` - 兼容性测试
- `@pytest.mark.ux` - 用户体验测试
- `@pytest.mark.data` - 数据一致性测试

### 优先级标记
- `@pytest.mark.P0` - 最高优先级（核心功能）
- `@pytest.mark.P1` - 高优先级（重要功能）
- `@pytest.mark.P2` - 中优先级（辅助功能）

## 🔧 配置说明

### 浏览器配置

在 `conftest.py` 中可以配置：
- `headless`: 设置为 `True` 启用无头模式
- `slow_mo`: 操作延迟（毫秒），便于观察测试过程
- `viewport`: 浏览器窗口大小

### SSL证书处理

测试已配置忽略HTTPS错误，适用于localhost的自签名证书。

### 测试数据

测试数据存储在 `test-data/` 目录的JSON文件中，包括：
- 有效/无效登录凭证
- 边界测试数据
- 个人信息测试数据
- 邮件配置数据

## 📊 测试报告

测试执行后会生成以下报告：

1. **HTML报告**: `reports/test_report.html`
2. **日志文件**: `logs/pytest.log`
3. **失败截图**: `screenshots/` 目录

## 🐛 调试技巧

### 1. 单个测试调试

```bash
# 运行单个测试并显示详细输出
pytest test_login.py::TestLogin::test_successful_login -vv -s
```

### 2. 使用浏览器开发者工具

设置 `slow_mo` 参数并保持浏览器窗口打开：

```python
# 在 conftest.py 中修改
"slow_mo": 500,  # 每个操作延迟500ms
```

### 3. 失败时暂停

```bash
# 失败时进入Python调试器
pytest --pdb
```

### 4. 查看Playwright追踪

```python
# 启用追踪
context.tracing.start(screenshots=True, snapshots=True)
# ... 执行测试 ...
context.tracing.stop(path="trace.zip")
```

然后使用 `playwright show-trace trace.zip` 查看。

## 📝 编写新测试

### 1. 创建新的测试文件

```python
"""
新模块功能测试
"""
import pytest
import logging
from pages.your_page import YourPage

logger = logging.getLogger(__name__)


@pytest.mark.your_module
class TestYourModule:
    """模块测试类"""
    
    @pytest.mark.P0
    @pytest.mark.functional
    def test_your_feature(self, page, test_data):
        """测试描述"""
        logger.info("开始测试")
        
        # 测试步骤
        your_page = YourPage(page)
        your_page.navigate()
        
        # 断言
        assert your_page.is_loaded()
        
        logger.info("测试完成")
```

### 2. 创建新的Page Object

```python
"""
YourPage - 页面描述
路径: /your-path
"""
from pages.base_page import BasePage


class YourPage(BasePage):
    """页面对象"""
    
    # 元素定位器
    ELEMENT = "selector"
    
    def navigate(self):
        """导航到页面"""
        self.navigate_to("/your-path")
    
    def is_loaded(self):
        """检查页面加载"""
        return self.is_visible(self.ELEMENT)
```

## 🔍 常见问题

### Q: SSL证书警告如何处理？
A: 已在 `base_page.py` 中实现 `handle_ssl_warning()` 方法自动处理。

### Q: 如何处理动态加载的元素？
A: 使用 `wait_for_element()` 或 `page.wait_for_selector()` 等待元素出现。

### Q: 测试数据如何管理？
A: 测试数据统一存储在 `test-data/` 目录的JSON文件中，通过 `test_data` fixture使用。

### Q: 如何调试失败的测试？
A: 
1. 查看生成的截图（`screenshots/` 目录）
2. 查看日志文件（`logs/pytest.log`）
3. 使用 `-vv -s` 参数查看详细输出
4. 使用 `--pdb` 参数在失败时进入调试器

## 📚 参考资料

- [Playwright Python文档](https://playwright.dev/python/docs/intro)
- [Pytest文档](https://docs.pytest.org/)
- [测试计划文档](../../docs/test-cases/aevatar/aevatar-station-test-plan.md)

## 🤝 贡献指南

1. 遵循现有的代码风格和目录结构
2. 每个测试用例都应有清晰的文档字符串
3. 使用Page Object模式避免重复代码
4. 添加适当的日志和断言
5. 确保测试的独立性（不依赖其他测试的执行顺序）

---

**最后更新**: 2025-11-28
**维护者**: Test Team

