# Workflow E2E 测试执行指南

## 概述

本文档描述如何执行Dashboard Workflows模块的端到端(E2E)测试。这些测试验证完整的功能流程，而不仅仅是单个UI元素。

## 测试环境

- **测试地址**: `http://localhost:5173`
- **测试账户**: `haylee@test.com / Wh520520!`
- **浏览器**: Chrome/Chromium
- **Python版本**: 3.8+
- **依赖**: Playwright, Pytest, Allure

## 测试用例列表

### P0级测试 (关键功能)

#### 1. test_workflow_create_and_run_e2e
**测试目标**: 验证Workflow创建和运行的完整流程

**测试步骤**:
1. 登录系统
2. 导航到Workflows页面
3. 创建新的Workflow
4. 添加InputGAgent到画布
5. 配置Agent参数 (member_name: "test_e2e", input: "中国美食推荐")
6. 运行Workflow
7. 验证执行结果

**预期结果**:
- Workflow成功创建
- Agent成功添加到画布
- Workflow成功运行
- 能检测到Execution log按钮或Success状态

**执行命令**:
```bash
pytest tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflowsE2E::test_workflow_create_and_run_e2e -v -s
```

### P1级测试 (重要功能)

#### 2. test_workflow_full_lifecycle_e2e
**测试目标**: 验证Workflow的完整生命周期

**测试步骤**:
1. 创建新Workflow
2. 运行Workflow
3. 返回Workflows列表页面
4. 验证Workflow存在于列表中
5. 清理测试数据

**预期结果**:
- 完整的创建-运行-返回流程顺利执行
- Workflow列表正常显示

**执行命令**:
```bash
pytest tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflowsE2E::test_workflow_full_lifecycle_e2e -v -s
```

#### 3. test_agent_drag_and_drop_e2e
**测试目标**: 验证Agent拖拽添加功能

**测试步骤**:
1. 点击New Workflow
2. 关闭AI助手弹窗
3. 拖拽InputGAgent到画布
4. 验证配置弹窗出现
5. 配置Agent参数

**预期结果**:
- Agent成功拖拽到画布
- 配置弹窗正常打开
- 参数配置成功

**执行命令**:
```bash
pytest tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflowsE2E::test_agent_drag_and_drop_e2e -v -s
```

## 批量执行

### 执行所有E2E测试
```bash
# 执行所有E2E标记的测试
pytest tests/aevatar/test_dashboard_workflows.py -m e2e -v -s

# 生成Allure报告
pytest tests/aevatar/test_dashboard_workflows.py -m e2e -v -s --alluredir=allure-results
allure serve allure-results
```

### 执行P0级E2E测试
```bash
pytest tests/aevatar/test_dashboard_workflows.py -m "e2e and p0" -v -s
```

### 执行P1级E2E测试
```bash
pytest tests/aevatar/test_dashboard_workflows.py -m "e2e and p1" -v -s
```

### 并行执行
```bash
# 使用pytest-xdist并行执行(注意：E2E测试可能有依赖，需谨慎使用)
pytest tests/aevatar/test_dashboard_workflows.py -m e2e -n 2 -v
```

## 测试数据

测试数据存储在: `test-data/aevatar/workflow_test_data.yaml`

### 主要测试场景

1. **基础创建和运行**
   - Agent类型: InputGAgent
   - 成员名称: test_basic
   - 输入内容: 中国美食推荐

2. **完整生命周期**
   - Agent类型: InputGAgent
   - 成员名称: lifecycle_test (动态生成时间戳)
   - 输入内容: 测试生命周期

3. **拖拽功能**
   - Agent类型: InputGAgent
   - 成员名称: drag_test
   - 输入内容: 拖拽测试输入

## 新增页面方法

在 `pages/aevatar/dashboard_workflows_page.py` 中新增了以下方法：

### 完整流程方法

1. **create_and_configure_workflow(workflow_config)**
   - 创建并配置新的Workflow
   - 参数: `{"agent_type": "InputGAgent", "member_name": "test", "input": "测试"}`

2. **add_agent_to_canvas(agent_type)**
   - 通过拖拽添加Agent到画布
   - 参数: Agent类型名称 (如 "InputGAgent")

3. **configure_agent(config)**
   - 配置Agent参数
   - 参数: `{"member_name": "test", "input": "测试输入"}`

4. **run_workflow()**
   - 运行Workflow

5. **verify_workflow_execution(timeout)**
   - 验证Workflow执行结果
   - 参数: 超时时间(毫秒)

6. **delete_workflow(workflow_name)**
   - 删除指定Workflow
   - 参数: Workflow名称

### 使用示例

```python
from pages.aevatar.dashboard_workflows_page import DashboardWorkflowsPage

# 创建页面对象
workflows_page = DashboardWorkflowsPage(page)

# 完整流程
workflow_config = {
    "agent_type": "InputGAgent",
    "member_name": "test",
    "input": "测试输入"
}

# 1. 创建和配置
workflows_page.create_and_configure_workflow(workflow_config)

# 2. 运行
workflows_page.run_workflow()

# 3. 验证
workflows_page.verify_workflow_execution(timeout=15000)

# 4. 删除
workflows_page.delete_workflow("test_workflow")
```

## 测试特点

### 与简单测试的区别

#### 简单测试 (之前)
```python
def test_new_workflow_button(self):
    """仅测试按钮是否可见"""
    button = self.page.locator("button:has-text('New Workflow')")
    assert button.is_visible()
```

#### E2E测试 (现在)
```python
def test_workflow_create_and_run_e2e(self):
    """测试完整的创建和运行流程"""
    # 1. 创建并配置
    success = self.workflows_page.create_and_configure_workflow(config)
    assert success
    
    # 2. 运行
    success = self.workflows_page.run_workflow()
    assert success
    
    # 3. 验证执行结果
    success = self.workflows_page.verify_workflow_execution()
    assert success
```

### E2E测试的优势

1. **验证真实功能**: 测试用户实际使用的完整流程
2. **发现集成问题**: 能发现单元测试无法发现的模块间集成问题
3. **业务价值高**: 直接验证业务功能是否正常
4. **覆盖范围广**: 一个测试用例覆盖多个功能点

## 调试建议

### 1. 查看详细日志
```bash
pytest tests/aevatar/test_dashboard_workflows.py::TestDashboardWorkflowsE2E::test_workflow_create_and_run_e2e -v -s --log-cli-level=INFO
```

### 2. 查看截图
测试失败时会自动截图，路径: `test-screenshots/workflows/`

关键截图包括:
- `workflow_create_failed.png` - 创建失败
- `add_agent_failed.png` - Agent添加失败
- `workflow_run_failed.png` - 运行失败
- `workflow_execution_failed.png` - 执行验证失败

### 3. 非Headless模式运行
修改 `config/test_config.yaml`:
```yaml
browser:
  headless: false  # 改为false可以看到浏览器操作
  slow_mo: 500     # 增加延迟，便于观察
```

### 4. 调试单个步骤
在代码中添加断点或额外的等待时间:
```python
# 在关键步骤后添加
self.page.wait_for_timeout(5000)  # 等待5秒观察
self.take_screenshot("debug_step_1.png")
```

## 常见问题

### Q1: Agent拖拽失败
**原因**: 元素定位不准确或页面还未完全加载
**解决**: 
- 增加等待时间
- 检查Agent选择器是否正确
- 确认画布位置计算是否准确

### Q2: Workflow运行后无法验证结果
**原因**: 执行时间超过超时设置
**解决**: 
- 增加 `verify_workflow_execution()` 的timeout参数
- 检查网络连接
- 确认Workflow配置是否正确

### Q3: 登录后跳转到错误页面
**原因**: 登录凭证错误或环境问题
**解决**:
- 验证测试账户是否有效
- 检查base_url配置是否正确
- 确认测试环境是否正常运行

## 性能指标

| 测试用例 | 预期耗时 | 操作数 |
|---------|---------|--------|
| test_workflow_create_and_run_e2e | ~30秒 | 7 |
| test_workflow_full_lifecycle_e2e | ~45秒 | 10 |
| test_agent_drag_and_drop_e2e | ~20秒 | 5 |

## 持续集成

### Jenkins配置示例
```groovy
stage('E2E Tests') {
    steps {
        sh 'pytest tests/aevatar/test_dashboard_workflows.py -m e2e --alluredir=allure-results'
    }
    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
```

### GitHub Actions配置示例
```yaml
- name: Run E2E Tests
  run: |
    pytest tests/aevatar/test_dashboard_workflows.py -m e2e -v --alluredir=allure-results
    
- name: Generate Allure Report
  if: always()
  uses: simple-elf/allure-report-action@master
  with:
    allure_results: allure-results
```

## 维护建议

1. **定期更新选择器**: UI变化时及时更新页面对象中的选择器
2. **增加新场景**: 发现新的业务流程时添加对应的E2E测试
3. **优化等待时间**: 根据实际执行情况调整各步骤的等待时间
4. **清理测试数据**: 定期清理测试环境中的测试Workflow
5. **监控失败率**: 关注E2E测试的失败率和失败原因

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

