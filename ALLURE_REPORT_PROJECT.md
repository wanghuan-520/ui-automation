# Project 测试 Allure 报告使用指南

**生成时间**: 2025-10-28 15:51  
**测试范围**: Project Management (Settings, Members, Roles)  
**测试用例数**: 6个  

---

## 📊 报告概览

### 测试结果
- ✅ **通过**: 4个测试
- ⏭️ **跳过**: 2个测试
- ❌ **失败**: 0个
- **通过率**: 100%
- **总耗时**: 约4分28秒

### 生成的文件
- **测试数据**: `allure-results/` (19个JSON文件)
- **HTML报告**: `allure-report/` (完整的Web报告)

---

## 🚀 快速查看报告

### 方式一：使用脚本（推荐）

```bash
# 在项目根目录执行
./view_project_allure_report.sh
```

这将自动启动 Allure 服务器并在浏览器中打开报告。

### 方式二：手动启动

```bash
# 进入项目目录
cd /Users/wanghuan/aelf/Cursor/ui-automation

# 启动 Allure 服务器
allure serve allure-results
```

### 方式三：直接打开生成的报告

```bash
# 打开已生成的报告
open allure-report/index.html
```

---

## 📈 Allure 报告功能

### 1. Overview（概览）
- 📊 测试结果统计
- ⏱️ 执行时间趋势
- 🎯 测试通过率
- 📉 失败率统计

### 2. Suites（测试套件）
- 📁 按测试套件分组
- 🔍 查看每个测试的详细信息
- 📸 包含测试截图（如果有）
- 📝 测试步骤和日志

### 3. Graphs（图表）
- 📊 状态分布图
- ⏱️ 持续时间图
- 🏆 严重性分布
- 📈 趋势图（需要多次运行）

### 4. Timeline（时间线）
- ⏰ 测试执行时间线
- 🔄 并行执行可视化
- 📊 资源使用情况

### 5. Behaviors（行为驱动）
- 🎯 按功能分组
- 📋 测试场景展示
- ✅ 验收标准检查

### 6. Categories（分类）
- 🏷️ 失败原因分类
- 🐛 已知问题标记
- ⚠️ 不稳定测试标识

---

## 🎯 报告中的测试用例

### ✅ 通过的测试

#### 1. test_project_role_add [P0]
**功能**: 添加 Project Role  
**路径**: `/profile/projects/role`  
**耗时**: ~42秒  
**步骤**:
1. 登录系统
2. 选择Project
3. 点击 "Add Role"
4. 输入Role名称
5. 保存并验证

#### 2. test_project_name_edit [P1]
**功能**: 修改 Project Name  
**路径**: `/profile/projects/general`  
**耗时**: ~41秒  
**步骤**:
1. 导航到Project设置
2. 修改名称
3. 保存并验证

#### 3. test_project_role_edit_permissions [P1]
**功能**: 编辑 Role 权限  
**路径**: `/profile/projects/role`  
**耗时**: ~45秒  
**步骤**:
1. 打开Role权限编辑
2. 勾选全部权限
3. 保存并验证

#### 4. test_project_role_delete [P2]
**功能**: 删除 Project Role  
**路径**: `/profile/projects/role`  
**耗时**: ~48秒  
**步骤**:
1. 选择自定义Role
2. 打开菜单
3. 点击删除
4. 确认并验证

### ⏭️ 跳过的测试

#### 1. test_project_member_add [P0]
**原因**: 无可添加的Organisation成员  
**说明**: 测试环境限制，需要更多Organisation成员

#### 2. test_project_member_delete [P1]
**原因**: 只有一个Owner，无法删除  
**说明**: 预期行为，不能删除唯一的Owner

---

## 🔍 报告详细信息

### 测试环境
- **URL**: https://aevatar-station-ui-staging.aevatar.ai
- **浏览器**: Google Chrome
- **Python**: 3.9.6
- **Pytest**: 8.4.2
- **Playwright**: 最新版

### 测试数据
- **账号**: aevatarwh1@teml.net
- **测试Project**: 自动选择
- **截图目录**: `test-screenshots/project/`

### 日志级别
- INFO: 正常流程信息
- WARNING: 非关键警告（如Toast未显示）
- ERROR: 错误信息（已处理）

---

## 📸 截图附件

报告中包含以下关键截图：

1. **project_member_page.png** - Member列表
2. **project_member_add_dialog.png** - 添加Member对话框
3. **project_role_page.png** - Role列表
4. **project_role_created.png** - Role创建成功
5. **project_role_delete_menu_opened.png** - 删除菜单
6. **project_settings_page.png** - 设置页面
7. 等等...

所有截图都可以在 Allure 报告中点击查看。

---

## 🔄 重新生成报告

### 完整重新生成

```bash
# 1. 清理旧数据
rm -rf allure-results allure-report

# 2. 运行测试并生成数据
python3 -m pytest tests/aevatar/test_daily_regression_project.py \
  -v -m project \
  --alluredir=allure-results \
  --clean-alluredir

# 3. 生成报告
allure generate allure-results -o allure-report --clean

# 4. 查看报告
allure open allure-report
```

### 追加测试结果

```bash
# 运行新测试（不清理旧数据）
python3 -m pytest tests/aevatar/test_daily_regression_project.py \
  -v -m project \
  --alluredir=allure-results

# 重新生成报告
allure generate allure-results -o allure-report --clean
```

---

## 📊 与其他报告对比

### HTML Report vs Allure Report

| 特性 | pytest-html | Allure |
|------|-------------|--------|
| 美观度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 功能丰富度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 交互性 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 趋势分析 | ❌ | ✅ |
| 分类管理 | ❌ | ✅ |
| 时间线 | ❌ | ✅ |
| 附件支持 | 基础 | 完整 |

---

## 🎨 自定义报告

### 添加标题和描述

在测试代码中使用 Allure 装饰器：

```python
import allure

@allure.title("添加 Project Role")
@allure.description("测试添加自定义Project Role的完整流程")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.p0
async def test_project_role_add():
    with allure.step("步骤1: 登录系统"):
        # 登录代码
        pass
    
    with allure.step("步骤2: 导航到Role页面"):
        # 导航代码
        pass
```

### 添加截图

```python
import allure

# 添加截图到报告
allure.attach.file(
    screenshot_path,
    name="测试截图",
    attachment_type=allure.attachment_type.PNG
)
```

---

## 🔧 故障排除

### 问题1: 报告无法打开
**解决**: 确保 Allure 已安装
```bash
brew install allure  # macOS
```

### 问题2: 数据未生成
**解决**: 检查 pytest 插件
```bash
pip install allure-pytest
```

### 问题3: 端口被占用
**解决**: 指定端口
```bash
allure open allure-report -p 8080
```

---

## 📚 参考文档

- [Allure 官方文档](https://docs.qameta.io/allure/)
- [allure-pytest 使用指南](https://docs.qameta.io/allure/#_pytest)
- [Allure 报告示例](https://demo.qameta.io/allure/)

---

## 🎉 总结

✅ **Allure 报告已成功生成！**

### 下一步建议
1. 🔍 浏览报告，了解测试详情
2. 📊 分析失败和跳过的测试
3. 🎯 优化测试覆盖率
4. 📈 建立测试趋势监控
5. 🔄 集成到CI/CD流程

**报告位置**: `/Users/wanghuan/aelf/Cursor/ui-automation/allure-report/`

---

**生成者**: HyperEcho (AI Testing Assistant)  
**日期**: 2025-10-28  
**版本**: 1.0

