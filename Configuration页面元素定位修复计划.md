# Configuration页面元素定位修复计划

## 问题分析

### 1. 区域定位问题
- ❌ `DLL_SECTION = "generic:has-text('DLL')"` - 不可见
- ❌ `CORS_SECTION = "generic:has-text('CORS')"` - 不可见  
**原因**：`generic`选择器太泛型，`has-text`可能匹配不准确

### 2. Add按钮定位冲突
- ❌ `CORS_ADD_BUTTON = "button:has-text('Add')"`
**错误**：strict mode violation，匹配到2个元素：
  1. 页面上的CORS Add按钮
  2. 对话框内的Add按钮

### 3. 对话框元素定位
- ❌ 对话框标题不可见
- ❌ 对话框无法正确打开

### 4. CORS列表获取失败
- 获取到0个CORS配置，但实际已创建
- 表格定位器不准确

## 修复方案

### 1. 使用更准确的文本定位器
```python
# 使用直接的文本匹配，不使用generic
DLL_SECTION = "text=DLL"
CORS_SECTION = "text=CORS"
```

### 2. 修正Add按钮定位器
```python
# 使用更具体的选择器，避免与对话框按钮冲突
# 方案1：使用可见性和位置
CORS_ADD_BUTTON = "div:has-text('CORS') >> button:has-text('Add')"

# 方案2：使用父容器限定
# 找到CORS标题所在的区域，然后找其中的Add按钮
```

### 3. 简化对话框定位器
```python
# 对话框本身
CORS_DIALOG = "dialog"  # 简化，页面只有一个dialog

# 对话框标题
CORS_DIALOG_TITLE = "heading:has-text('Add cross-origin domain')"

# Domain输入框 - 使用role更准确
CORS_DOMAIN_INPUT = "role=textbox[name='Domain']"

# 对话框内的Add按钮 - 使用role
CORS_DIALOG_ADD_BUTTON = "dialog >> button:has-text('Add')"
```

### 4. 修正CORS列表获取
```python
def get_cors_list(self):
    # 简化定位逻辑
    # 直接找包含CORS文本的最近的table
    # 或使用更明确的选择器路径
```

## 实施步骤

1. ✅ 修改页面对象定位器
2. ⏳ 重新运行测试验证
3. ⏳ 根据截图进一步调整
4. ⏳ 生成最终测试报告

