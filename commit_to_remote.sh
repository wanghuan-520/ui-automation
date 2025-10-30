#!/bin/bash
# 提交代码到远程仓库

echo "🚀 准备提交代码到远程..."
echo ""

cd "$(dirname "$0")"

# 1. 清理生成文件
echo "🧹 清理生成文件..."
bash cleanup.sh
echo ""

# 2. 查看状态
echo "📊 查看Git状态..."
git status
echo ""

# 3. 确认
echo "⚠️  请检查上面的文件列表，确认要提交的内容"
echo ""
read -p "确认提交？(y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ 取消提交"
    exit 0
fi

# 4. 添加文件
echo ""
echo "📦 添加文件到暂存区..."
git add .

# 5. 提交
echo ""
echo "💾 提交到本地仓库..."
git commit -m "feat: 优化测试框架

- 添加快速冒烟测试（run_smoke_test.py，1-3分钟）
- 添加并行测试支持（run_all_tests_parallel.py，20-30分钟）
- 优化.gitignore，排除截图和报告等生成文件
- 添加cleanup.sh清理脚本
- 简化项目文档结构，删除冗余文档
- 创建README_SIMPLIFIED.md快速指南"

# 6. 推送
echo ""
echo "📤 推送到远程仓库..."
git push

# 7. 完成
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 代码提交成功！"
    echo ""
    echo "📊 查看提交记录:"
    git log --oneline -3
else
    echo ""
    echo "❌ 推送失败，请检查错误信息"
    exit 1
fi

