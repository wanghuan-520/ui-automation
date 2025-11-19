# aevatar.ai API Keys 页面测试计划

## 1. 页面概述

### 1.1 基本信息
- **页面URL**: http://localhost:5173/dashboard/apikeys
- **页面标题**: aevatar station frontend
- **页面用途**: API密钥管理中心
- **前置条件**: 用户已登录（测试账户：haylee@test.com）

### 1.2 功能描述
API Keys页面用于管理项目的API密钥，提供以下功能：
- 创建新的API Key
- 查看API Key列表
- 查看Client ID和API Key
- 查看创建时间和创建者
- 编辑/删除API Key
- 复制Client ID和API Key

## 2. 页面元素映射

### 2.1 核心元素定位表

| 元素类型 | 元素名称 | 定位方式 | 定位器 |
|---------|---------|---------|--------|
| 标题 | API Keys标题 | Text | `text=API Keys` |
| 按钮 | Create按钮 | Button | `button:has-text('Create')` |
| 表格 | API Keys列表表格 | Role | `role=table` |
| 表头 | Name列 | Cell | `cell:has-text('Name')` |
| 表头 | Client ID列 | Cell | `cell:has-text('Client ID')` |
| 表头 | API Key列 | Cell | `cell:has-text('API Key')` |
| 表头 | Created列 | Cell | `cell:has-text('Created')` |
| 表头 | Created By列 | Cell | `cell:has-text('Created By')` |
| 文本 | 空状态提示 | Generic | `generic:has-text('No API keys created yet')` |
| 导航 | API Keys侧边栏 | Generic | `generic:has-text('API Keys')` |
| 导航 | Workflows侧边栏 | Generic | `generic:has-text('Workflows')` |
| 导航 | Configuration侧边栏 | Generic | `generic:has-text('Configuration')` |

### 2.2 页面对象设计

```python
class APIKeysPage(BasePage):
    """API Keys页面对象"""
    
    # 页面URL
    APIKEYS_URL = "http://localhost:5173/dashboard/apikeys"
    
    # 页面标题和按钮
    PAGE_TITLE = "text=API Keys"
    CREATE_BUTTON = "button:has-text('Create')"
    
    # 表格元素
    APIKEYS_TABLE = "role=table"
    TABLE_HEADER_NAME = "cell:has-text('Name')"
    TABLE_HEADER_CLIENT_ID = "cell:has-text('Client ID')"
    TABLE_HEADER_API_KEY = "cell:has-text('API Key')"
    TABLE_HEADER_CREATED = "cell:has-text('Created')"
    TABLE_HEADER_CREATED_BY = "cell:has-text('Created By')"
    
    # 空状态
    EMPTY_STATE = "generic:has-text('No API keys created yet')"
    
    # 侧边栏导航
    APIKEYS_MENU = "generic:has-text('API Keys')"
    WORKFLOWS_MENU = "generic:has-text('Workflows')"
    CONFIGURATION_MENU = "generic:has-text('Configuration')"
    
    # API Key行操作（动态）
    APIKEY_ROW = "tbody >> tr"
    APIKEY_NAME_CELL = "td:nth-child(1)"
    APIKEY_CLIENT_ID_CELL = "td:nth-child(2)"
    APIKEY_API_KEY_CELL = "td:nth-child(3)"
    APIKEY_ACTION_MENU = "combobox[cursor=pointer]"
    
    # 创建API Key对话框（如果存在）
    CREATE_DIALOG = "role=dialog"
    NAME_INPUT = "input[placeholder*='name' i]"
    DIALOG_CREATE_BUTTON = "button:has-text('Create')"
    DIALOG_CANCEL_BUTTON = "button:has-text('Cancel')"
    
    def navigate(self):
        """导航到API Keys页面"""
        self.page.goto(self.APIKEYS_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查API Keys页面是否已加载"""
        try:
            self.page.wait_for_selector(self.PAGE_TITLE, timeout=5000)
            return True
        except:
            return False
    
    @allure.step("点击Create按钮")
    def click_create_button(self):
        """点击Create按钮"""
        self.page.click(self.CREATE_BUTTON)
        self.page.wait_for_timeout(1000)
    
    @allure.step("创建API Key: {name}")
    def create_api_key(self, name: str):
        """创建新的API Key"""
        self.click_create_button()
        
        # 等待对话框出现
        self.page.wait_for_selector(self.CREATE_DIALOG, timeout=5000)
        
        # 填写名称
        self.page.fill(self.NAME_INPUT, name)
        
        # 点击创建
        self.page.click(self.DIALOG_CREATE_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("获取API Keys列表")
    def get_api_keys_list(self):
        """获取API Keys列表"""
        # 检查是否为空状态
        if self.page.is_visible(self.EMPTY_STATE):
            return []
        
        # 获取所有行
        rows = self.page.query_selector_all(f"{self.APIKEYS_TABLE} >> tbody >> tr")
        api_keys = []
        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 5:
                api_keys.append({
                    "name": cells[0].text_content().strip(),
                    "client_id": cells[1].text_content().strip(),
                    "api_key": cells[2].text_content().strip(),
                    "created": cells[3].text_content().strip(),
                    "created_by": cells[4].text_content().strip()
                })
        return api_keys
    
    @allure.step("验证API Key存在: {name}")
    def verify_api_key_exists(self, name: str):
        """验证API Key是否存在于列表中"""
        api_keys = self.get_api_keys_list()
        api_key_names = [key["name"] for key in api_keys]
        assert name in api_key_names, \
            f"API Key '{name}' 不在列表中"
    
    @allure.step("删除API Key: {name}")
    def delete_api_key(self, name: str):
        """删除指定的API Key"""
        # 找到包含该名称的行
        row = self.page.locator(f"tr:has-text('{name}')")
        # 点击操作菜单
        row.locator(self.APIKEY_ACTION_MENU).click()
        self.page.wait_for_timeout(500)
        # 点击删除选项
        self.page.click("text=Delete")
        self.page.wait_for_timeout(2000)
```

## 3. 测试用例设计

### 3.1 P0级测试用例（核心功能）

#### TC-APIKEYS-P0-001: API Keys页面加载
- **优先级**: P0
- **前置条件**: 用户已登录
- **测试步骤**:
  1. 通过侧边栏点击"API Keys"菜单
  2. 验证页面跳转
  3. 检查页面元素加载
- **预期结果**: 
  - 成功跳转到 /dashboard/apikeys 页面
  - 页面标题显示"API Keys"
  - Create按钮可见
  - API Keys列表表格显示

#### TC-APIKEYS-P0-002: 查看空状态
- **优先级**: P0
- **前置条件**: 
  - 用户已登录
  - 项目中没有API Key
- **测试步骤**:
  1. 访问API Keys页面
  2. 查看表格内容
- **预期结果**: 
  - 表格显示"No API keys created yet"提示
  - Create按钮依然可用

#### TC-APIKEYS-P0-003: 创建API Key
- **优先级**: P0
- **前置条件**: 用户已登录并在API Keys页面
- **测试步骤**:
  1. 点击"Create"按钮
  2. 在弹出对话框输入名称 "test_api_key"
  3. 点击对话框的"Create"按钮
  4. 等待创建完成
- **预期结果**: 
  - 弹出创建对话框
  - 创建成功后显示成功提示
  - 新API Key出现在列表中
  - 显示Client ID和API Key
  - 显示创建时间和创建者

#### TC-APIKEYS-P0-004: 查看API Key列表
- **优先级**: P0
- **前置条件**: 
  - 用户已登录
  - 至少存在一个API Key
- **测试步骤**:
  1. 访问API Keys页面
  2. 查看API Keys列表
  3. 验证列表字段完整性
- **预期结果**: 
  - 列表正确显示所有API Keys
  - 每个API Key包含：Name, Client ID, API Key, Created, Created By
  - Client ID和API Key以加密形式显示（如****）

#### TC-APIKEYS-P0-005: 删除API Key
- **优先级**: P0
- **前置条件**: 
  - 用户已登录
  - 至少存在一个API Key
- **测试步骤**:
  1. 找到要删除的API Key行
  2. 点击操作菜单（三点图标）
  3. 选择"Delete"选项
  4. 确认删除
- **预期结果**: 
  - 显示删除确认对话框
  - 确认后API Key从列表中移除
  - 显示删除成功提示

### 3.2 P1级测试用例（重要功能）

#### TC-APIKEYS-P1-001: 创建重复名称API Key
- **优先级**: P1
- **前置条件**: 已存在名为"test_key"的API Key
- **测试步骤**:
  1. 点击Create按钮
  2. 输入已存在的名称"test_key"
  3. 尝试创建
- **预期结果**: 
  - 显示错误提示："API Key名称已存在"
  - 创建失败，不添加到列表

#### TC-APIKEYS-P1-002: 创建空名称API Key
- **优先级**: P1
- **前置条件**: 用户在API Keys页面
- **测试步骤**:
  1. 点击Create按钮
  2. 名称输入框保持为空
  3. 点击Create
- **预期结果**: 
  - 显示"名称不能为空"提示
  - 或Create按钮disabled

#### TC-APIKEYS-P1-003: 复制Client ID
- **优先级**: P1
- **前置条件**: 至少存在一个API Key
- **测试步骤**:
  1. 找到API Key的Client ID列
  2. 点击复制图标（如果有）
  3. 验证剪贴板内容
- **预期结果**: 
  - Client ID成功复制到剪贴板
  - 显示"Copied"提示

#### TC-APIKEYS-P1-004: 复制API Key
- **优先级**: P1
- **前置条件**: 至少存在一个API Key
- **测试步骤**:
  1. 找到API Key列
  2. 点击显示/复制图标
  3. 验证API Key显示和复制
- **预期结果**: 
  - 点击后显示完整API Key
  - 成功复制到剪贴板

#### TC-APIKEYS-P1-005: 编辑API Key名称
- **优先级**: P1
- **前置条件**: 至少存在一个API Key
- **测试步骤**:
  1. 点击API Key的操作菜单
  2. 选择"Edit"选项
  3. 修改名称为"updated_key"
  4. 保存修改
- **预期结果**: 
  - 弹出编辑对话框
  - 名称成功更新
  - 列表显示新名称

#### TC-APIKEYS-P1-006: 取消创建API Key
- **优先级**: P1
- **前置条件**: 用户在API Keys页面
- **测试步骤**:
  1. 点击Create按钮
  2. 输入名称
  3. 点击Cancel按钮
- **预期结果**: 
  - 对话框关闭
  - 不创建新API Key

#### TC-APIKEYS-P1-007: API Key列表排序
- **优先级**: P1
- **前置条件**: 存在多个API Keys
- **测试步骤**:
  1. 观察默认排序
  2. 点击列标题（如Name、Created）
  3. 验证排序变化
- **预期结果**: 
  - 默认按创建时间倒序排列
  - 点击列标题可切换排序

#### TC-APIKEYS-P1-008: 删除确认对话框
- **优先级**: P1
- **前置条件**: 至少存在一个API Key
- **测试步骤**:
  1. 点击删除操作
  2. 在确认对话框点击"Cancel"
- **预期结果**: 
  - 对话框关闭
  - API Key未被删除

### 3.3 P2级测试用例（安全与边界）

#### TC-APIKEYS-P2-001: 特殊字符名称
- **优先级**: P2
- **前置条件**: 用户在API Keys页面
- **测试步骤**:
  1. 创建名称包含特殊字符的API Key
  2. 如："key@#$%", "key with spaces"
- **预期结果**: 
  - 系统正确处理特殊字符
  - 或显示"仅支持字母、数字、下划线"提示

#### TC-APIKEYS-P2-002: 超长名称
- **优先级**: P2
- **前置条件**: 用户在API Keys页面
- **测试步骤**:
  1. 输入超长名称（100+字符）
  2. 尝试创建
- **预期结果**: 
  - 显示长度限制提示
  - 或截断到最大长度

#### TC-APIKEYS-P2-003: 大量API Keys加载
- **优先级**: P2
- **前置条件**: 项目中存在50+个API Keys
- **测试步骤**:
  1. 访问API Keys页面
  2. 测量加载时间
  3. 验证分页功能
- **预期结果**: 
  - 页面在3秒内加载完成
  - 支持分页或虚拟滚动

#### TC-APIKEYS-P2-004: API Key安全显示
- **优先级**: P2
- **前置条件**: 至少存在一个API Key
- **测试步骤**:
  1. 查看API Key列显示
  2. 验证是否默认加密显示
  3. 检查是否需要点击才能查看完整Key
- **预期结果**: 
  - API Key默认以****形式显示
  - 需要明确操作才能查看完整Key
  - 查看后有超时自动隐藏

#### TC-APIKEYS-P2-005: 权限验证 - 普通成员
- **优先级**: P2
- **前置条件**: 使用普通成员账户登录
- **测试步骤**:
  1. 访问API Keys页面
  2. 尝试创建API Key
  3. 尝试删除API Key
- **预期结果**: 
  - 根据权限配置，普通成员可能无法创建/删除
  - 或只能查看自己创建的API Keys

#### TC-APIKEYS-P2-006: API Key唯一性验证
- **优先级**: P2
- **前置条件**: 系统中已存在API Keys
- **测试步骤**:
  1. 创建新API Key
  2. 验证生成的Client ID和API Key唯一性
  3. 与现有Keys对比
- **预期结果**: 
  - 每个Client ID全局唯一
  - 每个API Key全局唯一

#### TC-APIKEYS-P2-007: 删除正在使用的API Key
- **优先级**: P2
- **前置条件**: 
  - 存在API Key
  - 该Key正在被使用中
- **测试步骤**:
  1. 尝试删除正在使用的API Key
  2. 观察系统响应
- **预期结果**: 
  - 显示警告："该API Key正在使用中，删除后可能影响功能"
  - 需要二次确认才能删除

#### TC-APIKEYS-P2-008: 并发创建API Key
- **优先级**: P2
- **前置条件**: 多个用户同时在线
- **测试步骤**:
  1. 两个用户同时点击Create
  2. 同时提交创建请求
  3. 验证结果
- **预期结果**: 
  - 系统正确处理并发请求
  - 两个API Key都成功创建
  - 无数据冲突

## 4. 测试数据设计

### 4.1 有效API Key名称
```json
{
  "valid_names": [
    "test_api_key",
    "production_key",
    "dev_key_001",
    "KEY_WITH_UPPERCASE",
    "key-with-dash",
    "key.with.dot"
  ]
}
```

### 4.2 无效API Key名称
```json
{
  "invalid_names": [
    {"name": "", "expected_error": "名称不能为空"},
    {"name": "key with spaces", "expected_error": "不支持空格"},
    {"name": "key@#$%", "expected_error": "不支持特殊字符"},
    {"name": "a".repeat(101), "expected_error": "名称太长"}
  ]
}
```

### 4.3 测试场景数据
```json
{
  "test_scenarios": [
    {
      "scenario": "基础创建和删除",
      "steps": [
        {"action": "create", "name": "test_key_001"},
        {"action": "verify_exists", "name": "test_key_001"},
        {"action": "delete", "name": "test_key_001"},
        {"action": "verify_not_exists", "name": "test_key_001"}
      ]
    },
    {
      "scenario": "批量创建",
      "steps": [
        {"action": "create", "name": "key_001"},
        {"action": "create", "name": "key_002"},
        {"action": "create", "name": "key_003"},
        {"action": "verify_count", "expected": 3}
      ]
    }
  ]
}
```

## 5. 自动化实现建议

### 5.1 页面类实现
创建新文件：`pages/aevatar/api_keys_page.py`

```python
"""
API Keys页面对象
负责API密钥管理功能
"""
from pages.base_page import BasePage
from playwright.sync_api import expect
import allure

class APIKeysPage(BasePage):
    """API Keys页面"""
    
    # 实现上述定位器和方法
    # ...
```

### 5.2 测试类实现
创建新文件：`tests/aevatar/test_api_keys.py`

```python
import pytest
import allure
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.api_keys_page import APIKeysPage

@allure.feature("Dashboard功能")
@allure.story("API Keys管理")
class TestAPIKeys:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """自动登录前置条件"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        
        # 导航到API Keys页面
        page.click("text=API Keys")
        self.apikeys_page = APIKeysPage(page)
        self.apikeys_page.wait_for_page_load()
    
    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.title("TC-APIKEYS-P0-001: API Keys页面加载")
    def test_apikeys_page_loads(self, page):
        """测试API Keys页面正常加载"""
        assert "/dashboard/apikeys" in page.url
        assert self.apikeys_page.is_loaded()
    
    @pytest.mark.P0
    @allure.title("TC-APIKEYS-P0-003: 创建API Key")
    def test_create_api_key(self):
        """测试创建API Key功能"""
        key_name = "test_key_automation"
        self.apikeys_page.create_api_key(key_name)
        self.apikeys_page.verify_api_key_exists(key_name)
        
        # 清理：删除测试数据
        self.apikeys_page.delete_api_key(key_name)
```

### 5.3 配置建议
更新配置文件：`test-data/aevatar/aevatar_test_data.yaml`

```yaml
# API Keys页面配置
api_keys:
  apikeys_url: "http://localhost:5173/dashboard/apikeys"
  default_timeout: 10000
  
# API Key测试数据
api_key_test_data:
  valid_names:
    - "test_api_key_001"
    - "production_key"
    - "dev_key"
  invalid_names:
    - ""
    - "key@#$%"
    - "very_long_name_that_exceeds_limit..."
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
- API Key生成成功率 100%
- 安全验证无漏洞

### 6.3 风险评估
- **高风险**: API Key泄露风险，需确保安全显示
- **中风险**: 并发创建可能导致冲突
- **低风险**: UI元素定位器可能随版本更新

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

