# aevatar.ai Configuration 页面测试计划

## 1. 页面概述

### 1.1 基本信息
- **页面URL**: http://localhost:5173/dashboard/configuration
- **页面标题**: aevatar station frontend
- **页面用途**: 项目配置管理中心
- **前置条件**: 用户已登录（测试账户：haylee@test.com）

### 1.2 功能描述
Configuration页面用于管理项目的系统配置，包括：
- **服务管理**: 重启项目服务
- **DLL管理**: 上传、管理DLL文件
- **CORS管理**: 配置跨域访问白名单

## 2. 页面元素映射

### 2.1 核心元素定位表

| 元素类型 | 元素名称 | 定位方式 | 定位器 |
|---------|---------|---------|--------|
| 标题 | Configuration标题 | Text | `text=Configuration` |
| 按钮 | Restart services按钮 | Button | `button:has-text('Restart services')` |
| 标题 | DLL部分标题 | Text | `text=DLL` |
| 按钮 | Upload按钮(DLL) | Button | `button:has-text('Upload')` |
| 表格 | DLL文件表格 | Role | `role=table >> nth=0` |
| 表头 | DLL File列 | Cell | `cell:has-text('DLL File')` |
| 表头 | Created列 | Cell | `cell:has-text('Created')` |
| 表头 | Created By列 | Cell | `cell:has-text('Created By')` |
| 表头 | Updated列 | Cell | `cell:has-text('Updated')` |
| 表头 | Updated By列 | Cell | `cell:has-text('Updated By')` |
| 表头 | Status列 | Cell | `cell:has-text('Status')` |
| 标题 | CORS部分标题 | Text | `text=CORS` |
| 按钮 | Add按钮(CORS) | Button | `button:has-text('Add')` |
| 表格 | CORS域名表格 | Role | `role=table >> nth=1` |
| 表头 | Domain列 | Cell | `cell:has-text('Domain')` |
| 文本 | CORS空状态 | Generic | `generic:has-text('No Cross URL added yet')` |
| 导航 | Configuration侧边栏 | Generic | `generic:has-text('Configuration')` |

### 2.2 页面对象设计

```python
class ConfigurationPage(BasePage):
    """Configuration页面对象"""
    
    # 页面URL
    CONFIGURATION_URL = "http://localhost:5173/dashboard/configuration"
    
    # 页面标题和服务管理
    PAGE_TITLE = "text=Configuration"
    RESTART_SERVICES_BUTTON = "button:has-text('Restart services')"
    
    # DLL部分
    DLL_SECTION_TITLE = "text=DLL"
    DLL_UPLOAD_BUTTON = "button:has-text('Upload')"
    DLL_TABLE = "role=table >> nth=0"
    DLL_FILE_CELL = "cell:has-text('DLL File')"
    DLL_STATUS_CELL = "cell:has-text('Status')"
    
    # DLL行元素（动态）
    DLL_ROW = "tbody >> tr"
    DLL_FILE_NAME = "td:nth-child(1)"
    DLL_CREATED = "td:nth-child(2)"
    DLL_CREATED_BY = "td:nth-child(3)"
    DLL_UPDATED = "td:nth-child(4)"
    DLL_UPDATED_BY = "td:nth-child(5)"
    DLL_STATUS = "td:nth-child(6)"
    DLL_ACTION_MENU = "combobox[cursor=pointer]"
    
    # CORS部分
    CORS_SECTION_TITLE = "text=CORS"
    CORS_ADD_BUTTON = "button:has-text('Add')"
    CORS_TABLE = "role=table >> nth=1"
    CORS_DOMAIN_CELL = "cell:has-text('Domain')"
    CORS_EMPTY_STATE = "generic:has-text('No Cross URL added yet')"
    
    # CORS行元素（动态）
    CORS_ROW = "tbody >> tr"
    CORS_DOMAIN = "td:nth-child(1)"
    CORS_CREATED = "td:nth-child(2)"
    CORS_CREATED_BY = "td:nth-child(3)"
    CORS_ACTION_MENU = "combobox[cursor=pointer] >> nth=1"
    
    # 对话框元素
    UPLOAD_DIALOG = "role=dialog"
    FILE_INPUT = "input[type='file']"
    DIALOG_UPLOAD_BUTTON = "button:has-text('Upload')"
    DIALOG_CANCEL_BUTTON = "button:has-text('Cancel')"
    
    ADD_CORS_DIALOG = "role=dialog"
    DOMAIN_INPUT = "input[placeholder*='domain' i]"
    DIALOG_ADD_BUTTON = "button:has-text('Add')"
    
    def navigate(self):
        """导航到Configuration页面"""
        self.page.goto(self.CONFIGURATION_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查Configuration页面是否已加载"""
        try:
            self.page.wait_for_selector(self.PAGE_TITLE, timeout=5000)
            return True
        except:
            return False
    
    @allure.step("点击Restart services按钮")
    def click_restart_services(self):
        """重启项目服务"""
        self.page.click(self.RESTART_SERVICES_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("上传DLL文件: {file_path}")
    def upload_dll_file(self, file_path: str):
        """上传DLL文件"""
        # 点击Upload按钮
        self.page.click(self.DLL_UPLOAD_BUTTON)
        self.page.wait_for_timeout(1000)
        
        # 选择文件
        self.page.set_input_files(self.FILE_INPUT, file_path)
        
        # 确认上传
        self.page.click(self.DIALOG_UPLOAD_BUTTON)
        self.page.wait_for_timeout(3000)  # 等待上传完成
    
    @allure.step("获取DLL文件列表")
    def get_dll_list(self):
        """获取DLL文件列表"""
        rows = self.page.query_selector_all(f"{self.DLL_TABLE} >> tbody >> tr")
        dll_files = []
        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 6:
                dll_files.append({
                    "file_name": cells[0].text_content().strip(),
                    "created": cells[1].text_content().strip(),
                    "created_by": cells[2].text_content().strip(),
                    "updated": cells[3].text_content().strip(),
                    "updated_by": cells[4].text_content().strip(),
                    "status": cells[5].text_content().strip()
                })
        return dll_files
    
    @allure.step("添加CORS域名: {domain}")
    def add_cors_domain(self, domain: str):
        """添加CORS域名"""
        # 点击Add按钮
        self.page.click(self.CORS_ADD_BUTTON)
        self.page.wait_for_timeout(1000)
        
        # 输入域名
        self.page.fill(self.DOMAIN_INPUT, domain)
        
        # 确认添加
        self.page.click(self.DIALOG_ADD_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("获取CORS域名列表")
    def get_cors_list(self):
        """获取CORS域名列表"""
        # 检查是否为空状态
        if self.page.is_visible(self.CORS_EMPTY_STATE):
            return []
        
        rows = self.page.query_selector_all(f"{self.CORS_TABLE} >> tbody >> tr")
        cors_domains = []
        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 3:
                cors_domains.append({
                    "domain": cells[0].text_content().strip(),
                    "created": cells[1].text_content().strip(),
                    "created_by": cells[2].text_content().strip()
                })
        return cors_domains
    
    @allure.step("删除CORS域名: {domain}")
    def delete_cors_domain(self, domain: str):
        """删除指定CORS域名"""
        # 找到包含该域名的行
        row = self.page.locator(f"tr:has-text('{domain}')")
        # 点击操作菜单
        row.locator("combobox[cursor=pointer]").click()
        self.page.wait_for_timeout(500)
        # 点击删除选项
        self.page.click("text=Delete")
        self.page.wait_for_timeout(2000)
```

## 3. 测试用例设计

### 3.1 P0级测试用例（核心功能）

#### TC-CONFIG-P0-001: Configuration页面加载
- **优先级**: P0
- **前置条件**: 用户已登录
- **测试步骤**:
  1. 通过侧边栏点击"Configuration"菜单
  2. 验证页面跳转
  3. 检查页面元素加载
- **预期结果**: 
  - 成功跳转到 /dashboard/configuration 页面
  - 页面标题显示"Configuration"
  - 三大部分都显示：服务管理、DLL、CORS

#### TC-CONFIG-P0-002: 重启服务功能
- **优先级**: P0
- **前置条件**: 用户已登录并在Configuration页面
- **测试步骤**:
  1. 点击"Restart services"按钮
  2. 等待操作响应
  3. 验证操作结果
- **预期结果**: 
  - 显示确认对话框（可选）
  - 显示"服务重启中"或loading状态
  - 重启完成后显示成功提示
  - 服务正常运行

#### TC-CONFIG-P0-003: DLL列表加载
- **优先级**: P0
- **前置条件**: 用户已登录并在Configuration页面
- **测试步骤**:
  1. 查看DLL部分
  2. 验证表格显示
  3. 检查列标题
- **预期结果**: 
  - DLL表格正常显示
  - 表头包含：DLL File, Created, Created By, Updated, Updated By, Status
  - 如有DLL文件，显示文件列表

#### TC-CONFIG-P0-004: CORS空状态显示
- **优先级**: P0
- **前置条件**: 
  - 用户已登录
  - 项目中没有配置CORS域名
- **测试步骤**:
  1. 查看CORS部分
  2. 验证空状态提示
- **预期结果**: 
  - 显示"No Cross URL added yet"提示
  - Add按钮可用

#### TC-CONFIG-P0-005: 添加CORS域名
- **优先级**: P0
- **前置条件**: 用户已登录并在Configuration页面
- **测试步骤**:
  1. 点击CORS部分的"Add"按钮
  2. 输入域名 "https://example.com"
  3. 点击"Add"确认
  4. 验证添加结果
- **预期结果**: 
  - 弹出添加对话框
  - 域名成功添加到列表
  - 显示添加成功提示

### 3.2 P1级测试用例（重要功能）

#### TC-CONFIG-P1-001: 上传DLL文件
- **优先级**: P1
- **前置条件**: 
  - 用户已登录
  - 准备有效的DLL文件
- **测试步骤**:
  1. 点击DLL部分的"Upload"按钮
  2. 选择DLL文件
  3. 确认上传
  4. 等待上传完成
- **预期结果**: 
  - 弹出文件选择对话框
  - 显示上传进度
  - 上传成功后，文件出现在DLL列表
  - Status显示为"Active"或"Ready"

#### TC-CONFIG-P1-002: 查看DLL文件状态
- **优先级**: P1
- **前置条件**: DLL列表中存在文件
- **测试步骤**:
  1. 查看DLL列表的Status列
  2. 验证状态类型
- **预期结果**: 
  - Status显示：Active, Inactive, Error等状态
  - 状态与文件实际状态一致

#### TC-CONFIG-P1-003: 删除DLL文件
- **优先级**: P1
- **前置条件**: DLL列表中至少存在一个文件
- **测试步骤**:
  1. 点击DLL文件的操作菜单
  2. 选择"Delete"
  3. 确认删除
- **预期结果**: 
  - 显示删除确认对话框
  - 删除成功后文件从列表移除
  - 显示删除成功提示

#### TC-CONFIG-P1-004: 更新DLL文件
- **优先级**: P1
- **前置条件**: DLL列表中至少存在一个文件
- **测试步骤**:
  1. 点击DLL文件的操作菜单
  2. 选择"Update"或"Replace"
  3. 选择新的DLL文件
  4. 确认更新
- **预期结果**: 
  - 弹出文件选择对话框
  - 文件成功更新
  - Updated和Updated By字段更新

#### TC-CONFIG-P1-005: 添加多个CORS域名
- **优先级**: P1
- **前置条件**: 用户在Configuration页面
- **测试步骤**:
  1. 添加域名 "https://example1.com"
  2. 添加域名 "https://example2.com"
  3. 添加域名 "https://example3.com"
  4. 验证列表
- **预期结果**: 
  - 所有域名成功添加
  - 列表显示所有添加的域名
  - 按添加时间排序

#### TC-CONFIG-P1-006: 删除CORS域名
- **优先级**: P1
- **前置条件**: CORS列表中至少存在一个域名
- **测试步骤**:
  1. 点击CORS域名的操作菜单
  2. 选择"Delete"
  3. 确认删除
- **预期结果**: 
  - 显示删除确认对话框
  - 域名从列表中移除
  - 显示删除成功提示

#### TC-CONFIG-P1-007: 编辑CORS域名
- **优先级**: P1
- **前置条件**: CORS列表中至少存在一个域名
- **测试步骤**:
  1. 点击CORS域名的操作菜单
  2. 选择"Edit"
  3. 修改域名
  4. 保存修改
- **预期结果**: 
  - 弹出编辑对话框
  - 域名成功更新
  - 列表显示新域名

#### TC-CONFIG-P1-008: 取消添加CORS域名
- **优先级**: P1
- **前置条件**: 用户在Configuration页面
- **测试步骤**:
  1. 点击Add按钮
  2. 输入域名
  3. 点击Cancel
- **预期结果**: 
  - 对话框关闭
  - 域名未添加到列表

#### TC-CONFIG-P1-009: 重启服务确认机制
- **优先级**: P1
- **前置条件**: 用户在Configuration页面
- **测试步骤**:
  1. 点击"Restart services"按钮
  2. 在确认对话框点击"Cancel"
- **预期结果**: 
  - 对话框关闭
  - 服务未重启

### 3.3 P2级测试用例（验证与边界）

#### TC-CONFIG-P2-001: 上传无效DLL文件
- **优先级**: P2
- **前置条件**: 准备非DLL格式文件
- **测试步骤**:
  1. 尝试上传txt、jpg等非DLL文件
  2. 观察系统响应
- **预期结果**: 
  - 显示"仅支持.dll文件"错误提示
  - 上传失败

#### TC-CONFIG-P2-002: 上传超大DLL文件
- **优先级**: P2
- **前置条件**: 准备超过限制大小的DLL文件
- **测试步骤**:
  1. 尝试上传超大DLL文件（如100MB+）
  2. 观察上传过程
- **预期结果**: 
  - 显示文件大小限制提示
  - 或上传进度显示正常，超时后提示失败

#### TC-CONFIG-P2-003: 上传同名DLL文件
- **优先级**: P2
- **前置条件**: 已存在名为"test.dll"的文件
- **测试步骤**:
  1. 尝试上传同名文件"test.dll"
  2. 观察系统处理
- **预期结果**: 
  - 显示"文件名已存在"提示
  - 或询问是否覆盖/重命名

#### TC-CONFIG-P2-004: CORS域名格式验证
- **优先级**: P2
- **前置条件**: 用户在Configuration页面
- **测试步骤**:
  1. 尝试添加无效域名格式
  2. 如："invalid-url", "ftp://example.com", "http://"
- **预期结果**: 
  - 显示"域名格式不正确"提示
  - 只接受http://或https://开头的有效URL

#### TC-CONFIG-P2-005: CORS重复域名验证
- **优先级**: P2
- **前置条件**: 已存在域名 "https://example.com"
- **测试步骤**:
  1. 尝试再次添加 "https://example.com"
  2. 观察系统响应
- **预期结果**: 
  - 显示"域名已存在"错误提示
  - 不允许重复添加

#### TC-CONFIG-P2-006: CORS通配符支持
- **优先级**: P2
- **前置条件**: 用户在Configuration页面
- **测试步骤**:
  1. 尝试添加通配符域名
  2. 如："*", "*.example.com", "https://*.test.com"
- **预期结果**: 
  - 系统支持通配符配置
  - 或显示"不支持通配符"提示

#### TC-CONFIG-P2-007: 重启服务时的并发访问
- **优先级**: P2
- **前置条件**: 服务正在重启中
- **测试步骤**:
  1. 点击"Restart services"
  2. 服务重启期间，尝试访问其他页面
  3. 尝试执行其他操作
- **预期结果**: 
  - 显示"服务重启中"提示
  - 相关功能临时不可用
  - 重启完成后自动恢复

#### TC-CONFIG-P2-008: DLL文件加载失败处理
- **优先级**: P2
- **前置条件**: 上传了有问题的DLL文件
- **测试步骤**:
  1. 上传包含错误的DLL文件
  2. 观察Status显示
  3. 查看错误日志
- **预期结果**: 
  - Status显示为"Error"或"Failed"
  - 提供错误详情或日志查看入口

#### TC-CONFIG-P2-009: 权限验证 - 普通成员
- **优先级**: P2
- **前置条件**: 使用普通成员账户登录
- **测试步骤**:
  1. 访问Configuration页面
  2. 尝试重启服务
  3. 尝试上传DLL
  4. 尝试添加CORS域名
- **预期结果**: 
  - 普通成员可能无权限访问Configuration
  - 或只有只读权限
  - 管理操作被禁用

#### TC-CONFIG-P2-010: 大量CORS域名加载
- **优先级**: P2
- **前置条件**: 配置了50+个CORS域名
- **测试步骤**:
  1. 访问Configuration页面
  2. 查看CORS列表加载时间
  3. 验证分页功能
- **预期结果**: 
  - 页面在3秒内加载完成
  - 支持分页或虚拟滚动

## 4. 测试数据设计

### 4.1 有效CORS域名
```json
{
  "valid_cors_domains": [
    "https://example.com",
    "https://api.test.com",
    "http://localhost:3000",
    "https://sub.domain.example.com",
    "https://test-environment.com"
  ]
}
```

### 4.2 无效CORS域名
```json
{
  "invalid_cors_domains": [
    {"domain": "invalid-url", "expected_error": "URL格式不正确"},
    {"domain": "ftp://example.com", "expected_error": "仅支持http/https"},
    {"domain": "http://", "expected_error": "URL不完整"},
    {"domain": "", "expected_error": "域名不能为空"}
  ]
}
```

### 4.3 DLL测试文件
```json
{
  "valid_dll_files": [
    {"file": "test_valid.dll", "size": "1MB"},
    {"file": "large_valid.dll", "size": "10MB"}
  ],
  "invalid_dll_files": [
    {"file": "invalid.txt", "expected_error": "文件格式不支持"},
    {"file": "corrupted.dll", "expected_error": "文件损坏"},
    {"file": "too_large.dll", "size": "100MB", "expected_error": "文件过大"}
  ]
}
```

## 5. 自动化实现建议

### 5.1 页面类实现
创建新文件：`pages/aevatar/configuration_page.py`

```python
"""
Configuration页面对象
负责项目配置管理功能：服务重启、DLL管理、CORS配置
"""
from pages.base_page import BasePage
from playwright.sync_api import expect
import allure

class ConfigurationPage(BasePage):
    """Configuration页面"""
    
    # 实现上述定位器和方法
    # ...
```

### 5.2 测试类实现
创建新文件：`tests/aevatar/test_configuration.py`

```python
import pytest
import allure
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.configuration_page import ConfigurationPage

@allure.feature("Dashboard功能")
@allure.story("Configuration配置管理")
class TestConfiguration:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """自动登录前置条件"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        
        # 导航到Configuration页面
        page.click("text=Configuration")
        self.config_page = ConfigurationPage(page)
        self.config_page.wait_for_page_load()
    
    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.title("TC-CONFIG-P0-001: Configuration页面加载")
    def test_configuration_page_loads(self, page):
        """测试Configuration页面正常加载"""
        assert "/dashboard/configuration" in page.url
        assert self.config_page.is_loaded()
    
    @pytest.mark.P0
    @allure.title("TC-CONFIG-P0-005: 添加CORS域名")
    def test_add_cors_domain(self):
        """测试添加CORS域名功能"""
        domain = "https://test-automation.com"
        self.config_page.add_cors_domain(domain)
        cors_list = self.config_page.get_cors_list()
        domains = [cors["domain"] for cors in cors_list]
        assert domain in domains
        
        # 清理：删除测试数据
        self.config_page.delete_cors_domain(domain)
```

### 5.3 配置建议
更新配置文件：`test-data/aevatar/aevatar_test_data.yaml`

```yaml
# Configuration页面配置
configuration:
  configuration_url: "http://localhost:5173/dashboard/configuration"
  default_timeout: 10000
  dll_upload_timeout: 30000
  
# CORS测试数据
cors_test_data:
  valid_domains:
    - "https://example.com"
    - "https://api.test.com"
    - "http://localhost:3000"
  invalid_domains:
    - "invalid-url"
    - "ftp://example.com"
    - ""
```

## 6. 执行计划

### 6.1 测试阶段
- **P0测试**: 每次部署前执行，预计耗时 10分钟
- **P1测试**: 每日回归测试，预计耗时 20分钟
- **P2测试**: 每周完整测试，预计耗时 30分钟

### 6.2 验收标准
- P0测试用例通过率 100%
- P1测试用例通过率 ≥ 95%
- P2测试用例通过率 ≥ 90%
- 服务重启成功率 100%
- CORS配置准确率 100%

### 6.3 风险评估
- **高风险**: 服务重启可能影响在线用户
- **中风险**: DLL文件损坏可能导致系统异常
- **低风险**: CORS配置错误影响跨域访问

## 7. 注意事项

### 7.1 服务重启测试
- 在测试环境执行服务重启测试
- 避免在生产环境频繁重启
- 记录重启时间和影响范围

### 7.2 DLL文件管理
- 备份原有DLL文件
- 上传测试DLL前验证文件完整性
- 测试后恢复原配置

### 7.3 CORS安全性
- 避免配置过于宽松的CORS规则
- 验证通配符配置的安全性
- 定期审查CORS白名单

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

