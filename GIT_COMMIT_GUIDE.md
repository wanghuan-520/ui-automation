# 📤 代码提交指南

## 🚀 快速提交

### 方法1: 一键提交（推荐）

```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation

# 1. 清理生成文件
bash cleanup.sh

# 2. 查看要提交的文件
git status

# 3. 添加所有改动
git add .

# 4. 提交
git commit -m "feat: 优化测试框架，添加并行测试和清理脚本"

# 5. 推送到远程
git push
```

### 方法2: 分步提交

```bash
# 进入项目目录
cd /Users/wanghuan/aelf/Cursor/ui-automation

# 清理
bash cleanup.sh

# 查看状态
git status

# 添加特定文件
git add .gitignore
git add cleanup.sh
git add run_smoke_test.py
git add run_all_tests_parallel.py
git add README_SIMPLIFIED.md
git add CLEANUP_GUIDE.md

# 提交
git commit -m "feat: 优化测试框架"

# 推送
git push
```

---

## 📋 提交内容清单

### ✅ 会提交的文件

**测试脚本**:
- `run_smoke_test.py` - 快速测试
- `run_all_tests_parallel.py` - 并行测试
- `run_all_tests_sequential.py` - 顺序测试

**清理脚本**:
- `cleanup.sh` - 清理脚本

**配置文件**:
- `.gitignore` - Git配置（已优化）

**文档**:
- `README_SIMPLIFIED.md` - 快速指南
- `CLEANUP_GUIDE.md` - 清理指南
- `PROJECT_CLEANUP_SUMMARY.md` - 优化总结
- `QUICK_START_COMPARISON.md` - 方案对比
- `PARALLEL_TEST_GUIDE.md` - 并行测试指南
- `PARALLEL_EXPLAINED_SIMPLY.md` - 并行解释
- `SYSTEM_RECOVERY_AND_TEST_GUIDE.md` - 问题排查

**测试代码**:
- `tests/aevatar/*.py` - 所有测试文件

### ❌ 不会提交的文件（已在.gitignore）

- `test-screenshots/` - 测试截图
- `allure-results/` - Allure数据
- `allure-report/` - Allure报告
- `reports/` - 测试报告
- `logs/` - 日志文件
- `__pycache__/` - Python缓存
- `*.png, *.jpg, *.log` - 图片和日志

---

## 💡 提交信息建议

### 常用提交格式

```bash
# 功能添加
git commit -m "feat: 添加并行测试支持"

# 优化改进
git commit -m "refactor: 优化测试框架结构"

# 修复Bug
git commit -m "fix: 修复测试超时问题"

# 文档更新
git commit -m "docs: 更新测试指南"

# 配置调整
git commit -m "chore: 更新.gitignore配置"
```

### 推荐的提交信息（本次）

```bash
git commit -m "feat: 优化测试框架

- 添加快速冒烟测试（1-3分钟）
- 添加并行测试支持（20-30分钟）
- 优化.gitignore，排除生成文件
- 添加cleanup.sh清理脚本
- 简化项目文档结构
- 删除冗余文档"
```

---

## 🔍 提交前检查

### 检查清单

```bash
# 1. 清理生成文件
bash cleanup.sh
✅ 已清理

# 2. 查看Git状态
git status
✅ 确认没有不应提交的文件（截图、报告等）

# 3. 查看改动
git diff
✅ 确认改动正确

# 4. 测试运行
python3 run_smoke_test.py
✅ 测试通过
```

---

## 🚨 常见问题

### Q1: 如果有大文件？

```bash
# 查看文件大小
du -sh * | sort -hr | head -10

# 如果有大文件被追踪
git rm --cached <大文件>
git commit -m "chore: 移除大文件"
```

### Q2: 如果提交了不该提交的文件？

```bash
# 从暂存区移除
git reset HEAD <文件>

# 或者从历史中移除
git rm --cached <文件>
git commit -m "chore: 移除不需要的文件"
```

### Q3: 如果想撤销提交？

```bash
# 撤销最后一次提交（保留改动）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃改动）
git reset --hard HEAD~1
```

### Q4: 如果远程冲突？

```bash
# 先拉取
git pull --rebase

# 解决冲突后
git add .
git rebase --continue

# 推送
git push
```

---

## 📊 提交后验证

### 在远程仓库检查

1. 访问GitHub/GitLab
2. 查看提交记录
3. 确认文件列表
4. 验证`.gitignore`生效

### 本地验证

```bash
# 查看提交历史
git log --oneline -5

# 查看远程状态
git remote -v
git branch -a

# 确认推送成功
git status
# 应该显示: "Your branch is up to date with 'origin/main'"
```

---

## 🎯 完整操作流程

### 一键提交（复制粘贴执行）

```bash
cd /Users/wanghuan/aelf/Cursor/ui-automation && \
bash cleanup.sh && \
git status && \
git add . && \
git commit -m "feat: 优化测试框架

- 添加快速冒烟测试（1-3分钟）
- 添加并行测试支持（20-30分钟）  
- 优化.gitignore，排除生成文件
- 添加cleanup.sh清理脚本
- 简化项目文档结构" && \
git push
```

---

## ✅ 成功标志

提交成功后，你应该看到：

```bash
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XXX KiB | XXX MiB/s, done.
Total XX (delta XX), reused XX (delta XX)
To github.com:xxx/ui-automation.git
   xxxxxx..xxxxxx  main -> main
```

---

**最后更新**: 2025-10-30  
**状态**: 准备提交 ✅

