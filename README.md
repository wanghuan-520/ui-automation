# UI Automation Testing Framework

自动化测试框架，支持 Web 端和移动端的 UI 自动化测试。

## 🚀 快速开始

### 环境依赖

**Python 3.8+** 是必需的。

### 安装依赖

根据测试类型选择对应的依赖包：

#### Web UI 测试（Playwright + Pytest）
```bash
pip install -r requirements.txt
playwright install
```

#### 移动端测试（Appium + Selenium）
```bash
pip install -r test-requirements/mobile-requirements.txt
```

---

## 📂 项目结构

```
ui-automation/
├── config/                  # 测试配置文件
├── docs/                    # 测试文档
│   ├── test-cases/         # 当前测试用例文档
│   └── test-cases-history/ # 历史测试用例
├── pages/                   # 页面对象模型 (POM)
│   ├── aevatar/            # Aevatar 页面对象
│   └── godgpt/             # GodGPT 页面对象
├── tests/                   # 测试用例
│   ├── aevatar/            # Aevatar 测试
│   └── godgpt/             # GodGPT 测试
├── test-data/              # 测试数据
│   ├── aevatar/
│   └── godgpt/
├── test-requirements/       # 移动端测试依赖 & 产品需求文档
├── utils/                   # 工具类
├── reports/                 # 测试报告（生成文件）
├── logs/                    # 日志文件（生成文件）
├── requirements.txt         # Web UI 测试依赖
└── pytest.ini              # Pytest 配置
```

---

## 🧪 运行测试

### Aevatar 测试
```bash
# 运行所有 Aevatar 测试
pytest tests/aevatar/

# 运行特定测试文件
pytest tests/aevatar/test_localhost_login.py

# 运行每日回归测试
pytest tests/aevatar/test_daily_regression_*.py
```

### GodGPT 测试
```bash
# Python 测试
pytest tests/godgpt/python/

# TypeScript 测试
cd tests/godgpt/typescript/
npm test
```

---

## 📊 测试报告

测试报告将生成在 `reports/` 目录下：
- **Allure 报告**: `allure serve reports/allure-results/`
- **HTML 报告**: `reports/pytest-report.html`
- **JSON 报告**: `reports/pytest-report.json`

---

## 📖 文档

- [Aevatar 测试计划](docs/test-cases/aevatar/README.md)
- [Aevatar 快速开始](tests/aevatar/QUICKSTART.md)
- [每日回归测试指南](tests/aevatar/DAILY_REGRESSION_GUIDE.md)
- [GodGPT 测试指南](tests/godgpt/python/GODGPT_TEST_EXECUTION_GUIDE.md)

---

## 🔧 配置

测试配置文件位于 `config/test_config.yaml`，可配置：
- 测试环境 URL
- 超时设置
- 浏览器选项
- 日志级别

---

## 📝 日志

测试执行日志保存在 `logs/` 目录，按日期命名：
- `test_YYYYMMDD.log`

---

## 🤝 贡献

请参考各测试模块的 README 文档了解详细的测试用例编写规范。

---

## 📦 依赖说明

| 文件 | 用途 | 主要依赖 |
|------|------|----------|
| `requirements.txt` | Web UI 自动化测试 | Playwright, Pytest |
| `test-requirements/mobile-requirements.txt` | 移动端自动化测试 | Appium, Selenium |

