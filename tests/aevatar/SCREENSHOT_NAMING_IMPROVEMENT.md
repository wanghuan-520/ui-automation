# 📸 截图命名优化说明

## 概述

优化了测试截图的文件命名规则，自动添加测试用例名称和时间戳，使截图更易于识别和管理。

## 文件夹结构 & 命名格式

### 文件夹结构
```
test-screenshots/
├── test_aevatar_login/          # 登录测试的截图
│   ├── test_aevatar_login_20251023_152005_01_login_page.png
│   ├── test_aevatar_login_20251023_152019_02_form_filled.png
│   └── test_aevatar_login_20251023_152027_03_login_result.png
└── test_aevatar_workflow/       # Workflow测试的截图
    └── test_aevatar_workflow_20251023_152010_01_workflow_page.png
```

### 文件路径格式
```
test-screenshots/{测试用例名}/{测试用例名}_{时间戳}_{描述}.png
```

### 示例
```
test-screenshots/test_aevatar_login/test_aevatar_login_20251023_151231_01_login_page.png
test-screenshots/test_aevatar_login/test_aevatar_login_20251023_151245_02_form_filled.png
test-screenshots/test_aevatar_login/test_aevatar_login_20251023_151253_03_login_result.png
test-screenshots/test_aevatar_workflow/test_aevatar_workflow_20251023_152010_01_workflow_page.png
```

## 文件名组成

| 部分 | 说明 | 示例 | 来源 |
|------|------|------|------|
| 测试用例名 | 测试函数名 | `test_aevatar_login` | 自动获取 |
| 时间戳 | 执行时间 | `20251023_151231` | 自动生成 |
| 描述 | 步骤说明 | `01_login_page.png` | 测试代码指定 |

## 优势对比

### 优化前 ❌
```
test-screenshots/
├── 01_login_page.png
├── 02_form_filled.png
├── 03_login_result.png
├── 01_workflow_page.png
├── 02_agent_added.png
└── ... (所有测试的截图混在一起)
```

**问题**：
- ❌ 看不出是哪个测试用例
- ❌ 多个测试会互相覆盖
- ❌ 无法追溯执行时间
- ❌ 难以做历史对比
- ❌ 根目录文件过多

### 优化后 ✅
```
test-screenshots/
├── test_aevatar_login/          # 登录测试独立文件夹
│   ├── test_aevatar_login_20251023_151231_01_login_page.png
│   ├── test_aevatar_login_20251023_151245_02_form_filled.png
│   └── test_aevatar_login_20251023_151253_03_login_result.png
└── test_aevatar_workflow/       # Workflow测试独立文件夹
    ├── test_aevatar_workflow_20251023_152010_01_workflow_page.png
    └── test_aevatar_workflow_20251023_152025_02_agent_added.png
```

**优势**：
- ✅ 一眼识别测试用例
- ✅ 时间戳保证唯一性
- ✅ 保留原有描述信息
- ✅ 自动化实现
- ✅ 向后兼容
- ✅ **每个测试有独立文件夹**
- ✅ **文件组织清晰，易于管理**
- ✅ **快速定位特定测试的所有截图**

## 技术实现

### 修改的文件
- `tests/aevatar/base_test.py`

### 核心代码
```python
import inspect
from datetime import datetime

async def take_screenshot(self, filename: str):
    """截图，自动添加测试名称和时间戳前缀"""
    # 获取调用者的函数名（测试用例名）
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    test_name = caller_frame.f_code.co_name if caller_frame else "unknown_test"
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 组合新文件名
    new_filename = f"{test_name}_{timestamp}_{filename}"
    
    screenshot_path = os.path.join(self.SCREENSHOT_DIR, new_filename)
    await self.page.screenshot(path=screenshot_path, full_page=True)
    logger.info(f"📸 截图已保存: {screenshot_path}")
    return screenshot_path
```

### 关键技术
- `inspect.currentframe()` - 获取调用栈信息
- `f_code.co_name` - 获取函数名
- `datetime.now().strftime()` - 生成时间戳

## 使用场景

### 场景1：查看特定测试的所有截图
```bash
# 查看登录测试的所有截图
ls test-screenshots/test_aevatar_login/

# 或进入文件夹
cd test-screenshots/test_aevatar_login/
ls -lt  # 按时间排序查看
```

### 场景2：对比同一测试的多次运行
```bash
# 进入测试文件夹
cd test-screenshots/test_aevatar_login/

# 查看所有历史截图
ls -lt

# 对比两次运行的相同步骤
diff <first_run>_01_login_page.png <second_run>_01_login_page.png
```

### 场景3：快速清理特定测试的截图
```bash
# 只删除登录测试的截图
rm -rf test-screenshots/test_aevatar_login/

# 其他测试的截图不受影响
```

### 场景4：打包特定测试的截图
```bash
# 将登录测试的所有截图打包
zip -r login_screenshots.zip test-screenshots/test_aevatar_login/
```

### 场景5：失败分析
失败截图自动包含测试名和时间，且保存在独立文件夹中，方便追溯和分享

## 最佳实践

### 1. 描述性原始文件名
继续使用有意义的描述：
```python
await test_instance.take_screenshot("01_login_page.png")
await test_instance.take_screenshot("02_form_filled.png")
await test_instance.take_screenshot("03_login_result.png")
```

### 2. 按步骤编号
使用序号（01、02、03...）表示测试步骤顺序

### 3. 简洁明了
原始描述保持简短，关键信息已在测试名中

### 4. 统一格式
所有测试使用相同的命名规范

## 使用技巧

### 文件夹管理
```bash
# 查看所有测试的截图文件夹
ls -d test-screenshots/*/

# 查看每个测试的截图数量
for dir in test-screenshots/*/; do 
  echo "$dir: $(ls -1 $dir | wc -l) 张截图"
done

# 查看所有测试的总磁盘占用
du -sh test-screenshots/*/
```

### 快速查找
```bash
# 查看特定测试的所有截图
ls test-screenshots/test_aevatar_login/

# 查看最新的截图
find test-screenshots/ -name "*.png" -type f -mtime -1

# 按日期查找（查找今天的）
find test-screenshots/ -name "*20251023_*"
```

### 清理旧截图
```bash
# 删除7天前的截图（按文件夹）
find test-screenshots/* -type d -mtime +7 -exec rm -rf {} \;

# 或者手动删除特定测试的旧截图
rm -rf test-screenshots/test_aevatar_login/
```

## 兼容性

### ✅ 向后兼容
- 所有现有测试文件无需修改
- 自动应用于所有调用 `take_screenshot()` 的测试
- 不影响测试逻辑

### ✅ 自动生效的文件
- `test_daily_regression_login.py`
- `test_daily_regression_workflow.py`
- `test_daily_regression_complete.py`
- `test_daily_regression_dashboard.py`
- `test_daily_regression_organisation.py`
- `test_daily_regression_project.py`
- 所有其他使用 `base_test.py` 的测试

## 验证测试

### 运行测试
```bash
pytest tests/aevatar/test_daily_regression_login.py -v
```

### 生成的截图
```
✅ test_aevatar_login_20251023_151231_01_login_page.png
✅ test_aevatar_login_20251023_151245_02_form_filled.png
✅ test_aevatar_login_20251023_151253_03_login_result.png
```

## 时间戳格式

### 格式说明
- `YYYYMMDD_HHMMSS`
- 例如：`20251023_151231` = 2025年10月23日 15:12:31

### 为什么这样设计
- ✅ 文件名友好（无特殊字符）
- ✅ 按字母排序即按时间排序
- ✅ 紧凑且易读
- ✅ 跨平台兼容

## 常见问题

### Q: 会不会太长？
A: 虽然文件名较长，但信息完整，现代文件系统支持长文件名。

### Q: 如果不想要时间戳？
A: 可以修改 `base_test.py` 的 `take_screenshot` 方法，移除时间戳部分。

### Q: 如何自定义格式？
A: 修改 `base_test.py` 中的 `timestamp` 格式字符串。

### Q: 测试名太长怎么办？
A: 建议使用简洁的测试函数名，如 `test_login` 而不是 `test_user_login_with_email_and_password`。

## 关键改进点

- ✅ **自动化** - 无需手动命名，文件夹自动创建
- ✅ **标准化** - 统一的命名格式
- ✅ **可追溯** - 包含时间戳
- ✅ **易识别** - 测试名称清晰
- ✅ **不覆盖** - 每次运行独立保存
- ✅ **独立管理** - 每个测试有自己的文件夹
- ✅ **清晰组织** - 文件层次结构清晰
- ✅ **易于查找** - 快速定位特定测试的截图

## 未来扩展

### 可能的增强
1. 添加失败/成功标记
2. 添加浏览器类型标记
3. 添加分辨率标记
4. 支持自定义前缀

### 示例扩展格式
```
test_aevatar_login_20251023_151231_chrome_1920x1080_success_01_login_page.png
```

---

**创建时间**: 2025-10-23  
**版本**: v1.0  
**状态**: ✅ 已实施并验证

