# 🚨 系统资源恢复与测试执行指南

## 📋 当前状态

**问题**: 系统进程数达到上限
```
spawn /usr/local/bin/bash EAGAIN
fork: Resource temporarily unavailable
```

**影响**: 
- 无法启动新的命令
- 无法创建新进程
- 测试无法正常执行

**根本原因**: 可能有大量残留的浏览器/Playwright进程占用系统资源

---

## 🔧 解决方案

### 方案1: 重启系统（最彻底）

**推荐指数**: ⭐⭐⭐⭐⭐

这是最快速、最彻底的解决方案。

```bash
# 重启后，直接进入步骤3运行测试
```

### 方案2: 手动清理进程（不重启）

**推荐指数**: ⭐⭐⭐⭐

#### 步骤1: 打开活动监视器
1. 按 `Command + Space` 打开Spotlight
2. 输入 "Activity Monitor"（活动监视器）
3. 打开应用

#### 步骤2: 查找并终止进程
在活动监视器中搜索并强制退出以下进程：

**需要终止的进程**:
- `Google Chrome` (带 remote-debugging 参数的)
- `Chromium`
- `playwright`
- `node` (Playwright相关的)
- `python3` (之前失败的测试进程)

**操作方法**:
1. 在搜索框输入进程名
2. 选中进程
3. 点击 ❌ 按钮
4. 选择"强制退出"

#### 步骤3: 验证清理结果
打开终端，运行：
```bash
ps aux | grep -E "chrome|playwright|python.*pytest" | wc -l
```
如果返回的数字小于5，说明清理成功。

---

## 🚀 运行所有测试（3种方法）

清理完系统资源后，选择以下任一方法：

### 方法1: 使用顺序执行脚本（推荐）⭐⭐⭐⭐⭐

**优点**: 
- 逐个运行模块，不会耗尽资源
- 自动生成Allure报告
- 有详细的进度显示

```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation
python3 run_all_tests_sequential.py
```

**预计耗时**: 60-90分钟（8个模块）

**脚本特点**:
- 每个模块运行完等待10秒释放资源
- 自动收集所有结果到allure-results
- 最后统一生成Allure报告

---

### 方法2: 使用官方脚本

```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation
python3 run_daily_regression_allure.py --all
```

**提示**: 如果再次遇到资源问题，改用方法1

---

### 方法3: 分批运行（最安全）⭐⭐⭐⭐⭐

如果担心资源问题，可以分批运行：

#### 批次1: 核心功能（P0）
```bash
python3 run_daily_regression_allure.py --p0
```

#### 批次2: Dashboard模块
```bash
python3 -m pytest tests/aevatar/test_daily_regression_dashboard.py \
    -v --alluredir=allure-results
```

#### 批次3: API Keys
```bash
python3 -m pytest tests/aevatar/test_daily_regression_apikeys.py \
    -v --alluredir=allure-results
```

#### 批次4: Workflows
```bash
python3 -m pytest tests/aevatar/test_daily_regression_workflow.py \
    -v --alluredir=allure-results
```

#### 批次5: Configuration
```bash
python3 -m pytest tests/aevatar/test_daily_regression_configuration.py \
    -v --alluredir=allure-results
```

#### 批次6: Profile
```bash
python3 -m pytest tests/aevatar/test_daily_regression_profile.py \
    -v --alluredir=allure-results
```

#### 批次7: Organisation
```bash
python3 -m pytest tests/aevatar/test_daily_regression_organisation.py \
    -v --alluredir=allure-results
```

#### 批次8: Project
```bash
python3 -m pytest tests/aevatar/test_daily_regression_project.py \
    -v --alluredir=allure-results
```

#### 最后: 生成总报告
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## 📊 查看Allure报告

### 方法1: 直接打开HTML（最简单）
```bash
open allure-report/index.html
```

### 方法2: 使用Allure服务器
```bash
allure open allure-report
```

### 方法3: 实时服务器（推荐）
```bash
allure serve allure-results
```

---

## 🎯 测试模块清单

总共8个测试模块：

| # | 模块 | 文件 | 估计用例数 | 优先级 |
|---|------|------|-----------|-------|
| 1 | 登录 | test_daily_regression_login.py | 2 | P0 |
| 2 | Dashboard | test_daily_regression_dashboard.py | 3 | P0 |
| 3 | API Keys | test_daily_regression_apikeys.py | 6 | P0/P1 |
| 4 | Workflows | test_daily_regression_workflow.py | 4 | P0/P1 |
| 5 | Configuration | test_daily_regression_configuration.py | 4 | P1 |
| 6 | Profile | test_daily_regression_profile.py | 2 | P1 |
| 7 | Organisation | test_daily_regression_organisation.py | 9 | P0/P1/P2 |
| 8 | Project | test_daily_regression_project.py | 10 | P0/P1/P2 |

**总计**: 约40个测试用例

---

## ⚡ 快速开始（推荐流程）

### 1️⃣ 重启系统
最简单直接的方式

### 2️⃣ 打开终端
```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation
```

### 3️⃣ 运行测试
```bash
python3 run_all_tests_sequential.py
```

### 4️⃣ 等待完成
- 预计60-90分钟
- 可以去喝杯咖啡 ☕

### 5️⃣ 查看报告
```bash
open allure-report/index.html
```

---

## 🔍 监控执行状态

### 查看正在运行的测试
```bash
ps aux | grep pytest
```

### 查看Chrome进程数
```bash
ps aux | grep Chrome | wc -l
```

### 查看系统资源
```bash
top -l 1 | grep "Processes:"
```

---

## 💡 优化建议

### 1. 运行前准备
- 关闭不必要的应用程序
- 确保至少有4GB可用内存
- 关闭其他浏览器窗口

### 2. 运行时注意
- 不要在测试期间打开过多应用
- 让测试自动运行，避免手动干预
- 可以通过日志文件监控进度

### 3. 运行后清理
```bash
# 清理截图（如果不需要保留）
rm -rf test-screenshots/*/

# 清理旧的allure结果
rm -rf allure-results-old/
```

---

## 🆘 常见问题

### Q1: 测试卡住不动怎么办？
**A**: 按 `Ctrl+C` 停止，然后：
```bash
pkill -9 -f pytest
pkill -9 -f chrome
python3 run_all_tests_sequential.py
```

### Q2: 某个模块总是失败怎么办？
**A**: 跳过该模块，运行其他的：
```bash
# 编辑 run_all_tests_sequential.py
# 注释掉问题模块的行
```

### Q3: Allure报告打不开？
**A**: 使用Allure服务器：
```bash
allure serve allure-results
```

### Q4: 想只运行部分测试？
**A**: 使用pytest的-k参数：
```bash
pytest tests/aevatar/ -k "login or workflow" --alluredir=allure-results
```

---

## 📁 生成的文件

运行完成后，你会看到：

```
ui-automation/
├── allure-results/          # 测试结果JSON文件
│   ├── *-result.json
│   ├── *-container.json
│   └── *-attachment.*
├── allure-report/           # HTML报告
│   ├── index.html          # 主报告页面 ⭐
│   ├── data/
│   └── widgets/
└── test-screenshots/        # 测试截图
    ├── dashboard/
    ├── organisation/
    └── project/
```

---

## 🎉 成功标志

当你看到以下输出，说明成功：

```
✅ Allure报告生成成功！
📁 报告位置: allure-report/index.html
```

然后打开报告查看详细结果：
- 总体通过率
- 失败用例详情
- 执行时间趋势
- 测试截图

---

## 📞 需要帮助？

如果遇到问题，查看以下文档：
- `tests/aevatar/README.md` - 测试框架说明
- `tests/aevatar/QUICKSTART.md` - 快速开始
- `tests/aevatar/DAILY_REGRESSION_GUIDE.md` - 详细指南

---

**最后更新**: 2025-10-30  
**版本**: 1.0

