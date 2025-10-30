# Aevatar 测试套件

## 概述

这是一个基于 pytest 和 Playwright 的数据驱动测试框架，用于测试 Aevatar 平台的登录和 Workflow 功能。

## 特性

✅ **数据驱动测试** - 测试数据与测试逻辑分离，存储在 YAML 配置文件中  
✅ **参数化测试** - 使用 pytest 参数化功能，自动生成多个测试用例  
✅ **正常+异常场景** - 覆盖正常场景和各种异常场景（错误密码、无效邮箱、空字段等）  
✅ **可复用的 Fixtures** - 通过 conftest.py 提供共享的测试工具  
✅ **清晰的代码结构** - 每个文件职责单一，易于维护  

## 文件结构

```
tests/aevatar/
├── README.md              # 本文档
├── conftest.py            # pytest配置和共享fixtures
├── utils.py               # 工具类（数据加载、选择器查找等）
├── test_login.py          # 登录测试（约200行）
└── test_workflow.py       # Workflow测试（约300行）

test-data/
└── aevatar_test_data.yaml # 测试数据配置文件
```

## 测试数据配置

所有测试数据都存储在 `test-data/aevatar_test_data.yaml` 中，包括：

- **环境配置**: URL、超时时间等
- **浏览器配置**: 视口大小、User-Agent等
- **登录场景**: 正常登录、错误密码、无效邮箱、空字段等
- **Workflow场景**: 基础workflow、错误配置等
- **选择器配置**: 页面元素定位器

### 添加新的测试场景

只需在 YAML 文件中添加新的场景数据，无需修改代码：

```yaml
login_scenarios:
  - id: "new_scenario"
    description: "新的测试场景"
    email: "test@example.com"
    password: "password123"
    expected_result: "success"  # 或 "error"
    expected_url_contains: ["dashboard"]
    tags: ["smoke", "positive"]
```

## 运行测试

### 安装依赖

```bash
pip install -r requirements-pytest.txt
```

### 运行所有测试

```bash
pytest tests/aevatar/ -v
```

### 运行特定类型的测试

```bash
# 只运行登录测试
pytest tests/aevatar/test_login.py -v

# 只运行workflow测试
pytest tests/aevatar/test_workflow.py -v

# 只运行冒烟测试
pytest tests/aevatar/ -v -m smoke

# 只运行正向测试
pytest tests/aevatar/ -v -m positive

# 只运行负向测试
pytest tests/aevatar/ -v -m negative
```

### 生成HTML报告

```bash
pytest tests/aevatar/ -v \
  --html=reports/aevatar-report.html \
  --self-contained-html
```

### 并行执行测试（加速）

```bash
pytest tests/aevatar/ -v -n auto
```

### 失败重试

```bash
pytest tests/aevatar/ -v --reruns 2
```

## 测试标记 (Markers)

- `@pytest.mark.smoke` - 冒烟测试（快速验证核心功能）
- `@pytest.mark.positive` - 正向测试（正常场景）
- `@pytest.mark.negative` - 负向测试（异常场景）
- `@pytest.mark.login` - 登录相关测试
- `@pytest.mark.workflow` - Workflow相关测试
- `@pytest.mark.integration` - 集成测试

## 测试场景

### 登录测试场景

1. ✅ **valid_login** - 正常登录
2. ❌ **invalid_password** - 错误密码
3. ❌ **invalid_email_format** - 无效邮箱格式
4. ❌ **non_existent_account** - 不存在的账号
5. ❌ **empty_email** - 空邮箱
6. ❌ **empty_password** - 空密码
7. ❌ **empty_credentials** - 邮箱和密码都为空

### Workflow测试场景

1. ✅ **basic_workflow** - 基础workflow创建和运行
2. ❌ **workflow_without_config** - 未配置必填字段的workflow

## 快速冒烟测试

框架提供了快速冒烟测试函数，可以快速验证核心功能：

```bash
# 快速验证登录功能
pytest tests/aevatar/test_login.py::test_valid_login_only -v

# 快速验证安全机制
pytest tests/aevatar/test_login.py::test_invalid_credentials_only -v

# 快速验证workflow功能
pytest tests/aevatar/test_workflow.py::test_basic_workflow_only -v
```

## Fixtures 说明

### browser_context
提供独立的浏览器页面实例，每个测试函数使用独立的浏览器。

### screenshot_helper
截图辅助函数：
```python
await screenshot_helper("my_screenshot.png")
```

### login_helper
登录辅助函数：
```python
await login_helper("email@example.com", "password")
```

### test_data
加载的完整测试数据字典。

### environment_config
环境配置（URL、超时等）。

### browser_config
浏览器配置。

## 工具类使用

### 加载测试数据

```python
from .utils import TestDataLoader

# 加载所有数据
data = TestDataLoader.load_yaml_data()

# 获取登录场景
login_scenarios = TestDataLoader.get_login_scenarios()

# 按标签过滤
positive_scenarios = TestDataLoader.get_login_scenarios(tag="positive")
```

### 查找页面元素

```python
from .utils import SelectorHelper

# 使用多个选择器尝试查找元素
element = await SelectorHelper.find_element_with_selectors(
    page, 
    ['selector1', 'selector2', 'selector3']
)

# 检查错误消息
error_found = await SelectorHelper.check_error_message(
    page, 
    expected_keywords=['error', 'invalid']
)
```

## 最佳实践

1. **添加新场景时** - 优先在 YAML 中添加数据，避免修改代码
2. **使用标签** - 合理使用标签组织测试用例，便于筛选执行
3. **截图** - 关键步骤和失败时都要截图，便于问题定位
4. **日志** - 使用 logger 记录详细的执行过程
5. **断言** - 断言失败时提供清晰的错误信息

## 注意事项

- 测试使用有头模式运行，便于观察
- 浏览器路径硬编码为 Chrome，如需修改请编辑 conftest.py
- 截图保存在 `test-screenshots/` 目录
- 测试报告保存在 `reports/` 目录

## 扩展性

### 添加新的测试类型

1. 在 YAML 中添加新的场景类型
2. 创建新的测试文件（如 `test_settings.py`）
3. 在 `utils.py` 中添加对应的数据加载函数
4. 在 `conftest.py` 中添加必要的 fixtures

### 自定义选择器

在 YAML 的 `selectors` 部分添加新的选择器配置：

```yaml
selectors:
  my_feature:
    button: 'button[data-test="my-button"]'
    input: 'input[name="my-input"]'
```

然后在代码中使用：

```python
selectors = TestDataLoader.get_selectors('my_feature')
button = await page.wait_for_selector(selectors['button'])
```

## 贡献指南

1. 保持每个文件在 400 行以内
2. 所有注释使用中文
3. 遵循 PEP 8 代码规范
4. 添加新功能时更新本文档

## 问题排查

### 浏览器无法启动
检查 Chrome 路径是否正确，可在 conftest.py 中修改 `executable_path`。

### 元素无法找到
1. 检查选择器是否正确
2. 增加等待时间
3. 在 YAML 的 `selectors` 中添加更多备用选择器

### 测试超时
调整 YAML 中的 `timeout` 和 `slow_mo` 配置。

## 联系方式

如有问题，请联系团队或查看项目文档。

