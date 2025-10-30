# 🧹 项目清理和Git配置指南

## ✅ 已完成的优化

### 1. 更新 .gitignore

已配置以下文件/目录不提交到远程：

```gitignore
# 测试截图（不提交）
test-screenshots/
*.png, *.jpg, *.jpeg, *.gif, *.bmp

# Allure报告（不提交）
allure-results/
allure-report/

# Pytest缓存（不提交）
__pycache__/
.pytest_cache/
*.pyc

# 测试报告（不提交）
reports/
logs/
```

### 2. 创建清理脚本

`cleanup.sh` - 一键清理所有生成的文件

---

## 🚀 快速使用

### 清理生成的文件

```bash
# 清理截图、报告、缓存等
bash cleanup.sh
```

### 查看Git状态（清理后）

```bash
# 查看哪些文件会被提交
git status

# 应该看不到截图、报告等文件
```

---

## 📁 Git提交规则

### ✅ 应该提交的

```
tests/                    # 测试代码
test-cases/              # 测试用例文档
test-data/               # 测试数据
requirements*.txt        # 依赖文件
run_*.py                 # 运行脚本
.gitignore              # Git配置
README.md               # 说明文档
```

### ❌ 不应该提交的

```
test-screenshots/       # 测试截图
allure-*/              # Allure报告
reports/               # 测试报告
logs/                  # 日志文件
__pycache__/          # Python缓存
*.pyc, *.pyo          # 编译文件
```

---

## 🔄 清理工作流

### 运行测试后清理

```bash
# 1. 运行测试
python3 run_all_tests_parallel.py

# 2. 查看报告
open allure-report/index.html

# 3. 清理（如果不需要保留）
bash cleanup.sh
```

### 提交代码前清理

```bash
# 1. 清理生成文件
bash cleanup.sh

# 2. 查看要提交的文件
git status

# 3. 提交
git add .
git commit -m "你的提交信息"
```

---

## 💡 建议

### 本地保留的目录结构

```
ui-automation/
├── tests/                   # 提交
├── test-cases/             # 提交
├── test-screenshots/       # 本地（.gitignore）
├── allure-report/          # 本地（.gitignore）
├── run_*.py               # 提交
└── cleanup.sh             # 提交
```

### CI/CD中的配置

如果有CI/CD流水线：

```yaml
# .github/workflows/test.yml 示例
steps:
  - run: python3 run_all_tests_parallel.py
  - run: allure generate allure-results
  - uses: actions/upload-artifact@v2
    with:
      name: test-report
      path: allure-report/
```

---

## 🎯 快速命令参考

```bash
# 清理所有生成文件
bash cleanup.sh

# 查看Git状态
git status

# 提交（会自动忽略不需要的文件）
git add .
git commit -m "feat: update tests"

# 强制清理（包括未跟踪的文件）
git clean -fdx
```

---

**最后更新**: 2025-10-30

