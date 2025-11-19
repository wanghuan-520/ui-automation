# Aevatar测试执行指南

## 概述

本指南提供了基于生成的测试计划和自动化代码的执行说明。

## 生成的文件清单

### 页面对象文件（Page Objects）

```
pages/aevatar/
├── aevatar_login_page.py              # 登录页面（已存在）
├── localhost_email_login_page.py      # 本地登录页面（已存在）
├── dashboard_workflows_page.py        # ✨ Dashboard/Workflows页面
├── profile_settings_page.py           # ✨ Profile/Settings页面
├── api_keys_page.py                   # ✨ API Keys页面
└── configuration_page.py              # ✨ Configuration页面
```

### 测试脚本文件（Test Scripts）

```
tests/aevatar/
├── test_localhost_login.py            # 登录测试（已存在）
├── test_dashboard_workflows.py        # ✨ Dashboard/Workflows测试
├── test_profile_settings.py           # ✨ Profile/Settings测试
├── test_api_keys.py                   # ✨ API Keys测试
└── test_configuration.py              # ✨ Configuration测试
```

## 测试用例覆盖

### 1. Dashboard Workflows测试 (test_dashboard_workflows.py)

**测试类**: `TestDashboardWorkflows`

| 测试用例ID | 优先级 | 描述 |
|-----------|--------|------|
| tc-workflows-p0-001 | P0 | 登录后跳转验证 |
| tc-workflows-p0-002 | P0 | 工作流列表加载 |
| tc-workflows-p0-003 | P0 | 创建新工作流按钮 |
| tc-workflows-p0-004 | P0 | 工作流状态显示 |
| tc-workflows-p0-005 | P0 | 侧边栏导航功能 |
| tc-workflows-p1-001 | P1 | 导入工作流功能 |
| tc-workflows-p1-005 | P1 | Settings按钮跳转 |
| tc-workflows-p1-008 | P1 | 空工作流列表状态 |
| tc-workflows-p2-007 | P2 | 浏览器刷新后状态保持 |

**集成测试**: `TestDashboardWorkflowsIntegration`
- 登录到Workflows页面完整流程

### 2. Profile Settings测试 (test_profile_settings.py)

**测试类**: `TestProfileSettings`

| 测试用例ID | 优先级 | 描述 |
|-----------|--------|------|
| tc-profile-p0-001 | P0 | Profile页面加载验证 |
| tc-profile-p0-002 | P0 | Name字段显示和编辑 |
| tc-profile-p0-003 | P0 | Email字段显示且不可编辑 |
| tc-profile-p0-004 | P0 | Save按钮可见且可点击 |
| tc-profile-p0-005 | P0 | Reset Password按钮和说明 |
| tc-profile-p1-001 | P1 | 修改Name并保存 |
| tc-profile-p1-006 | P1 | Organisations导航菜单 |
| tc-profile-p1-007 | P1 | Projects导航菜单 |
| tc-profile-p1-008 | P1 | Notifications菜单导航 |
| tc-profile-p2-001 | P2 | Name字段边界值测试 |
| tc-profile-p2-003 | P2 | 刷新页面后数据保持 |
| tc-profile-p2-005 | P2 | Dashboard按钮跳转 |

**集成测试**: `TestProfileSettingsIntegration`
- 登录到Profile页面完整流程

### 3. API Keys测试 (test_api_keys.py)

**测试类**: `TestApiKeys`

| 测试用例ID | 优先级 | 描述 |
|-----------|--------|------|
| tc-apikeys-p0-001 | P0 | API Keys页面加载 |
| tc-apikeys-p0-002 | P0 | API Keys列表加载 |
| tc-apikeys-p0-003 | P0 | 创建API Key弹窗打开 |
| tc-apikeys-p0-004 | P0 | 创建新的API Key |
| tc-apikeys-p0-006 | P0 | 删除API Key |
| tc-apikeys-p1-001 | P1 | 编辑API Key名称 |
| tc-apikeys-p1-003 | P1 | 取消创建操作 |
| tc-apikeys-p1-005 | P1 | 侧边栏导航功能 |
| tc-apikeys-p2-001 | P2 | 空Key名称验证 |
| tc-apikeys-p2-004 | P2 | 刷新页面后列表保持 |
| tc-apikeys-p2-006 | P2 | Key状态显示 |

**集成测试**: `TestApiKeysIntegration`
- API Key完整生命周期（创建→编辑→删除）

### 4. Configuration测试 (test_configuration.py)

**测试类**: `TestConfiguration`

| 测试用例ID | 优先级 | 描述 |
|-----------|--------|------|
| tc-config-p0-001 | P0 | Configuration页面加载 |
| tc-config-p0-002 | P0 | Webhook标签页功能 |
| tc-config-p0-003 | P0 | CROS标签页功能 |
| tc-config-p0-004 | P0 | 创建Webhook配置 |
| tc-config-p0-005 | P0 | 创建CROS配置 |
| tc-config-p0-006 | P0 | 删除Webhook配置 |
| tc-config-p0-007 | P0 | 删除CROS配置 |
| tc-config-p1-001 | P1 | 标签页切换 |
| tc-config-p1-006 | P1 | 侧边栏导航功能 |
| tc-config-p2-002 | P2 | Webhook列表数据结构 |
| tc-config-p2-003 | P2 | CROS列表数据结构 |
| tc-config-p2-005 | P2 | 刷新页面后状态保持 |

**集成测试**: `TestConfigurationIntegration`
- Webhook完整生命周期
- CROS完整生命周期

## 执行命令

### 前置条件

1. 确保测试环境运行在 `http://localhost:5173`
2. 测试账户: `haylee@test.com / Wh520520!`
3. 安装依赖:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 运行所有测试

```bash
# 运行所有aevatar测试
pytest tests/aevatar/ -v

# 带Allure报告
pytest tests/aevatar/ --alluredir=allure-results
allure serve allure-results
```

### 按优先级运行

```bash
# 运行P0（冒烟测试）
pytest tests/aevatar/ -m "p0" -v

# 运行P0和P1测试
pytest tests/aevatar/ -m "p0 or p1" -v

# 运行smoke测试
pytest tests/aevatar/ -m "smoke" -v
```

### 按功能模块运行

```bash
# Dashboard Workflows测试
pytest tests/aevatar/test_dashboard_workflows.py -v

# Profile Settings测试
pytest tests/aevatar/test_profile_settings.py -v

# API Keys测试
pytest tests/aevatar/test_api_keys.py -v

# Configuration测试
pytest tests/aevatar/test_configuration.py -v
```

### 按测试类运行

```bash
# 运行特定测试类
pytest tests/aevatar/test_api_keys.py::TestApiKeys -v

# 运行集成测试
pytest tests/aevatar/ -m "integration" -v
```

### 运行单个测试用例

```bash
# 运行特定测试方法
pytest tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflows::test_login_redirect_to_workflows -v
```

## 配置说明

### pytest.ini

确保 `pytest.ini` 包含以下标记：

```ini
[pytest]
markers =
    smoke: 冒烟测试
    p0: 优先级P0 - 阻塞性测试
    p1: 优先级P1 - 重要功能测试
    p2: 优先级P2 - 次要功能测试
    integration: 集成测试
    ui: UI功能测试
```

### 测试数据

测试使用的登录凭证配置在各个测试文件的 `setup` fixture 中：

```python
login_page.login_with_email("haylee@test.com", "Wh520520!")
```

如需修改，请更新对应测试文件。

## 测试报告

### Allure报告

```bash
# 生成并查看Allure报告
pytest tests/aevatar/ --alluredir=allure-results
allure serve allure-results
```

### HTML报告

```bash
# 生成HTML报告
pytest tests/aevatar/ --html=reports/aevatar_test_report.html --self-contained-html
```

### JSON报告

```bash
# 生成JSON报告
pytest tests/aevatar/ --json-report --json-report-file=reports/aevatar_test_report.json
```

## 调试技巧

### 显示浏览器

修改 `conftest.py` 或在命令行传递参数：

```bash
# 显示浏览器窗口
pytest tests/aevatar/test_dashboard_workflows.py --headed

# 慢速模式
pytest tests/aevatar/test_dashboard_workflows.py --slowmo=1000
```

### 截图和视频

测试失败时会自动截图。如需视频录制，配置 `conftest.py`：

```python
@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_default_timeout(30000)
    
    # 开始录制
    page.video.path()
    
    yield page
    page.close()
```

### 日志输出

```bash
# 显示详细日志
pytest tests/aevatar/ -v -s --log-cli-level=INFO
```

## 常见问题

### 1. 元素定位失败

- 检查前端地址是否正确（`http://localhost:5173`）
- 验证页面是否完全加载
- 检查元素选择器是否需要更新

### 2. 登录失败

- 确认测试账户可用: `haylee@test.com / Wh520520!`
- 检查登录页面是否正常访问

### 3. 超时错误

- 增加超时时间：修改 `page.set_default_timeout(60000)`
- 检查网络连接
- 验证测试环境性能

## 代码结构说明

### 页面对象模式

所有页面对象继承自 `BasePage`，提供：

- 标准化的页面操作方法
- 统一的等待机制
- 日志记录
- 异常处理

### 测试类结构

```python
@allure.feature("功能模块")
@allure.story("功能故事")
class TestXXX:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        # 测试前置设置
        pass
    
    @pytest.mark.p0
    @allure.title("测试用例标题")
    def test_xxx(self):
        # 测试步骤
        pass
```

## 持续集成

### GitHub Actions示例

```yaml
name: Aevatar UI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run P0 tests
        run: pytest tests/aevatar/ -m "p0" --alluredir=allure-results
      
      - name: Generate Allure report
        uses: simple-elf/allure-report-action@master
        if: always()
        with:
          allure_results: allure-results
```

## 维护建议

1. **定期更新元素定位器**: 前端变更时及时更新页面对象中的选择器
2. **添加新测试用例**: 基于新功能补充测试覆盖
3. **优化测试稳定性**: 识别并修复不稳定的测试
4. **代码审查**: 确保新测试遵循项目规范
5. **文档同步**: 更新测试计划和执行指南

## 联系方式

如有问题，请：
- 查看项目文档: `docs/test-cases/aevatar/`
- 提交Issue到项目仓库
- 联系测试团队

---

**生成时间**: 2025-11-18  
**版本**: v1.0.0  
**状态**: ✅ 就绪

