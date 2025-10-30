# Aevatar 测试框架 - 快速开始

## 5分钟上手指南 🚀

### 1. 安装依赖（1分钟）

```bash
# 进入项目目录
cd /Users/wanghuan/aelf/Cursor/ui-automation

# 安装依赖
pip install -r requirements-pytest.txt

# 验证安装
pytest --version
```

### 2. 运行第一个测试（2分钟）

```bash
# 快速冒烟测试 - 验证登录功能
python run_aevatar_tests.py --test-file test_login.py -m smoke

# 或使用pytest直接运行
pytest tests/aevatar/test_login.py::test_valid_login_only -v
```

### 3. 查看测试结果（1分钟）

测试完成后：
- 查看终端输出的详细日志
- 查看 `test-screenshots/` 目录的截图
- （可选）生成HTML报告：`python run_aevatar_tests.py --html`

### 4. 添加你的第一个测试场景（1分钟）

编辑 `test-data/aevatar_test_data.yaml`，添加新场景：

```yaml
login_scenarios:
  # ... 现有场景
  
  # 你的新场景
  - id: "my_test_case"
    description: "我的测试用例"
    email: "test@example.com"
    password: "mypassword"
    expected_result: "error"
    expected_error_keywords: ["invalid", "错误"]
    tags: ["negative"]
```

再次运行测试，你的新场景会自动被执行！

```bash
pytest tests/aevatar/test_login.py -v
```

## 常用命令速查

```bash
# 运行所有测试
python run_aevatar_tests.py

# 只运行登录测试
python run_aevatar_tests.py --test-file test_login.py

# 只运行正向测试
python run_aevatar_tests.py -m positive

# 只运行负向测试
python run_aevatar_tests.py -m negative

# 生成HTML报告
python run_aevatar_tests.py --html

# 并行执行（加速）
python run_aevatar_tests.py --parallel

# 失败重试
python run_aevatar_tests.py --reruns 2

# 组合使用
python run_aevatar_tests.py -m smoke --html --parallel
```

## 文件说明

```
tests/aevatar/
├── README.md           # 详细文档
├── QUICKSTART.md       # 本文档
├── MIGRATION_GUIDE.md  # 迁移指南
├── conftest.py         # pytest配置（不需要修改）
├── utils.py            # 工具类（不需要修改）
├── test_login.py       # 登录测试
└── test_workflow.py    # Workflow测试

test-data/
└── aevatar_test_data.yaml  # ⭐ 测试数据（这里添加场景）
```

## 下一步

- 📖 阅读完整文档：`tests/aevatar/README.md`
- 🔄 了解迁移：`tests/aevatar/MIGRATION_GUIDE.md`
- 🎯 添加更多测试场景到 YAML 文件
- 🚀 集成到 CI/CD 流程

## 需要帮助？

- 查看测试日志：`logs/pytest.log`
- 查看截图：`test-screenshots/`
- 查看报告：`reports/`
- 查阅文档：`tests/aevatar/README.md`

## 示例：完整的测试流程

```bash
# 1. 快速验证核心功能
pytest tests/aevatar/test_login.py::test_valid_login_only -v

# 2. 验证安全机制
pytest tests/aevatar/test_login.py::test_invalid_credentials_only -v

# 3. 运行所有登录测试场景
pytest tests/aevatar/test_login.py -v

# 4. 运行workflow测试
pytest tests/aevatar/test_workflow.py::test_basic_workflow_only -v

# 5. 生成完整报告
python run_aevatar_tests.py --html --json

# 6. 查看报告
open reports/aevatar-report.html
```

就这么简单！开始测试吧！🎉

