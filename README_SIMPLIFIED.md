# ⚡ Aevatar UI自动化测试 - 快速指南

## 🚀 快速开始

### 1. 快速验证（1-3分钟）⚡

```bash
python3 run_smoke_test.py
```

测试最核心的2-3个功能，快速反馈。

### 2. 完整测试（20-30分钟）

```bash
python3 run_all_tests_parallel.py
```

并行运行所有40个测试用例，完整覆盖。

---

## 📊 测试方案对比

| 方案 | 命令 | 时间 | 用例数 | 适用场景 |
|------|------|------|--------|---------|
| **快速验证** | `run_smoke_test.py` | 1-3分钟 | 2-3个 | 日常开发、快速检查 |
| **P0核心** | `pytest -n 4 -m p0` | 8-12分钟 | 10-15个 | 功能提测前 |
| **完整并行** | `run_all_tests_parallel.py` | 20-30分钟 | 40个 | 发布前验证 |
| **完整顺序** | `run_all_tests_sequential.py` | 60-90分钟 | 40个 | 夜间回归 |

---

## 📁 项目结构

```
ui-automation/
├── tests/aevatar/              # 测试代码（提交）
│   ├── test_daily_regression_login.py
│   ├── test_daily_regression_dashboard.py
│   └── ...
├── test-cases/                 # 测试用例文档（提交）
├── test-screenshots/           # 测试截图（不提交）
├── allure-report/             # Allure报告（不提交）
├── run_smoke_test.py          # 快速测试脚本（提交）
├── run_all_tests_parallel.py  # 并行测试脚本（提交）
└── cleanup.sh                 # 清理脚本（提交）
```

---

## 🧹 清理生成的文件

```bash
# 清理截图、报告、缓存
bash cleanup.sh
```

---

## 📊 查看报告

测试完成后自动打开，或手动：

```bash
# 快速测试报告
open allure-report-smoke/index.html

# 完整测试报告
open allure-report/index.html
```

---

## 🔧 环境配置

```bash
# 安装依赖
pip install -r requirements-pytest.txt

# 安装Allure（macOS）
brew install allure
```

---

## 📝 测试模块

8个测试模块，约40个用例：

1. **Login** - 登录功能
2. **Dashboard** - 仪表板
3. **API Keys** - API密钥管理
4. **Workflows** - 工作流
5. **Configuration** - 配置管理
6. **Profile** - 用户配置
7. **Organisation** - 组织管理
8. **Project** - 项目管理

---

## ⚙️ Git配置

`.gitignore` 已配置，以下文件不会提交：

- ❌ `test-screenshots/` - 测试截图
- ❌ `allure-*/` - Allure报告
- ❌ `__pycache__/` - Python缓存
- ❌ `reports/` - 测试报告
- ❌ `*.log` - 日志文件

---

## 💡 常用命令

```bash
# 快速验证
python3 run_smoke_test.py

# 完整测试（并行）
python3 run_all_tests_parallel.py

# 只测试P0
pytest -n 4 -m "p0" tests/aevatar/

# 单个模块
pytest tests/aevatar/test_daily_regression_login.py -v

# 清理
bash cleanup.sh

# 查看报告
open allure-report/index.html
```

---

## 📚 详细文档

- 📘 `QUICK_START_COMPARISON.md` - 方案详细对比
- 📗 `PARALLEL_TEST_GUIDE.md` - 并行测试详解
- 📙 `SYSTEM_RECOVERY_AND_TEST_GUIDE.md` - 问题排查指南
- 📕 `CLEANUP_GUIDE.md` - 清理和Git配置

---

## 🎯 推荐工作流

### 日常开发
```bash
# 每次改动后
python3 run_smoke_test.py  # 1-3分钟
```

### 提测前
```bash
# 功能完成
pytest -n 4 -m "p0" tests/aevatar/  # 8-12分钟
```

### 发布前
```bash
# 最终验证
python3 run_all_tests_parallel.py  # 20-30分钟
```

### 提交代码
```bash
# 清理
bash cleanup.sh

# 提交
git add .
git commit -m "feat: update tests"
```

---

**测试环境**: https://aevatar-station-ui-staging.aevatar.ai  
**最后更新**: 2025-10-30

