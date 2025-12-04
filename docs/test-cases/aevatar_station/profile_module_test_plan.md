# Profile 模块测试计划

## 模块概览

Profile模块包含两个主要功能页面：
1. **Personal Settings** - 个人信息管理
2. **Change Password** - 密码修改

---

## 文件结构

```
tests/aevatar_station/
├── test_personal_settings.py       # Personal Settings 测试（5个测试用例）
├── test_change_password.py         # Change Password 测试（8个测试用例）
└── pages/
    ├── profile_settings_page.py    # Personal Settings Page Object
    └── change_password_page.py     # Change Password Page Object
```

---

## 1. Personal Settings 测试计划

### 页面信息

**测试页面**: Personal Settings  
**URL**: `https://localhost:3000/admin/profile`  
**测试文件**: `test_personal_settings.py`  
**测试用例数量**: 5个  

### 测试用例列表

| 用例编号 | 用例标题 | 优先级 | 类型 | 描述 |
|---------|---------|-------|------|------|
| TC-FUNC-004 | 查看用户个人信息 | P1 | Functional | 验证页面加载及所有表单元素可见 |
| TC-FUNC-005 | 修改个人信息 | P0 | Functional | 验证用户可以修改个人信息并持久化 |
| TC-FUNC-007 | 必填字段校验 | P1 | Functional | 验证Name/Surname为必填字段 |
| TC-VALID-004 | Email字段格式校验 | P1 | Validation | 验证Email格式验证（有效/无效格式） |
| TC-DATA-001 | 数据一致性验证 | P0 | Data | 验证修改后数据刷新后保持一致 |

### 功能覆盖

#### ✅ 页面加载验证
- Personal Settings Tab可见
- Save按钮可见
- Name/Surname/Email/Phone输入框可见

#### ✅ 个人信息修改
- 修改Name和Surname
- 修改Phone
- 保存并验证
- 刷新后验证持久化

#### ✅ 字段验证
- 必填字段校验（Name, Surname）
- Email格式验证
  - 无效格式：`invalidemail.com`（缺少@）
  - 有效格式：`valid.test@example.com`

#### ✅ 数据持久化
- 保存后立即验证
- 刷新后验证
- 数据一致性检查

### 截图点

每个测试用例包含 **3-4个关键截图**：
1. 初始状态
2. 操作进行中
3. 操作完成后
4. 刷新后验证（如需要）

---

## 2. Change Password 测试计划

### 页面信息

**测试页面**: Change Password  
**URL**: `https://localhost:3000/admin/profile/change-password`  
**测试文件**: `test_change_password.py`  
**测试用例数量**: 8个  

### 测试用例列表

| 用例编号 | 用例标题 | 优先级 | 类型 | 描述 |
|---------|---------|-------|------|------|
| TC-PWD-001 | 访问修改密码页面 | P0 | Functional | 验证页面加载及所有密码字段可见 |
| TC-PWD-002 | 新密码与确认密码不匹配 | P1 | Validation | 验证密码不匹配时显示错误 |
| TC-PWD-003 | 新密码与当前密码相同 | P1 | Validation | 验证新密码不能与旧密码相同 |
| TC-PWD-004 | 当前密码错误 | P1 | Validation | 验证输入错误的当前密码时显示错误 |
| TC-PWD-005 | 空字段验证 | P2 | Validation | 验证所有密码字段为必填项 |
| TC-PWD-006 | 密码复杂度要求 | P2 | Security | 验证密码复杂度（长度、大小写、特殊字符）|
| TC-PWD-007 | 密码字段遮罩显示 | P2 | Security | 验证密码以掩码形式显示 |
| TC-PWD-008 | 密码显示/隐藏切换 | P2 | Functional | 验证密码显示/隐藏功能（如有）|

### 功能覆盖

#### ✅ 页面加载验证
- Current Password输入框可见
- New Password输入框可见
- Confirm Password输入框可见
- Save按钮可见

#### ✅ 密码验证规则
1. **密码匹配验证**
   - 新密码 ≠ 确认密码 → 错误
   - 新密码 = 当前密码 → 错误

2. **当前密码验证**
   - 错误的当前密码 → 错误

3. **必填字段验证**
   - 所有字段为空 → 错误
   - 只填写部分字段 → 错误

4. **密码复杂度验证**
   - 过短（< 6字符） → 错误
   - 纯数字 → 错误
   - 纯字母 → 错误
   - 缺少特殊字符/数字 → 错误

#### ✅ 安全性验证
- 密码字段类型为 `type="password"`
- 输入显示为掩码（••••••）
- 密码不以明文显示

#### ✅ 用户体验
- 密码显示/隐藏切换按钮（如果存在）
- 清晰的错误提示信息

### 测试数据

#### 弱密码测试数据
```json
{
  "weak_passwords": [
    {
      "password": "123",
      "description": "过短（3字符）",
      "expected": "错误：密码太短"
    },
    {
      "password": "12345678",
      "description": "纯数字",
      "expected": "错误：需要字母"
    },
    {
      "password": "abcdefgh",
      "description": "纯小写字母",
      "expected": "错误：需要数字或特殊字符"
    },
    {
      "password": "ABCDEFGH",
      "description": "纯大写字母",
      "expected": "错误：需要数字或特殊字符"
    },
    {
      "password": "Password",
      "description": "缺少数字和特殊字符",
      "expected": "错误：需要数字和特殊字符"
    }
  ]
}
```

### 截图点

每个测试用例包含 **2-6个关键截图**：
1. 初始状态
2. 填写密码后
3. 提交后
4. 错误提示（如有）
5. 多种弱密码测试（TC-PWD-006有6个截图）

---

## 测试执行统计

### Personal Settings

```yaml
测试用例: 5个
  - P0: 2个 (40%)
  - P1: 3个 (60%)

测试类型:
  - Functional: 3个
  - Validation: 1个
  - Data: 1个

预计执行时间: ~5分钟
预计截图数量: ~15张
```

### Change Password

```yaml
测试用例: 8个
  - P0: 1个 (12.5%)
  - P1: 3个 (37.5%)
  - P2: 4个 (50%)

测试类型:
  - Functional: 2个
  - Validation: 4个
  - Security: 2个

预计执行时间: ~8分钟
预计截图数量: ~24张
```

### 总计

```yaml
Profile模块总计:
  - 测试文件: 2个
  - 测试用例: 13个
  - Page Objects: 2个
  - 预计执行时间: ~13分钟
  - 预计截图数量: ~39张
```

---

## 运行测试

### 运行所有Profile模块测试

```bash
# 运行Personal Settings和Change Password所有测试
pytest tests/aevatar_station/test_personal_settings.py \
       tests/aevatar_station/test_change_password.py \
       -v --alluredir=allure-results

# 生成Allure报告
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### 按优先级运行

```bash
# 只运行P0优先级测试
pytest tests/aevatar_station/test_personal_settings.py \
       tests/aevatar_station/test_change_password.py \
       -m P0 -v

# 运行P0和P1优先级测试
pytest tests/aevatar_station/test_personal_settings.py \
       tests/aevatar_station/test_change_password.py \
       -m "P0 or P1" -v
```

### 按功能模块运行

```bash
# 只运行Personal Settings测试
pytest tests/aevatar_station/test_personal_settings.py -v

# 只运行Change Password测试
pytest tests/aevatar_station/test_change_password.py -v
```

### 按测试类型运行

```bash
# 只运行验证类测试
pytest tests/aevatar_station/test_personal_settings.py \
       tests/aevatar_station/test_change_password.py \
       -m validation -v

# 只运行安全性测试
pytest tests/aevatar_station/test_change_password.py -m security -v
```

---

## 测试标记 (Markers)

### 功能模块标记
- `@pytest.mark.profile` - Personal Settings相关
- `@pytest.mark.password` - Change Password相关

### 优先级标记
- `@pytest.mark.P0` - 关键功能（3个）
- `@pytest.mark.P1` - 重要功能（6个）
- `@pytest.mark.P2` - 一般功能（4个）

### 测试类型标记
- `@pytest.mark.functional` - 功能测试（5个）
- `@pytest.mark.validation` - 验证测试（5个）
- `@pytest.mark.data` - 数据一致性测试（1个）
- `@pytest.mark.security` - 安全性测试（2个）

---

## 关键改进点

### 相比原 test_profile.py 的优化

1. **模块化拆分**
   - ✅ 按功能拆分为2个独立文件
   - ✅ 每个文件职责单一明确
   - ✅ 更易维护和扩展

2. **测试精简**
   - ✅ 从原来的30+个测试精简到13个核心测试
   - ✅ 保留最关键的测试场景
   - ✅ 删除冗余和重复的测试

3. **截图优化**
   - ✅ 每个测试保留2-4个关键截图
   - ✅ 截图命名清晰易懂
   - ✅ 截图时机准确

4. **代码质量**
   - ✅ 统一的fixture设计
   - ✅ 清晰的测试用例描述
   - ✅ 完整的中文注释

---

## 测试环境

- **测试环境**: https://localhost:3000
- **后端服务**: https://localhost:44320
- **浏览器**: Chromium (Playwright)
- **分辨率**: 1920x1080
- **测试账号**: haylee2 / Wh520520!

---

## 缺陷严重级别定义

- **Blocker**: 页面无法加载，无法保存数据
- **Critical**: 数据丢失，密码明文显示
- **Major**: 验证不正确，数据不持久化
- **Minor**: 提示信息不清晰，布局小问题
- **Trivial**: 文案错误，样式细节

---

## 测试执行记录

| 模块 | 文件 | 执行日期 | 执行人 | 状态 | 通过率 | 备注 |
|-----|------|---------|-------|------|--------|------|
| Personal Settings | test_personal_settings.py | - | - | 🔄 | - | 待执行 |
| Change Password | test_change_password.py | - | - | 🔄 | - | 待执行 |

---

**文档版本**: 1.0  
**创建日期**: 2025-12-02  
**最后更新**: 2025-12-02  
**维护人**: Test Team

