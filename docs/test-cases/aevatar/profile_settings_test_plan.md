# aevatar.ai Profile/Settings 页面测试计划

## 1. 页面概述

### 1.1 基本信息
- **页面URL**: http://localhost:5173/profile
- **页面标题**: aevatar station frontend
- **页面用途**: 用户个人设置、组织管理、项目管理
- **前置条件**: 用户已登录（测试账户：haylee@test.com）

### 1.2 功能描述
Profile/Settings页面是用户的设置中心，提供三大功能模块：
1. **Profile设置**: 个人信息管理（姓名、邮箱、密码重置）
2. **Organisations管理**: 组织级别的设置（组织信息、项目、成员、角色）
3. **Projects管理**: 项目级别的设置（项目信息、成员、角色）

## 2. 页面结构映射

### 2.1 侧边栏导航结构

```
Profile
├── General (个人信息)
└── Notifications (通知设置)

Organisations
├── General (组织信息)
├── Project (项目管理)
├── Member (成员管理)
└── Role (角色管理)

Projects
├── General (项目信息)
├── Member (成员管理)
└── Role (角色管理)
```

### 2.2 核心元素定位表

| 元素类型 | 元素名称 | 定位方式 | 定位器 |
|---------|---------|---------|--------|
| 导航 | Profile标题 | Text | `text=Profile` |
| 菜单 | Profile-General | Generic | `generic:has-text('General')` (Profile下) |
| 菜单 | Profile-Notifications | Generic | `generic:has-text('Notifications')` |
| 导航 | Organisations标题 | Text | `text=Organisations` |
| 菜单 | Org-General | Generic | `generic:has-text('General')` (Org下) |
| 菜单 | Org-Project | Generic | `generic:has-text('Project')` |
| 菜单 | Org-Member | Generic | `generic:has-text('Member')` |
| 菜单 | Org-Role | Generic | `generic:has-text('Role')` |
| 导航 | Projects标题 | Text | `text=Projects` |
| 菜单 | Project-General | Generic | `generic:has-text('General')` (Projects下) |
| 菜单 | Project-Member | Generic | `generic:has-text('Member')` |
| 菜单 | Project-Role | Generic | `generic:has-text('Role')` |
| 输入 | Name输入框 | Textbox | `textbox[value='Haylee']` |
| 按钮 | Save按钮 | Button | `button:has-text('Save')` |
| 输入 | Email输入框 | Textbox | `textbox[disabled]` |
| 按钮 | Reset Password按钮 | Button | `button:has-text('Reset Password')` |

### 2.3 页面对象设计

```python
class ProfileSettingsPage(BasePage):
    """Profile/Settings页面对象"""
    
    # 页面URL
    PROFILE_URL = "http://localhost:5173/profile"
    
    # 侧边栏导航 - Profile
    PROFILE_SECTION = "text=Profile"
    PROFILE_GENERAL_MENU = "generic:has-text('General')"
    PROFILE_NOTIFICATIONS_MENU = "generic:has-text('Notifications')"
    
    # 侧边栏导航 - Organisations
    ORGANISATIONS_SECTION = "text=Organisations"
    ORG_GENERAL_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='General']"
    ORG_PROJECT_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Project']"
    ORG_MEMBER_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Member']"
    ORG_ROLE_MENU = "xpath=//div[text()='Organisations']/following-sibling::div//div[text()='Role']"
    
    # 侧边栏导航 - Projects
    PROJECTS_SECTION = "text=Projects"
    PROJECT_GENERAL_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='General']"
    PROJECT_MEMBER_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='Member']"
    PROJECT_ROLE_MENU = "xpath=//div[text()='Projects']/following-sibling::div//div[text()='Role']"
    
    # Profile General页面元素
    NAME_INPUT = "textbox >> nth=0"  # 第一个textbox
    EMAIL_INPUT = "textbox[disabled]"
    SAVE_BUTTON = "button:has-text('Save')"
    RESET_PASSWORD_BUTTON = "button:has-text('Reset Password')"
    RESET_PASSWORD_DESCRIPTION = "text=A password reset link will be sent"
    
    def navigate(self):
        """导航到Profile页面"""
        self.page.goto(self.PROFILE_URL)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """检查Profile页面是否已加载"""
        try:
            self.page.wait_for_selector(self.PROFILE_SECTION, timeout=5000)
            return True
        except:
            return False
    
    @allure.step("修改用户名称为: {new_name}")
    def update_name(self, new_name: str):
        """更新用户名称"""
        self.page.fill(self.NAME_INPUT, "")
        self.page.fill(self.NAME_INPUT, new_name)
        self.page.click(self.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("获取当前用户名称")
    def get_current_name(self) -> str:
        """获取当前用户名称"""
        return self.page.input_value(self.NAME_INPUT)
    
    @allure.step("获取当前邮箱地址")
    def get_current_email(self) -> str:
        """获取当前邮箱地址"""
        return self.page.input_value(self.EMAIL_INPUT)
    
    @allure.step("点击Reset Password按钮")
    def click_reset_password(self):
        """点击重置密码按钮"""
        self.page.click(self.RESET_PASSWORD_BUTTON)
        self.page.wait_for_timeout(2000)
    
    @allure.step("导航到 {section} > {menu}")
    def navigate_to_menu(self, section: str, menu: str):
        """导航到指定菜单"""
        section_map = {
            "Profile": {
                "General": self.PROFILE_GENERAL_MENU,
                "Notifications": self.PROFILE_NOTIFICATIONS_MENU
            },
            "Organisations": {
                "General": self.ORG_GENERAL_MENU,
                "Project": self.ORG_PROJECT_MENU,
                "Member": self.ORG_MEMBER_MENU,
                "Role": self.ORG_ROLE_MENU
            },
            "Projects": {
                "General": self.PROJECT_GENERAL_MENU,
                "Member": self.PROJECT_MEMBER_MENU,
                "Role": self.PROJECT_ROLE_MENU
            }
        }
        
        menu_selector = section_map.get(section, {}).get(menu)
        if menu_selector:
            self.page.click(menu_selector)
            self.page.wait_for_timeout(1000)
```

## 3. 测试用例设计

### 3.1 P0级测试用例（核心功能）

#### TC-PROFILE-P0-001: Profile页面加载
- **优先级**: P0
- **前置条件**: 用户已登录
- **测试步骤**:
  1. 点击顶部导航的"Settings"按钮
  2. 验证跳转到Profile页面
  3. 检查页面元素加载
- **预期结果**: 
  - 成功跳转到 /profile 页面
  - 侧边栏显示三大部分：Profile, Organisations, Projects
  - 默认显示Profile > General内容

#### TC-PROFILE-P0-002: 查看当前用户信息
- **优先级**: P0
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 查看Name输入框内容
  2. 查看Email输入框内容
  3. 验证Email输入框为disabled状态
- **预期结果**: 
  - Name显示用户当前名称（如"Haylee"）
  - Email显示用户邮箱地址（haylee@test.com）
  - Email输入框不可编辑

#### TC-PROFILE-P0-003: 修改用户名称
- **优先级**: P0
- **前置条件**: 用户已在Profile > General页面
- **测试步骤**:
  1. 清空Name输入框
  2. 输入新名称 "Test User"
  3. 点击"Save"按钮
  4. 刷新页面或重新进入
  5. 验证名称是否保存成功
- **预期结果**: 
  - 显示保存成功提示
  - 名称成功更新为 "Test User"
  - 刷新后名称保持不变

#### TC-PROFILE-P0-004: 重置密码功能
- **优先级**: P0
- **前置条件**: 用户已在Profile > General页面
- **测试步骤**:
  1. 阅读"Reset Password"说明文字
  2. 点击"Reset Password"按钮
  3. 等待响应
- **预期结果**: 
  - 显示说明："A password reset link will be sent to your email..."
  - 点击后显示成功提示
  - 用户邮箱收到密码重置邮件

#### TC-PROFILE-P0-005: 侧边栏导航功能
- **优先级**: P0
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击"Notifications"菜单
  2. 验证内容区域变化
  3. 点击"Organisations > General"
  4. 验证内容区域变化
  5. 点击"Projects > General"
  6. 验证内容区域变化
- **预期结果**: 
  - 每次点击菜单，内容区域切换到对应页面
  - 当前菜单项高亮显示
  - 页面URL可能更新（如果有子路由）

### 3.2 P1级测试用例（重要功能）

#### TC-PROFILE-P1-001: 空名称保存验证
- **优先级**: P1
- **前置条件**: 用户已在Profile > General页面
- **测试步骤**:
  1. 清空Name输入框
  2. 点击"Save"按钮
- **预期结果**: 
  - 显示错误提示："名称不能为空"
  - 或Save按钮变为disabled状态

#### TC-PROFILE-P1-002: 超长名称保存
- **优先级**: P1
- **前置条件**: 用户已在Profile > General页面
- **测试步骤**:
  1. 输入超长名称（100+字符）
  2. 点击"Save"按钮
- **预期结果**: 
  - 显示长度限制提示
  - 或成功保存并截断显示

#### TC-PROFILE-P1-003: 特殊字符名称保存
- **优先级**: P1
- **前置条件**: 用户已在Profile > General页面
- **测试步骤**:
  1. 输入包含特殊字符的名称（如"User@123", "测试用户"）
  2. 点击"Save"按钮
- **预期结果**: 
  - 成功保存特殊字符名称
  - 或显示"仅支持字母和数字"提示

#### TC-PROFILE-P1-004: Notifications页面功能
- **优先级**: P1
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击"Notifications"菜单
  2. 查看通知设置选项
  3. 修改通知设置
  4. 保存设置
- **预期结果**: 
  - 显示通知设置界面
  - 包含邮件通知、推送通知等选项
  - 设置成功保存

#### TC-PROFILE-P1-005: Organisations - General页面
- **优先级**: P1
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击"Organisations > General"
  2. 查看组织信息
  3. 修改组织设置（如组织名称）
- **预期结果**: 
  - 显示当前组织信息
  - 有权限的用户可以修改组织设置

#### TC-PROFILE-P1-006: Organisations - Project管理
- **优先级**: P1
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击"Organisations > Project"
  2. 查看项目列表
  3. 尝试创建/编辑/删除项目
- **预期结果**: 
  - 显示组织下的所有项目
  - 有权限的用户可以管理项目

#### TC-PROFILE-P1-007: Organisations - Member管理
- **优先级**: P1
- **前置条件**: 用户已在Profile页面，且是组织管理员
- **测试步骤**:
  1. 点击"Organisations > Member"
  2. 查看成员列表
  3. 尝试邀请新成员
  4. 尝试移除成员
- **预期结果**: 
  - 显示组织成员列表
  - 管理员可以邀请/移除成员
  - 普通成员只能查看

#### TC-PROFILE-P1-008: Organisations - Role管理
- **优先级**: P1
- **前置条件**: 用户已在Profile页面，且是组织管理员
- **测试步骤**:
  1. 点击"Organisations > Role"
  2. 查看角色列表
  3. 尝试创建自定义角色
  4. 尝试分配角色权限
- **预期结果**: 
  - 显示角色列表（Admin, Member等）
  - 管理员可以创建自定义角色
  - 可以配置角色权限

#### TC-PROFILE-P1-009: Projects - General页面
- **优先级**: P1
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击"Projects > General"
  2. 查看当前项目信息
  3. 修改项目设置
- **预期结果**: 
  - 显示当前选中项目的信息
  - 有权限的用户可以修改项目设置

#### TC-PROFILE-P1-010: Projects - Member管理
- **优先级**: P1
- **前置条件**: 用户已在Profile页面，且是项目管理员
- **测试步骤**:
  1. 点击"Projects > Member"
  2. 查看项目成员列表
  3. 添加/移除项目成员
- **预期结果**: 
  - 显示项目成员列表
  - 管理员可以管理项目成员

#### TC-PROFILE-P1-011: Projects - Role管理
- **优先级**: P1
- **前置条件**: 用户已在Profile页面，且是项目管理员
- **测试步骤**:
  1. 点击"Projects > Role"
  2. 查看项目角色配置
  3. 修改成员角色
- **预期结果**: 
  - 显示项目角色配置
  - 可以为成员分配不同角色

#### TC-PROFILE-P1-012: 返回Dashboard功能
- **优先级**: P1
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 点击顶部导航的"Dashboard"按钮
  2. 验证页面跳转
- **预期结果**: 
  - 成功返回到Dashboard/Workflows页面

### 3.3 P2级测试用例（权限与边界）

#### TC-PROFILE-P2-001: 权限验证 - 普通成员
- **优先级**: P2
- **前置条件**: 使用普通成员账户登录
- **测试步骤**:
  1. 访问Profile页面
  2. 尝试访问Organisations管理功能
  3. 尝试修改组织设置
- **预期结果**: 
  - 普通成员只能查看，不能修改
  - 或管理功能按钮不可见/disabled

#### TC-PROFILE-P2-002: 权限验证 - 组织管理员
- **优先级**: P2
- **前置条件**: 使用组织管理员账户登录
- **测试步骤**:
  1. 访问Profile页面
  2. 访问Organisations所有子菜单
  3. 尝试执行管理操作
- **预期结果**: 
  - 管理员可以访问所有管理功能
  - 所有操作按钮可用

#### TC-PROFILE-P2-003: 跨组织切换
- **优先级**: P2
- **前置条件**: 用户属于多个组织
- **测试步骤**:
  1. 在顶部导航切换组织
  2. 观察Organisations设置变化
  3. 验证Projects列表更新
- **预期结果**: 
  - 切换组织后，显示对应组织的设置
  - Projects列表更新为新组织下的项目

#### TC-PROFILE-P2-004: 修改名称时的并发冲突
- **优先级**: P2
- **前置条件**: 同一用户在两个浏览器同时登录
- **测试步骤**:
  1. 浏览器A修改名称为"User A"
  2. 浏览器B修改名称为"User B"
  3. 观察最终结果
- **预期结果**: 
  - 系统正确处理并发更新
  - 最后一次保存生效

#### TC-PROFILE-P2-005: Reset Password多次点击
- **优先级**: P2
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 连续快速点击"Reset Password"按钮5次
  2. 观察系统响应
- **预期结果**: 
  - 系统防止重复请求
  - 只发送一次重置邮件
  - 或显示"请勿重复操作"提示

#### TC-PROFILE-P2-006: 邮箱显示安全性
- **优先级**: P2
- **前置条件**: 用户已在Profile页面
- **测试步骤**:
  1. 检查Email输入框的disabled属性
  2. 尝试通过浏览器开发工具修改Email
  3. 尝试保存
- **预期结果**: 
  - Email输入框严格禁用
  - 即使前端修改，后端也应拒绝更新

#### TC-PROFILE-P2-007: 成员列表大数据量
- **优先级**: P2
- **前置条件**: 组织中有100+成员
- **测试步骤**:
  1. 访问Organisations > Member
  2. 查看成员列表加载时间
  3. 测试分页/虚拟滚动功能
- **预期结果**: 
  - 页面在3秒内加载完成
  - 支持分页或虚拟滚动
  - 搜索/筛选功能正常

#### TC-PROFILE-P2-008: 角色权限细粒度控制
- **优先级**: P2
- **前置条件**: 已创建自定义角色
- **测试步骤**:
  1. 创建自定义角色"Viewer"
  2. 分配只读权限
  3. 使用Viewer角色账户登录
  4. 验证权限限制
- **预期结果**: 
  - Viewer角色只能查看，不能修改
  - 所有修改操作被正确拦截

## 4. 测试数据设计

### 4.1 用户名称测试数据
```json
{
  "valid_names": [
    {"name": "John Doe", "description": "英文名称"},
    {"name": "张三", "description": "中文名称"},
    {"name": "User123", "description": "包含数字"},
    {"name": "Test-User", "description": "包含连字符"}
  ],
  "invalid_names": [
    {"name": "", "expected_error": "名称不能为空"},
    {"name": "a", "expected_error": "名称太短", "note": "如果有最小长度限制"},
    {"name": "a".repeat(101), "expected_error": "名称太长", "note": "超过最大长度"}
  ],
  "edge_case_names": [
    {"name": "Name with spaces", "description": "包含空格"},
    {"name": "Name@#$%", "description": "特殊字符"},
    {"name": "😀Emoji User", "description": "包含Emoji"}
  ]
}
```

### 4.2 权限测试数据
```json
{
  "user_roles": [
    {
      "role": "admin",
      "email": "admin@test.com",
      "permissions": ["read", "write", "delete", "manage_members"]
    },
    {
      "role": "member",
      "email": "member@test.com",
      "permissions": ["read"]
    },
    {
      "role": "project_admin",
      "email": "project_admin@test.com",
      "permissions": ["read", "write", "manage_project_members"]
    }
  ]
}
```

## 5. 自动化实现建议

### 5.1 页面类实现
创建新文件：`pages/aevatar/profile_settings_page.py`

```python
"""
Profile/Settings页面对象
负责用户个人设置、组织管理、项目管理功能
"""
from pages.base_page import BasePage
from playwright.sync_api import expect
import allure

class ProfileSettingsPage(BasePage):
    """Profile/Settings页面"""
    
    # 实现上述定位器和方法
    # ...
    
    @allure.step("验证名称修改成功")
    def verify_name_updated(self, expected_name: str):
        """验证名称是否更新成功"""
        current_name = self.get_current_name()
        assert current_name == expected_name, \
            f"名称未更新。期望: {expected_name}, 实际: {current_name}"
```

### 5.2 测试类实现
创建新文件：`tests/aevatar/test_profile_settings.py`

```python
import pytest
import allure
from pages.aevatar.localhost_email_login_page import LocalhostEmailLoginPage
from pages.aevatar.profile_settings_page import ProfileSettingsPage

@allure.feature("Profile功能")
@allure.story("个人设置管理")
class TestProfileSettings:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """自动登录前置条件"""
        login_page = LocalhostEmailLoginPage(page)
        login_page.navigate()
        login_page.login_with_email("haylee@test.com", "Wh520520!")
        
        # 导航到Profile页面
        page.click("button:has-text('Settings')")
        self.profile_page = ProfileSettingsPage(page)
        self.profile_page.wait_for_page_load()
    
    @pytest.mark.smoke
    @pytest.mark.P0
    @allure.title("TC-PROFILE-P0-001: Profile页面加载")
    def test_profile_page_loads(self, page):
        """测试Profile页面正常加载"""
        assert "/profile" in page.url
        assert self.profile_page.is_loaded()
    
    @pytest.mark.P0
    @allure.title("TC-PROFILE-P0-003: 修改用户名称")
    def test_update_user_name(self):
        """测试修改用户名称功能"""
        new_name = "Test User Updated"
        self.profile_page.update_name(new_name)
        self.profile_page.verify_name_updated(new_name)
        
        # 恢复原名称
        self.profile_page.update_name("Haylee")
```

### 5.3 配置建议
更新配置文件：`test-data/aevatar/aevatar_test_data.yaml`

```yaml
# Profile页面配置
profile:
  profile_url: "http://localhost:5173/profile"
  default_timeout: 10000
  
# 用户信息测试数据
user_profile_data:
  valid_names:
    - "John Doe"
    - "张三"
    - "User123"
  invalid_names:
    - ""
    - "a"
    - "verylongnamethatexceedsthelimitverylongnamethatexceedsthelimit"
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
- 权限控制无漏洞
- 数据保存成功率 100%

### 6.3 风险评估
- **高风险**: 权限控制逻辑复杂，容易出现漏洞
- **中风险**: 多级菜单导航，定位器可能不稳定
- **低风险**: UI布局调整影响测试

---

**文档版本**: v1.0  
**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护人**: QA Team

