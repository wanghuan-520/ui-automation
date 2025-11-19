# GodGPT UI 自动化测试执行指南

## 📋 目录
- [环境准备](#环境准备)
- [测试执行](#测试执行)
- [测试报告](#测试报告)
- [常见问题](#常见问题)

---

## 🔧 环境准备

### 1. 安装依赖

确保已安装项目依赖：

```bash
cd /Users/wanghuan/aelf/Cursor/ui_frame-master
pip3 install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
python3 -m playwright install chromium
```

### 3. 验证环境

```bash
# 检查 Python 版本（需要 3.8+）
python3 --version

# 检查 Playwright 安装
python3 -m playwright --version
```

### 4. 解决依赖问题（如果遇到 xonsh 错误）

如果执行测试时遇到 `ModuleNotFoundError: No module named 'prompt_toolkit'`，执行：

```bash
pip3 install prompt_toolkit
# 或者卸载 xonsh 插件
pip3 uninstall pytest-xonsh
```

---

## 🚀 测试执行

### 执行所有 GodGPT 测试

```bash
# 使用 pytest 直接执行
python3 -m pytest tests/test_godgpt_*.py -v

# 使用项目脚本执行
python3 run_tests.py --tests tests/test_godgpt_login.py --verbose
```

### 按模块执行测试

#### 1. 登录模块测试（TC001-TC006, TC016-TC022）

```bash
python3 -m pytest tests/test_godgpt_login.py -v
```

包含测试用例：
- ✅ TC001: 邮箱登录 - 正常流程
- ✅ TC002: 邮箱输入 - 编辑功能
- ✅ TC003: 密码可见性切换
- ✅ TC004: 忘记密码链接
- ✅ TC005: Skip 跳过登录
- ✅ TC006: 返回按钮功能
- ✅ TC016: 邮箱格式验证（参数化测试）
- ✅ TC021: 登录 - 错误密码
- ✅ TC022: 登录 - 未注册邮箱

#### 2. 主界面功能测试（TC007-TC015）

```bash
python3 -m pytest tests/test_godgpt_main.py -v
```

包含测试用例：
- ✅ TC007: 新建对话
- ✅ TC008: 历史对话切换
- ✅ TC009: Soul Link 卡片
- ✅ TC010: Unlock Your Path 卡片
- ✅ TC011: Annual 会员功能
- ✅ TC012: 用户头像 - 个人中心
- ✅ TC013: 语音输入功能
- ✅ TC014: 附件上传功能
- ✅ TC015: Get App 下载推广

#### 3. 边界和UI/UX测试（TC017-TC030）

```bash
python3 -m pytest tests/test_godgpt_boundary.py -v
```

包含测试用例：
- ✅ TC017: 邮箱输入 - 空值提交
- ✅ TC018: 密码输入 - 空值提交
- ✅ TC019: 密码输入 - 长度边界（参数化）
- ✅ TC020: 对话输入 - 最大字符数
- ✅ TC023: 网络中断模拟
- ✅ TC024: 页面刷新 - Token 持久化
- ✅ TC027: 响应式设计（参数化多种设备）
- ✅ TC028: 页面加载性能
- ✅ TC029: 键盘导航
- ✅ TC030: 浏览器兼容性

### 按标记执行测试

```bash
# 只执行冒烟测试
python3 -m pytest tests/test_godgpt_*.py -m smoke -v

# 只执行高优先级测试
python3 -m pytest tests/test_godgpt_*.py -m high_priority -v

# 执行登录相关测试
python3 -m pytest tests/test_godgpt_*.py -m login -v

# 执行边界测试
python3 -m pytest tests/test_godgpt_*.py -m boundary -v
```

### 执行单个测试用例

```bash
# 执行 TC001 邮箱登录测试
python3 -m pytest tests/test_godgpt_login.py::TestGodGPTLogin::test_tc001_email_login_success -v

# 执行 TC007 新建对话测试
python3 -m pytest tests/test_godgpt_main.py::TestGodGPTMain::test_tc007_new_chat -v
```

### 并行执行测试（需要 pytest-xdist）

```bash
# 安装 pytest-xdist
pip3 install pytest-xdist

# 使用 4 个进程并行执行
python3 -m pytest tests/test_godgpt_*.py -n 4 -v
```

---

## 📊 测试报告

### 1. HTML 报告（pytest-html）

```bash
# 生成 HTML 报告
python3 -m pytest tests/test_godgpt_*.py --html=reports/godgpt_report.html --self-contained-html

# 查看报告
open reports/godgpt_report.html
```

### 2. Allure 报告（推荐）

```bash
# 安装 Allure（如果未安装）
brew install allure  # macOS
# 或 pip3 install allure-pytest

# 生成 Allure 结果
python3 -m pytest tests/test_godgpt_*.py --alluredir=reports/allure-results

# 启动 Allure 报告服务器
allure serve reports/allure-results
```

### 3. JUnit XML 报告

```bash
python3 -m pytest tests/test_godgpt_*.py --junitxml=reports/junit.xml
```

### 4. 覆盖率报告（可选）

```bash
# 安装 pytest-cov
pip3 install pytest-cov

# 生成覆盖率报告
python3 -m pytest tests/test_godgpt_*.py --cov=pages --cov-report=html --cov-report=term

# 查看报告
open htmlcov/index.html
```

---

## 📸 截图和视频

### 失败时自动截图

测试失败时会自动截图到 `reports/screenshots/` 目录。

### 录制测试视频

在 `conftest.py` 中启用视频录制：

```python
@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(
        record_video_dir="reports/videos",
        record_video_size={"width": 1920, "height": 1080}
    )
    yield context
    context.close()
```

---

## 🐛 常见问题

### 1. 浏览器未安装

**错误信息**: `Executable doesn't exist at ...`

**解决方案**:
```bash
python3 -m playwright install chromium
```

### 2. xonsh 插件错误

**错误信息**: `ModuleNotFoundError: No module named 'prompt_toolkit'`

**解决方案**:
```bash
pip3 install prompt_toolkit
# 或者
pip3 uninstall pytest-xonsh
```

### 3. 测试超时

**解决方案**:
- 检查网络连接
- 增加 `config/test_config.yaml` 中的 `timeout` 值
- 使用 `--timeout=60` 参数

```bash
python3 -m pytest tests/test_godgpt_*.py --timeout=60
```

### 4. 元素定位失败

**解决方案**:
- 检查目标网站是否可访问
- 页面结构可能已更改，需要更新定位器
- 增加等待时间

### 5. 登录失败

**检查事项**:
- 测试账号密码是否正确（在 `config/test_config.yaml` 或 `test_data/godgpt_login_data.json` 中配置）
- 网络是否可以访问测试环境
- 是否有验证码或其他安全机制

---

## 📂 测试文件结构

```
ui_frame-master/
├── pages/
│   ├── godgpt_landing_page.py       # 登录首页 PO
│   ├── godgpt_email_login_page.py   # 密码输入页 PO
│   └── godgpt_main_page.py          # 主界面 PO
├── tests/
│   ├── test_godgpt_login.py         # 登录模块测试（11个用例）
│   ├── test_godgpt_main.py          # 主界面功能测试（10个用例）
│   └── test_godgpt_boundary.py      # 边界和UI测试（12个用例）
├── test_data/
│   ├── godgpt_login_data.json       # 登录测试数据
│   └── godgpt_conversation_data.json # 对话测试数据
├── config/
│   └── test_config.yaml             # GodGPT 测试配置
└── reports/
    ├── screenshots/                 # 失败截图
    ├── videos/                      # 测试视频
    ├── allure-results/              # Allure 结果
    └── godgpt_report.html           # HTML 报告
```

---

## 🎯 测试覆盖情况

| 模块 | 测试用例数 | 文件 |
|------|-----------|------|
| 登录功能 | 11 | `test_godgpt_login.py` |
| 主界面功能 | 10 | `test_godgpt_main.py` |
| 边界和UI/UX | 12 | `test_godgpt_boundary.py` |
| **总计** | **33** | - |

### 优先级分布

- 🔴 高优先级（High）: 15 个用例
- 🟡 中优先级（Medium）: 15 个用例
- 🟢 低优先级（Low）: 3 个用例

### 标记分类

- `smoke`: 冒烟测试（核心功能验证）
- `login`: 登录模块
- `main`: 主界面功能
- `boundary`: 边界条件测试
- `exception`: 异常场景测试
- `ui`: UI/UX 测试

---

## 📝 持续集成（CI/CD）

### GitHub Actions 示例

创建 `.github/workflows/godgpt-ui-tests.yml`:

```yaml
name: GodGPT UI Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # 每天执行

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        python -m playwright install chromium
    
    - name: Run tests
      run: |
        python -m pytest tests/test_godgpt_*.py -v --html=reports/report.html --self-contained-html
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: reports/
```

---

## 🔗 相关文档

- [测试计划文档](./test-case.md) - 完整的测试用例设计
- [项目 README](../README.md) - 项目总体说明
- [使用指南](../使用指南.md) - 框架使用方法

---

## 💡 最佳实践

1. **执行前检查**
   - 确保测试环境可访问
   - 确认测试账号有效
   - 检查浏览器是否已安装

2. **调试技巧**
   - 使用 `-s` 参数查看日志输出
   - 使用 `--headed` 参数显示浏览器窗口
   - 查看 `logs/test_*.log` 日志文件

3. **性能优化**
   - 使用并行执行（pytest-xdist）
   - 启用浏览器缓存
   - 复用登录状态（使用 storage state）

4. **报告管理**
   - 定期清理旧报告
   - 使用 Allure 生成美观的报告
   - 集成 CI/CD 自动发送报告

---

**文档更新日期**: 2025-11-13  
**维护人员**: HyperEcho  
**联系方式**: 参考项目 README

---

## 🎉 快速开始

```bash
# 一键执行所有测试并生成报告
cd /Users/wanghuan/aelf/Cursor/ui_frame-master
python3 -m pytest tests/test_godgpt_*.py -v --html=reports/godgpt_report.html --self-contained-html
open reports/godgpt_report.html
```

祝测试顺利！🚀

