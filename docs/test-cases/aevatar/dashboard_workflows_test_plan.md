# aevatar.ai Dashboard/Workflows 页面测试计划

## 1. 页面概述

### 1.1 基本信息
- **页面URL**: http://localhost:5173/dashboard/workflows
- **页面标题**: aevatar station frontend
- **页面用途**: 工作流管理中心
- **前置条件**: 用户已登录（测试账户：haylee@test.com）

### 1.2 功能描述
Dashboard/Workflows页面是登录后的主工作空间，提供以下功能：
- 查看工作流列表
- 创建新工作流
- 导入工作流
- 查看工作流状态（Pending, Failed, Success）
- 管理工作流（编辑、删除、运行）
- 侧边栏导航（API Keys, Workflows, Configuration）

## 2. 页面元素映射

### 2.1 核心元素定位表

| 元素类型 | 元素名称 | 定位方式 | 定位器 |
|---------|---------|---------|--------|
| 导航栏 | 组织选择器 | Button | `button:has-text('O1')` |
| 导航栏 | 项目选择器 | Button | `button:has-text('default project')` |
| 导航栏 | Dashboard按钮 | Button | `button:has-text('Dashboard')` |
| 导航栏 | Settings按钮 | Button | `button:has-text('Settings')` |
| 导航栏 | Profile按钮 | Role | `button[name='profile']` |
| 侧边栏 | API Keys菜单 | Text | `text=API Keys` |
| 侧边栏 | Workflows菜单 | Text | `text=Workflows` |
| 侧边栏 | Configuration菜单 | Text | `text=Configuration` |
| 按钮 | New Workflow按钮 | Text | `button:has-text('New Workflow')` |
| 按钮 | Import Workflow按钮 | Text | `button:has-text('Import Workflow')` |
| 输入 | 文件选择器 | Button | `button:has-text('Choose File')` |
| 表格 | 工作流列表表格 | Role | `role=table` |
| 表头 | Name列 | Cell | `cell:has-text('Name')` |
| 表头 | Last updated列 | Cell | `cell:has-text('Last updated')` |
| 表头 | Last run列 | Cell | `cell:has-text('Last run')` |
| 表头 | Status列 | Cell | `cell:has-text('Status')` |
| 单元格 | 工作流名称 | Generic | `generic[cursor=pointer]` |
| 下拉菜单 | 操作菜单 | Combobox | `combobox[cursor=pointer]` |
| 链接 | Website链接 | Link | `link:has-text('Website')` |
| 链接 | Github链接 | Link | `link:has-text('Github')` |
| 链接 | Docs链接 | Link | `link:has-text('Docs')` |

### 2.2 页面对象设计

```python
class DashboardWorkflowsPage(BasePage):
    """Dashboard Workflows页面对象"""
    
    # 页面URL
    WORKFLOWS_URL = "http://localhost:5173/dashboard/workflows"
    
    # 顶部导航栏
    ORG_SELECTOR = "button:has-text('O1')"
    PROJECT_SELECTOR = "button:has-text('default project')"
    DASHBOARD_BUTTON = "button:has-text('Dashboard')"
    SETTINGS_BUTTON = "button:has-text('Settings')"
    PROFILE_BUTTON = "button[name='profile']"
    
    # 侧边栏导航
    APIKEYS_MENU = "text=API Keys"
    WORKFLOWS_MENU = "text=Workflows"
    CONFIGURATION_MENU = "text=Configuration"
    
    # 页面主要按钮
    NEW_WORKFLOW_BUTTON = "button:has-text('New Workflow')"
    IMPORT_WORKFLOW_BUTTON = "button:has-text('Import Workflow')"
    CHOOSE_FILE_BUTTON = "button:has-text('Choose File')"
    
    # 工作流表格
    WORKFLOW_TABLE = "role=table"
    WORKFLOW_NAME_CELL = "cell >> generic[cursor=pointer]"
    WORKFLOW_STATUS = "generic:has-text('Pending')"
    WORKFLOW_ACTION_MENU = "combobox[cursor=pointer]"
    
    # 底部链接
    WEBSITE_LINK = "link:has-text('Website')"
    GITHUB_LINK = "link:has-text('Github')"
    DOCS_LINK = "link:has-text('Docs')"
    
    def navigate(self):
        """导航到Workflows页面"""
        self.page.goto(self.WORKFLOWS_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查Workflows页面是否已加载"""
        try:
            self.page.wait_for_selector(self.WORKFLOW_TABLE, timeout=10000)
            return True
        except:
            return False
    
    def click_new_workflow(self):
        """点击New Workflow按钮"""
        self.page.click(self.NEW_WORKFLOW_BUTTON)
        self.page.wait_for_timeout(2000)
    
    def get_workflow_list(self):
        """获取工作流列表"""
        rows = self.page.query_selector_all(f"{self.WORKFLOW_TABLE} >> tbody >> tr")
        workflows = []
        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 4:
                workflows.append({
                    "name": cells[0].text_content().strip(),
                    "last_updated": cells[1].text_content().strip(),
                    "last_run": cells[2].text_content().strip(),
                    "status": cells[3].text_content().strip()
                })
        return workflows
```

## 3. 测试用例设计

### 3.1 P0级测试用例（核心功能）

#### TC-WORKFLOWS-P0-001: 登录后跳转验证
- **优先级**: P0
- **前置条件**: 用户已在登录页面输入有效凭证
- **测试步骤**:
  1. 在登录页面登录成功
  2. 等待页面跳转
  3. 验证当前URL
- **预期结果**: 
  - 跳转到 /dashboard/workflows 页面
  - 页面正常加载，显示工作流列表
- **自动化**: `test_login_redirect_to_workflows()`

#### TC-WORKFLOWS-P0-002: 工作流列表加载
- **优先级**: P0
- **前置条件**: 用户已登录并进入Workflows页面
- **测试步骤**:
  1. 访问 /dashboard/workflows 页面
  2. 等待页面完全加载
  3. 验证表格是否显示
- **预期结果**: 
  - 工作流列表表格正常显示
  - 表头包含：Name, Last updated, Last run, Status
  - 显示现有工作流记录（如果有）

#### TC-WORKFLOWS-P0-003: 创建新工作流按钮
- **优先级**: P0
- **前置条件**: 用户已登录并进入Workflows页面
- **测试步骤**:
  1. 定位"New Workflow"按钮
  2. 验证按钮是否可见和可点击
  3. 点击按钮
- **预期结果**: 
  - "New Workflow"按钮可见且可点击
  - 点击后跳转到工作流创建/编辑页面

#### TC-WORKFLOWS-P0-004: 工作流状态显示
- **优先级**: P0
- **前置条件**: 
  - 用户已登录
  - 系统中存在不同状态的工作流
- **测试步骤**:
  1. 访问Workflows页面
  2. 查看工作流列表中的Status列
  3. 验证状态类型
- **预期结果**: 
  - 正确显示工作流状态：Pending, Failed, Success, "-"（未运行）
  - 状态显示与实际工作流状态一致

#### TC-WORKFLOWS-P0-005: 侧边栏导航功能
- **优先级**: P0
- **前置条件**: 用户已登录并进入Workflows页面
- **测试步骤**:
  1. 点击侧边栏"API Keys"菜单
  2. 验证页面跳转
  3. 返回Workflows页面
  4. 点击"Configuration"菜单
  5. 验证页面跳转
- **预期结果**: 
  - API Keys菜单：跳转到API Keys页面
  - Configuration菜单：跳转到Configuration页面
  - Workflows菜单：停留在当前页面或刷新

### 3.2 P1级测试用例（重要功能）

#### TC-WORKFLOWS-P1-001: 导入工作流功能
- **优先级**: P1
- **前置条件**: 
  - 用户已登录
  - 准备有效的工作流配置文件
- **测试步骤**:
  1. 点击"Import Workflow"按钮
  2. 选择工作流配置文件
  3. 确认导入
- **预期结果**: 
  - 文件选择对话框打开
  - 成功导入后，工作流出现在列表中

#### TC-WORKFLOWS-P1-002: 工作流名称点击跳转
- **优先级**: P1
- **前置条件**: 
  - 用户已登录
  - 工作流列表中存在至少一个工作流
- **测试步骤**:
  1. 点击工作流名称
  2. 验证页面跳转
- **预期结果**: 
  - 跳转到工作流详情/编辑页面
  - 显示该工作流的配置信息

#### TC-WORKFLOWS-P1-003: 工作流操作菜单
- **优先级**: P1
- **前置条件**: 工作流列表中存在至少一个工作流
- **测试步骤**:
  1. 点击工作流行末尾的操作菜单（三点图标）
  2. 验证菜单选项
- **预期结果**: 
  - 显示操作菜单
  - 包含选项：Edit, Delete, Run, Export等

#### TC-WORKFLOWS-P1-004: 组织和项目切换
- **优先级**: P1
- **前置条件**: 
  - 用户账户属于多个组织或项目
- **测试步骤**:
  1. 点击组织选择器
  2. 选择不同组织
  3. 验证页面更新
  4. 点击项目选择器
  5. 选择不同项目
- **预期结果**: 
  - 组织切换后，显示该组织的工作流
  - 项目切换后，显示该项目的工作流

#### TC-WORKFLOWS-P1-005: Settings按钮跳转
- **优先级**: P1
- **前置条件**: 用户已登录
- **测试步骤**:
  1. 点击顶部导航栏的"Settings"按钮
  2. 验证页面跳转
- **预期结果**: 
  - 跳转到 /profile 或 /settings 页面
  - 显示用户设置界面

#### TC-WORKFLOWS-P1-006: Profile按钮功能
- **优先级**: P1
- **前置条件**: 用户已登录
- **测试步骤**:
  1. 点击顶部导航栏的Profile按钮（用户头像）
  2. 验证下拉菜单或跳转
- **预期结果**: 
  - 显示用户菜单（如有）
  - 或跳转到用户Profile页面

#### TC-WORKFLOWS-P1-007: 工作流列表排序
- **优先级**: P1
- **前置条件**: 工作流列表中存在多个工作流
- **测试步骤**:
  1. 观察工作流列表的默认排序
  2. 点击列标题（如Name、Last updated）
  3. 验证排序变化
- **预期结果**: 
  - 默认按Last updated倒序排列
  - 点击列标题可切换排序

#### TC-WORKFLOWS-P1-008: 空工作流列表状态
- **优先级**: P1
- **前置条件**: 
  - 用户首次登录
  - 或工作流已全部删除
- **测试步骤**:
  1. 访问Workflows页面
  2. 验证空状态显示
- **预期结果**: 
  - 显示空状态提示（如"No workflows yet"）
  - "New Workflow"按钮依然可用

### 3.3 P2级测试用例（增强功能与边界）

#### TC-WORKFLOWS-P2-001: 长工作流名称显示
- **优先级**: P2
- **前置条件**: 存在名称很长的工作流
- **测试步骤**:
  1. 创建或查看名称超过50字符的工作流
  2. 在列表中查看显示效果
- **预期结果**: 
  - 长名称正确显示（截断+省略号或换行）
  - 鼠标悬停显示完整名称

#### TC-WORKFLOWS-P2-002: 大量工作流加载性能
- **优先级**: P2
- **前置条件**: 系统中存在100+个工作流
- **测试步骤**:
  1. 访问Workflows页面
  2. 测量页面加载时间
  3. 验证分页或虚拟滚动
- **预期结果**: 
  - 页面在3秒内加载完成
  - 如有分页，显示分页控件

#### TC-WORKFLOWS-P2-003: 导入无效工作流文件
- **优先级**: P2
- **前置条件**: 准备无效的工作流配置文件
- **测试步骤**:
  1. 点击"Import Workflow"
  2. 选择无效文件（如txt、图片等）
  3. 或选择格式错误的JSON文件
- **预期结果**: 
  - 显示错误提示
  - 不创建工作流记录

#### TC-WORKFLOWS-P2-004: 工作流状态实时更新
- **优先级**: P2
- **前置条件**: 有正在运行的工作流
- **测试步骤**:
  1. 运行一个工作流
  2. 停留在Workflows页面
  3. 观察状态变化
- **预期结果**: 
  - 工作流状态从Pending → Running → Success/Failed
  - 状态自动刷新（WebSocket或轮询）

#### TC-WORKFLOWS-P2-005: 同时操作多个工作流
- **优先级**: P2
- **前置条件**: 工作流列表中存在多个工作流
- **测试步骤**:
  1. 同时运行多个工作流
  2. 或批量删除多个工作流
- **预期结果**: 
  - 系统正常处理并发操作
  - 状态更新正确

#### TC-WORKFLOWS-P2-006: 网络断开时的表现
- **优先级**: P2
- **前置条件**: 用户已登录Workflows页面
- **测试步骤**:
  1. 断开网络连接
  2. 尝试创建新工作流
  3. 恢复网络连接
- **预期结果**: 
  - 显示网络错误提示
  - 恢复连接后自动重试或提示刷新

#### TC-WORKFLOWS-P2-007: 浏览器刷新后状态保持
- **优先级**: P2
- **前置条件**: 用户已在Workflows页面
- **测试步骤**:
  1. 在Workflows页面执行操作
  2. 刷新浏览器（F5）
  3. 验证页面状态
- **预期结果**: 
  - 用户仍保持登录状态
  - 工作流列表正确加载

#### TC-WORKFLOWS-P2-008: 底部链接打开方式
- **优先级**: P2
- **前置条件**: 用户在Workflows页面
- **测试步骤**:
  1. 右键点击Website/Github/Docs链接
  2. 选择"在新标签页打开"
  3. 验证打开方式
- **预期结果**: 
  - 链接应在新标签页打开（target="_blank"）
  - 原页面保持不变

## 4. 测试数据设计

### 4.1 工作流测试数据
```json
{
  "valid_workflows": [
    {
      "name": "test_workflow_001",
      "description": "基础测试工作流",
      "type": "simple"
    },
    {
      "name": "long_name_workflow_with_very_long_description_that_exceeds_normal_length",
      "description": "长名称工作流",
      "type": "edge_case"
    }
  ],
  "invalid_workflows": [
    {
      "name": "",
      "description": "空名称工作流",
      "expected_error": "名称不能为空"
    },
    {
      "name": "duplicate_workflow",
      "description": "重复名称工作流",
      "expected_error": "工作流名称已存在"
    }
  ]
}
```

### 4.2 工作流状态测试数据
```json
{
  "workflow_statuses": [
    "Pending",
    "Running",
    "Success",
    "Failed",
    "-"
  ]
}
```

### 4.3 导入文件测试数据
```json
{
  "valid_import_files": [
    "test_workflow.json",
    "workflow_config.yaml"
  ],
  "invalid_import_files": [
    "invalid.txt",
    "corrupted.json",
    "image.png"
  ]
}
```

## 5. 自动化实现建议

### 5.1 页面类实现
创建新文件：`pages/aevatar/dashboard_workflows_page.py`

```python
"""
Dashboard Workflows页面对象
负责工作流列表管理功能
"""
from pages.base_page import BasePage
from playwright.sync_api import expect
import allure

class DashboardWorkflowsPage(BasePage):
    """Dashboard Workflows页面"""
    
    # 实现上述定位器和方法
    # ...
    
    @allure.step("创建新工作流")
    def create_new_workflow(self, workflow_name: str):
        """创建新工作流"""
        self.click_new_workflow()
        # 在工作流编辑页面填写信息
        # ...
    
    @allure.step("验证工作流列表包含指定工作流")
    def verify_workflow_exists(self, workflow_name: str):
        """验证工作流是否存在于列表中"""
        workflows = self.get_workflow_list()
        workflow_names = [wf["name"] for wf in workflows]
        assert workflow_name in workflow_names, \
            f"工作流 '{workflow_name}' 不在列表中"
```

### 5.2 测试类实现
创建新文件：`tests/aevatar/test_dashboard_workflows.py`

```python
import pytest
import allure
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.dashboard_workflows_page import DashboardWorkflowsPage

@allure.feature("Dashboard功能")
@allure.story("工作流管理")
class TestDashboardWorkflows:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """自动登录前置条件"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        self.workflows_page = DashboardWorkflowsPage(page)
        self.workflows_page.wait_for_page_load()
    
    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.title("TC-WORKFLOWS-P0-001: 登录后跳转验证")
    def test_login_redirect_to_workflows(self, page):
        """测试登录后跳转到Workflows页面"""
        assert "/dashboard/workflows" in page.url
        assert self.workflows_page.is_loaded()
    
    @pytest.mark.P0
    @allure.title("TC-WORKFLOWS-P0-002: 工作流列表加载")
    def test_workflow_list_loads(self):
        """测试工作流列表正常加载"""
        workflows = self.workflows_page.get_workflow_list()
        assert isinstance(workflows, list)
    
    @pytest.mark.P0
    @allure.title("TC-WORKFLOWS-P0-003: 创建新工作流按钮")
    def test_new_workflow_button(self):
        """测试New Workflow按钮功能"""
        self.workflows_page.click_new_workflow()
        # 验证跳转到工作流编辑页面
        # assert workflow_edit_page.is_loaded()
```

### 5.3 配置建议
更新配置文件：`test-data/aevatar/aevatar_test_data.yaml`

```yaml
# Dashboard Workflows页面配置
dashboard:
  workflows_url: "http://localhost:5173/dashboard/workflows"
  default_timeout: 10000
  
# 工作流测试数据
workflow_test_data:
  - name: "test_workflow_basic"
    type: "simple"
    expected_status: "Success"
  - name: "test_workflow_complex"
    type: "complex"
    expected_status: "Pending"
```

## 6. 执行计划

### 6.1 测试阶段
- **P0测试**: 每次部署前执行，预计耗时 8分钟
- **P1测试**: 每日回归测试，预计耗时 15分钟
- **P2测试**: 每周完整测试，预计耗时 20分钟

### 6.2 验收标准
- P0测试用例通过率 100%
- P1测试用例通过率 ≥ 95%
- P2测试用例通过率 ≥ 90%
- 页面加载时间 < 3秒
- 工作流操作响应时间 < 2秒

### 6.3 风险评估
- **高风险**: WebSocket连接可能影响实时状态更新
- **中风险**: 大量工作流时的性能问题
- **低风险**: UI元素定位器可能随版本更新

## 7. 集成测试建议

### 7.1 与其他页面的集成
- **登录 → Workflows**: 验证登录后跳转流程
- **Workflows → Profile**: 验证Settings按钮跳转
- **Workflows → API Keys**: 验证侧边栏导航
- **Workflows → Configuration**: 验证配置管理流程

### 7.2 端到端测试场景
```python
@allure.title("E2E: 完整工作流创建和运行流程")
def test_complete_workflow_lifecycle(page):
    """端到端测试：登录 → 创建工作流 → 运行 → 验证结果"""
    # 1. 登录
    login_page.login_with_email("haylee@test.com", "Wh520520!")
    
    # 2. 创建工作流
    workflows_page.create_new_workflow("e2e_test_workflow")
    
    # 3. 运行工作流
    workflows_page.run_workflow("e2e_test_workflow")
    
    # 4. 验证状态
    workflows_page.wait_for_workflow_status("e2e_test_workflow", "Success")
    
    # 5. 清理
    workflows_page.delete_workflow("e2e_test_workflow")
```

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

