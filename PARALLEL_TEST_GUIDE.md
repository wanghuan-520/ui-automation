# ⚡ 并行测试指南 - 加速测试执行

## 🚀 快速开始

### 运行并行测试（推荐）

```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation
python3 run_all_tests_parallel.py
```

**预计时间**: 20-30分钟 ⚡（vs 顺序执行60-90分钟）

---

## 📊 并行 vs 顺序对比

| 方案 | 执行时间 | 资源占用 | 适用场景 |
|------|---------|---------|---------|
| **并行执行** ⚡ | 20-30分钟 | 高（4个浏览器） | 正常运行、CI/CD |
| 顺序执行 | 60-90分钟 | 低（1个浏览器） | 资源受限、调试 |

---

## ⚙️ 并行配置说明

### 默认配置（推荐）

```python
PARALLEL_WORKERS = 4  # 4个并行worker
```

**说明**:
- 同时运行4个测试模块
- 每个worker一个独立的浏览器实例
- 约占用4-6GB内存
- 适合大部分Mac电脑

### 自定义并行数

根据你的硬件调整：

#### 高性能机器（16GB+ 内存）
```bash
pytest tests/aevatar/ -n 6 --alluredir=allure-results
```
- 6个并行worker
- **预计时间**: 15-20分钟

#### 标准机器（8GB 内存）
```bash
pytest tests/aevatar/ -n 4 --alluredir=allure-results
```
- 4个并行worker（默认）
- **预计时间**: 20-30分钟

#### 低配机器（4GB 内存）
```bash
pytest tests/aevatar/ -n 2 --alluredir=allure-results
```
- 2个并行worker
- **预计时间**: 35-45分钟

---

## 🔧 pytest-xdist 详解

### 分发策略

#### 1. loadfile（推荐）
```bash
pytest -n 4 --dist loadfile tests/aevatar/
```
- 按文件分发
- 每个测试文件作为一个整体
- 适合我们的场景（8个独立的测试文件）

#### 2. loadscope
```bash
pytest -n 4 --dist loadscope tests/aevatar/
```
- 按测试类/模块分发
- 更细粒度的分发
- 适合单文件内有多个测试类

#### 3. load（默认）
```bash
pytest -n 4 tests/aevatar/
```
- 动态负载均衡
- 自动平衡各worker的工作量

### 并行选项

```bash
# 自动检测CPU核心数
pytest -n auto tests/aevatar/

# 指定worker数
pytest -n 4 tests/aevatar/

# 单独运行（不并行）
pytest tests/aevatar/
```

---

## 📋 完整命令示例

### 基础并行运行
```bash
pytest tests/aevatar/ \
    -n 4 \
    --dist loadfile \
    --alluredir=allure-results
```

### 带详细输出
```bash
pytest tests/aevatar/ \
    -n 4 \
    --dist loadfile \
    -v \
    --tb=short \
    --alluredir=allure-results
```

### 快速失败模式
```bash
pytest tests/aevatar/ \
    -n 4 \
    --dist loadfile \
    --maxfail=5 \
    --alluredir=allure-results
```

### 只运行特定优先级
```bash
# P0测试（并行）
pytest tests/aevatar/ \
    -n 4 \
    -m p0 \
    --dist loadfile \
    --alluredir=allure-results

# P1测试（并行）
pytest tests/aevatar/ \
    -n 4 \
    -m p1 \
    --dist loadfile \
    --alluredir=allure-results
```

---

## ⚠️ 注意事项

### 1. 浏览器窗口
- 并行测试会同时打开多个Chrome窗口
- 这是正常现象，不要手动关闭
- 测试完成后会自动清理

### 2. 资源占用
每个worker大约占用：
- **CPU**: 15-25%
- **内存**: 1-1.5GB
- **总计** (4 workers): CPU 60-100%, 内存 4-6GB

### 3. 端口冲突
- 每个worker使用不同的调试端口
- Playwright会自动处理，无需手动配置

### 4. 数据隔离
- 每个worker有独立的浏览器上下文
- 测试数据互不影响
- 使用时间戳生成唯一标识避免冲突

---

## 🐛 问题排查

### 问题1: 资源不足错误
```
fork: Resource temporarily unavailable
```

**解决方案**:
1. 减少并行数: `-n 2`
2. 关闭其他应用程序
3. 重启系统释放资源

### 问题2: 某些测试一直失败
```
FAILED tests/aevatar/test_xxx.py::test_xxx
```

**解决方案**:
1. 单独运行该测试调试:
```bash
pytest tests/aevatar/test_xxx.py -v
```

2. 排除该测试，运行其他:
```bash
pytest tests/aevatar/ -n 4 --ignore=tests/aevatar/test_xxx.py
```

### 问题3: 测试顺序问题
某些测试依赖执行顺序？

**解决方案**:
1. 使用 `@pytest.mark.dependency`
2. 或改用顺序执行:
```bash
python3 run_all_tests_sequential.py
```

### 问题4: 截图混乱
多个测试同时运行，截图文件名冲突？

**解决方案**:
使用时间戳+随机数命名（已在测试代码中实现）:
```python
filename = f"screenshot_{datetime.now().strftime('%H%M%S')}_{random.randint(1000,9999)}.png"
```

---

## 📊 性能优化建议

### 1. 按模块分批并行
如果全部运行仍然资源紧张，可以分2批：

#### 批次1: 快速测试（10分钟）
```bash
pytest tests/aevatar/test_daily_regression_login.py \
       tests/aevatar/test_daily_regression_dashboard.py \
       tests/aevatar/test_daily_regression_profile.py \
       -n 3 --alluredir=allure-results
```

#### 批次2: 复杂测试（15-20分钟）
```bash
pytest tests/aevatar/test_daily_regression_organisation.py \
       tests/aevatar/test_daily_regression_project.py \
       tests/aevatar/test_daily_regression_workflow.py \
       -n 3 --alluredir=allure-results
```

#### 批次3: 其他测试（10分钟）
```bash
pytest tests/aevatar/test_daily_regression_apikeys.py \
       tests/aevatar/test_daily_regression_configuration.py \
       -n 2 --alluredir=allure-results
```

#### 最后生成报告
```bash
allure generate allure-results -o allure-report --clean
open allure-report/index.html
```

### 2. 使用测试标记分组
```bash
# 只运行核心功能（并行）
pytest -n 4 -m "p0" tests/aevatar/

# 只运行Organisation相关（并行）
pytest -n 3 -m "organisation" tests/aevatar/

# 只运行Project相关（并行）
pytest -n 3 -m "project" tests/aevatar/
```

---

## 🎯 推荐方案矩阵

| 场景 | 命令 | 时间 | 资源 |
|------|------|------|------|
| **日常回归** ⭐ | `python3 run_all_tests_parallel.py` | 20-30分钟 | 中等 |
| 快速验证 | `pytest -n auto -m p0 tests/aevatar/` | 10-15分钟 | 高 |
| CI/CD | `pytest -n 6 --maxfail=5 tests/aevatar/` | 15-20分钟 | 高 |
| 本地调试 | `python3 run_all_tests_sequential.py` | 60-90分钟 | 低 |
| 资源受限 | `pytest -n 2 tests/aevatar/` | 35-45分钟 | 低 |

---

## 📈 预期加速效果

### 理论加速比

```
加速比 = 顺序执行时间 / 并行执行时间
```

| Worker数 | 理论加速 | 实际加速 | 原因 |
|---------|---------|---------|------|
| 2 | 2x | 1.7x | 启动开销、测试不平衡 |
| 4 | 4x | 3x | 浏览器初始化时间 |
| 6 | 6x | 4x | CPU/IO瓶颈 |
| 8 | 8x | 4.5x | 资源竞争严重 |

**结论**: 4个worker是性价比最高的选择

---

## 🔍 监控并行执行

### 查看正在运行的测试
```bash
# 查看pytest进程
ps aux | grep pytest

# 查看Chrome进程数
ps aux | grep Chrome | wc -l

# 预期看到: 4-5个Chrome进程（4 workers + 1主进程）
```

### 查看系统资源
```bash
# 实时监控
top -l 1

# 或使用活动监视器
open -a "Activity Monitor"
```

---

## ✅ 执行检查清单

运行并行测试前确认：

- [ ] 系统内存 ≥ 8GB
- [ ] 可用内存 ≥ 4GB
- [ ] 已关闭不必要的应用
- [ ] pytest-xdist 已安装 (`pip install pytest-xdist`)
- [ ] Chrome浏览器已安装
- [ ] 网络连接正常

---

## 🆚 三种执行模式对比

### 并行执行（推荐）
```bash
python3 run_all_tests_parallel.py
```
- ⚡ **速度**: 最快（20-30分钟）
- 💾 **资源**: 中高（4-6GB）
- 🎯 **适用**: 日常回归、CI/CD

### 顺序执行
```bash
python3 run_all_tests_sequential.py
```
- 🐢 **速度**: 慢（60-90分钟）
- 💾 **资源**: 低（1-2GB）
- 🎯 **适用**: 资源受限、详细调试

### 混合执行
```bash
# 先并行运行快速测试
pytest -n 4 -m p0 tests/aevatar/

# 再顺序运行复杂测试
pytest tests/aevatar/test_daily_regression_organisation.py
```
- ⚖️ **速度**: 中等（35-50分钟）
- 💾 **资源**: 中等（2-4GB）
- 🎯 **适用**: 平衡方案

---

## 🎉 开始并行测试！

**一键运行**:
```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation
python3 run_all_tests_parallel.py
```

**自定义运行**:
```bash
# 高性能模式
pytest tests/aevatar/ -n 6 --dist loadfile --alluredir=allure-results

# 标准模式
pytest tests/aevatar/ -n 4 --dist loadfile --alluredir=allure-results

# 安全模式
pytest tests/aevatar/ -n 2 --dist loadfile --alluredir=allure-results
```

**生成报告**:
```bash
allure generate allure-results -o allure-report --clean
open allure-report/index.html
```

---

**最后更新**: 2025-10-30  
**推荐配置**: 4 workers, loadfile分发策略  
**预计时间**: 20-30分钟 ⚡
